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
        placeholder="系統名・事業者名・停留所名（ひらがな可）で検索"
      />

      <button
        v-if="geoSupported"
        class="locate-btn"
        @click="locateUser"
        :disabled="locating"
      >
        📍 {{ locating ? '取得中…' : '現在地を表示' }}
      </button>
      <p class="geo-unsupported" v-else>このブラウザ・接続方法では現在地取得は使えません</p>
      <p class="geo-error" v-if="geoError">{{ geoError }}</p>

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
          <span class="route-matched-stop" v-if="r.matchedStopNames.length">
            🚏 {{ r.matchedStopNames.join('、') }}
          </span>
        </button>
        <p class="no-hit" v-if="filteredRoutes.length === 0">該当する系統・停留所がありません</p>
      </div>

      <div class="selected" v-if="selectedRoute">
        <span>選択中: <strong>{{ selectedRoute.route }}</strong>（{{ selectedRoute.operator }}）</span>
        <button class="clear" @click="clearSelection">解除</button>
      </div>
    </div>

    <div class="landmark-panel">
      <div class="landmark-header">📍 ランドマークを追加</div>
      <form class="landmark-form" @submit.prevent="addLandmark">
        <input
          class="landmark-input"
          type="text"
          v-model="landmarkAddress"
          placeholder="住所を入力"
          :disabled="geocoding"
        />
        <button
          class="landmark-add-btn"
          type="submit"
          :disabled="geocoding || !landmarkAddress.trim()"
        >
          {{ geocoding ? '検索中…' : '追加' }}
        </button>
      </form>
      <p class="landmark-error" v-if="landmarkError">{{ landmarkError }}</p>
      <p class="landmark-count" v-if="landmarks.length">{{ landmarks.length }} 件登録中</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { normalize } from '@geolonia/normalize-japanese-addresses'

const mapEl = ref(null)
const loading = ref(true)
const stopCount = ref(0)
const routeCount = ref(0)
const query = ref('')
const selectedRoute = ref(null)
const geoSupported = ref(false)
const locating = ref(false)
const geoError = ref('')

// ランドマーク機能：ユーザーが住所を入力→ジオコーディング→地図に追加。
// localStorageに保存し、次回訪問時も復元する
const landmarkAddress = ref('')
const landmarkError = ref('')
const geocoding = ref(false)
const landmarks = ref([]) // [{id, address, lat, lng, level, createdAt}]

let allRoutes = []
let map = null
let baseLayer = null
let highlightLayer = null
let landmarkLayer = null
let stopsById = {}
let markersById = {}
let highlightMarkersById = {}
let hiddenMarkerIds = []
let dataBounds = null
let userMarker = null

const LANDMARK_STORAGE_KEY = 'kyoto-bus-app:landmarks'

// 「系統名・事業者名」に加えて「停留所名・ひらがな読み」でも検索できるようにする。
// ひらがな読み(kana)は元データに用意されているものだけを対象にし、
// 自動生成(pykakashiなど)は地名変換の精度が低かったため行わない。
// 停留所名にヒットした場合は、その停留所を含む系統も検索結果に含める。
const filteredRoutes = computed(() => {
  const q = query.value.trim()
  if (!q) return []

  const seenKeys = new Set()
  const result = []

  // 1) 系統名・事業者名で直接マッチする系統
  for (const r of allRoutes) {
    if (r.route.includes(q) || r.operator.includes(q)) {
      const key = r.operator + '||' + r.route
      if (!seenKeys.has(key)) {
        seenKeys.add(key)
        result.push({ ...r, matchedStopNames: [] })
      }
    }
  }

  // 2) 停留所名・ひらがな読みでマッチする停留所を探す
  const matchedStopIds = new Set()
  for (const id in stopsById) {
    const s = stopsById[id]
    if (s.name.includes(q) || (s.kana && s.kana.includes(q))) {
      matchedStopIds.add(s.id)
    }
  }

  // 3) その停留所を含む系統を検索結果に追加（どの停留所名でヒットしたか付記する）
  if (matchedStopIds.size) {
    for (const r of allRoutes) {
      const key = r.operator + '||' + r.route
      if (seenKeys.has(key)) continue
      const hitNames = [...new Set(
        r.stopIds
          .filter(id => matchedStopIds.has(id))
          .map(id => stopsById[id]?.name)
          .filter(Boolean)
      )]
      if (hitNames.length) {
        seenKeys.add(key)
        result.push({ ...r, matchedStopNames: hitNames })
      }
    }
  }

  return result.slice(0, 40)
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

// 星アイコンの半径（アイコンサイズの半分）。createStarIconとツールチップの
// オフセット計算の両方で使うので共通化しておく
function starIconHalf(zoom) {
  return (stopRadius(zoom, true) * 3.2) / 2
}

// 選択中の系統の停留所用：星形アイコン（サイズはズームに応じて可変）
function createStarIcon(zoom) {
  const half = starIconHalf(zoom)
  const size = half * 2
  const html = `<svg width="${size}" height="${size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path class="star-glow-path" d="M12 1.2l3.35 6.79 7.5 1.09-5.43 5.29 1.28 7.47L12 18.02l-6.7 3.82 1.28-7.47-5.43-5.29 7.5-1.09L12 1.2z"
      fill="#db2777" stroke="#f9a8d4" stroke-width="1.4" stroke-linejoin="round"/>
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

// 現在地マーカー用のパルスアイコン（停留所のアイコンと見分けやすいよう青系のドット＋波紋）
function createUserLocationIcon() {
  return window.__L.divIcon({
    html: `<span class="user-location-dot"><span class="user-location-pulse"></span></span>`,
    className: 'user-location-icon',
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  })
}

// ランドマーク用：ピン針型の自作SVGアイコン（バス停の丸ドット・星とは
// 形状も色も明確に区別できるようにする）。サイズは固定（ズームに応じて
// 可変にしているバス停アイコンとは異なり、常に一定の大きさで目立たせる）
const LANDMARK_ICON_W = 30
const LANDMARK_ICON_H = 40
function createLandmarkIcon() {
  const html = `<svg width="${LANDMARK_ICON_W}" height="${LANDMARK_ICON_H}" viewBox="0 0 30 40" xmlns="http://www.w3.org/2000/svg">
    <path d="M15 0C6.716 0 0 6.716 0 15c0 11.25 15 25 15 25s15-13.75 15-25C30 6.716 23.284 0 15 0z"
      fill="#7c3aed" stroke="#ffffff" stroke-width="1.5"/>
    <circle cx="15" cy="15" r="5.5" fill="#ffffff"/>
  </svg>`
  return window.__L.divIcon({
    html,
    className: 'landmark-pin-icon',
    iconSize: [LANDMARK_ICON_W, LANDMARK_ICON_H],
    iconAnchor: [LANDMARK_ICON_W / 2, LANDMARK_ICON_H], // 針先が座標点になるようアンカーを最下部に
    popupAnchor: [0, -LANDMARK_ICON_H]
  })
}

// ポップアップ内に番号・入力住所・削除ボタンを表示する（番号はピン自体には
// 焼き込まず、あくまでポップアップ内だけの表示。表示中の並び順＝landmarks
// 配列の順序で採番するため、削除すると後続の番号が詰め直される）。
// buildPopupHtml（停留所側）と同様、ストリートビューは座標にパノラマが
// 無いと真っ黒になるため、代わりにAPIキー不要の地図埋め込み(output=embed)を使う
function buildLandmarkPopupHtml(landmark, number) {
  const lat = landmark.lat
  const lng = landmark.lng
  const streetViewHtml = `<div class="landmark-streetview">
  <iframe
    src="https://maps.google.com/maps?q=${lat},${lng}&z=18&output=embed"
    width="200"
    height="200"
    style="border:0;"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>`
  const externalLinksHtml = `
    <div class="landmark-external-links">
      <a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}&heading=180&pitch=0&fov=80" target="_blank" rel="noopener">📍 Street View</a>
    </div>`
  return `<div class="landmark-popup">
    <p class="landmark-popup-title">📍 ランドマーク #${number}</p>
    <p class="landmark-popup-address">${escapeHtml(landmark.address)}</p>
    ${streetViewHtml}
    ${externalLinksHtml}
    <button class="landmark-delete-btn" data-id="${escapeHtml(landmark.id)}">このランドマークを削除</button>
  </div>`
}

function loadLandmarksFromStorage() {
  if (typeof localStorage === 'undefined') return []
  try {
    const raw = localStorage.getItem(LANDMARK_STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (err) {
    console.error('ランドマークの読み込みに失敗したにゃ:', err)
    return []
  }
}

function saveLandmarksToStorage() {
  if (typeof localStorage === 'undefined') return
  try {
    localStorage.setItem(LANDMARK_STORAGE_KEY, JSON.stringify(landmarks.value))
  } catch (err) {
    console.error('ランドマークの保存に失敗したにゃ:', err)
  }
}

// landmarks配列の現在の内容から、landmarkLayerを丸ごと描き直す。
// 追加・削除どちらの後もこれを呼べば表示とポップアップ番号が常に一致する
function renderLandmarks() {
  if (!landmarkLayer) return
  landmarkLayer.clearLayers()
  const L = window.__L
  landmarks.value.forEach((lm, idx) => {
    const marker = L.marker([lm.lat, lm.lng], { icon: createLandmarkIcon() })
    marker.bindPopup(buildLandmarkPopupHtml(lm, idx + 1), { maxWidth: 320 })
    marker.addTo(landmarkLayer)
  })
}

// 住所入力→ジオコーディング→ランドマーク追加。
// levelは町丁目レベル(5)を要求。通り名住所など正規化に失敗するケースが
// あるため、point が取れなかった場合はエラーメッセージを出すだけに留める
async function addLandmark() {
  const address = landmarkAddress.value.trim()
  if (!address) return

  landmarkError.value = ''
  geocoding.value = true
  try {
    const result = await normalize(address, { level: 5 })
    if (!result || !result.point) {
      landmarkError.value = '座標を特定できませんでした。住所を見直してください'
      return
    }

    const landmark = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      address,
      lat: result.point.lat,
      lng: result.point.lng,
      level: result.point.level,
      createdAt: Date.now()
    }
    landmarks.value.push(landmark)
    saveLandmarksToStorage()
    renderLandmarks()
    landmarkAddress.value = ''

    if (map) map.setView([landmark.lat, landmark.lng], Math.max(map.getZoom(), 16))
  } catch (err) {
    console.error('ジオコーディングに失敗したにゃ:', err)
    landmarkError.value = '住所の変換に失敗しました。しばらくして再度お試しください'
  } finally {
    geocoding.value = false
  }
}

function removeLandmark(id) {
  landmarks.value = landmarks.value.filter(lm => lm.id !== id)
  saveLandmarksToStorage()
  renderLandmarks()
}

// ブラウザのGeolocation APIで現在地を取得し、地図上にプロットする。
// ユーザーが「現在地を表示」ボタンを押した時だけ呼ばれる（無断で位置情報を
// 取得しない）。このアプリは京都エリアのバス停を探すためのものなので、
// 取得した現在地が実際の停留所データの分布範囲（dataBounds）の外にある
// 場合はプロットしない＝京都にいないユーザーには現在地マーカーを出さない。
function locateUser() {
  geoError.value = ''

  if (!navigator.geolocation) {
    geoError.value = 'このブラウザでは現在地取得に対応していません'
    return
  }
  if (!dataBounds) {
    geoError.value = '停留所データの読み込みが完了していません'
    return
  }

  locating.value = true
  navigator.geolocation.getCurrentPosition(
    (position) => {
      locating.value = false
      const { latitude, longitude } = position.coords
      if (!dataBounds.contains([latitude, longitude])) {
        geoError.value = '現在地が京都のバス停エリア外のため表示できません'
        return
      }
      const L = window.__L
      if (userMarker) userMarker.remove()
      userMarker = L.marker([latitude, longitude], {
        icon: createUserLocationIcon(),
        zIndexOffset: 1000
      }).addTo(map)
      userMarker.bindPopup('現在地')
      map.setView([latitude, longitude], 15)
    },
    (error) => {
      locating.value = false
      // PERMISSION_DENIED=1, POSITION_UNAVAILABLE=2, TIMEOUT=3
      if (error.code === 1) {
        geoError.value = '位置情報の利用が許可されませんでした'
      } else if (error.code === 2) {
        geoError.value = '現在地を取得できませんでした'
      } else if (error.code === 3) {
        geoError.value = '現在地の取得がタイムアウトしました'
      } else {
        geoError.value = '現在地の取得に失敗しました'
      }
      console.error('位置情報の取得に失敗したにゃ:', error)
    },
    { enableHighAccuracy: true, timeout: 10000 }
  )
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

// 系統選択時、アンカー以外の星マーカーに常時表示する「小さいラベル」
// (停留所名＋ひらがな読み[あれば])。Tooltip(permanent)を使うことで、
// 既存のPopup(ホバー時のフル情報表示・アンカーの開きっぱなしポップアップ)の
// autoClose挙動に一切影響を与えずに独立して表示できる。
function buildMiniStopLabel(stop) {
  const kanaHtml = stop.kana ? `<br><span class="stop-mini-kana">${escapeHtml(stop.kana)}</span>` : ''
  return `<span class="stop-mini-name">${escapeHtml(stop.name)}</span>${kanaHtml}`
}

function buildPopupHtml(stop, subLabel) {
  const kanaHtml = stop.kana ? `<p class="stop-kana">${escapeHtml(stop.kana)}</p>` : ''
  const subLabelHtml = subLabel ? `<p class="stop-sub">${subLabel}</p>` : ''
  const linkHtml = stop.url
    ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">🕒 時刻表を見る</a></p>`
    : ''

  const lat = stop.lat
  const lng = stop.lng

  // ストリートビューは停留所の座標にパノラマが無いと真っ黒になってしまうため、
  // 代わりに座標さえあれば確実にその地点へピンが立つ「地図埋め込み」形式を使う。
  // https://maps.google.com/maps?q=LAT,LNG&z=ZOOM&output=embed はAPIキー不要で
  // 座標をそのまま渡せる、Googleの昔からある素の埋め込み形式。
  const streetViewHtml = `<div class="stop-streetview">
  <iframe
    src="https://maps.google.com/maps?q=${lat},${lng}&z=18&output=embed"
    width="200"
    height="200"
    style="border:0;"
    loading="lazy"
    allowfullscreen>
  </iframe>
</div>`


  const externalLinksHtml = `
    <div class="stop-external-links">
      <a href="https://www.google.com/maps/search/?api=1&query=${lat},${lng}&zoom=16" target="_blank" rel="noopener">📍 Google Maps</a>
      <a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}&heading=180&pitch=0&fov=80" target="_blank" rel="noopener">📍 Street View</a>
      <a href="https://earth.google.com/web/@${lat},${lng},0a,1000d" target="_blank" rel="noopener">📍 Google Earth</a>
      <a href="https://map.yahoo.co.jp/place?lat=${lat}&lon=${lng}&zoom=16&maptype=basic" target="_blank" rel="noopener">📍 Yahoo! Map</a>
      <a href="https://labs.mapple.com/mapplevt.html#17/${lat}/${lng}" target="_blank" rel="noopener">📍 MAPPLE</a>
    </div>`

  return `<div class="stop-popup">
    <p class="stop-name">${escapeHtml(stop.name)}</p>
    ${kanaHtml}
    ${subLabelHtml}
    ${streetViewHtml}
    ${linkHtml}
    ${externalLinksHtml}
  </div>`
}

// 通常表示時／薄く表示する時のマーカー不透明度
const BASE_OPACITY = 0.45
const DIMMED_OPACITY = 0.3

function renderHighlight(route, anchorStopId) {
  if (!map) return
  highlightMarkersById = {}
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
  const half = starIconHalf(zoom)
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

    // どの停留所かを識別できるようマーカーに直接タグ付けしておく
    // （map全体のpopupopen/popupcloseイベントから、この星かどうかを判定するため）
    marker._highlightStopId = id

    // まず全員に停留所名＋ひらがな読みの小さいラベルを付けておく。
    // ポップアップが開いている星だけは、popupopenイベント側で自動的に
    // このツールチップを外す（下のonMountedの map.on('popupopen', ...) 参照）
    marker.bindTooltip(buildMiniStopLabel(stop), {
      permanent: true,
      direction: 'top',
      offset: [0, -half],
      className: 'stop-mini-tooltip'
    })

    marker.addTo(highlightLayer)
    highlightMarkersById[id] = marker

    if (anchorStopId != null && String(id) === String(anchorStopId)) {
      anchorMarker = marker
    }
  }

  if (anchorMarker) {
    // ポップアップ内の系統名クリックから来た場合：どの停留所を見ていたか
    // 見失わないよう、地図の中心・ズームは動かさず、同じ場所の星マーカーの
    // ポップアップを開き直す（開いた瞬間、popupopenハンドラがこの星の
    // ツールチップを自動的に外す）
    anchorMarker.openPopup()
  } else if (bounds.length) {
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 })
  }
}

onMounted(async () => {
  // Geolocation APIはHTTPS(またはlocalhost)などのセキュアコンテキストでないと
  // 使えない。navigator.geolocation自体が無いブラウザもあるため、両方チェックして
  // ボタンを出すかどうかを決める（使えない環境ではボタンごと出さず、無言で
  // 失敗させない）
  geoSupported.value = typeof navigator !== 'undefined'
    && !!navigator.geolocation
    && (typeof window === 'undefined' || window.isSecureContext !== false)

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
    zoom: 14
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

    // 星マーカー（ハイライト中の系統の停留所）のポップアップが開いたら、
    // その星だけ小さいラベル(ツールチップ)を一時的に外す。
    // 「ポップアップが表示されているもの以外にツールチップが表示される」
    // というルールを、系統選択直後だけでなく別の星に切り替えた時にも保つため。
    if (marker._highlightStopId != null && marker.getTooltip()) {
      marker.unbindTooltip()
    }
  })

  // 星マーカーのポップアップが閉じたら（＝別の星に移った、または解除された）、
  // まだ同じ系統内の星として現役なら、小さいラベルを付け直す
  map.on('popupclose', (e) => {
    const marker = e.popup._source
    if (!marker || marker._highlightStopId == null) return
    const id = marker._highlightStopId
    if (highlightMarkersById[id] !== marker) return
    if (marker.getTooltip()) return
    const stop = stopsById[id]
    if (!stop) return
    marker.bindTooltip(buildMiniStopLabel(stop), {
      permanent: true,
      direction: 'top',
      offset: [0, -starIconHalf(map.getZoom())],
      className: 'stop-mini-tooltip'
    })
  })

  // ポップアップ内の系統名・運行会社名・ランドマーク削除ボタンクリックをイベント委譲で処理
  mapEl.value.addEventListener('click', (e) => {
    const deleteEl = e.target.closest('.landmark-delete-btn')
    if (deleteEl) {
      removeLandmark(deleteEl.dataset.id)
      return
    }
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
  
  //L.tileLayer("https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}", {
  //  attribution: '<a href="https://developers.google.com/maps/documentation" target="_blank">Google Map</a>',
  //  maxZoom: 21
  //}).addTo(map);

  

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
    maxZoom: 21
  }).addTo(map)

  // ランドマークレイヤーは停留所データの読み込みを待たずに初期化し、
  // localStorageに保存済みのランドマークがあればすぐ復元して表示する
  landmarkLayer = L.layerGroup().addTo(map)
  landmarks.value = loadLandmarksFromStorage()
  renderLandmarks()
  
  try {
    // lyrs=m: Standard Roadmap（通常の地図）
    // lyrs=s: Satellite only（航空写真のみ、文字なし）
    // lyrs=y: Hybrid（航空写真 ＋ 道路 ＋ 日本語ラベル）
    // lyrs=p: Terrain（地形図）
    // hl=ja: 言語を日本語に固定
    
    L.tileLayer('https://mt1.google.com/vt/lyrs=s&hl=ja&x={x}&y={y}&z={z}', {
      attribution: '© Google',
      maxZoom: 21,
      opacity: 0.6
    }).addTo(map);
  } catch (e) {
    console.error('❌ Error adding tile layer:', e);
  }

  // 事業者単位のバスルート線　道路 // 事業者単位のバスルート線
  //fetch('/data/route_lines.geojson')
  //  .then(res => res.json())
  //  .then(routeLines => {
  //    L.geoJSON(routeLines, {
  //      interactive: false,
  //      style: { color: '#94a3b8', weight: 1.5, opacity: 0.5 }
  //    }).addTo(map)
  //  })

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

  // 実際の停留所データの分布範囲を「京都エリア」とみなす（都道府県境で
  // 厳密に区切るのではなく、このアプリが対象とするバス停の分布範囲そのものを使う）
  dataBounds = L.latLngBounds(stops.map(s => [s.lat, s.lng]))

  // 画面からはみ出た／密集している停留所は自動でクラスタリングしてアイコン数を
  // 減らし、描画・操作の負荷を下げる（chunkedLoading で4685件の初期追加も分割処理）
  // ※ プラグインが読み込めなかった場合は通常のlayerGroupにフォールバックする
  baseLayer = (clusteringAvailable && typeof L.markerClusterGroup === 'function')
    ? L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 60,
        disableClusteringAtZoom: 15,
        // クラスタを放射状に展開(スパイダーファイ)すると停留所が実際とは
        // 違う位置に配置され、つなぎの線も表示されて紛らわしいため無効化。
        // クリック時は zoomToBoundsOnClick（デフォルト有効）でズームインするのみにする
        spiderfyOnMaxZoom: false,
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

.locate-btn {
  margin-top: 6px;
  width: 100%;
  box-sizing: border-box;
  padding: 6px 8px;
  border: 1px solid #2563eb;
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
}

.locate-btn:hover:not(:disabled) {
  background: #dbeafe;
}

.locate-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

.geo-unsupported {
  margin: 6px 0 0;
  font-size: 11px;
  color: #888;
}

.geo-error {
  margin: 6px 0 0;
  font-size: 12px;
  color: #dc2626;
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

.route-matched-stop {
  font-size: 11px;
  color: #0d9488;
  margin-top: 2px;
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

.landmark-panel {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.96);
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.25);
  width: min(260px, calc(100vw - 24px));
}

.landmark-header {
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.landmark-form {
  display: flex;
  gap: 6px;
}

.landmark-input {
  flex: 1;
  min-width: 0;
  box-sizing: border-box;
  padding: 6px 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 13px;
}

.landmark-add-btn {
  border: 1px solid #7c3aed;
  background: #f5f3ff;
  color: #6d28d9;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
}

.landmark-add-btn:hover:not(:disabled) {
  background: #ede9fe;
}

.landmark-add-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

.landmark-error {
  margin: 6px 0 0;
  font-size: 12px;
  color: #dc2626;
}

.landmark-count {
  margin: 6px 0 0;
  font-size: 11px;
  color: #888;
}

:deep(.landmark-pin-icon) {
  background: transparent;
  border: none;
  overflow: visible;
}

:deep(.landmark-pin-icon) svg {
  display: block;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.4));
}

:deep(.landmark-popup) {
  line-height: 1.4;
}

:deep(.landmark-popup-title) {
  font-weight: 700;
  margin: 0 0 4px;
}

:deep(.landmark-popup-address) {
  margin: 0 0 8px;
  color: #444;
  font-size: 12px;
}

:deep(.landmark-delete-btn) {
  border: none;
  background: #dc2626;
  color: white;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

:deep(.landmark-streetview) {
  margin-top: 6px;
}

:deep(.landmark-external-links) {
  margin-top: 6px;
  padding-top: 4px;
  border-top: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

:deep(.landmark-external-links a) {
  color: #1d4ed8;
  font-size: 11px;
  text-decoration: none;
}

:deep(.landmark-external-links a:hover) {
  text-decoration: underline;
}

:deep(.landmark-delete-btn:hover) {
  background: #b91c1c;
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
    stroke-opacity: 0.6;
    filter: drop-shadow(0 0 1px rgba(157, 23, 77, 0.45));
  }
  50% {
    stroke-width: 1.6;
    stroke-opacity: 1;
    filter: drop-shadow(0 0 3px rgba(100, 23, 77, 0.5));
  }
  100% {
    stroke-width: 1.4;
    stroke-opacity: 0.6;
    filter: drop-shadow(0 0 1px rgba(157, 23, 77, 0.45));
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
  background: rgba(234, 255, 0, 0.35);
  border: 1px solid rgba(250, 250, 200, 0.45);
  
  text-align: center;
  font-weight: 700;
  font-size: 12px;
  color: #eaff00;
}

:deep(.user-location-icon) {
  background: transparent;
  border: none;
}

:deep(.user-location-dot) {
  position: relative;
  display: block;
  width: 14px;
  height: 14px;
  margin: 1px;
  background: #2563eb;
  border: 2px solid #fff;
  border-radius: 50%;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

:deep(.user-location-pulse) {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 14px;
  height: 14px;
  margin: -7px 0 0 -7px;
  background: rgba(37, 99, 235, 0.5);
  border-radius: 50%;
  animation: user-location-pulse 2s ease-out infinite;
}

@keyframes user-location-pulse {
  0% {
    transform: scale(1);
    opacity: 0.7;
  }
  100% {
    transform: scale(3);
    opacity: 0;
  }
}

:deep(.stop-mini-tooltip) {
  font-size: 11px;
  line-height: 1.3;
  padding: 2px 6px;
  white-space: nowrap;
  background: #fff;      /* ← 追加: 薄いピンクの背景 */
  border-color: #fff;    /* ← 追加: 枠線も薄ピンクに揃える(任意) */
}

:deep(.stop-mini-name) {
  font-weight: 700;
  color: #111;
}

:deep(.stop-mini-kana) {
  color: #666;
  font-size: 10px;
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