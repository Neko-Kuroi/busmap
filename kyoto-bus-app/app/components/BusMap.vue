<template>
  <div class="map-wrap" :dir="isRtl ? 'rtl' : 'ltr'">
    <div id="map" ref="mapEl"></div>

    <!-- 右下のズームボタンのすぐ上に小さく表示するロゴ -->
    <img src="/logobus.webp" alt="" class="corner-logo" />

    <!-- 「ランドマークを追加」パネル：画面右端に張り付くタブ。閉状態では📍アイコンだけが
         はみ出て見え、クリックすると左側へパネルが引き出される（現状のトグル開閉と同じ
         landmarkPanelOpenで開閉する）。ui-overlayのflexフローから独立させ、position:fixed
         でロゴ(corner-logo, bottom:120px)のすぐ上に固定する -->
    <div class="landmark-tab" :class="{ open: landmarkPanelOpen }">
      <div class="landmark-tab-panel">
        <div class="landmark-panel-inner">
          <p class="landmark-panel-title">{{ t('addLandmarkTitle') }}</p>
          <form class="landmark-form" @submit.prevent="addLandmark">
            <input
              class="landmark-input"
              type="text"
              v-model="landmarkAddress"
              maxlength="140"
              :placeholder="t('addressPlaceholder')"
              :disabled="geocoding"
            />
            <button
              class="landmark-add-btn"
              type="submit"
              :disabled="geocoding || !landmarkAddress.trim()"
            >
              {{ geocoding ? t('searching') : t('add') }}
            </button>
          </form>
          <p class="landmark-error" v-if="landmarkError">{{ landmarkError }}</p>
          <p class="landmark-count" v-if="landmarks.length">{{ t('landmarkCount', { count: landmarks.length, limit: LANDMARK_LIMIT }) }}</p>
        </div>
      </div>
      <button
        class="landmark-tab-handle"
        type="button"
        :aria-label="t('addLandmarkTitle')"
        :title="t('addLandmarkTitle')"
        @click="landmarkPanelOpen = !landmarkPanelOpen"
      >
        📍
      </button>
    </div>

    <!-- 検索ウィジェット：画面下部に固定表示。片手操作での使いやすさを優先し、
         以前のui-overlay内(画面上部)から独立させてposition:fixedで下部に置く -->
    <div class="search-widget-wrap">
      <div class="status" v-if="loading">{{ t('loadingStops') }}</div>

      <div class="panel" v-else>
        <input
          class="search"
          type="text"
          v-model="query"
          maxlength="100"
          :placeholder="t('searchPlaceholder')"
        />

        <button
          v-if="geoSupported"
          class="locate-btn"
          @click="locateUser"
          :disabled="locating"
        >
          📍 {{ locating ? t('locating') : t('showMyLocation') }}
        </button>
        <p class="geo-unsupported" v-else>{{ t('geoUnsupported') }}</p>
        <p class="geo-error" v-if="geoError">
          {{ geoError }}
          <button
            v-if="SETTINGS_GUIDE_ERROR_TYPES.includes(geoErrorType)"
            class="geo-error-help-btn"
            type="button"
            @click="openSettingsGuide"
          >
            {{ t('viewSolution') }}
          </button>
          <button
            class="popup-close-btn geo-error-dismiss-btn"
            type="button"
            @click="dismissGeoError"
          >
            {{ t('closePopup') }}
          </button>
        </p>

        <div class="route-list" v-if="query">
          <button
            v-for="r in filteredRoutes"
            :key="r.operator + '||' + r.route"
            class="route-item"
            :class="{ active: isActive(r) }"
            @click="selectRoute(r)"
          >
            <span class="route-name">{{ displayRouteName(r.operator, r.route) }}</span>
            <span class="route-operator">{{ t('routeOperatorCount', { operator: displayOperator(r.operator), count: r.count }) }}</span>
            <span class="route-matched-stop" v-if="r.matchedStopNames.length">
              {{ t('matchedStopPrefix', { names: r.matchedStopNames.map(displayStopName).join(locale === 'ja' ? '、' : ', ') }) }}
            </span>
          </button>
          <p class="no-hit" v-if="filteredRoutes.length === 0">{{ t('noMatch') }}</p>
        </div>

        <div class="selected" v-if="selectedRoute">
          <span>{{ t('selectedRoute', { route: displayRouteName(selectedRoute.operator, selectedRoute.route), operator: displayOperator(selectedRoute.operator) }) }}</span>
          <button class="clear" @click="clearSelection">{{ t('clearSelection') }}</button>
        </div>
      </div>
    </div>

    <div class="ui-overlay">
      <div class="right-stack">
        <div class="history-panel" v-if="viewHistory.length">
          <button class="history-header" @click="historyPanelOpen = !historyPanelOpen">
            {{ t('recentlyViewed') }}
            <span class="history-toggle-arrow">{{ historyPanelOpen ? '▲' : '▼' }}</span>
          </button>
          <div class="history-list" v-if="historyPanelOpen">
            <button
              v-for="h in viewHistory"
              :key="h.coordKey"
              class="history-item"
              @click="goToHistoryEntry(h)"
            >
              <span class="history-name">{{ displayStopName({ id: h.stopId, name: h.name }) }}</span>
              <span class="history-other" v-if="h.otherCount">{{ t('moreCount', { count: h.otherCount }) }}</span>
            </button>
          </div>
        </div>

        <select
          class="lang-select"
          :title="t('langSelectTitle')"
          :aria-label="t('langSelectTitle')"
          :value="locale"
          @change="setLocale($event.target.value)"
        >
          <option v-for="opt in LOCALE_OPTIONS" :key="opt.value" :value="opt.value">
            🌐 {{ opt.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- 位置情報の権限/設定がOFFの疑いがある時に「解決方法を見る」から開く、
         OS・ブラウザ別の設定手順モーダル -->
    <div class="settings-guide-overlay" v-if="settingsGuideOpen" @click.self="closeSettingsGuide">
      <div class="settings-guide-box">
        <p class="settings-guide-title">{{ t('settingsGuideTitle') }}</p>
        <p class="settings-guide-body">{{ t(detectSettingsGuideKey()) }}</p>
        <div class="settings-guide-actions">
          <button class="popup-close-btn" type="button" @click="closeSettingsGuide">{{ t('closePopup') }}</button>
          <button class="settings-guide-retry-btn" type="button" :disabled="locating" @click="retryLocateFromGuide">
            🔄 {{ locating ? t('locating') : t('retryLocate') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { normalize } from '@geolonia/normalize-japanese-addresses'
import { useI18n, LOCALE_OPTIONS } from '../composables/useI18n'

const { locale, t, setLocale, isRtl } = useI18n()

// 地図タイル：6言語対応（ja/en/th/hi/es/fr）。言語切替ドロップダウン(locale)と
// 自動連動する。
// ※Wikimedia(osm-intl)は2020年10月から第三者サイトを403でブロックする仕様に
//   変更されているため使用不可と判明。
// ※国土地理院「白地図」(xyz/blank)は実際に組み合わせたところ表示に失敗（高ズームで
//   タイルが提供されていない可能性が高い）。
// ※Google lyrs=h（透過ラベルのみ）・CARTO nolabelsも検証したが、最終的に
//   衛星写真+OSM(JA) / 衛星写真+Google lyrs=m(他言語) の組み合わせを採用した。
//   日本語だけOSMを使うのは、OSMの方が日本国内の地物・POIラベルが充実している
//   ため。th/hi/es/frはenと同じ理由（OSM(JA)相当の充実したデータが無い）で
//   Google lyrs=mにhl=<locale>を渡す方式に統一する
let currentBaseTileLayer = null
let currentOverlayTileLayer = null

function googleSatelliteTile(hl) {
  return {
    url: `https://mt1.google.com/vt/lyrs=s&hl=${hl}&x={x}&y={y}&z={z}`,
    // minZoom:15はこのレイヤー単体の描画開始ズームを絞るだけ。マップ全体の
    // ズーム下限はL.map()初期化時のminZoom:9で別途固定済みなので、
    // ここでの指定がマップ全体の挙動（初期表示ズーム等）に影響することはない
    options: { attribution: '© Google', maxZoom: 21, minZoom: 15, opacity: 0.75 }
  }
}

function googleRoadmapTile(hl) {
  return {
    url: `https://mt1.google.com/vt/lyrs=m&hl=${hl}&x={x}&y={y}&z={z}`,
    options: { attribution: '© Google', maxZoom: 21, opacity: 0.85 }
  }
}

function gsiSeamlessPhotoTile() {
  return {
    url: 'https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg',
    options: {
      attribution: '© 国土地理院',
      maxZoom: 21,
      minZoom: 16,
      opacity: 0.75,
      // GSIのシームレス写真タイル自体はズームレベル18までしか実データが無いため、
      // maxZoomをGoogle衛星写真と揃えて21のままにする場合、19〜21はLeafletが
      // 18のタイルを自動的に拡大表示する（過去のコメントアウト版はmaxZoom:17で
      // 打ち止めにしていたが、Google衛星写真とズーム比率を揃える今回の方針では
      // ここを明示してLeafletの拡大表示に委ねる）
      maxNativeZoom: 18
    }
  }
}

const OSM_OVERLAY_JA = {
  url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  options: {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
    maxZoom: 21,
    opacity: 0.85
  }
}

// ロケールごとのタイルプリセットを都度組み立てる。jaのみOSMオーバーレイ、
// それ以外（en/th/hi/es/fr）はGoogleロードマップにhl=<locale>を渡して
// ラベル言語を切り替える
function tilePresetForLocale(loc) {
  if (loc === 'ja') {
    // return { base: googleSatelliteTile('ja'), overlay: OSM_OVERLAY_JA }
    return { base: gsiSeamlessPhotoTile(), overlay: OSM_OVERLAY_JA }
  }
  return { base: googleSatelliteTile(loc), overlay: googleRoadmapTile(loc) }
}

function setTileLayersForLocale(loc) {
  const L = window.__L
  if (!L || !map) return
  const preset = tilePresetForLocale(loc)
  if (currentBaseTileLayer) {
    map.removeLayer(currentBaseTileLayer)
    currentBaseTileLayer = null
  }
  if (currentOverlayTileLayer) {
    map.removeLayer(currentOverlayTileLayer)
    currentOverlayTileLayer = null
  }
  try {
    currentBaseTileLayer = L.tileLayer(preset.base.url, preset.base.options).addTo(map)
    currentOverlayTileLayer = L.tileLayer(preset.overlay.url, preset.overlay.options).addTo(map)
  } catch (e) {
    console.error('❌ Error adding tile layer:', e)
  }
}

// 🌐ボタンで言語が切り替わったら地図タイルも自動追従させる
watch(locale, (newLocale) => {
  setTileLayersForLocale(newLocale)
  refreshPopupsForLocale()
})

const mapEl = ref(null)
const loading = ref(true)
const query = ref('')
const selectedRoute = ref(null)
const geoSupported = ref(false)
const locating = ref(false)
const geoError = ref('')
// geoErrorの翻訳済み文字列だけでは「設定ガイドを出すべきエラーか」を
// ロケール非依存で判定できないため、エラー種別のキー自体も別途保持する
const geoErrorType = ref('')
// 「解決方法を見る」から開く、OS/ブラウザ別の設定手順モーダルの開閉状態
const settingsGuideOpen = ref(false)

const landmarkAddress = ref('')
const landmarkError = ref('')
const geocoding = ref(false)
const landmarks = ref([])
// ランドマーク入力欄は初期状態でたたんでおき、ヘッダー部分をクリックすると開く
const landmarkPanelOpen = ref(false)
const historyPanelOpen = ref(false)

// 最近見た停留所の履歴。座標(coordKey)ごとに1件のみ保持し、再訪すると
// 先頭に繰り上がる（ブラウザの閲覧履歴と同じ挙動）。localStorageに永続化する
const viewHistory = ref([]) // [{coordKey, name, otherCount, lat, lng, lastViewedAt}]

// 地図クリックで座標のみ記録するピン。ランドマークと違いジオコーディングは
// 行わない（住所フィールドを持たない）。クリック即記録ではなく、ポップアップの
// 「記録する」ボタンを押した時だけ配列に追加・localStorageに保存する
const clickedPins = ref([]) // [{id, lat, lng, createdAt}]

// 停留所ポップアップの「📍記録する」で保存する、お気に入り停留所。
// ランドマーク/ピンと違い実体は既存の停留所そのものなので、保存内容は
// id(記録自体のid)・stopId(参照先)・name(停留所名)・createdAtのみに留め、
// 表示位置(lat/lng)は保存せず描画時にstopsById[stopId]から都度解決する
const savedStops = ref([]) // [{id, stopId, name, createdAt}]

let allRoutes = []
let map = null
let baseLayer = null
let highlightLayer = null
let landmarkLayer = null
let poiLayer = null
let routeLinesLayer = null
let routeLinesGeojson = null // {type:'FeatureCollection', features:[...]} 全事業者ぶんを保持し、activeOperatorで都度絞り込む
let pinLayer = null
let savedStopLayer = null
// クリックのたびに開く「未記録・下見用」のポップアップ。マーカーには紐付かない
// L.popup単体で、次のクリック時や記録確定時に閉じる
let pendingPinPopup = null
let stopsById = {}

// 英語版データのルックアップ（fetch完了前は空オブジェクトなので、
// 見つからない場合は元の日本語にフォールバックする設計）
let stopNameEnById = {}
let routeNameEnByKey = {}
let operatorEnByJa = {}

// 日本語以外のロケール（en/th/hi/es/fr）では共通で英語ローマ字版を返し、
// 訳が無い場合や日本語ロケールの時は元の文字列にフォールバックする
// （英語データが未生成・欠けていてもアプリ全体は壊れない）。
// 停留所名・系統名・事業者名は固有名詞であり、タイ語話者もヒンディー語話者も
// スペイン語話者もフランス語話者も日本の看板ではローマ字表記を見るため、
// 英語版データを「非日本語話者共通のローマ字レイヤー」として全ロケールで流用する
function displayStopName(stop) {
  if (!stop) return ''
  if (locale.value !== 'ja') {
    const en = stopNameEnById[String(stop.id)]
    if (en) return en
  }
  return stop.name
}

function displayRouteName(operator, route) {
  if (locale.value !== 'ja') {
    const en = routeNameEnByKey[operator + '||' + route]
    if (en) return en
  }
  return route
}

function displayOperator(operatorJa) {
  if (locale.value !== 'ja') {
    const en = operatorEnByJa[operatorJa]
    if (en) return en
  }
  return operatorJa
}
let markersById = {}
let highlightMarkersById = {}
let hiddenMarkerIds = []
let dataBounds = null
let userMarker = null
// 現在ポップアップが開いている停留所の座標キー（開いていなければnull）。
// ポップアップ表示中に系統を選び直した際、ズーム・中心を変えずに
// その停留所を見失わないためのアンカー自動検出に使う
let popupOpenCoordKey = null

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
const CLICKED_PIN_STORAGE_KEY = 'kyoto-bus-app:clickedPins'
const CLICKED_PIN_LIMIT = 20 // ランドマークと同じ考え方：無制限は脆弱性になるため上限を設け、
                              // 超えたら自動で古いものを消さず追加をブロックする
const SAVED_STOP_STORAGE_KEY = 'kyoto-bus-app:savedStops'
const SAVED_STOP_LIMIT = 20 // ランドマーク/ピンと同じ上限方式

// 停留所の緯度経度から、重複統合・ページ記憶・履歴で共通して使う座標キーを作る
function coordKeyOf(lat, lng) {
  return `${lat.toFixed(6)},${lng.toFixed(6)}`
}

// routeが指定座標(coordKey)の停留所を通るなら、そのstop idを返す。
// ポップアップ表示中に系統を切り替えた際、元の停留所を見失わないための
// 自動アンカー検出に使う
function findAnchorStopIdAtCoord(route, coordKey) {
  for (const id of route.stopIds) {
    const s = stopsById[id]
    if (s && coordKeyOf(s.lat, s.lng) === coordKey) return id
  }
  return null
}

// 同一座標(coordKey)グループに含まれる停留所名を重複なく集める。
// 事業者・ページによって「地下鉄」の有無等で名称が異なる場合があるため、
// OR検索キーワードの元ネタとして使う
function uniqueStopNamesForCoord(coordKey) {
  const entry = groupsByCoordKey[coordKey]
  if (!entry) return []
  const seen = new Set()
  const names = []
  for (const s of entry.stops) {
    const name = displayStopName(s)
    if (!seen.has(name)) {
      seen.add(name)
      names.push(name)
    }
  }
  return names
}

const filteredRoutes = computed(() => {
  // OR連結された複数語（例:「烏丸御池 OR 地下鉄烏丸御池」）を50文字制限で
  // 途中で切ってしまわないよう、通常の単語検索より長めの上限にする。
  // 英語の停留所名は日本語より文字数が長くなりがちなため、
  // OR連結した際に途中で切れないよう180文字に拡張
  const raw = sanitizeInput(query.value, 180)
  if (!raw) return []

  // 日本語以外のロケール（en/th/hi/es/fr）では画面に見えてる文字列
  // （displayXxx系ヘルパー、無ければ日本語にフォールバック）と照合する。
  // 停留所名・系統名のローマ字データはth/hi/es/frでも共通で英語版を流用する
  // 方針のため、ラテン文字である以上は英語同様に大文字小文字を無視して比較する
  const isRomanized = locale.value !== 'ja'

  // " OR " で分割し、いずれかの語にマッチすればヒット扱いにする。
  // 手動入力の通常検索では1語のみになるため、従来の単純一致と同じ挙動になる
  const terms = raw.split(' OR ').map(t => t.trim()).filter(Boolean)
  const normalizedTerms = isRomanized ? terms.map(t => t.toLowerCase()) : terms
  const matchesQuery = (str) => {
    if (!str) return false
    const target = isRomanized ? str.toLowerCase() : str
    return normalizedTerms.some(t => target.includes(t))
  }

  const seenKeys = new Set()
  const result = []

  for (const r of allRoutes) {
    const routeText = isRomanized ? displayRouteName(r.operator, r.route) : r.route
    const operatorText = isRomanized ? displayOperator(r.operator) : r.operator
    if (matchesQuery(routeText) || matchesQuery(operatorText)) {
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
    const nameText = isRomanized ? displayStopName(s) : s.name
    // かなは日本語ロケール以外では表示自体していない（buildMiniStopLabel等で
    // locale.value === 'ja' の時だけ出す仕様）ので、検索対象からも外す
    if (matchesQuery(nameText) || (locale.value === 'ja' && s.kana && matchesQuery(s.kana))) {
      matchedStopIds.add(s.id)
    }
  }

  if (matchedStopIds.size) {
    for (const r of allRoutes) {
      const key = r.operator + '||' + r.route
      if (seenKeys.has(key)) continue
      const hitStops = [...new Map(
        r.stopIds
          .filter(id => matchedStopIds.has(id))
          .map(id => stopsById[id])
          .filter(Boolean)
          .map(s => [displayStopName(s), s])
      ).values()]
      if (hitStops.length) {
        seenKeys.add(key)
        result.push({ ...r, matchedStopNames: hitStops })
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
    style: { color: '#ed55a0', weight: 4.0, opacity: 0.4 } //#f472b6 #ec4899
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
  // 塗り(#db2777)はそのまま残し、その上にストライプ画像を星型にclip-pathで
  // 切り抜いて重ねる。position:relativeはLeafletがマーカー自体の絶対配置に
  // 使っている.stop-star-icon（Leafletのアイコン要素そのもの）には付けず、
  // 内側に新設した.stop-star-innerというラッパーに付けることで、
  // マーカー位置がズレる問題を避ける
  const html = `<div class="stop-star-inner">
    <svg width="${size}" height="${size}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path class="star-glow-path" d="M12 1.2l3.35 6.79 7.5 1.09-5.43 5.29 1.28 7.47L12 18.02l-6.7 3.82 1.28-7.47-5.43-5.29 7.5-1.09L12 1.2z"
        fill="#db2777" stroke="#f9a8d4" stroke-width="1.4" stroke-linejoin="round"/>
    </svg>
    <div class="star-stripe-fill"></div>
  </div>`
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

// ピンのメモ欄用。sanitizeInputは改行(\x0A)も含めて全ての制御文字と連続空白を
// 1個のスペースに潰してしまうため、複数行のメモには使えない。ここでは
// \n(0x0A)だけは残しつつ、それ以外の制御文字を除去し、前後の空白のみtrimする
function sanitizeMemo(str, maxLength) {
  return String(str)
    .replace(/\r\n/g, '\n')
    .replace(/[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]/g, '')
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

// クリックピン用：ランドマークと同じピン形状だが、色は青系統の明るい色にして
// 見分けられるようにする（住所ジオコーディングを伴わない、座標のみの記録）
const CLICKED_PIN_ICON_W = 30
const CLICKED_PIN_ICON_H = 40
function createClickedPinIcon() {
  const html = `<svg width="${CLICKED_PIN_ICON_W}" height="${CLICKED_PIN_ICON_H}" viewBox="0 0 30 40" xmlns="http://www.w3.org/2000/svg">
    <path d="M15 0C6.716 0 0 6.716 0 15c0 11.25 15 25 15 25s15-13.75 15-25C30 6.716 23.284 0 15 0z"
      fill="#0ea5e9" stroke="#ffffff" stroke-width="1.5"/>
    <circle cx="15" cy="15" r="5.5" fill="#ffffff"/>
  </svg>`
  return window.__L.divIcon({
    html,
    className: 'clicked-pin-icon',
    iconSize: [CLICKED_PIN_ICON_W, CLICKED_PIN_ICON_H],
    iconAnchor: [CLICKED_PIN_ICON_W / 2, CLICKED_PIN_ICON_H],
    popupAnchor: [0, -CLICKED_PIN_ICON_H]
  })
}

// 記録した停留所用：ランドマーク/ピンと同じピン形状だが、色は黄緑系統にして
// 見分けられるようにする（既存の停留所そのものを指すため、住所ジオコーディングも
// 座標入力も伴わない）
const SAVED_STOP_ICON_W = 30
const SAVED_STOP_ICON_H = 40
function createSavedStopIcon() {
  const html = `<svg width="${SAVED_STOP_ICON_W}" height="${SAVED_STOP_ICON_H}" viewBox="0 0 30 40" xmlns="http://www.w3.org/2000/svg">
    <path d="M15 0C6.716 0 0 6.716 0 15c0 11.25 15 25 15 25s15-13.75 15-25C30 6.716 23.284 0 15 0z"
      fill="#84cc16" stroke="#ffffff" stroke-width="1.5"/>
    <circle cx="15" cy="15" r="5.5" fill="#ffffff"/>
  </svg>`
  return window.__L.divIcon({
    html,
    className: 'saved-stop-pin-icon',
    iconSize: [SAVED_STOP_ICON_W, SAVED_STOP_ICON_H],
    iconAnchor: [SAVED_STOP_ICON_W / 2, SAVED_STOP_ICON_H],
    popupAnchor: [0, -SAVED_STOP_ICON_H]
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
      <a href="https://earth.google.com/web/@${lat},${lng},0a,1000d" target="_blank" rel="noopener">📍 Google Earth</a>
      <a href="https://maps.apple.com/?ll=${lat},${lng}&z=19" target="_blank" rel="noopener">📍 Apple Maps</a>
      <a href="https://map.yahoo.co.jp/place?lat=${lat}&lon=${lng}&zoom=16&maptype=basic" target="_blank" rel="noopener">📍 Yahoo! Map</a>
      <a href="https://labs.mapple.com/mapplevt.html#17/${lat}/${lng}" target="_blank" rel="noopener">📍 MAPPLE</a>
    </div>`
  return `<div class="landmark-popup">
    <p class="landmark-popup-title">${escapeHtml(t('landmarkPopupTitle', { number }))}</p>
    <p class="landmark-popup-address">${escapeHtml(landmark.address)}</p>
    ${streetViewHtml}
    ${externalLinksHtml}
    <div class="popup-actions has-primary">
      <button class="popup-close-btn" data-close="1">${escapeHtml(t('closePopup'))}</button>
      <button class="landmark-delete-btn" data-id="${escapeHtml(landmark.id)}">${escapeHtml(t('deleteThisLandmark'))}</button>
    </div>
  </div>`
}

function loadLandmarksFromStorage() {
  if (typeof localStorage === 'undefined') return []
  try {
    const raw = localStorage.getItem(LANDMARK_STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (err) {
    console.error(t('landmarkLoadFail'), err)
    return []
  }
}

function saveLandmarksToStorage() {
  if (typeof localStorage === 'undefined') return
  try {
    localStorage.setItem(LANDMARK_STORAGE_KEY, JSON.stringify(landmarks.value))
  } catch (err) {
    console.error(t('landmarkSaveFail'), err)
  }
}

function renderLandmarks() {
  if (!landmarkLayer) return
  landmarkLayer.clearLayers()
  const L = window.__L
  landmarks.value.forEach((lm, idx) => {
    const marker = L.marker([lm.lat, lm.lng], { icon: createLandmarkIcon(), bubblingMouseEvents: false })
    marker.bindPopup(buildLandmarkPopupHtml(lm, idx + 1), { maxWidth: 300 })
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
    landmarkError.value = t('landmarkLimit', { limit: LANDMARK_LIMIT })
    return
  }

  geocoding.value = true
  try {
    const result = await normalize(address, { level: 5 })
    if (!result || !result.point) {
      landmarkError.value = t('geocodeNoCoords')
      return
    }

    // このアプリは京都エリアのバス停を対象にしているため、ジオコーディング
    // 結果の都道府県が京都府でない場合は入り口で弾く。pref自体が取れない
    // （通り名住所などで正規化レベルが足りず特定できない）場合も安全側で弾く
    // ジオコーディングAPI(@geolonia/normalize-japanese-addresses)は表示言語に関わらず
    // 常に日本語の都道府県名を返すため、ここは翻訳せず固定の日本語文字列と比較する
    if (result.pref !== '京都府') {
      landmarkError.value = t('kyotoOnly')
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
    console.error(t('geocodeFail'), err)
    landmarkError.value = t('addressConvertFail')
  } finally {
    geocoding.value = false
  }
}

function removeLandmark(id) {
  landmarks.value = landmarks.value.filter(lm => lm.id !== id)
  saveLandmarksToStorage()
  renderLandmarks()
}

// まだ記録していない、クリックした地点の「下見用」ポップアップ。
// ランドマークのポップアップとほぼ同じ内容だが、ジオコーディングを行わない
// ため住所の行が無い。上限に達している場合は「記録する」ボタンの代わりに
// 上限メッセージを出す（ボタン自体を無効化するだけだと、なぜ押せないか
// 伝わらないため）
function buildPendingPinPopupHtml(lat, lng) {
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
      <a href="https://earth.google.com/web/@${lat},${lng},0a,1000d" target="_blank" rel="noopener">📍 Google Earth</a>
      <a href="https://maps.apple.com/?ll=${lat},${lng}&z=19" target="_blank" rel="noopener">📍 Apple Maps</a>
      <a href="https://map.yahoo.co.jp/place?lat=${lat}&lon=${lng}&zoom=16&maptype=basic" target="_blank" rel="noopener">📍 Yahoo! Map</a>
      <a href="https://labs.mapple.com/mapplevt.html#17/${lat}/${lng}" target="_blank" rel="noopener">📍 MAPPLE</a>
    </div>`
  const actionHtml = clickedPins.value.length >= CLICKED_PIN_LIMIT
    ? `<p class="landmark-error">${escapeHtml(t('pinLimit', { limit: CLICKED_PIN_LIMIT }))}</p>
       <div class="popup-actions">
         <button class="popup-close-btn" data-close="1">${escapeHtml(t('closePopup'))}</button>
       </div>`
    : `<textarea class="pin-memo-input" maxlength="300" placeholder="${escapeHtml(t('memoPlaceholder'))}"></textarea>
       <div class="popup-actions has-primary">
         <button class="popup-close-btn" data-close="1">${escapeHtml(t('closePopup'))}</button>
         <button class="pin-record-btn" data-lat="${lat}" data-lng="${lng}">${escapeHtml(t('saveBtn'))}</button>
       </div>`
  return `<div class="landmark-popup">
    <p class="landmark-popup-title">${escapeHtml(t('thisLocation'))}</p>
    ${streetViewHtml}
    ${externalLinksHtml}
    ${actionHtml}
  </div>`
}

// 記録済みピンのポップアップ。ランドマークとほぼ同じだが住所の代わりに
// 番号のみ表示し、削除ボタンを付ける
function buildClickedPinPopupHtml(pin, number) {
  const lat = pin.lat
  const lng = pin.lng
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
      <a href="https://earth.google.com/web/@${lat},${lng},0a,1000d" target="_blank" rel="noopener">📍 Google Earth</a>
      <a href="https://maps.apple.com/?ll=${lat},${lng}&z=19" target="_blank" rel="noopener">📍 Apple Maps</a>
      <a href="https://map.yahoo.co.jp/place?lat=${lat}&lon=${lng}&zoom=16&maptype=basic" target="_blank" rel="noopener">📍 Yahoo! Map</a>
      <a href="https://labs.mapple.com/mapplevt.html#17/${lat}/${lng}" target="_blank" rel="noopener">📍 MAPPLE</a>
    </div>`
  // 6行(line-height 1.5em × 6 = 9em)を超えるメモはCSS側(.pin-memo-display)で
  // 縦スクロールになる。改行はescapeHtml後もそのまま残るので、
  // white-space: pre-wrap で見た目上の改行として反映させる
  const memoHtml = pin.memo
    ? `<div class="pin-memo-display">${escapeHtml(pin.memo)}</div>`
    : ''
  return `<div class="landmark-popup">
    <p class="landmark-popup-title">${escapeHtml(t('pinPopupTitle', { number }))}</p>
    ${memoHtml}
    ${streetViewHtml}
    ${externalLinksHtml}
    <div class="popup-actions has-primary">
      <button class="popup-close-btn" data-close="1">${escapeHtml(t('closePopup'))}</button>
      <button class="pin-delete-btn" data-id="${escapeHtml(pin.id)}">${escapeHtml(t('deleteThisPin'))}</button>
    </div>
  </div>`
}

// 記録した停留所のポップアップ。既存の停留所を指すだけなので、住所欄・
// 地図埋め込み・外部リンク一覧は持たず、番号＋停留所名のみのシンプルな構成にする
function buildSavedStopPopupHtml(saved, number) {
  const stop = stopsById[saved.stopId]
  const name = stop ? displayStopName(stop) : saved.name
  return `<div class="landmark-popup">
    <p class="landmark-popup-title">${escapeHtml(t('savedStopPopupTitle', { number }))}</p>
    <p class="landmark-popup-address">${escapeHtml(name)}</p>
    <div class="popup-actions has-primary">
      <button class="popup-close-btn" data-close="1">${escapeHtml(t('closePopup'))}</button>
      <button class="saved-stop-delete-btn" data-id="${escapeHtml(saved.id)}">${escapeHtml(t('deleteThisSavedStop'))}</button>
    </div>
  </div>`
}

function loadClickedPinsFromStorage() {
  if (typeof localStorage === 'undefined') return []
  try {
    const raw = localStorage.getItem(CLICKED_PIN_STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (err) {
    console.error(t('pinLoadFail'), err)
    return []
  }
}

function saveClickedPinsToStorage() {
  if (typeof localStorage === 'undefined') return
  try {
    localStorage.setItem(CLICKED_PIN_STORAGE_KEY, JSON.stringify(clickedPins.value))
  } catch (err) {
    console.error(t('pinSaveFail'), err)
  }
}

function renderClickedPins() {
  if (!pinLayer) return
  pinLayer.clearLayers()
  const L = window.__L
  clickedPins.value.forEach((pin, idx) => {
    const marker = L.marker([pin.lat, pin.lng], { icon: createClickedPinIcon(), bubblingMouseEvents: false })
    marker.bindPopup(buildClickedPinPopupHtml(pin, idx + 1), { maxWidth: 300 })
    bindHoverPopup(marker)
    marker.addTo(pinLayer)
  })
}

// 言語切り替え時に呼ばれる。bindPopup()はその場のHTML文字列を1回だけ
// 焼き込むだけで、Vueのリアクティブバインディングではないため、
// あとからlocaleが変わっても自動では更新されない。baseLayer/highlightLayer
// 双方のマーカーのポップアップ（開いているものも含む。setPopupContentは
// 開いている最中のポップアップも即座に再描画する）と、星マーカーの
// ミニツールチップ、ランドマーク・ピンのポップアップを全て作り直す。
function refreshPopupsForLocale() {
  for (const coordKey in groupsByCoordKey) {
    const entry = groupsByCoordKey[coordKey]
    const page = groupPageByCoord[coordKey] || 0
    const html = buildGroupedPopupHtml(coordKey, page)
    if (entry.baseMarker) {
      entry.baseMarker.setPopupContent(html)
    }
    if (entry.starMarker) {
      entry.starMarker.setPopupContent(html)
      if (entry.starMarker.getTooltip()) {
        entry.starMarker.setTooltipContent(buildMiniStopLabel(entry.stops[0], entry.stops.length))
      }
    }
  }
  renderLandmarks()
  renderClickedPins()
  renderSavedStops()
}

// ポップアップ内の「記録する」ボタンが押された時だけ、ここで初めてデータを
// 確定する（クリックした時点ではまだ何も保存していない）
function addClickedPin(lat, lng, memoRaw) {
  if (clickedPins.value.length >= CLICKED_PIN_LIMIT) return

  const pin = {
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    lat,
    lng,
    memo: sanitizeMemo(memoRaw || '', 300),
    createdAt: Date.now()
  }
  clickedPins.value.push(pin)
  saveClickedPinsToStorage()
  renderClickedPins()

  if (map) map.closePopup()
  pendingPinPopup = null
}

function removeClickedPin(id) {
  clickedPins.value = clickedPins.value.filter(p => p.id !== id)
  saveClickedPinsToStorage()
  renderClickedPins()
}

function loadSavedStopsFromStorage() {
  if (typeof localStorage === 'undefined') return []
  try {
    const raw = localStorage.getItem(SAVED_STOP_STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (err) {
    console.error(t('savedStopLoadFail'), err)
    return []
  }
}

function saveSavedStopsToStorage() {
  if (typeof localStorage === 'undefined') return
  try {
    localStorage.setItem(SAVED_STOP_STORAGE_KEY, JSON.stringify(savedStops.value))
  } catch (err) {
    console.error(t('savedStopSaveFail'), err)
  }
}

// 保存内容にlat/lngを持たないため、描画のたびにstopsById[stopId]から現在の
// 停留所データを引いて位置を解決する。データ更新等でstopIdが見つからなく
// なった場合（起こりにくいが）は、その記録だけ描画をスキップする
function renderSavedStops() {
  if (!savedStopLayer) return
  savedStopLayer.clearLayers()
  const L = window.__L
  savedStops.value.forEach((saved, idx) => {
    const stop = stopsById[saved.stopId]
    if (!stop) return
    const marker = L.marker([stop.lat, stop.lng], { icon: createSavedStopIcon(), bubblingMouseEvents: false })
    marker.bindPopup(buildSavedStopPopupHtml(saved, idx + 1), { maxWidth: 300 })
    bindHoverPopup(marker)
    // 星マーカー(.stop-mini-tooltip)と同じ考え方：ホバーしなくても地図上で
    // どの停留所を記録したものか分かるよう、常時表示のラベルを付ける
    marker.bindTooltip(escapeHtml(displayStopName(stop)), {
      permanent: true,
      direction: 'top',
      offset: [0, -SAVED_STOP_ICON_H / 2],
      className: 'saved-stop-tooltip'
    })
    marker.addTo(savedStopLayer)
  })
}

// 停留所ポップアップ内の「📍記録する」ボタンは、その場のHTML文字列として
// bindPopup()で1回だけ焼き込まれるため、後から保存/削除してalreadySavedの
// 判定結果が変わっても、既に開かれた（or 過去に開かれてバインド済みの）
// ポップアップの中身は自動更新されない。addSavedStop/removeSavedStopの
// 直後に必ずこれを呼び、対象stopIdの黄色ドット・星どちらのポップアップも
// 作り直す（開いている最中でもsetPopupContentは即座に反映される）
function refreshStopPopupForStopId(stopId) {
  const stop = stopsById[stopId]
  if (!stop) return
  const coordKey = coordKeyOf(stop.lat, stop.lng)
  const entry = groupsByCoordKey[coordKey]
  if (!entry) return
  const page = groupPageByCoord[coordKey] || 0
  const html = buildGroupedPopupHtml(coordKey, page)
  if (entry.baseMarker) entry.baseMarker.setPopupContent(html)
  if (entry.starMarker) entry.starMarker.setPopupContent(html)
}

// 停留所ポップアップの「📍記録する」ボタンから呼ばれる。同じstopIdは
// 二重記録しない（ボタン自体もalreadySavedの間は出さないが、念のため関数側でも防ぐ）
function addSavedStop(stopId, name) {
  if (savedStops.value.length >= SAVED_STOP_LIMIT) return
  if (savedStops.value.some(s => s.stopId === stopId)) return

  const saved = {
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    stopId,
    name,
    createdAt: Date.now()
  }
  savedStops.value.push(saved)
  saveSavedStopsToStorage()
  renderSavedStops()
  refreshStopPopupForStopId(stopId)

  if (map) map.closePopup()
}

function removeSavedStop(id) {
  const removed = savedStops.value.find(s => s.id === id)
  savedStops.value = savedStops.value.filter(s => s.id !== id)
  saveSavedStopsToStorage()
  renderSavedStops()
  if (removed) refreshStopPopupForStopId(removed.stopId)
}

function loadHistoryFromStorage() {
  if (typeof localStorage === 'undefined') return []
  try {
    const raw = localStorage.getItem(HISTORY_STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (err) {
    console.error(t('historyLoadFail'), err)
    return []
  }
}

function saveHistoryToStorage() {
  if (typeof localStorage === 'undefined') return
  try {
    localStorage.setItem(HISTORY_STORAGE_KEY, JSON.stringify(viewHistory.value))
  } catch (err) {
    console.error(t('historySaveFail'), err)
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
    stopId: first.id,
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
  geoErrorType.value = ''

  if (!navigator.geolocation) {
    geoError.value = t('geoNotSupported')
    geoErrorType.value = 'geoNotSupported'
    return
  }
  if (!dataBounds) {
    geoError.value = t('stopsNotReady')
    geoErrorType.value = 'stopsNotReady'
    return
  }

  locating.value = true
  navigator.geolocation.getCurrentPosition(
    (position) => {
      locating.value = false
      const { latitude, longitude } = position.coords
      if (!dataBounds.contains([latitude, longitude])) {
        geoError.value = t('outsideKyoto')
        geoErrorType.value = 'outsideKyoto'
        return
      }
      const L = window.__L
      if (userMarker) userMarker.remove()
      userMarker = L.marker([latitude, longitude], {
        icon: createUserLocationIcon(),
        zIndexOffset: 1000
      }).addTo(map)
      userMarker.bindPopup(
        `<div class="landmark-popup">
          <p class="landmark-popup-title">${escapeHtml(t('myLocation'))}</p>
          <div class="popup-actions">
            <button class="popup-close-btn" data-close="1">${escapeHtml(t('closePopup'))}</button>
          </div>
        </div>`
      )
      map.setView([latitude, longitude], 15)
      // 取得に成功したら、直前まで開いていた設定ガイドモーダルは用済みなので閉じる
      settingsGuideOpen.value = false
    },
    (error) => {
      locating.value = false
      if (error.code === 1) {
        geoError.value = t('geoPermissionDenied')
        geoErrorType.value = 'geoPermissionDenied'
      } else if (error.code === 2) {
        geoError.value = t('geoUnavailable')
        geoErrorType.value = 'geoUnavailable'
      } else if (error.code === 3) {
        geoError.value = t('geoTimeout')
        geoErrorType.value = 'geoTimeout'
      } else {
        geoError.value = t('geoFail')
        geoErrorType.value = 'geoFail'
      }
      console.error(t('geoFailLog'), error)
    },
    { enableHighAccuracy: true, timeout: 10000 }
  )
}

// 「解決方法を見る」リンクを出すべきエラー種別。位置情報サービス自体がOFF、
// または既に恒久的に権限拒否されている場合に典型的な2種類に絞る
// （geoNotSupportedは端末側で直しようがない、geoTimeout/geoFailは電波・GPS要因の
// 可能性が高く設定ガイドとは無関係なため対象外）
const SETTINGS_GUIDE_ERROR_TYPES = ['geoPermissionDenied', 'geoUnavailable']

function openSettingsGuide() {
  settingsGuideOpen.value = true
}

// geoError表示の×ボタン、および設定ガイドモーダルを閉じた時に共通で呼ぶ。
// モーダルだけ閉じてエラーメッセージが下に居座り続けたままにならないよう連動させる
function dismissGeoError() {
  geoError.value = ''
  geoErrorType.value = ''
}

function closeSettingsGuide() {
  settingsGuideOpen.value = false
  dismissGeoError()
}

// 設定手順モーダル内の「再試行」ボタン。locateUser()を再実行し、
// 成功すればlocateUser内でモーダルは自動的に閉じる
function retryLocateFromGuide() {
  locateUser()
}

// OS・ブラウザ・インストール形態（通常タブ/ホーム画面PWA）に応じて
// 表示すべき設定手順の翻訳キーを選ぶ。判定はUser-Agentベースの簡易分岐のため
// 完全ではないが、代表的な組み合わせはカバーできる
function detectSettingsGuideKey() {
  if (typeof navigator === 'undefined') return 'settingsGuideDesktop'
  const ua = navigator.userAgent || ''
  const isIOS = /iP(hone|ad|od)/.test(ua) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)
  const isAndroid = /Android/.test(ua)
  const isStandalone =
    (typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) ||
    window.navigator.standalone === true

  if (isIOS) return isStandalone ? 'settingsGuideIosPwa' : 'settingsGuideIosBrowser'
  if (isAndroid) return isStandalone ? 'settingsGuideAndroidPwa' : 'settingsGuideAndroidBrowser'
  return 'settingsGuideDesktop'
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

// ポップアップ内の系統名クリック → 検索欄には「その系統名」ではなく
// 「クリック元の停留所名」をセットする。系統名で検索しても完全一致の
// 自分自身しかヒットせずユーザーにとって無意味だったため、停留所名にする
// ことで、同じ停留所を使う事業者・系統が全部リストアップされるようにする。
// クリックした系統自体の地図上でのハイライト表示（星マーカー）は従来通り
// その場で行う。
// 同一座標グループに事業者違いで名称の異なる停留所（例:「地下鉄」の有無）が
// 含まれる場合、クリック元の名称だけでなく他ページの名称も重複を除いて
// OR連結し、そのどちらの表記でも系統検索にヒットするようにする
function onPopupRouteClick(operator, route, anchorStopId) {
  const match = allRoutes.find(r => r.operator === operator && r.route === route)
  if (!match) return
  const anchorStop = anchorStopId != null ? stopsById[anchorStopId] : null

  if (anchorStop) {
    const coordKey = coordKeyOf(anchorStop.lat, anchorStop.lng)
    const names = uniqueStopNamesForCoord(coordKey)
    query.value = names.length ? names.join(' OR ') : displayStopName(anchorStop)
  } else {
    query.value = displayRouteName(operator, route)
  }

  selectRoute(match, anchorStopId)
}

function onPopupOperatorClick(operator) {
  query.value = displayOperator(operator)
  // 系統は選択しないが、事業者の路線パスだけは表示する
  renderRouteLines(operator)
}

function buildStopSubLabel(stop) {
  const routesHtml = stop.routes.length
    ? stop.routes
        .map(rt => `<span class="route-link" data-operator="${escapeHtml(stop.operator)}" data-route="${escapeHtml(rt)}" data-stop-id="${stop.id}">${escapeHtml(displayRouteName(stop.operator, rt))}</span>`)
        .join('')
    : t('noRouteInfo')
  // 系統が多い停留所ではポップアップが縦にどんどん伸びてしまうため、
  // 系統一覧だけを独立したブロック(stop-routes-scroll)にして、5行を超えたら
  // その部分だけ縦スクロールにする（停留所名・かな等は伸びず固定のまま）
  return `<span class="operator-link" data-operator="${escapeHtml(stop.operator)}">${escapeHtml(displayOperator(stop.operator))}</span><div class="stop-routes-inline stop-routes-scroll">${routesHtml}</div>`
}

// groupSizeが2以上の場合、代表停留所名の下に「他◯件」を添える
// （同一座標に複数stopがある場合、ツールチップに全件詰め込まず代表1件＋件数のみ表示する）
function buildMiniStopLabel(stop, groupSize) {
  const kanaHtml = (stop.kana && locale.value === 'ja') ? `<br><span class="stop-mini-kana">${escapeHtml(stop.kana)}</span>` : ''
  const otherHtml = groupSize && groupSize > 1
    ? `<br><span class="stop-mini-other">${escapeHtml(t('moreCount', { count: groupSize - 1 }))}</span>`
    : ''
  return `<span class="stop-mini-name">${escapeHtml(displayStopName(stop))}</span>${kanaHtml}${otherHtml}`
}

function buildLocationExtrasHtml(stop) {
  const lat = stop.lat
  const lng = stop.lng
  const streetViewHtml = `<div class="stop-streetview">
  <iframe
    src="https://maps.google.com/maps?q=${lat},${lng}&z=17&output=embed"
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

  // 「📍記録する」ボタン：既に記録済みの停留所なら出さない（二重記録防止）。
  // 上限到達時も出さず、代わりに上限メッセージを表示する
  const alreadySaved = savedStops.value.some(s => String(s.stopId) === String(stop.id))
  let recordBtnHtml = ''
  let limitMsgHtml = ''
  if (alreadySaved) {
    // 何も出さない（記録するボタンを表示しない）
  } else if (savedStops.value.length >= SAVED_STOP_LIMIT) {
    limitMsgHtml = `<p class="landmark-error">${escapeHtml(t('savedStopLimit', { limit: SAVED_STOP_LIMIT }))}</p>`
  } else {
    recordBtnHtml = `<button class="record-stop-btn" data-stop-id="${escapeHtml(String(stop.id))}" data-stop-name="${escapeHtml(stop.name)}">${escapeHtml(t('recordStopBtn'))}</button>`
  }
  const hasPrimary = !!recordBtnHtml

  // 停留所ポップアップは「閉じる」を左端、「記録する」を右端に配置する
  // （記録するボタンが無い＝上限到達時・記録済み時は閉じるボタンのみ右寄せになる）。
  // stop-popup-actionsで外部リンク一覧との間隔を他ポップアップより詰める
  const closeActionHtml = `
    ${limitMsgHtml}
    <div class="popup-actions stop-popup-actions${hasPrimary ? ' has-primary' : ''}">
      <button class="popup-close-btn" data-close="1">${escapeHtml(t('closePopup'))}</button>
      ${recordBtnHtml}
    </div>`

  return streetViewHtml + externalLinksHtml + closeActionHtml
}

function buildPopupHtml(stop, subLabel) {
  const kanaHtml = (stop.kana && locale.value === 'ja') ? `<p class="stop-kana">${escapeHtml(stop.kana)}</p>` : ''
  const subLabelHtml = subLabel ? `<div class="stop-sub">${subLabel}</div>` : ''
  const linkHtml = stop.url
    ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">${escapeHtml(t('viewTimetable'))}</a></p>`
    : ''

  const extrasHtml = buildLocationExtrasHtml(stop)

  return `<div class="stop-popup">
    <p class="stop-name">${escapeHtml(displayStopName(stop))}</p>
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

  const kanaHtml = (stop.kana && locale.value === 'ja') ? `<p class="stop-kana">${escapeHtml(stop.kana)}</p>` : ''
  const subLabelHtml = `<div class="stop-sub">${buildStopSubLabel(stop)}</div>`
  const linkHtml = stop.url
    ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">${escapeHtml(t('viewTimetable'))}</a></p>`
    : ''

  const pagerLinksHtml = stopGroup
    .map((_, i) => {
      const activeClass = i === page ? ' active' : ''
      return `<span class="stop-page-link${activeClass}" data-coord-key="${escapeHtml(coordKey)}" data-page="${i}">${i + 1}</span>`
    })
    .join('')

  const pagerHtml = `<div class="stop-pager">
    <span class="stop-pager-label">${escapeHtml(t('stopPager', { page: page + 1, total }))}</span>
    <div class="stop-pager-links">${pagerLinksHtml}</div>
  </div>`

  const extrasHtml = buildLocationExtrasHtml(stop)

  return `<div class="stop-popup">
    ${pagerHtml}
    <p class="stop-name">${escapeHtml(displayStopName(stop))}</p>
    ${kanaHtml}
    ${subLabelHtml}
    ${linkHtml}
    ${extrasHtml}
  </div>`
}

const BASE_OPACITY = 0.55
const DIMMED_OPACITY = 0.55

// markerClusterGroupのdisableClusteringAtZoomと、zoomendハンドラでの
// アイコン更新ループの両方から参照する共有定数。2箇所に同じ値を別々に
// 書くと、片方だけ変更してズレる事故を防ぐため一箇所にまとめる
const DISABLE_CLUSTERING_AT_ZOOM = 14

function renderHighlight(route, anchorStopId) {
  if (!map) return

  // clearLayers()で古い星のポップアップが閉じるとpopupOpenCoordKeyが
  // 書き換わってしまうため、処理の一番最初に値を退避しておく
  const currentPopupCoordKey = popupOpenCoordKey

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

  // 明示的なanchorStopIdが無くても、ポップアップが開いている最中の
  // 系統切り替えなら、その停留所を優先アンカーとして自動的に採用する
  if (anchorStopId == null && currentPopupCoordKey != null) {
    anchorStopId = findAnchorStopIdAtCoord(route, currentPopupCoordKey)
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
        icon: createStarIcon(zoom),
        bubblingMouseEvents: false
      })
      const initialPage = groupPageByCoord[coordKey] || 0
      marker.bindPopup(buildGroupedPopupHtml(coordKey, initialPage), { maxWidth: 300 })
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
  } else if (currentPopupCoordKey != null) {
    // ポップアップ表示中に、そのポップアップの停留所を通らない系統へ
    // 切り替えた場合も、ズーム・中心は変えない。表示継続のため、
    // 新しい系統に含まれていれば星、含まれていなければ元の黄色ドットの
    // ポップアップを開き直す
    const entry = groupsByCoordKey[currentPopupCoordKey]
    const fallbackMarker =
      (entry && entry.starMarker && highlightLayer.hasLayer(entry.starMarker) && entry.starMarker) ||
      (entry && entry.baseMarker)
    if (fallbackMarker) fallbackMarker.openPopup()
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
    console.error(t('clusterLoadFail'), err)
  }

  map = L.map(mapEl.value, {
    center: [35.011, 135.768],
    zoom: 13,
    // 明示しないとLeafletがgetMinZoom()を「追加された各レイヤーのminZoomの最大値」
    // から自動算出してしまう。衛星写真タイル(googleSatelliteTile)にminZoom:15を
    // 付けているため、ここでマップ全体のminZoomを明示しておかないと、初期表示の
    // zoom:13がminZoom:15にクランプされてしまう
    minZoom: 9,
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
      popupOpenCoordKey = marker._coordKey
    }
  })

  map.on('popupclose', (e) => {
    const marker = e.popup._source
    if (!marker) return

    // このポップアップが「今追跡している座標」のものなら追跡を解除する。
    // renderHighlight側でcurrentPopupCoordKeyへ退避済みなので、
    // clearLayers()による一時的なclose発火で処理が壊れることはない
    if (marker._coordKey != null && marker._coordKey === popupOpenCoordKey) {
      popupOpenCoordKey = null
    }

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
    const closeEl = e.target.closest('.popup-close-btn')
    if (closeEl) {
      if (map) map.closePopup()
      return
    }
    const deleteEl = e.target.closest('.landmark-delete-btn')
    if (deleteEl) {
      removeLandmark(deleteEl.dataset.id)
      return
    }
    const pinDeleteEl = e.target.closest('.pin-delete-btn')
    if (pinDeleteEl) {
      removeClickedPin(pinDeleteEl.dataset.id)
      return
    }
    const pinRecordEl = e.target.closest('.pin-record-btn')
    if (pinRecordEl) {
      const popupEl = pinRecordEl.closest('.landmark-popup')
      const memoEl = popupEl ? popupEl.querySelector('.pin-memo-input') : null
      addClickedPin(Number(pinRecordEl.dataset.lat), Number(pinRecordEl.dataset.lng), memoEl ? memoEl.value : '')
      return
    }
    const savedStopDeleteEl = e.target.closest('.saved-stop-delete-btn')
    if (savedStopDeleteEl) {
      removeSavedStop(savedStopDeleteEl.dataset.id)
      return
    }
    const recordStopEl = e.target.closest('.record-stop-btn')
    if (recordStopEl) {
      addSavedStop(recordStopEl.dataset.stopId, recordStopEl.dataset.stopName)
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

  // 何もない場所の地図クリック→下見用ポップアップを開く。既存マーカーは
  // bubblingMouseEvents:falseでここまでバブリングしてこないので、
  // マーカーの無い場所をクリックした時だけ発火する
  map.on('click', (e) => {
    if (pendingPinPopup) {
      map.closePopup(pendingPinPopup)
    }
    const { lat, lng } = e.latlng
    const L = window.__L
    pendingPinPopup = L.popup({ maxWidth: 300 })
      .setLatLng(e.latlng)
      .setContent(buildPendingPinPopupHtml(lat, lng))
      .openOn(map)
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

  
  // 地図タイル（日本語/英語）。現在のlocaleに合わせて初期化し、
  // 以降は🌐ボタンでのlocale変更をwatchで検知して自動追従する
  setTileLayersForLocale(locale.value)
  
  // try {
  //   L.tileLayer("https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}", {
  //     attribution: '<a href="https://developers.google.com/maps/documentation" target="_blank">Google Map</a>',
  //     maxZoom: 21,
  //     opacity: 0.8
  //   }).addTo(map);
  // } catch (e) {
  //   console.error('❌ Error adding tile layer:', e);
  // }
  
  landmarkLayer = L.layerGroup().addTo(map)
  landmarks.value = loadLandmarksFromStorage()
  renderLandmarks()

  // pinLayerが未初期化のままだとrenderClickedPins()が毎回何もせず早期returnし、
  // 「記録する」ボタンを押してもclickedPins配列・localStorageへの保存は
  // 正常に行われるのに、地図上にピンが一切表示されない不具合になっていた
  pinLayer = L.layerGroup().addTo(map)
  clickedPins.value = loadClickedPinsFromStorage()
  renderClickedPins()

  // savedStopLayerも同じ理由で先に初期化しておく。renderSavedStops()自体は
  // stopsById（停留所データ）を参照するため、実際の描画はstops読み込み後に行う
  savedStopLayer = L.layerGroup().addTo(map)
  savedStops.value = loadSavedStopsFromStorage()

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

  const [stopsRes, routesRes, poisRes, routeLinesRes, stopsEnRes, routesEnRes, operatorsEnRes] = await Promise.all([
    fetch('/data/mlit_stops.json'),
    fetch('/data/mlit_routes.json'),
    // nearby_pois.jsonはオフラインの距離計算スクリプトで別途生成する想定のファイル。
    // まだ生成していない・置いていない環境でもアプリ自体は動くよう、
    // 取得失敗はcatchして空データ扱いにする（POI機能が使えないだけで他は正常動作する）
    fetch('/data/nearby_pois.json').catch(() => null),
    fetch('/data/route_lines.geojson').catch(() => null),
    // 英語版データ（停留所名・系統名・事業者名）。無くても日本語表示に
    // フォールバックしてアプリは正常動作するよう、取得失敗はcatchする
    fetch('/data/mlit_stops_en.json').catch(() => null),
    fetch('/data/mlit_routes_en.json').catch(() => null),
    fetch('/data/operators_en.json').catch(() => null)
  ])
  const stops = await stopsRes.json()
  allRoutes = await routesRes.json()
  const nearbyPoisByCoord = (poisRes && poisRes.ok) ? await poisRes.json() : {}
  routeLinesGeojson = (routeLinesRes && routeLinesRes.ok) ? await routeLinesRes.json() : null
  stopNameEnById = (stopsEnRes && stopsEnRes.ok) ? await stopsEnRes.json() : {}
  routeNameEnByKey = (routesEnRes && routesEnRes.ok) ? await routesEnRes.json() : {}
  operatorEnByJa = (operatorsEnRes && operatorsEnRes.ok) ? await operatorsEnRes.json() : {}

  loading.value = false

  for (const s of stops) stopsById[s.id] = s

  // stopsById構築後でないと停留所位置を解決できないため、ここで初めて描画する
  renderSavedStops()

  dataBounds = L.latLngBounds(stops.map(s => [s.lat, s.lng]))
  
  baseLayer = (clusteringAvailable && typeof L.markerClusterGroup === 'function')
    ? L.markerClusterGroup({
        chunkedLoading: true,
        // 60→80: クラスタ半径を広げてクラスタ数自体を減らし、パン・ズームのたびに
        // 発生する再クラスタリング計算（内部グリッドの再評価）の対象ノード数を削減する
        maxClusterRadius: 80,
        disableClusteringAtZoom: DISABLE_CLUSTERING_AT_ZOOM,
        spiderfyOnMaxZoom: false,
        showCoverageOnHover: false,
        // クラスターのズームイン/アウト時、子マーカーがクラスタ中心から
        // 飛び出す/収束するアニメーションを無効化。4685件規模だとこの
        // アニメーション計算・DOM再構成のコストが無視できないため、
        // まずここを false で体感速度を測る?
        animate: true,
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
      opacity: BASE_OPACITY,
      bubblingMouseEvents: false
    })

    const initialPage = groupPageByCoord[coordKey] || 0
    marker.bindPopup(buildGroupedPopupHtml(coordKey, initialPage), { maxWidth: 300 })
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
  /* フォントを明示指定しないとブラウザ・OSによっては日本語が明朝体（セリフ体）で
     表示されてしまうことがあるため、ゴシック体（サンセリフ体）を明示する */
  font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Hiragino Kaku Gothic ProN",
    "Yu Gothic", "Noto Sans JP", "Segoe UI", Roboto, sans-serif;
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
  max-height: calc(100vh - 24px); /* dvh未対応ブラウザ向けフォールバック */
  max-height: calc(100dvh - 24px); /* モバイルのアドレスバー分の高さズレに追従する */
}

.ui-overlay > * {
  pointer-events: auto;
}

/* 検索ウィジェット（.status/.panel）を画面下部に固定するラッパー。
   ランドマークタブ(.landmark-tab)が右下固定なのに対し、こちらは左下固定にする */
.search-widget-wrap {
  position: fixed;
  left: 12px;
  bottom: 12px;
  z-index: 1000;
}

.status {
  background: rgba(255, 255, 255, 0.42);
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 12px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.lang-select {
  align-self: flex-end;
  border: none;
  background: rgba(255, 255, 255, 0.75);
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  max-width: min(160px, calc(100vw - 24px));
}

.lang-select:hover {
  background: rgba(255, 255, 255, 0.95);
}

.panel {
  background: rgba(255, 255, 255, 0.46);
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 12px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.25);
  width: min(280px, calc(100vw - 24px));
  max-height: calc(100vh - 24px); /* dvh未対応ブラウザ向けフォールバック */
  max-height: calc(100dvh - 24px); /* モバイルのアドレスバー分の高さズレに追従する */
  overflow-y: auto;
}

.search {
  width: 100%;
  box-sizing: border-box;
  padding: 5px 7px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 12px;
}

.locate-btn {
  margin-top: 5px;
  width: 100%;
  box-sizing: border-box;
  padding: 5px 7px;
  border: 1px solid #2563eb;
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 6px;
  font-size: 12px;
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
  margin: 5px 0 0;
  font-size: 10px;
  color: #888;
}

.geo-error {
  margin: 5px 0 0;
  font-size: 11px;
  color: #dc2626;
}

.geo-error-help-btn {
  display: inline-block;
  margin-left: 4px;
  border: none;
  background: none;
  padding: 0;
  color: #1d4ed8;
  font-size: 11px;
  text-decoration: underline;
  cursor: pointer;
}

.geo-error-help-btn:hover {
  color: #1e40af;
}

.geo-error-dismiss-btn {
  display: inline-block;
  margin-left: 4px;
  vertical-align: middle;
}

.settings-guide-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.settings-guide-box {
  background: #fff;
  border-radius: 10px;
  padding: 16px;
  width: min(340px, 100%);
  max-height: calc(100vh - 32px); /* dvh未対応ブラウザ向けフォールバック */
  max-height: calc(100dvh - 32px); /* モバイルのアドレスバー分の高さズレに追従する */
  overflow-y: auto;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.settings-guide-title {
  margin: 0 0 10px;
  font-size: 14px;
  font-weight: 700;
  color: #111;
}

.settings-guide-body {
  margin: 0;
  font-size: 12px;
  line-height: 1.7;
  color: #333;
  /* messages辞書内の\nを見た目上の改行として反映する */
  white-space: pre-line;
}

.settings-guide-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
}

.settings-guide-retry-btn {
  border: none;
  background: #2563eb;
  color: white;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
}

.settings-guide-retry-btn:disabled {
  opacity: 0.6;
  cursor: default;
}

.route-list {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  gap: 3px;
  /* 画面の高さに応じて伸びる45vhではなく、約5件ぶんの高さに固定して
     それ以降はスクロールで見る（下へ下へ伸び続けないようにする） */
  max-height: 220px;
  overflow-y: auto;
}

/* iPhoneなど表示領域が狭い画面では、検索結果が多いと地図を覆い隠して
   しまうため1行ぶんだけ見せてスクロールにする。10インチタブレットなど
   幅・高さともに余裕がある画面では従来通り複数行表示のままにする。
   幅だけ・高さだけで判定すると、画面回転時に片方だけ大きくなる
   ケース（例: 横向きの976×450）で正しく判定できない（実機検証で確認）。
   縦横どちらか一方でも基準未満ならコンパクト表示（OR条件）とする */
@media (max-width: 600px), (max-height: 600px) {
  .route-list {
    /* route-itemは系統名・事業者名・マッチ停留所バッジで最大3行になりうる
       ため、1行ぶんでも60px程度は確保し、項目の途中で見切れないようにする */
    max-height: 60px;
  }
}

.route-item {
  text-align: left;
  background: rgba(243, 244, 246, 0.85);
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 5px 7px;
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
  font-size: 12px;
}

.route-operator {
  font-size: 10px;
  color: #666;
}

.route-matched-stop {
  font-size: 10px;
  color: #0d9488;
  margin-top: 2px;
}

.no-hit {
  color: #888;
  font-size: 11px;
  margin: 4px 0 0;
}

.selected {
  margin-top: 6px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  background: #fef2f2;
  padding: 5px 7px;
  border-radius: 6px;
}

.clear {
  border: none;
  background: #dc2626;
  color: white;
  border-radius: 4px;
  padding: 3px 7px;
  font-size: 11px;
  cursor: pointer;
}

.right-stack {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: min(260px, calc(100vw - 24px));
  max-height: calc(100vh - 24px); /* dvh未対応ブラウザ向けフォールバック */
  max-height: calc(100dvh - 24px); /* モバイルのアドレスバー分の高さズレに追従する */
  /* 横並びできる時は右端に寄せ、折り返して2行目に落ちた時はその行の
     右端に寄る（ui-overlayがflex-wrapのため、折り返し後の行にも効く） */
  margin-left: auto;
}

/* 画面右端に固定されるタブ全体のコンテナ。ロゴ(corner-logo, bottom:120px)の
   すぐ上に来るようbottomを指定する。widthはauto（中身に応じて可変）だが
   right:0のため、中身(landmark-tab-panel)の幅がwidth:0→開いた幅へ変化しても
   コンテナの右端(=landmark-tab-handleの右端)は画面右端に固定されたまま動かず、
   「ハンドルは動かずパネルだけが左へ引き出される」動きになる */
.landmark-tab {
  position: fixed;
  right: 0;
  bottom: 210px; /* ※ /logobus.webp の実際の縦幅により微調整が必要な場合がある */
  z-index: 1000;
  display: flex;
  align-items: stretch;
}

.landmark-tab-panel {
  width: 0;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.96);
  border-radius: 8px 0 0 8px;
  box-shadow: -2px 2px 8px rgba(0, 0, 0, 0.25);
  transition: width 0.2s ease;
}

.landmark-tab.open .landmark-tab-panel {
  width: min(260px, calc(100vw - 48px));
}

/* パネル内側は開いた時の幅で固定しておく。外側(.landmark-tab-panel)の
   width:0→開いた幅のトランジション中に中身が折り返し直したりガタつかないよう、
   中身自体は常にフル幅で組んでおき、外側のoverflow:hiddenで見た目上だけ隠す */
.landmark-panel-inner {
  width: min(260px, calc(100vw - 48px));
  box-sizing: border-box;
  padding: 10px 12px;
  font-size: 13px;
}

.landmark-panel-title {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  color: #333;
}

/* タブの見出し部分。閉状態では📍アイコンだけが画面右端からはみ出て見える
   「タブの頭」として機能し、クリックでlandmarkPanelOpenをトグルする */
.landmark-tab-handle {
  flex-shrink: 0;
  width: 34px;
  border: none;
  border-radius: 8px 0 0 8px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: -1px 1px 4px rgba(0, 0, 0, 0.25);
  font-size: 17px;
  line-height: 1;
  cursor: pointer;
}

.landmark-tab-handle:hover {
  background: rgba(255, 255, 255, 1);
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

.history-toggle-arrow {
  font-size: 10px;
  color: #888;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 6px;
  /* 直近4件ぶんの高さに収め、5件目以降はスクロールで見る
     (history-item高さ約26px + gap4px を4件ぶん) */
  max-height: 124px;
  overflow-y: auto;
}

/* route-list側と同じ理由・同じOR条件（幅・高さどちらか一方でも
   狭ければコンパクト表示）にする */
@media (max-width: 600px), (max-height: 600px) {
  .history-list {
    /* history-itemは1行構成(約26px)なので、1行ぶんだけ見せる */
    max-height: 30px;
  }
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

:deep(.saved-stop-pin-icon) {
  background: transparent;
  border: none;
  overflow: visible;
}

:deep(.saved-stop-pin-icon) svg {
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

:deep(.pin-memo-input) {
  display: block;
  width: 100%;
  box-sizing: border-box;
  margin-top: 6px;
  padding: 6px 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 12px;
  font-family: inherit;
  resize: vertical;
  min-height: 6em;
}

/* 6行(line-height 1.5em × 6 = 9em)を超えたら縦スクロールにする */
:deep(.pin-memo-display) {
  margin: 6px 0;
  padding: 6px 8px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 12px;
  color: #333;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.5em;
  max-height: 9em;
  overflow-y: auto;
}

/* ポップアップ最下部のアクション行。閉じるボタン(.popup-close-btn)は既定で右寄せ、
   削除/記録ボタン(.landmark-delete-btn等)が同居する場合のみhas-primaryを付けて
   両端揃え（閉じる=左端・既存ボタン=右端）にする。
   このHTMLはLeafletのbindPopup()に文字列として渡す動的注入コンテンツで、
   Vueのテンプレートが描画したものではないため、scoped属性が付かない。
   :deep()を付けないとCSSが一切マッチせず無効化されるので注意（実際に
   一度この付け忘れで両端揃え・上マージンが効かない不具合が発生した） */
:deep(.popup-actions) {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-top: 10px;
}

:deep(.popup-actions.has-primary) {
  justify-content: space-between;
}

/* 停留所ポップアップの最下部（外部リンク一覧とのマージン）だけ、
   他ポップアップ(margin-top:10px)より詰めて表示する */
:deep(.popup-actions.stop-popup-actions) {
  margin-top: 6px;
}

:deep(.popup-close-btn) {
  border: none;
  background: #f3f4f6;
  color: #444;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

:deep(.popup-close-btn:hover) {
  background: #e5e7eb;
}

:deep(.landmark-delete-btn),
:deep(.pin-delete-btn),
:deep(.saved-stop-delete-btn) {
  border: 1px solid #dc2626;
  background: #fef2f2;
  color: #b91c1c;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

:deep(.pin-record-btn) {
  border: 1px solid #2563eb;
  background: #eff6ff;
  color: #1d4ed8;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

:deep(.pin-record-btn:hover) {
  background: #dbeafe;
}

/* 停留所を記録するボタン。マーカーの黄緑色(#84cc16)と揃えた配色にする */
:deep(.record-stop-btn) {
  border: none;
  background: #65a30d;
  color: white;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

:deep(.landmark-streetview) {
  margin-top: 6px;
}

/* Google Maps埋め込みiframeのサイズ。HTML属性側は200のままにしてあるが、
   CSSの方が優先されるのでここで実際の表示サイズを決める。iPhoneなど
   幅の狭い画面では200のまま、10インチタブレットなど幅・高さともに
   余裕がある画面では300に広げる。幅だけで判定すると画面回転時に
   正しく判定できないため、縦横どちらも基準を超えた時だけ大画面と
   判断する（AND条件） */
:deep(.landmark-streetview iframe) {
  width: 200px;
  height: 200px;
}

@media (min-width: 601px) and (min-height: 601px) {
  :deep(.landmark-streetview iframe) {
    width: 300px;
    height: 300px;
  }
}

/* 停留所ポップアップの.stop-external-linksと同じ考え方で、約2件ぶんの
   高さを超えたら縦スクロールにして、ポップアップの縦幅を抑える */
:deep(.landmark-external-links) {
  margin-top: 6px;
  padding-top: 4px;
  border-top: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 2px;
  max-height: 32px;
  overflow-y: auto;
  padding-right: 2px;
}

:deep(.landmark-external-links a) {
  color: #1d4ed8;
  font-size: 11px;
  text-decoration: none;
}

:deep(.landmark-external-links a:hover) {
  text-decoration: underline;
}

:deep(.landmark-delete-btn:hover),
:deep(.pin-delete-btn:hover),
:deep(.saved-stop-delete-btn:hover) {
  background: #fee2e2;
}

:deep(.stop-star-icon) {
  background: transparent;
  border: none;
  overflow: visible;
}

/* position:relativeはここ(内側の新しいラッパー)に付ける。
   .stop-star-icon自体はLeafletが絶対配置に使っている要素なので、
   ここにposition:relativeを付けるとマーカーの位置がズレてしまう */
:deep(.stop-star-inner) {
  position: relative;
  width: 100%;
  height: 100%;
}

:deep(.stop-star-icon) svg {
  display: block;
  overflow: visible;
  filter: drop-shadow(0 0 1px rgba(0, 0, 0, 0.2));
}

/* 星の塗り(#db2777)の上に、ストライプ画像を星型にclip-pathで切り抜いて
   重ねる。画像は背景を透明化・斜め線だけ半透明の赤にしてあるので、
   下の塗り色が透けて見える「模様を重ねる」表現になる */
:deep(.star-stripe-fill) {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: url('/stripe-overlay.png');
  background-repeat: repeat;
  background-size: 5px 5px;
  clip-path: polygon(
    50% 5%, 63.96% 33.29%, 95.21% 37.83%, 72.58% 59.88%, 77.92% 91%,
    50% 75.08%, 22.08% 91%, 27.42% 59.88%, 4.79% 37.83%, 36.04% 33.29%
  );
  animation: stripe-scroll 1.0s linear infinite;
}

@keyframes stripe-scroll {
  from {
    background-position: 0 0;
  }
  to {
    background-position: -5px -5px;
  }
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
    stroke-width: 1.9;
    stroke-opacity: 1;
    filter: drop-shadow(0 0 3px rgba(80, 23, 77, 0.7));
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
  border: 3px solid #fff; /*#d4e100;*/
  /* box-shadow: 0 0 3px rgba(0, 0, 0, 0.6); */ /* 描画負荷軽減のため無効化 ? BASE_OPACITY も参照 */
}

:deep(.stop-cluster-icon) {
  background: transparent;
  border: none;
}

:deep(.stop-cluster-dot) {
  display: block;
  border-radius: 50%;
  background: rgba(234, 255, 0, 0.25);
  border: 1px solid rgba(250, 230, 200, 0.65);
  
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

/* 記録した停留所(緑アイコン)の常時ラベル。アイコンの色(#84cc16)に
   合わせた枠線にして、星マーカーの白ラベルと見分けられるようにする */
:deep(.saved-stop-tooltip) {
  font-size: 11px;
  line-height: 1.3;
  padding: 2px 6px;
  white-space: nowrap;
  background: #fff;
  border-color: #84cc16;
  color: #3f6212;
}

:deep(.saved-stop-tooltip)::before {
  border-top-color: #84cc16;
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

/* 系統一覧を縦積みのパレット状にする。display:flexで各route-linkを
   ブロック化することで、文字列以外の右側の空白部分もタップ領域になる
   （下部の外部リンク一覧 .stop-external-links と同じ考え方） */
:deep(.stop-routes-inline) {
  color: #666;
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 4px;
}

/* 系統が多い停留所ではポップアップが縦にどんどん伸びてしまうため、
   系統一覧だけを独立したブロックにして、約4件ぶんの高さを超えたら
   その部分だけ縦スクロールにする（地図を覆う面積を抑えるため5件→4件に縮小） */
:deep(.stop-routes-scroll) {
  max-height: 90px;
  overflow-y: auto;
  margin-top: 2px;
  padding-right: 2px;
}

:deep(.operator-link) {
  cursor: pointer;
  color: #1d4ed8;
  text-decoration: underline dotted;
}

:deep(.operator-link:hover) {
  color: #dc2626;
  text-decoration: underline;
}

/* 系統リンクは検索結果パネルの .route-item と同じパレット状ボタンに見せる。
   display:blockで幅いっぱいに広げ、文字列以外の余白部分もタップできるようにする */
:deep(.route-link) {
  display: block;
  cursor: pointer;
  color: #1d4ed8;
  text-decoration: none;
  background: rgba(243, 244, 246, 0.5);
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 3px 7px;
  font-size: 11px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
}

:deep(.route-link:hover) {
  background: #e0e7ff;
  color: #dc2626;
}

:deep(.stop-link) {
  margin: 4px 0 0;
}

/* 系統リンク(.route-link)・外部マップリンク(.stop-external-links a)と同じ理由で、
   display:blockにより文字列以外の右側の余白部分もタップ領域にする */
:deep(.stop-link a) {
  display: block;
  color: #1d4ed8;
  font-size: 12px;
  text-decoration: underline;
}

/* 「時刻表を見る」リンク（stop.urlが無い場合は停留所名等）とすぐ下の
   Googleマップ埋め込みiframeが接近しすぎないよう間隔を設ける。
   狭いデバイス（幅・高さどちらかが600px以下）では埋め込み自体を非表示にし、
   幅・高さとも601px以上（AND条件）の時だけ表示する */
:deep(.stop-streetview) {
  display: none;
  margin-top: 6px;
}

/* landmark-streetview側と同じ理由・同じサイズ設定・同じAND条件で統一する */
:deep(.stop-streetview iframe) {
  width: 200px;
  height: 200px;
}

@media (min-width: 601px) and (min-height: 601px) {
  :deep(.stop-streetview) {
    display: block;
  }

  :deep(.stop-streetview iframe) {
    width: 300px;
    height: 300px;
  }
}

/* 他のマップサービスへのリンク一覧も、約2件ぶんの高さを超えたら
   縦スクロールにして地図を覆う面積を抑える */
:deep(.stop-external-links) {
  margin-top: 6px;
  padding-top: 4px;
  border-top: 1px solid #eee;
  display: flex;
  flex-direction: column;
  gap: 2px;
  max-height: 32px;
  overflow-y: auto;
  padding-right: 2px;
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
  background: rgba(255, 255, 255, 0.75);   /* 0.75の数値を下げるほど透明に */
  backdrop-filter: blur(2px);              /* 任意：すりガラス風にしたい場合 */
}

/* 画面最下部に表示されるタイル提供元の著作権表示。デフォルトのままだと
   地図に対して目立ちすぎるため小さくする */
:deep(.leaflet-control-attribution) {
  font-size: 9px;
}

/* Leaflet標準の.leaflet-popup-contentは margin: 13px 24px 13px 20px 相当と余白が
   大きいため、検索パネル(.panel { padding: 8px 10px; })に近い値へ縮小する。
   停留所・ランドマーク・ピン・現在地など全ポップアップ種類に共通で効く */
:deep(.leaflet-popup-content) {
  margin: 8px 10px;
}

:deep(.leaflet-popup-tip) {
  background: rgba(255, 255, 255, 0.85);   /* ← これを忘れると、箱は透明なのに
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
  opacity: 0.95;
  right: 0px;
  bottom: 120px;
  width: 120px;
  height: auto;
  z-index: 1000;
  pointer-events: none;
}
</style>
