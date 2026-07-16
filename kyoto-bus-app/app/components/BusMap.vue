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

function selectRoute(r) {
  selectedRoute.value = r
  renderHighlight(r)
}

function renderHighlight(route) {
  if (!map) return
  highlightLayer.clearLayers()
  baseLayer.eachLayer(l => l.setStyle({ opacity: route ? 0.15 : 0.9, fillOpacity: route ? 0.1 : 0.85 }))

  if (!route) return

  const L = window.__L
  const bounds = []
  for (const id of route.stopIds) {
    const stop = stopsById[id]
    if (!stop) continue
    bounds.push([stop.lat, stop.lng])
    const marker = L.circleMarker([stop.lat, stop.lng], {
      radius: 7,
      weight: 2,
      color: '#dc2626',
      fillColor: '#f87171',
      fillOpacity: 0.95
    })
    const linkHtml = stop.url
      ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">時刻表を見る</a></p>`
      : ''
    marker.bindPopup(`<div class="stop-popup"><p class="stop-name">${stop.name}</p><p class="stop-kana">${route.operator} / ${route.route}</p>${linkHtml}</div>`)
    marker.on('mouseover', function () { this.openPopup() })
    marker.on('mouseout', function () { this.closePopup() })
    marker.addTo(highlightLayer)
  }
  if (bounds.length) map.fitBounds(bounds, { padding: [40, 40], maxZoom: 15 })
}

onMounted(async () => {
  const L = await import('leaflet')
  window.__L = L

  map = L.map(mapEl.value, {
    center: [35.011, 135.768], // 京都御所付近
    zoom: 12
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map)

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

  baseLayer = L.layerGroup()
  highlightLayer = L.layerGroup().addTo(map)

  for (const stop of stops) {
    const marker = L.circleMarker([stop.lat, stop.lng], {
      radius: 4,
      weight: 1,
      color: '#1d4ed8',
      fillColor: '#3b82f6',
      fillOpacity: 0.85
    })

    const routesLabel = stop.routes.length ? stop.routes.join('、') : '（系統情報なし）'
    const linkHtml = stop.url
      ? `<p class="stop-link"><a href="${stop.url}" target="_blank" rel="noopener">時刻表を見る</a></p>`
      : ''
    const popupHtml = `<div class="stop-popup"><p class="stop-name">${stop.name}</p><p class="stop-kana">${stop.operator}</p><p class="stop-routes">${routesLabel}</p>${linkHtml}</div>`
    marker.bindPopup(popupHtml)

    marker.on('mouseover', function () { this.openPopup() })
    marker.on('mouseout', function () { this.closePopup() })

    marker.addTo(baseLayer)
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

:deep(.stop-link) {
  margin: 4px 0 0;
}

:deep(.stop-link a) {
  color: #1d4ed8;
  font-size: 12px;
  text-decoration: underline;
}
</style>
