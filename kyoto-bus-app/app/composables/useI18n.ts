import { ref, computed } from 'vue'

export type Locale = 'ja' | 'en'

const STORAGE_KEY = 'busmap_locale'

// UIの固定文言辞書。停留所名・系統名・POI名などのデータ自体はここでは扱わず、
// 別途データ変換パイプライン（ローマ字化＋種別語ハイブリッド訳）で対応する。
const messages: Record<Locale, Record<string, string>> = {
  ja: {
    loadingStops: '停留所データを読み込み中…',
    stopCount: '{stops} 件の停留所（{routes} 系統）',
    searchPlaceholder: '系統名・事業者名・停留所名で検索',
    locating: '取得中…',
    showMyLocation: '現在地を表示',
    geoUnsupported: 'このブラウザ・接続方法では現在地取得は使えません',
    routeOperatorCount: '{operator}（{count}件）',
    matchedStopPrefix: '🚏 {names}',
    noMatch: '該当する系統・停留所がありません',
    selectedRoute: '選択中: {route}（{operator}）',
    clearSelection: '解除',
    addLandmarkTitle: '📍 ランドマークを追加',
    addressPlaceholder: '住所を入力',
    searching: '検索中…',
    add: '追加',
    landmarkCount: '{count} / {limit} 件登録中',
    landmarkLoadFail: 'ランドマークの読み込みに失敗したにゃ:',
    landmarkSaveFail: 'ランドマークの保存に失敗したにゃ:',
    landmarkLimit: 'ランドマークは{limit}件までです。削除してから追加してください',
    geocodeNoCoords: '座標を特定できませんでした。住所を見直してください',
    kyotoPrefecture: '京都府',
    kyotoOnly: '京都府内の住所のみ登録できます',
    geocodeFail: 'ジオコーディングに失敗したにゃ:',
    addressConvertFail: '住所の変換に失敗しました。しばらくして再度お試しください',
    pinLimit: 'ピンは{limit}件までです。削除してから追加してください',
    memoPlaceholder: 'メモ（300文字まで）',
    saveBtn: '📌 記録する',
    thisLocation: '📍 この地点',
    landmarkPopupTitle: '📍 ランドマーク #{number}',
    pinPopupTitle: '📍 ピン #{number}',
    pinLoadFail: 'ピンの読み込みに失敗したにゃ:',
    pinSaveFail: 'ピンの保存に失敗したにゃ:',
    historyLoadFail: '履歴の読み込みに失敗したにゃ:',
    historySaveFail: '履歴の保存に失敗したにゃ:',
    geoNotSupported: 'このブラウザでは現在地取得に対応していません',
    stopsNotReady: '停留所データの読み込みが完了していません',
    outsideKyoto: '現在地が京都のバス停エリア外のため表示できません',
    myLocation: '現在地',
    geoPermissionDenied: '位置情報の利用が許可されませんでした',
    geoUnavailable: '現在地を取得できませんでした',
    geoTimeout: '現在地の取得がタイムアウトしました',
    geoFail: '現在地の取得に失敗しました',
    geoFailLog: '位置情報の取得に失敗したにゃ:',
    noRouteInfo: '（系統情報なし）',
    moreCount: '他{count}件',
    viewTimetable: '🕒 時刻表を見る',
    stopPager: '{page} / {total}件（事業者・系統違い）',
    clusterLoadFail: 'leaflet.markercluster の読み込みに失敗したにゃ。クラスタリングなしで表示するにゃ:',
    deleteThisPin: 'このピンを削除',
    deleteThisLandmark: 'このランドマークを削除',
    recentlyViewed: '🕘 最近見た停留所',
    langToggleLabel: 'EN',
    langToggleTitle: '言語を切り替え / Switch language'
  },
  en: {
    loadingStops: 'Loading stop data…',
    stopCount: '{stops} stops ({routes} routes)',
    searchPlaceholder: 'Search by route, operator, or stop name',
    locating: 'Locating…',
    showMyLocation: 'Show my location',
    geoUnsupported: 'Location access is not available in this browser or connection',
    routeOperatorCount: '{operator} ({count})',
    matchedStopPrefix: '🚏 {names}',
    noMatch: 'No matching routes or stops',
    selectedRoute: 'Selected: {route} ({operator})',
    clearSelection: 'Clear',
    addLandmarkTitle: '📍 Add Landmark',
    addressPlaceholder: 'Enter an address',
    searching: 'Searching…',
    add: 'Add',
    landmarkCount: '{count} / {limit} registered',
    landmarkLoadFail: 'Failed to load landmarks:',
    landmarkSaveFail: 'Failed to save landmarks:',
    landmarkLimit: 'You can register up to {limit} landmarks. Please delete one before adding another.',
    geocodeNoCoords: 'Could not determine the coordinates. Please check the address.',
    kyotoPrefecture: 'Kyoto Prefecture',
    kyotoOnly: 'Only addresses within Kyoto Prefecture can be registered',
    geocodeFail: 'Geocoding failed:',
    addressConvertFail: 'Failed to convert the address. Please try again later.',
    pinLimit: 'You can save up to {limit} pins. Please delete one before adding another.',
    memoPlaceholder: 'Memo (up to 300 characters)',
    saveBtn: '📌 Save',
    thisLocation: '📍 This Location',
    landmarkPopupTitle: '📍 Landmark #{number}',
    pinPopupTitle: '📍 Pin #{number}',
    pinLoadFail: 'Failed to load pins:',
    pinSaveFail: 'Failed to save pins:',
    historyLoadFail: 'Failed to load history:',
    historySaveFail: 'Failed to save history:',
    geoNotSupported: 'This browser does not support location access',
    stopsNotReady: 'Stop data has not finished loading yet',
    outsideKyoto: 'Your current location is outside the Kyoto bus stop area, so it cannot be shown',
    myLocation: 'My Location',
    geoPermissionDenied: 'Location access was not permitted',
    geoUnavailable: 'Could not get your current location',
    geoTimeout: 'Getting your location timed out',
    geoFail: 'Failed to get your current location',
    geoFailLog: 'Failed to get location:',
    noRouteInfo: '(no route info)',
    moreCount: '+{count} more',
    viewTimetable: '🕒 View timetable',
    stopPager: '{page} / {total} (different operator/route)',
    clusterLoadFail: 'Failed to load leaflet.markercluster. Showing without clustering:',
    deleteThisPin: 'Delete this pin',
    deleteThisLandmark: 'Delete this landmark',
    recentlyViewed: '🕘 Recently viewed stops',
    langToggleLabel: '日本語',
    langToggleTitle: 'Switch language / 言語を切り替え'
  }
}

const locale = ref<Locale>('ja')
let initialized = false

function detectInitialLocale(): Locale {
  if (typeof window === 'undefined') return 'ja'
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY)
    if (saved === 'ja' || saved === 'en') return saved
  } catch {
    // localStorage が使えない環境（プライベートモード等）は無視してブラウザ言語判定へ
  }
  const nav = (window.navigator.language || window.navigator.languages?.[0] || '').toLowerCase()
  return nav.startsWith('ja') ? 'ja' : 'en'
}

function ensureInit() {
  if (!initialized) {
    locale.value = detectInitialLocale()
    initialized = true
  }
}

function setLocale(next: Locale) {
  locale.value = next
  if (typeof window !== 'undefined') {
    try {
      window.localStorage.setItem(STORAGE_KEY, next)
    } catch {
      // 保存できなくても表示上の切替は継続する
    }
  }
}

function toggleLocale() {
  setLocale(locale.value === 'ja' ? 'en' : 'ja')
}

function t(key: string, vars?: Record<string, string | number>): string {
  ensureInit()
  const table = messages[locale.value] || messages.ja
  let str = table[key] ?? messages.ja[key] ?? key
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      str = str.split(`{${k}}`).join(String(v))
    }
  }
  return str
}

export function useI18n() {
  ensureInit()
  return {
    locale: computed(() => locale.value),
    t,
    setLocale,
    toggleLocale
  }
}
