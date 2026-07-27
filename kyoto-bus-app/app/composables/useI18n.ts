import { ref, computed } from 'vue'

export type Locale = 'ja' | 'en' | 'th' | 'hi' | 'es' | 'fr'

// 言語切替ドロップダウンの選択肢。ラベルは各言語の話者が読める「自言語名」を
// 常に固定表示する（他の言語ピッカーの慣習と同じで、現在のlocaleに応じて
// 翻訳はしない。例えば en ロケール中でも「日本語」はそのまま「日本語」と出す）
export const LOCALE_OPTIONS: { value: Locale; label: string }[] = [
  { value: 'ja', label: '日本語' },
  { value: 'en', label: 'English' },
  { value: 'th', label: 'ไทย' },
  { value: 'hi', label: 'हिन्दी' },
  { value: 'es', label: 'Español' },
  { value: 'fr', label: 'Français' }
]

const LOCALE_VALUES: Locale[] = LOCALE_OPTIONS.map(o => o.value)

const STORAGE_KEY = 'busmap_locale'

// UIの固定文言辞書。停留所名・系統名・POI名などのデータ自体はここでは扱わず、
// 別途データ変換パイプライン（ローマ字化＋種別語ハイブリッド訳）で対応する。
// 停留所名・系統名は th/hi/es/fr でも既存の英語ローマ字データをそのまま流用する
// 方針（非日本語話者共通のローマ字レイヤーとして扱う）。
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
    closePopup: '✕ 閉じる',
    langSelectTitle: '言語を選択'
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
    closePopup: '✕ Close',
    langSelectTitle: 'Select language'
  },
  th: {
    loadingStops: 'กำลังโหลดข้อมูลป้ายรถเมล์…',
    stopCount: '{stops} ป้าย ({routes} สาย)',
    searchPlaceholder: 'ค้นหาด้วยชื่อสาย ผู้ให้บริการ หรือชื่อป้าย',
    locating: 'กำลังค้นหาตำแหน่ง…',
    showMyLocation: 'แสดงตำแหน่งของฉัน',
    geoUnsupported: 'ไม่สามารถเข้าถึงตำแหน่งได้ในเบราว์เซอร์หรือการเชื่อมต่อนี้',
    routeOperatorCount: '{operator} ({count})',
    matchedStopPrefix: '🚏 {names}',
    noMatch: 'ไม่พบสายหรือป้ายที่ตรงกัน',
    selectedRoute: 'เลือกแล้ว: {route} ({operator})',
    clearSelection: 'ล้าง',
    addLandmarkTitle: '📍 เพิ่มจุดสังเกต',
    addressPlaceholder: 'กรอกที่อยู่',
    searching: 'กำลังค้นหา…',
    add: 'เพิ่ม',
    landmarkCount: 'ลงทะเบียนแล้ว {count} / {limit} รายการ',
    landmarkLoadFail: 'โหลดจุดสังเกตไม่สำเร็จ:',
    landmarkSaveFail: 'บันทึกจุดสังเกตไม่สำเร็จ:',
    landmarkLimit: 'คุณสามารถลงทะเบียนจุดสังเกตได้สูงสุด {limit} รายการ กรุณาลบรายการหนึ่งก่อนเพิ่มใหม่',
    geocodeNoCoords: 'ไม่สามารถระบุพิกัดได้ กรุณาตรวจสอบที่อยู่',
    kyotoPrefecture: 'จังหวัดเกียวโต',
    kyotoOnly: 'ลงทะเบียนได้เฉพาะที่อยู่ในจังหวัดเกียวโตเท่านั้น',
    geocodeFail: 'การระบุพิกัดล้มเหลว:',
    addressConvertFail: 'แปลงที่อยู่ไม่สำเร็จ กรุณาลองใหม่อีกครั้งในภายหลัง',
    pinLimit: 'คุณสามารถบันทึกหมุดได้สูงสุด {limit} รายการ กรุณาลบรายการหนึ่งก่อนเพิ่มใหม่',
    memoPlaceholder: 'บันทึกช่วยจำ (สูงสุด 300 ตัวอักษร)',
    saveBtn: '📌 บันทึก',
    thisLocation: '📍 ตำแหน่งนี้',
    landmarkPopupTitle: '📍 จุดสังเกต #{number}',
    pinPopupTitle: '📍 หมุด #{number}',
    pinLoadFail: 'โหลดหมุดไม่สำเร็จ:',
    pinSaveFail: 'บันทึกหมุดไม่สำเร็จ:',
    historyLoadFail: 'โหลดประวัติไม่สำเร็จ:',
    historySaveFail: 'บันทึกประวัติไม่สำเร็จ:',
    geoNotSupported: 'เบราว์เซอร์นี้ไม่รองรับการเข้าถึงตำแหน่ง',
    stopsNotReady: 'ข้อมูลป้ายรถเมล์ยังโหลดไม่เสร็จ',
    outsideKyoto: 'ตำแหน่งปัจจุบันของคุณอยู่นอกพื้นที่ป้ายรถเมล์เกียวโต จึงไม่สามารถแสดงได้',
    myLocation: 'ตำแหน่งของฉัน',
    geoPermissionDenied: 'ไม่ได้รับอนุญาตให้เข้าถึงตำแหน่ง',
    geoUnavailable: 'ไม่สามารถรับตำแหน่งปัจจุบันของคุณได้',
    geoTimeout: 'การรับตำแหน่งหมดเวลา',
    geoFail: 'รับตำแหน่งปัจจุบันไม่สำเร็จ',
    geoFailLog: 'รับตำแหน่งไม่สำเร็จ:',
    noRouteInfo: '(ไม่มีข้อมูลสาย)',
    moreCount: 'อีก {count} รายการ',
    viewTimetable: '🕒 ดูตารางเวลา',
    stopPager: '{page} / {total} (ผู้ให้บริการ/สายต่างกัน)',
    clusterLoadFail: 'โหลด leaflet.markercluster ไม่สำเร็จ กำลังแสดงโดยไม่มีการจัดกลุ่ม:',
    deleteThisPin: 'ลบหมุดนี้',
    deleteThisLandmark: 'ลบจุดสังเกตนี้',
    recentlyViewed: '🕘 ป้ายที่ดูล่าสุด',
    closePopup: '✕ ปิด',
    langSelectTitle: 'เลือกภาษา'
  },
  hi: {
    loadingStops: 'स्टॉप डेटा लोड हो रहा है…',
    stopCount: '{stops} स्टॉप ({routes} रूट)',
    searchPlaceholder: 'रूट, ऑपरेटर या स्टॉप नाम से खोजें',
    locating: 'स्थान खोजा जा रहा है…',
    showMyLocation: 'मेरा स्थान दिखाएं',
    geoUnsupported: 'इस ब्राउज़र या कनेक्शन में स्थान एक्सेस उपलब्ध नहीं है',
    routeOperatorCount: '{operator} ({count})',
    matchedStopPrefix: '🚏 {names}',
    noMatch: 'कोई मिलान रूट या स्टॉप नहीं मिला',
    selectedRoute: 'चयनित: {route} ({operator})',
    clearSelection: 'साफ़ करें',
    addLandmarkTitle: '📍 लैंडमार्क जोड़ें',
    addressPlaceholder: 'पता दर्ज करें',
    searching: 'खोजा जा रहा है…',
    add: 'जोड़ें',
    landmarkCount: '{count} / {limit} पंजीकृत',
    landmarkLoadFail: 'लैंडमार्क लोड करने में विफल:',
    landmarkSaveFail: 'लैंडमार्क सहेजने में विफल:',
    landmarkLimit: 'आप अधिकतम {limit} लैंडमार्क पंजीकृत कर सकते हैं। नया जोड़ने से पहले कृपया एक हटाएं।',
    geocodeNoCoords: 'निर्देशांक निर्धारित नहीं किए जा सके। कृपया पता जांचें।',
    kyotoPrefecture: 'क्योटो प्रान्त',
    kyotoOnly: 'केवल क्योटो प्रान्त के भीतर के पते ही पंजीकृत किए जा सकते हैं',
    geocodeFail: 'जियोकोडिंग विफल:',
    addressConvertFail: 'पता परिवर्तित करने में विफल। कृपया बाद में पुनः प्रयास करें।',
    pinLimit: 'आप अधिकतम {limit} पिन सहेज सकते हैं। नया जोड़ने से पहले कृपया एक हटाएं।',
    memoPlaceholder: 'नोट (अधिकतम 300 अक्षर)',
    saveBtn: '📌 सहेजें',
    thisLocation: '📍 यह स्थान',
    landmarkPopupTitle: '📍 लैंडमार्क #{number}',
    pinPopupTitle: '📍 पिन #{number}',
    pinLoadFail: 'पिन लोड करने में विफल:',
    pinSaveFail: 'पिन सहेजने में विफल:',
    historyLoadFail: 'इतिहास लोड करने में विफल:',
    historySaveFail: 'इतिहास सहेजने में विफल:',
    geoNotSupported: 'यह ब्राउज़र स्थान एक्सेस का समर्थन नहीं करता',
    stopsNotReady: 'स्टॉप डेटा अभी लोड होना पूरा नहीं हुआ है',
    outsideKyoto: 'आपका वर्तमान स्थान क्योटो बस स्टॉप क्षेत्र के बाहर है, इसलिए इसे नहीं दिखाया जा सकता',
    myLocation: 'मेरा स्थान',
    geoPermissionDenied: 'स्थान एक्सेस की अनुमति नहीं दी गई',
    geoUnavailable: 'आपका वर्तमान स्थान प्राप्त नहीं किया जा सका',
    geoTimeout: 'स्थान प्राप्त करने का समय समाप्त हो गया',
    geoFail: 'आपका वर्तमान स्थान प्राप्त करने में विफल',
    geoFailLog: 'स्थान प्राप्त करने में विफल:',
    noRouteInfo: '(रूट जानकारी नहीं)',
    moreCount: '+{count} और',
    viewTimetable: '🕒 समय सारणी देखें',
    stopPager: '{page} / {total} (अलग ऑपरेटर/रूट)',
    clusterLoadFail: 'leaflet.markercluster लोड करने में विफल। क्लस्टरिंग के बिना दिखाया जा रहा है:',
    deleteThisPin: 'यह पिन हटाएं',
    deleteThisLandmark: 'यह लैंडमार्क हटाएं',
    recentlyViewed: '🕘 हाल ही में देखे गए स्टॉप',
    closePopup: '✕ बंद करें',
    langSelectTitle: 'भाषा चुनें'
  },
  es: {
    loadingStops: 'Cargando datos de paradas…',
    stopCount: '{stops} paradas ({routes} rutas)',
    searchPlaceholder: 'Buscar por ruta, operador o parada',
    locating: 'Localizando…',
    showMyLocation: 'Mostrar mi ubicación',
    geoUnsupported: 'El acceso a la ubicación no está disponible en este navegador o conexión',
    routeOperatorCount: '{operator} ({count})',
    matchedStopPrefix: '🚏 {names}',
    noMatch: 'No hay rutas ni paradas coincidentes',
    selectedRoute: 'Seleccionado: {route} ({operator})',
    clearSelection: 'Borrar',
    addLandmarkTitle: '📍 Añadir punto de referencia',
    addressPlaceholder: 'Introduce una dirección',
    searching: 'Buscando…',
    add: 'Añadir',
    landmarkCount: '{count} / {limit} registrados',
    landmarkLoadFail: 'Error al cargar los puntos de referencia:',
    landmarkSaveFail: 'Error al guardar los puntos de referencia:',
    landmarkLimit: 'Puedes registrar hasta {limit} puntos de referencia. Elimina uno antes de añadir otro.',
    geocodeNoCoords: 'No se pudieron determinar las coordenadas. Comprueba la dirección.',
    kyotoPrefecture: 'Prefectura de Kioto',
    kyotoOnly: 'Solo se pueden registrar direcciones dentro de la prefectura de Kioto',
    geocodeFail: 'La geocodificación falló:',
    addressConvertFail: 'No se pudo convertir la dirección. Inténtalo de nuevo más tarde.',
    pinLimit: 'Puedes guardar hasta {limit} marcadores. Elimina uno antes de añadir otro.',
    memoPlaceholder: 'Nota (hasta 300 caracteres)',
    saveBtn: '📌 Guardar',
    thisLocation: '📍 Esta ubicación',
    landmarkPopupTitle: '📍 Punto de referencia n.º {number}',
    pinPopupTitle: '📍 Marcador n.º {number}',
    pinLoadFail: 'Error al cargar los marcadores:',
    pinSaveFail: 'Error al guardar los marcadores:',
    historyLoadFail: 'Error al cargar el historial:',
    historySaveFail: 'Error al guardar el historial:',
    geoNotSupported: 'Este navegador no admite el acceso a la ubicación',
    stopsNotReady: 'Los datos de las paradas aún no han terminado de cargarse',
    outsideKyoto: 'Tu ubicación actual está fuera del área de paradas de autobús de Kioto, por lo que no se puede mostrar',
    myLocation: 'Mi ubicación',
    geoPermissionDenied: 'No se concedió el acceso a la ubicación',
    geoUnavailable: 'No se pudo obtener tu ubicación actual',
    geoTimeout: 'Se agotó el tiempo para obtener tu ubicación',
    geoFail: 'No se pudo obtener tu ubicación actual',
    geoFailLog: 'Error al obtener la ubicación:',
    noRouteInfo: '(sin información de ruta)',
    moreCount: '+{count} más',
    viewTimetable: '🕒 Ver horario',
    stopPager: '{page} / {total} (operador/ruta distintos)',
    clusterLoadFail: 'Error al cargar leaflet.markercluster. Mostrando sin agrupación:',
    deleteThisPin: 'Eliminar este marcador',
    deleteThisLandmark: 'Eliminar este punto de referencia',
    recentlyViewed: '🕘 Paradas vistas recientemente',
    closePopup: '✕ Cerrar',
    langSelectTitle: 'Seleccionar idioma'
  },
  fr: {
    loadingStops: "Chargement des données d'arrêts…",
    stopCount: '{stops} arrêts ({routes} lignes)',
    searchPlaceholder: 'Rechercher par ligne, opérateur ou arrêt',
    locating: 'Localisation en cours…',
    showMyLocation: 'Afficher ma position',
    geoUnsupported: "L'accès à la position n'est pas disponible sur ce navigateur ou cette connexion",
    routeOperatorCount: '{operator} ({count})',
    matchedStopPrefix: '🚏 {names}',
    noMatch: 'Aucune ligne ou arrêt correspondant',
    selectedRoute: 'Sélectionné : {route} ({operator})',
    clearSelection: 'Effacer',
    addLandmarkTitle: '📍 Ajouter un repère',
    addressPlaceholder: 'Saisir une adresse',
    searching: 'Recherche en cours…',
    add: 'Ajouter',
    landmarkCount: '{count} / {limit} enregistrés',
    landmarkLoadFail: 'Échec du chargement des repères :',
    landmarkSaveFail: "Échec de l'enregistrement des repères :",
    landmarkLimit: "Vous pouvez enregistrer jusqu'à {limit} repères. Supprimez-en un avant d'en ajouter un autre.",
    geocodeNoCoords: "Impossible de déterminer les coordonnées. Veuillez vérifier l'adresse.",
    kyotoPrefecture: 'Préfecture de Kyoto',
    kyotoOnly: 'Seules les adresses situées dans la préfecture de Kyoto peuvent être enregistrées',
    geocodeFail: 'Le géocodage a échoué :',
    addressConvertFail: "Échec de la conversion de l'adresse. Veuillez réessayer plus tard.",
    pinLimit: "Vous pouvez enregistrer jusqu'à {limit} épingles. Supprimez-en une avant d'en ajouter une autre.",
    memoPlaceholder: 'Note (300 caractères maximum)',
    saveBtn: '📌 Enregistrer',
    thisLocation: '📍 Cet endroit',
    landmarkPopupTitle: '📍 Repère n° {number}',
    pinPopupTitle: '📍 Épingle n° {number}',
    pinLoadFail: 'Échec du chargement des épingles :',
    pinSaveFail: "Échec de l'enregistrement des épingles :",
    historyLoadFail: "Échec du chargement de l'historique :",
    historySaveFail: "Échec de l'enregistrement de l'historique :",
    geoNotSupported: 'Ce navigateur ne prend pas en charge l\u2019accès à la position',
    stopsNotReady: "Le chargement des données d'arrêts n'est pas encore terminé",
    outsideKyoto: 'Votre position actuelle se trouve hors de la zone des arrêts de bus de Kyoto, elle ne peut donc pas être affichée',
    myLocation: 'Ma position',
    geoPermissionDenied: "L'accès à la position n'a pas été autorisé",
    geoUnavailable: 'Impossible d\u2019obtenir votre position actuelle',
    geoTimeout: 'Le délai d\u2019obtention de votre position a été dépassé',
    geoFail: 'Échec de l\u2019obtention de votre position actuelle',
    geoFailLog: "Échec de l'obtention de la position :",
    noRouteInfo: "(pas d'information de ligne)",
    moreCount: '+{count} de plus',
    viewTimetable: '🕒 Voir les horaires',
    stopPager: '{page} / {total} (opérateur/ligne différents)',
    clusterLoadFail: 'Échec du chargement de leaflet.markercluster. Affichage sans regroupement :',
    deleteThisPin: 'Supprimer cette épingle',
    deleteThisLandmark: 'Supprimer ce repère',
    recentlyViewed: '🕘 Arrêts récemment consultés',
    closePopup: '✕ Fermer',
    langSelectTitle: 'Choisir la langue'
  }
}

const locale = ref<Locale>('ja')
let initialized = false

function isLocale(v: string | null): v is Locale {
  return !!v && (LOCALE_VALUES as string[]).includes(v)
}

function detectInitialLocale(): Locale {
  if (typeof window === 'undefined') return 'ja'
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY)
    if (isLocale(saved)) return saved
  } catch {
    // localStorage が使えない環境（プライベートモード等）は無視してブラウザ言語判定へ
  }
  const navLangs = [window.navigator.language, ...(window.navigator.languages || [])]
    .filter(Boolean)
    .map(l => l.toLowerCase())
  for (const nav of navLangs) {
    const hit = LOCALE_VALUES.find(v => nav.startsWith(v))
    if (hit) return hit
  }
  return 'en'
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

// 6択になったため単純トグルは意味を失った。UIはドロップダウン(setLocale直接呼び出し)
// に置き換えたが、他から呼ばれる可能性を考慮し ja/en の往復用に残しておく
function toggleLocale() {
  setLocale(locale.value === 'ja' ? 'en' : 'ja')
}

function t(key: string, vars?: Record<string, string | number>): string {
  ensureInit()
  const table = messages[locale.value] || messages.en
  // 訳が無いキーは日本語ではなく英語にフォールバックする。非日本語話者に
  // とっては日本語が出るより英語が出る方がまだ読める可能性が高いため
  let str = table[key] ?? messages.en[key] ?? key
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
