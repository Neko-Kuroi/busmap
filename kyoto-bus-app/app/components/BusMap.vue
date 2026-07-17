<template>
  <div class="map-wrap">
    <div id="map" ref="mapEl"></div>

    <div class="status" v-if="loading">停留所データを読み込み中…</div>

    <div class="panel" v-else>
      <div class="count">{{ stopCount.toLocaleString() }} 件の停留所（{{ routeCount.toLocaleString() }} 系統）</div>

      <input
        class="search"
        type="text"
        v-model="query"
        placeholder="系統名・事業者名で検索（例: 洛北高校、17、京都バス）"
      />

      <div class="route-list" v-if="query">
        <button
          v-for="r in filteredRoutes"
          :key="r.operator + '||' + r.route"
          class="route-item"
          :class="{ active: isActive(r) }"
          @click="selectRoute(r)"
        >
          <span class="route-name">{{ r.route }}</span>
          <span class="route-operator">{{ r.operator }}（{{ r.count }}件）</span>
        </button>
        <p class="no-hit" v-if="filteredRoutes.length === 0">該当する系統がありません</p>
      </div>

      <div class="selected" v-if="selectedRoute">
        <span>選択中: <strong>{{ selectedRoute.route }}</strong>（{{ selectedRoute.operator }}）</span>
        <button class="clear" @click="clearSelection">解除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const mapEl = ref(null)
const loading = ref(true)
const stopCount = ref(0)
const routeCount = ref(0)
const query = ref('')
const selectedRoute = ref(null)

let allRoutes = []
let map = null
let baseLayer = null
let highlightLayer = null
let stopsById = {}
let markersById = {}
let hiddenMarkerIds = []

const filteredRoutes = computed(() => {
  const q = query.value.trim()
  if (!q) return []
  return allRoutes
    .filter(r => r.route.includes(q) || r.operator.includes(q))
    .slice(0, 40)
})

function isActive(r) {
  return selectedRoute.value && selectedRoute.value.operator === r.operator && selectedRoute.value.route === r.route
}

function clearSelection() {
  selectedRoute.value = null
  query.value = ''
  renderHighlight(null)
}

function selectRoute(r, anchorStopId) {
  selectedRoute.value = r
  renderHighlight(r, anchorStopId)
}

// ズームレベルに応じたマーカー半径（ズームインしても小さくなりすぎないよう下限を確保しつつ、ズームに応じて拡大）
function stopRadius(zoom, isHighlight) {
  const base = Math.max(6, Math.min(14, zoom - 6))
  return isHighlight ? base + 3 : base
}

// 選択中の系統の停留所用：星形アイコン（サイズはズームに応じて可変）
function createStarIcon(zoom) {
  const size = stopRadius(zoom, true) * 3.2
  const half = size / 2
  const html = `<svg width="${size}" height="${size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path class="star-glow-path" d="M12 1.2l3.35 6.79 7.5 1.09-5.43 5.29 1.28 7.47L12 18.02l-6.7 3.82 1.28-7.47-5.43-5.29 7.5-1.09L12 1.2z"
      fill="#f9a8d4" stroke="#db2777" stroke-width="1.4" stroke-linejoin="round"/>
  </svg>`
  return window.__L.divIcon({
    html,
    className: 'stop-star-icon',
    iconSize: [size, size],
    iconAnchor: [half, half],
    popupAnchor: [0, -half]
  })
}

// 通常の停留所用：丸いdivIcon（クラスタリング対応のため circleMarker ではなく
// L.marker + divIcon を使う。サイズはズームに応じて可変）
function createDotIcon(zoom) {
  const size = stopRadius(zoom, false) * 2
  const half = size / 2
  return window.__L.divIcon({
    html: `<span class="stop-dot" style="width:${size}px;height:${size}px;"></span>`,
    className: 'stop-dot-icon',
    iconSize: [size, size],
    iconAnchor: [half, half],
    popupAnchor: [0, -half]
  })
}

// クラスター（複数停留所をまとめた丸）のアイコン生成
function createClusterIcon(cluster) {
  const count = cluster.getChildCount()
  const size = count < 10 ? 34 : count < 50 ? 42 : count < 200 ? 50 : 58
  return window.__L.divIcon({
    html: `<div class="stop-cluster-dot" style="width:${size}px;height:${size}px;line-height:${size}px;">${count}</div>`,
    className: 'stop-cluster-icon',
    iconSize: [size, size]
  })
}

function escapeHtml(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;')
}

// ホバーでポップアップを開閉しつつ、カーソルがポップアップ内(系統名リンクなど)に
// 移動した場合は閉じないようにするための遅延クローズ管理
let closeTimer = null

function cancelClose() {
  clearTimeout(closeTimer)
  closeTimer = null
}

function scheduleClose(marker) {
  cancelClose()
  closeTimer = setTimeout(() => {
    const popup = marker.getPopup && marker.getPopup()
    const el = popup && popup.isOpen() && popup.getElement()
    // マウスが実際にポップアップの上にある場合は閉じない（保険）
    if (el && el.matches(':hover')) return
    marker.closePopup()
  }, 250)
}

function bindHoverPopup(marker) {
  marker.on('mouseover', () => {
    cancelClose()
    marker.openPopup()
  })
  marker.on('mouseout', () => {
    scheduleClose(marker)
  })
}

// ポップアップ内の系統名クリック → 検索欄にセットし、その系統を選択状態にする
// anchorStopId: クリック元のポップアップがどの停留所のものだったか（表示位置を保つため）
function onPopupRouteClick(operator, route, anchorStopId) {
  const match = allRoutes.find(r => r.operator === operator && r.route === route)
  if (!match) return
  query.value = route
  selectRoute(match, anchorStopId)
}

// ポップアップ内の運行会社名クリック → 検索欄にセットするのみ（選択状態は変更しない）
function onPopupOperatorClick(operator) {
  query.value = operator
}

// 停留所ポップアップ内の「運行会社名＋系統名」部分（クリック可能）を生成
function buildStopSubLabel(stop) {
  const routesHtml = stop.routes.length
    ? stop.routes
        .map(rt => `<span class="route-link" data-operator="${escapeHtml(stop.operator)}" data-route="${escapeHtml(rt)}" data-stop-id="${stop.id}">${escapeHtml(rt)}</span>`)
        .join('<br>')
    : '（系統情報なし）'
  return `<span class="operator-link" data-operator="${escapeHtml(stop.operator)}">${escapeHtml(stop.operator)}</span><br><span class="stop-routes-inline">${routesHtml}</span>`
}

function buildPopupHtml(stop, subLabel) {
  const kanaHtml = stop.kana ? `<p class="stop-kana">${escapeHtml(stop.kana)}</p>` : ''
  const subLabelHtml = subLabel ? `<p class="stop-sub">${subLabel}</p>` : ''
  const linkHtml = stop.url
    ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">🕒 時刻表を見る</a></p>`
    : ''

  const lat = stop.lat
  const lng = stop.lng
  const externalLinksHtml = `
    <div class="stop-external-links">
      <a href="https://www.google.com/maps/search/?api=1&query=${lat},${lng}&zoom=16" target="_blank" rel="noopener">📍 Google Maps</a>
      <a href="https://earth.google.com/web/@${lat},${lng},0a,1000d" target="_blank" rel="noopener">📍 Google Earth</a>
      <a href="https://map.yahoo.co.jp/place?lat=${lat}&lon=${lng}&zoom=16&maptype=basic" target="_blank" rel="noopener">📍 Yahoo! Map</a>
      <a href="https://labs.mapple.com/mapplevt.html#17/${lat}/${lng}" target="_blank" rel="noopener">📍 MAPPLE</a>
    </div>`

  return `<div class="stop-popup">
    <p class="stop-name">${escapeHtml(stop.name)}</p>
    ${kanaHtml}
    ${subLabelHtml}
    ${linkHtml}
    ${externalLinksHtml}
  </div>`
}

// 通常表示時／薄く表示する時のマーカー不透明度
const BASE_OPACITY = 0.85
const DIMMED_OPACITY = 0.3

function renderHighlight(route, anchorStopId) {
  if (!map) return
  highlightLayer.clearLayers()

  // 前回、星の下に隠すため非表示にしていた丸を元に戻す
  for (const id of hiddenMarkerIds) {
    const m = markersById[id]
    if (m) m.setOpacity(BASE_OPACITY)
  }
  hiddenMarkerIds = []

  if (!route) {
    baseLayer.eachLayer(l => l.setOpacity(BASE_OPACITY))
    return
  }

  // 選択中の系統以外の停留所を薄くする
  baseLayer.eachLayer(l => l.setOpacity(DIMMED_OPACITY))

  const L = window.__L
  const zoom = map.getZoom()
  const bounds = []
  let anchorMarker = null
  for (const id of route.stopIds) {
    const stop = stopsById[id]
    if (!stop) continue
    bounds.push([stop.lat, stop.lng])

    // 星アイコンの下に丸が二重に残らないよう、完全に非表示にする
    const baseMarker = markersById[id]
    if (baseMarker) {
      baseMarker.setOpacity(0)
      hiddenMarkerIds.push(id)
    }

    const marker = L.marker([stop.lat, stop.lng], {
      icon: createStarIcon(zoom)
    })
    marker.bindPopup(buildPopupHtml(stop, buildStopSubLabel(stop)), { maxWidth: 320 })
    bindHoverPopup(marker)
    marker.addTo(highlightLayer)

    if (anchorStopId != null && String(id) === String(anchorStopId)) {
      anchorMarker = marker
    }
  }

  if (anchorMarker) {
    // ポップアップ内の系統名クリックから来た場合：どの停留所を見ていたか
    // 見失わないよう、地図の中心・ズームは動かさず、同じ場所の星マーカーの
    // ポップアップを開き直す
    anchorMarker.openPopup()
  } else if (bounds.length) {
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 })
  }
}

onMounted(async () => {
  const L = await import('leaflet')
  window.__L = L
  // leaflet.markercluster は古いUMD形式で `import` ではなくグローバル変数
  // window.L を直接参照する作りになっている（L.MarkerClusterGroup = ... など）。
  // これを設定せずに読み込むと "L is not defined" で例外が発生し、
  // このあとのマーカー描画処理まで到達できなくなる。
  window.L = L
  let clusteringAvailable = true
  try {
    await import('leaflet.markercluster')
  } catch (err) {
    clusteringAvailable = false
    console.error('leaflet.markercluster の読み込みに失敗したにゃ。クラスタリングなしで表示するにゃ:', err)
  }

  map = L.map(mapEl.value, {
    center: [35.011, 135.768], // 京都御所付近
    zoom: 12
  })

  // ポップアップが開いたら、その要素自体にカーソルが乗っている間は
  // クローズタイマーを止め、離れたら閉じる（マーカー→ポップアップへの
  // カーソル移動中に mouseout で即座に閉じてしまう問題への対処）
  map.on('popupopen', (e) => {
    const el = e.popup.getElement()
    const marker = e.popup._source
    if (!el || !marker) return
    el.addEventListener('mouseenter', cancelClose)
    el.addEventListener('mouseleave', () => scheduleClose(marker))
  })

  // ポップアップ内の系統名・運行会社名クリックをイベント委譲で処理
  mapEl.value.addEventListener('click', (e) => {
    const routeEl = e.target.closest('.route-link')
    if (routeEl) {
      onPopupRouteClick(routeEl.dataset.operator, routeEl.dataset.route, routeEl.dataset.stopId)
      return
    }
    const operatorEl = e.target.closest('.operator-link')
    if (operatorEl) {
      onPopupOperatorClick(operatorEl.dataset.operator)
    }
  })

  // ズーム変化に応じてマーカーサイズを再計算（ズームインしても小さくなりすぎないように）
  map.on('zoomend', () => {
    const z = map.getZoom()
    if (baseLayer) baseLayer.eachLayer(l => l.setIcon(createDotIcon(z)))
    if (highlightLayer) highlightLayer.eachLayer(l => l.setIcon(createStarIcon(z)))
  })
  
  L.tileLayer("https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}", {
    attribution: '<a href="https://developers.google.com/maps/documentation" target="_blank">Google Map</a>',
    maxZoom: 22
  }).addTo(map);

  try {
    // lyrs=m: Standard Roadmap（通常の地図）
    // lyrs=s: Satellite only（航空写真のみ、文字なし）
    // lyrs=y: Hybrid（航空写真 ＋ 道路 ＋ 日本語ラベル）
    // lyrs=p: Terrain（地形図）
    // hl=ja: 言語を日本語に固定
    L.tileLayer('https://mt1.google.com/vt/lyrs=s&hl=ja&x={x}&y={y}&z={z}', {
      attribution: '© Google',
      maxZoom: 22,
      opacity: 0.14
    }).addTo(map);
  } catch (e) {
    console.error('❌ Error adding tile layer:', e);
  }

  //L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  //  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
  //  maxZoom: 19
  //}).addTo(map)

  // 事業者単位のバスルート線（背景・薄いグレー、系統別ではない）
  fetch('/data/route_lines.geojson')
    .then(res => res.json())
    .then(routeLines => {
      L.geoJSON(routeLines, {
        interactive: false,
        style: { color: '#94a3b8', weight: 1.5, opacity: 0.5 }
      }).addTo(map)
    })

  const [stopsRes, routesRes] = await Promise.all([
    fetch('/data/mlit_stops.json'),
    fetch('/data/mlit_routes.json')
  ])
  const stops = await stopsRes.json()
  allRoutes = await routesRes.json()

  stopCount.value = stops.length
  routeCount.value = allRoutes.length
  loading.value = false

  for (const s of stops) stopsById[s.id] = s

  // 画面からはみ出た／密集している停留所は自動でクラスタリングしてアイコン数を
  // 減らし、描画・操作の負荷を下げる（chunkedLoading で4685件の初期追加も分割処理）
  // ※ プラグインが読み込めなかった場合は通常のlayerGroupにフォールバックする
  baseLayer = (clusteringAvailable && typeof L.markerClusterGroup === 'function')
    ? L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 60,
        disableClusteringAtZoom: 14,
        spiderfyOnMaxZoom: true,
        showCoverageOnHover: false,
        iconCreateFunction: createClusterIcon
      })
    : L.layerGroup()
  highlightLayer = L.layerGroup().addTo(map)

  for (const stop of stops) {
    const marker = L.marker([stop.lat, stop.lng], {
      icon: createDotIcon(map.getZoom())
    })

    marker.bindPopup(buildPopupHtml(stop, buildStopSubLabel(stop)), { maxWidth: 320 })
    bindHoverPopup(marker)

    marker.addTo(baseLayer)
    markersById[stop.id] = marker
  }

  baseLayer.addTo(map)
})
</script>

<style scoped>
.map-wrap {
  position: relative;
  width: 100%;
  height: 100vh;
}

#map {
  width: 100%;
  height: 100%;
}

.status {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.92);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.panel {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.96);
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.25);
  width: min(340px, calc(100vw - 24px));
  max-height: calc(100vh - 24px);
  overflow-y: auto;
}

.count {
  color: #333;
  margin-bottom: 6px;
}

.search {
  width: 100%;
  box-sizing: border-box;
  padding: 6px 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 13px;
}

.route-list {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 45vh;
  overflow-y: auto;
}

.route-item {
  text-align: left;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 6px 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.route-item:hover {
  background: #e0e7ff;
}

.route-item.active {
  background: #fee2e2;
  border-color: #dc2626;
}

.route-name {
  font-weight: 600;
}

.route-operator {
  font-size: 11px;
  color: #666;
}

.no-hit {
  color: #888;
  font-size: 12px;
  margin: 4px 0 0;
}

.selected {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  background: #fef2f2;
  padding: 6px 8px;
  border-radius: 6px;
}

.clear {
  border: none;
  background: #dc2626;
  color: white;
  border-radius: 4px;
  padding: 3px 8px;
  font-size: 12px;
  cursor: pointer;
}

:deep(.stop-star-icon) {
  background: transparent;
  border: none;
  overflow: visible;
}

:deep(.stop-star-icon) svg {
  display: block;
  overflow: visible;
  filter: drop-shadow(0 0 1px rgba(0, 0, 0, 0.5));
}

/* 選択中の系統の星マーカーをゆっくり光らせるアニメーション */
:deep(.star-glow-path) {
  transform-origin: center;
  animation: star-glow 4s ease-in-out infinite;
}

@keyframes star-glow {
  0% {
    stroke-width: 1.4;
    stroke-opacity: 0.7;
    filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.35)) brightness(1);
  }
  50% {
    stroke-width: 3;
    stroke-opacity: 1;
    filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.95)) brightness(1.35);
  }
  100% {
    stroke-width: 1.4;
    stroke-opacity: 0.7;
    filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.35)) brightness(1);
  }
}

:deep(.stop-dot-icon) {
  background: transparent;
  border: none;
}

:deep(.stop-dot) {
  display: block;
  border-radius: 50%;
  background: #eaff00;
  border: 1px solid #d4e100;
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.5);
}

:deep(.stop-cluster-icon) {
  background: transparent;
  border: none;
}

:deep(.stop-cluster-dot) {
  display: block;
  border-radius: 50%;
  background: rgba(234, 255, 0, 0.5);
  border: 2px solid rgba(168, 184, 0, 0.6);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
  text-align: center;
  font-weight: 700;
  font-size: 12px;
  color: #3a3a00;
}

:deep(.stop-popup) {
  line-height: 1.4;
}

:deep(.stop-name) {
  font-weight: 700;
  margin: 0;
}

:deep(.stop-kana) {
  margin: 2px 0 0;
  color: #555;
  font-size: 12px;
}

:deep(.stop-routes) {
  margin: 2px 0 0;
  font-size: 11px;
  color: #444;
}

:deep(.stop-sub) {
  margin: 2px 0 0;
  font-size: 11px;
  color: #444;
}

:deep(.stop-routes-inline) {
  color: #666;
}

:deep(.route-link),
:deep(.operator-link) {
  cursor: pointer;
  color: #1d4ed8;
  text-decoration: underline dotted;
}

:deep(.route-link:hover),
:deep(.operator-link:hover) {
  color: #dc2626;
  text-decoration: underline;
}

:deep(.stop-link) {
  margin: 4px 0 0;
}

:deep(.stop-link a) {
  color: #1d4ed8;
  font-size: 12px;
  text-decoration: underline;
}

:deep(.stop-external-links) {
  margin-top: 6px;
  padding-top: 4px;
  border-top: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

:deep(.stop-external-links a) {
  color: #1d4ed8;
  font-size: 11px;
  text-decoration: none;
}

:deep(.stop-external-links a:hover) {
  text-decoration: underline;
}
</style>