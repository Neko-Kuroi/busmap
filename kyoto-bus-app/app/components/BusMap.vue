<template>
  <div class="map-wrap">
    <div id="map" ref="mapEl"></div>

    <!-- 右下のズームボタンのすぐ上に小さく表示するロゴ -->
    <img src="/logo.png" alt="" class="corner-logo" />

    <div class="ui-overlay">
      <div class="status" v-if="loading">停留所データを読み込み中…</div>

      <div class="panel" v-else>
        <div class="count">{{ stopCount.toLocaleString() }} 件の停留所（{{ routeCount.toLocaleString() }} 系統）</div>

        <input
          class="search"
          type="text"
          v-model="query"
          maxlength="50"
          placeholder="系統名・事業者名・停留所名で検索"
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

      <div class="right-stack">
        <div class="landmark-panel">
          <button class="landmark-header" @click="landmarkPanelOpen = !landmarkPanelOpen">
            📍 ランドマークを追加
            <span class="landmark-toggle-arrow">{{ landmarkPanelOpen ? '▲' : '▼' }}</span>
          </button>
          <template v-if="landmarkPanelOpen">
            <form class="landmark-form" @submit.prevent="addLandmark">
              <input
                class="landmark-input"
                type="text"
                v-model="landmarkAddress"
                maxlength="140"
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
            <p class="landmark-count" v-if="landmarks.length">{{ landmarks.length }} / {{ LANDMARK_LIMIT }} 件登録中</p>
          </template>
        </div>

        <div class="history-panel" v-if="viewHistory.length">
          <div class="history-header">🕘 最近見た停留所</div>
          <div class="history-list">
            <button
              v-for="h in viewHistory"
              :key="h.coordKey"
              class="history-item"
              @click="goToHistoryEntry(h)"
            >
              <span class="history-name">{{ h.name }}</span>
              <span class="history-other" v-if="h.otherCount">他{{ h.otherCount }}件</span>
            </button>
          </div>
        </div>
      </div>
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

const landmarkAddress = ref('')
const landmarkError = ref('')
const geocoding = ref(false)
const landmarks = ref([])
// ランドマーク入力欄は初期状態でたたんでおき、ヘッダー部分をクリックすると開く
const landmarkPanelOpen = ref(false)

// 最近見た停留所の履歴。座標(coordKey)ごとに1件のみ保持し、再訪すると
// 先頭に繰り上がる（ブラウザの閲覧履歴と同じ挙動）。localStorageに永続化する
const viewHistory = ref([]) // [{coordKey, name, otherCount, lat, lng, lastViewedAt}]

let allRoutes = []
let map = null
let baseLayer = null
let highlightLayer = null
let landmarkLayer = null
let poiLayer = null
let routeLinesLayer = null
let routeLinesGeojson = null // {type:'FeatureCollection', features:[...]} 全事業者ぶんを保持し、activeOperatorで都度絞り込む
let stopsById = {}
let markersById = {}
let highlightMarkersById = {}
let hiddenMarkerIds = []
let dataBounds = null
let userMarker = null

// 座標(coordKey)ごとの重複統合グループ情報。{ stops: [...], baseMarker, starMarker }
// 黄色ドット・星どちらのグループポップアップもここを参照して同じstops配列を使う
// （星がハイライト中に黄色ドットを隠しても、星のポップアップから同じ情報にアクセスできる）
let groupsByCoordKey = {}

// 座標(coordKey)ごとに「最後に見ていたポップアップのページ番号」を記憶する。
// マーカーインスタンス自体は星側だと系統選択のたびに作り直されるため、
// マーカーの外（座標キー）に持たせることで選び直しても記憶が引き継がれる
let groupPageByCoord = {}

const LANDMARK_STORAGE_KEY = 'kyoto-bus-app:landmarks'
const HISTORY_STORAGE_KEY = 'kyoto-bus-app:viewHistory'
const HISTORY_LIMIT = 50

// 停留所の緯度経度から、重複統合・ページ記憶・履歴で共通して使う座標キーを作る
function coordKeyOf(lat, lng) {
  return `${lat.toFixed(6)},${lng.toFixed(6)}`
}

const filteredRoutes = computed(() => {
  const q = sanitizeInput(query.value, 50)
  if (!q) return []

  const seenKeys = new Set()
  const result = []

  for (const r of allRoutes) {
    if (r.route.includes(q) || r.operator.includes(q)) {
      const key = r.operator + '||' + r.route
      if (!seenKeys.has(key)) {
        seenKeys.add(key)
        result.push({ ...r, matchedStopNames: [] })
      }
    }
  }

  const matchedStopIds = new Set()
  for (const id in stopsById) {
    const s = stopsById[id]
    if (s.name.includes(q) || (s.kana && s.kana.includes(q))) {
      matchedStopIds.add(s.id)
    }
  }

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

// 事業者名(activeOperator)でroute_lines.geojsonを絞り込んで描き直す。
// 系統選択・運行会社名クリックのどちらからも呼ばれる共通のレンダリング関数。
// operatorがnullなら消すだけ（系統選択解除時など）
function renderRouteLines(operator) {
  if (!routeLinesLayer) return
  routeLinesLayer.clearLayers()
  if (!operator || !routeLinesGeojson) return

  const L = window.__L
  const filtered = {
    type: 'FeatureCollection',
    features: routeLinesGeojson.features.filter(f => f.properties.operator === operator)
  }
  L.geoJSON(filtered, {
    interactive: false,
    style: { color: '#f472b6', weight: 3, opacity: 0.5 }
  }).addTo(routeLinesLayer)
}

function clearSelection() {
  selectedRoute.value = null
  query.value = ''
  renderHighlight(null)
  renderRouteLines(null)
}

function selectRoute(r, anchorStopId) {
  selectedRoute.value = r
  renderHighlight(r, anchorStopId)
  renderRouteLines(r.operator)
}

function stopRadius(zoom, isHighlight) {
  const base = Math.max(6, Math.min(14, zoom - 6))
  return isHighlight ? base + 3 : base
}

function starIconHalf(zoom) {
  return (stopRadius(zoom, true) * 3.2) / 2
}

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

// 検索欄・ランドマーク住所欄、両方の入力を使う直前にかける軽いサニタイズ。
// 制御文字(改行・タブ含む)を除去し、連続する空白を1つに圧縮してから前後を
// trimする。表示時のXSS対策はescapeHtml側で別途行っているため、ここでは
// あくまで「見た目の崩れ・無駄なAPI呼び出しを防ぐための入力クレンジング」
function sanitizeInput(str, maxLength) {
  return String(str)
    .replace(/[\x00-\x1F\x7F]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, maxLength)
}

function createUserLocationIcon() {
  return window.__L.divIcon({
    html: `<span class="user-location-dot"><span class="user-location-pulse"></span></span>`,
    className: 'user-location-icon',
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  })
}

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
    iconAnchor: [LANDMARK_ICON_W / 2, LANDMARK_ICON_H],
    popupAnchor: [0, -LANDMARK_ICON_H]
  })
}

// 周辺POI用：小さい逆三角形の自作SVGアイコン。バス停の丸ドット・星・
// ランドマークピンのいずれとも被らない青系統・半透明(40%)にして、
// 最大50個同時に出ても地図が主張しすぎないようにする
const POI_ICON_SIZE = 14
function createPoiIcon() {
  const html = `<svg width="${POI_ICON_SIZE}" height="${POI_ICON_SIZE}" viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg">
    <polygon points="1,1 13,1 7,13" fill="#2563eb" fill-opacity="0.4" stroke="#1d4ed8" stroke-width="1"/>
  </svg>`
  return window.__L.divIcon({
    html,
    className: 'poi-marker-icon',
    iconSize: [POI_ICON_SIZE, POI_ICON_SIZE],
    iconAnchor: [POI_ICON_SIZE / 2, POI_ICON_SIZE / 2]
  })
}

// 停留所（黄色ドット・星どちらも）をクリックしたときに呼ばれる。
// その座標の周辺POI(事前計算済み・最大50件)を、既存のPOIマーカーを全部
// 消してから描き直す。POIは常時表示ではなくクリックした名称のみ
// ツールチップで見せる（bindTooltipはpermanent:falseでクリック時にopenTooltip）
function showPoisForCoord(coordKey) {
  if (!poiLayer) return
  poiLayer.clearLayers()
  const entry = groupsByCoordKey[coordKey]
  const pois = entry && entry.nearbyPois
  if (!pois || !pois.length) return

  const L = window.__L
  for (const poi of pois) {
    const marker = L.marker([poi.lat, poi.lon], { icon: createPoiIcon() })
    marker.bindTooltip(escapeHtml(poi.name), {
      direction: 'top',
      offset: [0, -POI_ICON_SIZE / 2],
      className: 'poi-tooltip'
    })
    marker.on('click', (e) => {
      // 停留所側のクリックハンドラ(showPoisForCoord自体)が再度呼ばれて
      // poiLayerが消えてしまわないよう、マップへのクリック伝播を止める
      L.DomEvent.stopPropagation(e)
      marker.openTooltip()
    })
    marker.addTo(poiLayer)
  }
}

// function buildLandmarkPopupHtml(landmark, number) {
//   const lat = landmark.lat
//   const lng = landmark.lng
//   const streetViewHtml = `<div class="landmark-streetview">
//   <iframe
//     src="https://maps.google.com/maps?q=${lat},${lng}&z=18&output=embed"
//     width="200"
//     height="200"
//     style="border:0;"
//     loading="lazy"
//     allowfullscreen>
//   </iframe>
// </div>`
//   const externalLinksHtml = `
//     <div class="landmark-external-links">
//       <a href="https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}&heading=180&pitch=0&fov=80" target="_blank" rel="noopener">📍 Street View</a>
//     </div>`
//   return `<div class="landmark-popup">
//     <p class="landmark-popup-title">📍 ランドマーク #${number}</p>
//     <p class="landmark-popup-address">${escapeHtml(landmark.address)}</p>
//     ${streetViewHtml}
//     ${externalLinksHtml}
//     <button class="landmark-delete-btn" data-id="${escapeHtml(landmark.id)}">このランドマークを削除</button>
//   </div>`
// }

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
      <a href="https://maps.apple.com/?ll=${lat},${lng}&z=19" target="_blank" rel="noopener">📍 Apple Maps</a>
      <a href="https://map.yahoo.co.jp/place?lat=${lat}&lon=${lng}&zoom=16&maptype=basic" target="_blank" rel="noopener">📍 Yahoo! Map</a>
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

const LANDMARK_LIMIT = 20 // 上限に厳密な根拠はないが、無制限は脆弱性になるため上限を設ける

async function addLandmark() {
  const address = sanitizeInput(landmarkAddress.value, 140)
  if (!address) return

  landmarkError.value = ''

  // 上限に達している場合はジオコーディングすら行わずここで止める。
  // 「新しい方を優先して古いものを自動的に消す」方式は、上限の存在を
  // 知らないユーザーが前に登録したランドマークが突然消えて驚くことになるため、
  // 追加をブロックして「削除してから追加してください」と促す方式にする
  if (landmarks.value.length >= LANDMARK_LIMIT) {
    landmarkError.value = `ランドマークは${LANDMARK_LIMIT}件までです。削除してから追加してください`
    return
  }

  geocoding.value = true
  try {
    const result = await normalize(address, { level: 5 })
    if (!result || !result.point) {
      landmarkError.value = '座標を特定できませんでした。住所を見直してください'
      return
    }

    // このアプリは京都エリアのバス停を対象にしているため、ジオコーディング
    // 結果の都道府県が京都府でない場合は入り口で弾く。pref自体が取れない
    // （通り名住所などで正規化レベルが足りず特定できない）場合も安全側で弾く
    if (result.pref !== '京都府') {
      landmarkError.value = '京都府内の住所のみ登録できます'
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

function loadHistoryFromStorage() {
  if (typeof localStorage === 'undefined') return []
  try {
    const raw = localStorage.getItem(HISTORY_STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (err) {
    console.error('履歴の読み込みに失敗したにゃ:', err)
    return []
  }
}

function saveHistoryToStorage() {
  if (typeof localStorage === 'undefined') return
  try {
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(viewHistory.value))
  } catch (err) {
    console.error('履歴の保存に失敗したにゃ:', err)
  }
}

// 停留所（黄色ドット・星どちらでも）のポップアップが開いた瞬間に呼ばれる。
// 同じcoordKeyが既に履歴にあれば新規追加せず、日時だけ更新して先頭に繰り上げる
// （ブラウザの閲覧履歴と同じ挙動）。直近HISTORY_LIMIT件を超えたら古い順に削除する
function recordHistory(coordKey) {
  const entry = groupsByCoordKey[coordKey]
  if (!entry) return
  const first = entry.stops[0]
  const otherCount = entry.stops.length - 1

  const existingIndex = viewHistory.value.findIndex(h => h.coordKey === coordKey)
  if (existingIndex !== -1) viewHistory.value.splice(existingIndex, 1)

  viewHistory.value.unshift({
    coordKey,
    name: first.name,
    otherCount,
    lat: first.lat,
    lng: first.lng,
    lastViewedAt: Date.now()
  })

  if (viewHistory.value.length > HISTORY_LIMIT) {
    viewHistory.value.length = HISTORY_LIMIT
  }

  saveHistoryToStorage()
}

// 履歴パネルの項目クリック→その座標へ地図をジャンプし、黄色ドット側のポップアップを開く。
// 系統ハイライト中でその座標が非表示（opacity 0）になっている場合は、
// ポップアップ自体は開けるがドットが見えない状態になりうる（既知の制約）
function goToHistoryEntry(h) {
  if (!map) return
  map.setView([h.lat, h.lng], Math.max(map.getZoom(), 16))
  const entry = groupsByCoordKey[h.coordKey]
  if (entry && entry.baseMarker) {
    entry.baseMarker.openPopup()
  }
}

// ポップアップ内のページ送りリンククリック→該当座標の記憶ページを更新し、
// 今開いているポップアップ（黄色ドット・星どちらか開いている方）の中身だけ差し替える
function goToStopPage(coordKey, page) {
  const entry = groupsByCoordKey[coordKey]
  if (!entry) return
  groupPageByCoord[coordKey] = page
  const html = buildGroupedPopupHtml(coordKey, page)
  if (entry.baseMarker && entry.baseMarker.isPopupOpen()) {
    entry.baseMarker.setPopupContent(html)
  }
  if (entry.starMarker && entry.starMarker.isPopupOpen()) {
    entry.starMarker.setPopupContent(html)
  }
}

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

function onPopupRouteClick(operator, route, anchorStopId) {
  const match = allRoutes.find(r => r.operator === operator && r.route === route)
  if (!match) return
  query.value = route
  selectRoute(match, anchorStopId)
}

function onPopupOperatorClick(operator) {
  query.value = operator
  // 系統は選択しないが、事業者の路線パスだけは表示する
  renderRouteLines(operator)
}

function buildStopSubLabel(stop) {
  const routesHtml = stop.routes.length
    ? stop.routes
        .map(rt => `<span class="route-link" data-operator="${escapeHtml(stop.operator)}" data-route="${escapeHtml(rt)}" data-stop-id="${stop.id}">${escapeHtml(rt)}</span>`)
        .join('<br>')
    : '（系統情報なし）'
  // 系統が多い停留所ではポップアップが縦にどんどん伸びてしまうため、
  // 系統一覧だけを独立したブロック(stop-routes-scroll)にして、5行を超えたら
  // その部分だけ縦スクロールにする（停留所名・かな等は伸びず固定のまま）
  return `<span class="operator-link" data-operator="${escapeHtml(stop.operator)}">${escapeHtml(stop.operator)}</span><div class="stop-routes-inline stop-routes-scroll">${routesHtml}</div>`
}

// groupSizeが2以上の場合、代表停留所名の下に「他◯件」を添える
// （同一座標に複数stopがある場合、ツールチップに全件詰め込まず代表1件＋件数のみ表示する）
function buildMiniStopLabel(stop, groupSize) {
  const kanaHtml = stop.kana ? `<br><span class="stop-mini-kana">${escapeHtml(stop.kana)}</span>` : ''
  const otherHtml = groupSize && groupSize > 1
    ? `<br><span class="stop-mini-other">他${groupSize - 1}件</span>`
    : ''
  return `<span class="stop-mini-name">${escapeHtml(stop.name)}</span>${kanaHtml}${otherHtml}`
}

function buildLocationExtrasHtml(lat, lng) {
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
      <a href="https://maps.apple.com/?ll=${lat},${lng}&z=19" target="_blank" rel="noopener">📍 Apple Maps</a>
      <a href="https://earth.google.com/web/@${lat},${lng},0a,1000d" target="_blank" rel="noopener">📍 Google Earth</a>
      <a href="https://map.yahoo.co.jp/place?lat=${lat}&lon=${lng}&zoom=16&maptype=basic" target="_blank" rel="noopener">📍 Yahoo! Map</a>
      <a href="https://labs.mapple.com/mapplevt.html#17/${lat}/${lng}" target="_blank" rel="noopener">📍 MAPPLE</a>
    </div>`

  return streetViewHtml + externalLinksHtml
}

function buildPopupHtml(stop, subLabel) {
  const kanaHtml = stop.kana ? `<p class="stop-kana">${escapeHtml(stop.kana)}</p>` : ''
  const subLabelHtml = subLabel ? `<div class="stop-sub">${subLabel}</div>` : ''
  const linkHtml = stop.url
    ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">🕒 時刻表を見る</a></p>`
    : ''

  const extrasHtml = buildLocationExtrasHtml(stop.lat, stop.lng)

  return `<div class="stop-popup">
    <p class="stop-name">${escapeHtml(stop.name)}</p>
    ${kanaHtml}
    ${subLabelHtml}
    ${linkHtml}
    ${extrasHtml}
  </div>`
}

// 同一座標(小数点6桁まで完全一致)に複数のstopレコードが存在する場合の
// ポップアップ。1件を超える場合は「1ページ1レコード」のページング表示に
// する（全件を縦に並べると長くなりすぎるため）。ページ番号はgroupPageByCoord
// に座標キーで記憶されており、ポップアップを開き直しても・系統を選び直しても
// 保持される。地図埋め込み・外部リンクは座標共通なので、どのページでも
// 末尾に1回だけ表示する。coordKeyはgroupsByCoordKeyを引くためのキーで、
// 黄色ドット・星どちらのグループポップアップからも共通で参照する
function buildGroupedPopupHtml(coordKey, pageIndex) {
  const entry = groupsByCoordKey[coordKey]
  if (!entry) return ''
  const stopGroup = entry.stops

  if (stopGroup.length === 1) {
    return buildPopupHtml(stopGroup[0], buildStopSubLabel(stopGroup[0]))
  }

  const total = stopGroup.length
  const page = Math.min(Math.max(pageIndex || 0, 0), total - 1)
  const stop = stopGroup[page]

  const kanaHtml = stop.kana ? `<p class="stop-kana">${escapeHtml(stop.kana)}</p>` : ''
  const subLabelHtml = `<div class="stop-sub">${buildStopSubLabel(stop)}</div>`
  const linkHtml = stop.url
    ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">🕒 時刻表を見る</a></p>`
    : ''

  const pagerLinksHtml = stopGroup
    .map((_, i) => {
      const activeClass = i === page ? ' active' : ''
      return `<span class="stop-page-link${activeClass}" data-coord-key="${escapeHtml(coordKey)}" data-page="${i}">${i + 1}</span>`
    })
    .join('')

  const pagerHtml = `<div class="stop-pager">
    <span class="stop-pager-label">${page + 1} / ${total}件（事業者・系統違い）</span>
    <div class="stop-pager-links">${pagerLinksHtml}</div>
  </div>`

  const extrasHtml = buildLocationExtrasHtml(stop.lat, stop.lng)

  return `<div class="stop-popup">
    ${pagerHtml}
    <p class="stop-name">${escapeHtml(stop.name)}</p>
    ${kanaHtml}
    ${subLabelHtml}
    ${linkHtml}
    ${extrasHtml}
  </div>`
}

const BASE_OPACITY = 0.45
const DIMMED_OPACITY = 0.55

// markerClusterGroupのdisableClusteringAtZoomと、zoomendハンドラでの
// アイコン更新ループの両方から参照する共有定数。2箇所に同じ値を別々に
// 書くと、片方だけ変更してズレる事故を防ぐため一箇所にまとめる
const DISABLE_CLUSTERING_AT_ZOOM = 14

function renderHighlight(route, anchorStopId) {
  if (!map) return
  highlightMarkersById = {}
  highlightLayer.clearLayers()

  for (const id of hiddenMarkerIds) {
    const m = markersById[id]
    if (m) m.setOpacity(BASE_OPACITY)
  }
  hiddenMarkerIds = []

  if (!route) {
    baseLayer.eachLayer(l => l.setOpacity(BASE_OPACITY))
    return
  }

  baseLayer.eachLayer(l => l.setOpacity(DIMMED_OPACITY))

  const L = window.__L
  const zoom = map.getZoom()
  const half = starIconHalf(zoom)
  const bounds = []
  let anchorMarker = null

  // 黄色ドット側と同じ理由（同一座標に複数stopレコードが乗るケースがある）で、
  // 星も座標キーで重複統合する。今のデータで同一系統に同座標の重複が
  // 含まれるかは未確認だが、他エリア拡張時に必ず起こりうる前提で対応する
  const seenCoordKeys = new Set()

  for (const id of route.stopIds) {
    const stop = stopsById[id]
    if (!stop) continue
    bounds.push([stop.lat, stop.lng])

    const coordKey = coordKeyOf(stop.lat, stop.lng)

    // 黄色ドットの非表示化はstop.id単位のまま。groupsByCoordKeyのおかげで
    // 同じ座標のどのidを渡してもmarkersById[id]は同じ1個のマーカーを指すので、
    // 二重に隠す・二重に戻す心配はない
    const baseMarker = markersById[id]
    if (baseMarker) {
      baseMarker.setOpacity(0)
      hiddenMarkerIds.push(id)
    }

    let marker
    if (seenCoordKeys.has(coordKey)) {
      // この座標の星は既にこのループ内で作成済み。既存のマーカーを再利用する
      marker = groupsByCoordKey[coordKey] && groupsByCoordKey[coordKey].starMarker
    } else {
      seenCoordKeys.add(coordKey)
      const entry = groupsByCoordKey[coordKey]

      marker = L.marker([stop.lat, stop.lng], {
        icon: createStarIcon(zoom)
      })
      const initialPage = groupPageByCoord[coordKey] || 0
      marker.bindPopup(buildGroupedPopupHtml(coordKey, initialPage), { maxWidth: 320 })
      bindHoverPopup(marker)

      marker._coordKey = coordKey
      marker.on('click', () => showPoisForCoord(coordKey))

      const groupStops = entry ? entry.stops : [stop]
      marker.bindTooltip(buildMiniStopLabel(groupStops[0], groupStops.length), {
        permanent: true,
        direction: 'top',
        offset: [0, -half],
        className: 'stop-mini-tooltip'
      })

      marker.addTo(highlightLayer)
      if (entry) entry.starMarker = marker
    }

    if (!marker) continue

    // このidが指す星マーカーが何であれ、popupopen/popupcloseハンドラが
    // 「これは星である」と判定するためのフラグとして使う（表示上は最後に
    // マッチしたidで上書きされるが、ツールチップ再構築はcoordKey経由で
    // groupsByCoordKeyを見るためstopsById[marker._highlightStopId]には依存しない）
    marker._highlightStopId = id
    highlightMarkersById[id] = marker

    if (anchorStopId != null && String(id) === String(anchorStopId)) {
      anchorMarker = marker
    }
  }

  if (anchorMarker) {
    anchorMarker.openPopup()
  } else if (bounds.length) {
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 })
  }
}


onMounted(async () => {
  geoSupported.value = typeof navigator !== 'undefined'
    && !!navigator.geolocation
    && (typeof window === 'undefined' || window.isSecureContext !== false)

  // `await import('leaflet')` が返すのはESモジュールのnamespaceオブジェクトで、
  // 仕様上フリーズされていて後からプロパティを追加できない(non-extensible)。
  // leaflet.markercluster は古いプラグインで、グローバルのLに対して
  // L.MarkerClusterGroup = ... のように直接プロパティを生やす作りなので、
  // window.L にこのfrozenなnamespaceをそのまま入れると「Cannot add property
  // MarkerClusterGroup, object is not extensible」で例外になり、下のtry/catchに
  // 静かに握りつぶされてクラスタリングが常に無効化されていた
  // （コンソールにエラーは出るが、黄色ドットが個別表示されるだけで一見動いて
  // 見えるため、何十回コミットしても気づきにくいタイプの不具合だった）。
  // ミュータブルなプレーンオブジェクトにコピーし、window.Lとローカルの
  // Lを同じオブジェクト参照にすることで、プラグインが追加したプロパティが
  // 両方から見えるようにする
  const LeafletModule = await import('leaflet')
  const L = Object.assign({}, LeafletModule)
  window.__L = L
  window.L = L
  let clusteringAvailable = true
  try {
    await import('leaflet.markercluster')
  } catch (err) {
    clusteringAvailable = false
    console.error('leaflet.markercluster の読み込みに失敗したにゃ。クラスタリングなしで表示するにゃ:', err)
  }

  map = L.map(mapEl.value, {
    center: [35.011, 135.768],
    zoom: 13,
    // デフォルトのズームボタン(左上)は検索パネルの下に隠れて押せなくなるため
    // 無効化し、右下(bottomright)に付け直す。一時的に右側中央付近まで
    // CSSで引き上げていたが、同じコーナーの帰属表示(Leaflet/OSM/Google)まで
    // 一緒に動いて地図が見づらくなったため撤回し、右下のまま据え置く
    zoomControl: false
  })
  L.control.zoom({ position: 'bottomright' }).addTo(map)

  map.on('popupopen', (e) => {
    const el = e.popup.getElement()
    const marker = e.popup._source
    if (!el || !marker) return
    el.addEventListener('mouseenter', cancelClose)
    el.addEventListener('mouseleave', () => scheduleClose(marker))

    if (marker._highlightStopId != null && marker.getTooltip()) {
      marker.unbindTooltip()
    }

    // 黄色ドット・星どちらのポップアップが開いても、その座標を履歴に記録する
    // （ランドマーク・現在地マーカーには_coordKeyが無いので対象外）
    if (marker._coordKey != null) {
      recordHistory(marker._coordKey)
    }
  })

  map.on('popupclose', (e) => {
    const marker = e.popup._source
    if (!marker) return

    // 停留所（黄色ドット・星どちらも）のポップアップが閉じたら、
    // クリックで表示していたPOIマーカーも一緒に消す
    if (marker._coordKey != null && poiLayer) {
      poiLayer.clearLayers()
    }

    if (marker._highlightStopId == null) return
    const id = marker._highlightStopId
    if (highlightMarkersById[id] !== marker) return
    if (marker.getTooltip()) return
    const entry = marker._coordKey != null ? groupsByCoordKey[marker._coordKey] : null
    const stop = entry ? entry.stops[0] : stopsById[id]
    if (!stop) return
    marker.bindTooltip(buildMiniStopLabel(stop, entry ? entry.stops.length : 1), {
      permanent: true,
      direction: 'top',
      offset: [0, -starIconHalf(map.getZoom())],
      className: 'stop-mini-tooltip'
    })
  })

  mapEl.value.addEventListener('click', (e) => {
    const deleteEl = e.target.closest('.landmark-delete-btn')
    if (deleteEl) {
      removeLandmark(deleteEl.dataset.id)
      return
    }
    const pageEl = e.target.closest('.stop-page-link')
    if (pageEl) {
      goToStopPage(pageEl.dataset.coordKey, Number(pageEl.dataset.page))
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

  map.on('zoomend', () => {
    const z = map.getZoom()
    // DISABLE_CLUSTERING_AT_ZOOM未満では黄色ドットは全てクラスタに吸収されて
    // 画面上に個別マーカーとして1つも見えていない。それにもかかわらず
    // baseLayer.eachLayerは(leaflet.markercluster内部の実装上)クラスタツリー
    // 全体の全マーカーを返す仕様のため、見た目に変化が無いのに毎回全件分の
    // setIconが走っていた。個別ドットが実際に見えるズーム帯だけループを回す
    if (baseLayer && z >= DISABLE_CLUSTERING_AT_ZOOM) {
      baseLayer.eachLayer(l => l.setIcon(createDotIcon(z)))
    }
    if (highlightLayer) highlightLayer.eachLayer(l => l.setIcon(createStarIcon(z)))
  })

  // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  //   attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
  //   maxZoom: 21
  // }).addTo(map)
  
  // try {
  //   L.tileLayer('https://mt1.google.com/vt/lyrs=s&hl=ja&x={x}&y={y}&z={z}', {
    
  //     attribution: '© Google',
  //     maxZoom: 21,
  //     opacity: 0.5
  //   }).addTo(map);
  // } catch (e) {
  //   console.error('❌ Error adding tile layer:', e);
  // }
  
  try {
    L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg', {
      attribution: '© 国土地理院',
      maxZoom: 21,
      opacity: 0.6
    }).addTo(map);
  } catch (e) {
    console.error('❌ Error adding tile layer:', e);
  }
  // try {
  //   L.tileLayer('https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png', {
  //     maxZoom: 21,
  //     opacity: 0.6
  //   }).addTo(map);
  // } catch (e) {
  //   console.error('❌ Error adding tile layer:', e);
  // }

  try {
    L.tileLayer("https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}", {
      attribution: '<a href="https://developers.google.com/maps/documentation" target="_blank">Google Map</a>',
      maxZoom: 21,
      opacity: 0.8
    }).addTo(map);
  } catch (e) {
    console.error('❌ Error adding tile layer:', e);
  }
  
  landmarkLayer = L.layerGroup().addTo(map)
  landmarks.value = loadLandmarksFromStorage()
  renderLandmarks()

  viewHistory.value = loadHistoryFromStorage()

  // 事業者単位のバスルート線　道路 // 事業者単位のバスルート線
  //fetch('/data/route_lines.geojson')
  //  .then(res => res.json())
  //  .then(routeLines => {
  //    L.geoJSON(routeLines, {
  //      interactive: false,
  //      style: { color: '#94a3b8', weight: 1.5, opacity: 0.5 }
  //    }).addTo(map)
  //  })

  const [stopsRes, routesRes, poisRes, routeLinesRes] = await Promise.all([
    fetch('/data/mlit_stops.json'),
    fetch('/data/mlit_routes.json'),
    // nearby_pois.jsonはオフラインの距離計算スクリプトで別途生成する想定のファイル。
    // まだ生成していない・置いていない環境でもアプリ自体は動くよう、
    // 取得失敗はcatchして空データ扱いにする（POI機能が使えないだけで他は正常動作する）
    fetch('/data/nearby_pois.json').catch(() => null),
    fetch('/data/route_lines.geojson').catch(() => null)
  ])
  const stops = await stopsRes.json()
  allRoutes = await routesRes.json()
  const nearbyPoisByCoord = (poisRes && poisRes.ok) ? await poisRes.json() : {}
  routeLinesGeojson = (routeLinesRes && routeLinesRes.ok) ? await routeLinesRes.json() : null

  stopCount.value = stops.length
  routeCount.value = allRoutes.length
  loading.value = false

  for (const s of stops) stopsById[s.id] = s

  dataBounds = L.latLngBounds(stops.map(s => [s.lat, s.lng]))

  baseLayer = (clusteringAvailable && typeof L.markerClusterGroup === 'function')
    ? L.markerClusterGroup({
        chunkedLoading: true,
        maxClusterRadius: 60,
        disableClusteringAtZoom: DISABLE_CLUSTERING_AT_ZOOM,
        spiderfyOnMaxZoom: false,
        showCoverageOnHover: false,
        iconCreateFunction: createClusterIcon
      })
    : L.layerGroup()
  highlightLayer = L.layerGroup().addTo(map)
  poiLayer = L.layerGroup().addTo(map)
  routeLinesLayer = L.layerGroup().addTo(map)

  const stopGroupsByCoord = new Map()
  for (const stop of stops) {
    const coordKey = coordKeyOf(stop.lat, stop.lng)
    if (!stopGroupsByCoord.has(coordKey)) stopGroupsByCoord.set(coordKey, [])
    stopGroupsByCoord.get(coordKey).push(stop)
  }

  // groupsByCoordKeyを先に全件分作っておく（黄色ドットのマーカー作成ループの中で
  // buildGroupedPopupHtml(coordKey, ...)が参照するため、先に埋めておく必要がある）。
  // nearbyPois（周辺POIリスト、最大50件・距離順）もここで一緒に紐付けておく
  for (const [coordKey, group] of stopGroupsByCoord) {
    groupsByCoordKey[coordKey] = {
      stops: group,
      baseMarker: null,
      starMarker: null,
      nearbyPois: nearbyPoisByCoord[coordKey] || null
    }
  }

  for (const [coordKey, group] of stopGroupsByCoord) {
    const first = group[0]
    const marker = L.marker([first.lat, first.lng], {
      icon: createDotIcon(map.getZoom()),
      // 初期表示時からBASE_OPACITYを適用する。これが無いとLeafletの
      // デフォルト(不透明度1.0)のまま描画され、系統選択→解除を一度も
      // していない状態ではBASE_OPACITYの値が一切反映されなかった
      opacity: BASE_OPACITY
    })

    const initialPage = groupPageByCoord[coordKey] || 0
    marker.bindPopup(buildGroupedPopupHtml(coordKey, initialPage), { maxWidth: 320 })
    bindHoverPopup(marker)

    marker._coordKey = coordKey
    marker.on('click', () => showPoisForCoord(coordKey))
    marker.addTo(baseLayer)
    groupsByCoordKey[coordKey].baseMarker = marker

    for (const stop of group) {
      markersById[stop.id] = marker
    }
  }

  baseLayer.addTo(map)
})
</script>

<style scoped>
.map-wrap {
  position: relative;
  width: 100%;
  height: 100vh; /* dvh未対応ブラウザ向けフォールバック */
  height: 100dvh; /* モバイルのアドレスバー分の高さズレに追従し、
                     右下のズームボタン・帰属表示が画面外にはみ出さないようにする */
}

#map {
  width: 100%;
  height: 100%;
}

/* 左の検索パネルと右のランドマーク・履歴パネルをまとめる外枠。
   flex-wrapにより、横幅が足りる画面では横並び、足りない画面（iPhone等）では
   自動的に折り返して縦積みになり、重なりを防ぐ。優先順位は書いた順
   （panelが先＝1行目を占有、right-stackは入りきらなければ2行目に折り返す） */
.ui-overlay {
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  z-index: 1000;
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 8px;
  pointer-events: none;
  max-height: calc(100vh - 24px);
}

.ui-overlay > * {
  pointer-events: auto;
}

.status {
  background: rgba(255, 255, 255, 0.42);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.panel {
  background: rgba(255, 255, 255, 0.46);
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
  /* 画面の高さに応じて伸びる45vhではなく、約5件ぶんの高さに固定して
     それ以降はスクロールで見る（下へ下へ伸び続けないようにする） */
  max-height: 260px;
  overflow-y: auto;
}

.route-item {
  text-align: left;
  background: rgba(243, 244, 246, 0.85);
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 6px 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}

/* 一つおきに白寄りの明るさにして、同じグレーが並ぶ単調さを崩す */
.route-item:nth-child(even) {
  background: rgba(250, 250, 252, 0.85);
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

.right-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: min(260px, calc(100vw - 24px));
  max-height: calc(100vh - 24px);
  /* 横並びできる時は右端に寄せ、折り返して2行目に落ちた時はその行の
     右端に寄る（ui-overlayがflex-wrapのため、折り返し後の行にも効く） */
  margin-left: auto;
}

.landmark-panel {
  background: rgba(255, 255, 255, 0.96);
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.25);
}

.landmark-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: none;
  background: none;
  padding: 0;
  font: inherit;
  font-weight: 600;
  color: #333;
  cursor: pointer;
}

.landmark-toggle-arrow {
  font-size: 10px;
  color: #888;
}

.landmark-form {
  display: flex;
  gap: 6px;
  margin-top: 6px;
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

.history-panel {
  background: rgba(255, 255, 255, 0.96);
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.25);
}

.history-header {
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  /* 直近4件ぶんの高さに収め、5件目以降はスクロールで見る
     (history-item高さ約26px + gap4px を4件ぶん) */
  max-height: 124px;
  overflow-y: auto;
}

.history-item {
  text-align: left;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 5px 8px;
  cursor: pointer;
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.history-item:hover {
  background: #e0e7ff;
}

.history-name {
  font-weight: 600;
  font-size: 12px;
}

.history-other {
  font-size: 10px;
  color: #666;
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

:deep(.poi-marker-icon) {
  background: transparent;
  border: none;
  cursor: pointer;
}

:deep(.poi-tooltip) {
  font-size: 11px;
  padding: 2px 6px;
  background: #1d4ed8;
  color: #fff;
  border-color: #1d4ed8;
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
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.4); /* 描画負荷軽減のため無効化 ? BASE_OPACITY も参照 */
}

:deep(.stop-cluster-icon) {
  background: transparent;
  border: none;
}

:deep(.stop-cluster-dot) {
  display: block;
  border-radius: 50%;
  background: rgba(234, 255, 0, 0.25);
  border: 2px solid rgba(250, 230, 200, 0.55);
  
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
  background: #fff;
  border-color: #fff;
}

:deep(.stop-mini-name) {
  font-weight: 700;
  color: #111;
}

:deep(.stop-mini-kana) {
  color: #666;
  font-size: 10px;
}

:deep(.stop-mini-other) {
  color: #0d9488;
  font-size: 10px;
}

:deep(.stop-popup) {
  line-height: 1.4;
}

:deep(.stop-pager) {
  margin: 0 0 6px;
  padding-bottom: 6px;
  border-bottom: 1px solid #eee;
}

:deep(.stop-pager-label) {
  display: block;
  font-size: 11px;
  color: #888;
  margin-bottom: 3px;
}

:deep(.stop-pager-links) {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

:deep(.stop-page-link) {
  display: inline-block;
  min-width: 18px;
  text-align: center;
  padding: 1px 5px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 11px;
  cursor: pointer;
  color: #444;
}

:deep(.stop-page-link:hover) {
  background: #f3f4f6;
}

:deep(.stop-page-link.active) {
  background: #1d4ed8;
  border-color: #1d4ed8;
  color: #fff;
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

/* 系統が多い停留所でポップアップが縦にどんどん伸びないよう、系統一覧だけを
   5行ぶんの高さ(line-height 1.5em × 5)に収めてそこだけ縦スクロールにする */
:deep(.stop-routes-scroll) {
  max-height: 7.5em;
  line-height: 1.5em;
  overflow-y: auto;
  margin-top: 2px;
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

:deep(.leaflet-popup-content-wrapper) {
  background: rgba(255, 255, 255, 0.55);   /* 0.75の数値を下げるほど透明に */
  backdrop-filter: blur(5px);               /* 任意：すりガラス風にしたい場合 */
}

:deep(.leaflet-popup-tip) {
  background: rgba(255, 255, 255, 0.55);   /* ← これを忘れると、箱は透明なのに
                                                下の三角だけ真っ白のまま浮いて見える */
}

/* ズームボタンはbottomright（右下）に据え置く。以前は右手親指が届く高さまで
   引き上げるCSSを付けていたが、同じコーナーにいる帰属表示(Leaflet/OSM/Google)
   まで一緒に引き上がって地図の視認性を損なうため撤回し、素直に右下のまま
   にする（地図の見やすさを優先） */

/* 右下コーナー(ズームボタン＋帰属表示)を地図の端から少し浮かせる。
   0だと帰属表示の文字が地図の縁ぎりぎりで見切れることがあるため、
   下に余白を入れて全体を少し上に持ち上げる */
:deep(.leaflet-bottom.leaflet-right) {
  margin-bottom: 10px;
}

/* 右下ロゴ：ズームボタンのすぐ上に小さく配置する。
   ズームボタンの実際の高さが変わった場合はここも調整が必要 */
.corner-logo {
  position: absolute;
  opacity: 0.65;
  right: 0px;
  bottom: 120px;
  width: 270px;
  height: auto;
  z-index: 1000;
  pointer-events: none;
}
</style>
