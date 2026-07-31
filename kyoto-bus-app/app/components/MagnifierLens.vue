<template>
  <div
    ref="lensRef"
    class="magnifier-lens"
    :class="{ dragging: isDragging }"
    :style="lensStyle"
    @pointerdown="onPointerDown"
  >
    <div ref="contentWrapperRef" class="magnifier-content" :style="contentStyle"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  // レンズの直径(px)。デフォルトは大きめ
  diameter: { type: Number, default: 220 },
  // 拡大対象のルート要素を指すセレクタ（画面全体＝UIも含む）
  targetSelector: { type: String, default: '#magnify-target' },
  // 画面外にドラッグしたとき、最低限画面内に残す割合（直径に対する比率）
  minVisibleFraction: { type: Number, default: 0.16 },
  // 複製(clone)の更新間隔(ms)。画面複製方式なので完全リアルタイムではない
  refreshInterval: { type: Number, default: 200 }
})

const lensRef = ref(null)
const contentWrapperRef = ref(null)
const isDragging = ref(false)

const centerX = ref(0)
const centerY = ref(0)
let dragOffsetX = 0
let dragOffsetY = 0
let refreshTimer = null

const radius = computed(() => props.diameter / 2)

function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max)
}

// 中心座標が画面端からどれだけ外にはみ出せるか（px）。
// 「直径のminVisibleFraction割合だけ画面内に残す」を満たす値を、
// 円のバウンディングボックス基準で近似計算する
function overflowAllowance() {
  return radius.value * (1 - 2 * props.minVisibleFraction)
}

function clampPosition(x, y) {
  const vw = window.innerWidth
  const vh = window.innerHeight
  const allowance = overflowAllowance()
  return {
    x: clamp(x, -allowance, vw + allowance),
    y: clamp(y, -allowance, vh + allowance)
  }
}

// デフォルト位置: 画面左側に、クランプ限界までギリギリ寄せた位置。縦は画面中央
function setDefaultPosition() {
  const vh = window.innerHeight
  centerX.value = -overflowAllowance()
  centerY.value = vh / 2
}

const lensStyle = computed(() => ({
  width: `${props.diameter}px`,
  height: `${props.diameter}px`,
  left: `${centerX.value - radius.value}px`,
  top: `${centerY.value - radius.value}px`
}))

// レンズ内の複製コンテンツは常にビューポート全体サイズで固定表示し、
// transform-originをレンズの中心座標に合わせて2倍拡大することで、
// 「レンズの中心にある地点を軸に2倍に見える」状態を作る
const contentStyle = computed(() => ({
  transformOrigin: `${centerX.value}px ${centerY.value}px`
}))

function onPointerDown(e) {
  isDragging.value = true
  const rect = lensRef.value.getBoundingClientRect()
  dragOffsetX = e.clientX - (rect.left + rect.width / 2)
  dragOffsetY = e.clientY - (rect.top + rect.height / 2)
  lensRef.value.setPointerCapture(e.pointerId)
  window.addEventListener('pointermove', onPointerMove)
  window.addEventListener('pointerup', onPointerUp)
}

function onPointerMove(e) {
  if (!isDragging.value) return
  const rawX = e.clientX - dragOffsetX
  const rawY = e.clientY - dragOffsetY
  const { x, y } = clampPosition(rawX, rawY)
  centerX.value = x
  centerY.value = y
}

function onPointerUp() {
  isDragging.value = false
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', onPointerUp)
}

function handleResize() {
  const { x, y } = clampPosition(centerX.value, centerY.value)
  centerX.value = x
  centerY.value = y
}

// #magnify-target を複製してレンズの中身として差し込む。
// canvas要素はcloneNode(true)では描画済みピクセルがコピーされないため、
// 元のcanvasから手動でdrawImageし直す
function refreshClone() {
  const target = document.querySelector(props.targetSelector)
  const wrapper = contentWrapperRef.value
  if (!target || !wrapper) return

  const clone = target.cloneNode(true)

  const originalCanvases = target.querySelectorAll('canvas')
  const clonedCanvases = clone.querySelectorAll('canvas')
  originalCanvases.forEach((origCanvas, i) => {
    const clonedCanvas = clonedCanvases[i]
    if (!clonedCanvas) return
    clonedCanvas.width = origCanvas.width
    clonedCanvas.height = origCanvas.height
    const ctx = clonedCanvas.getContext('2d')
    if (ctx) ctx.drawImage(origCanvas, 0, 0)
  })

  wrapper.innerHTML = ''
  wrapper.appendChild(clone)
}

onMounted(() => {
  setDefaultPosition()
  refreshClone()
  refreshTimer = window.setInterval(refreshClone, props.refreshInterval)
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  if (refreshTimer) window.clearInterval(refreshTimer)
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', onPointerUp)
})
</script>

<style scoped>
.magnifier-lens {
  position: fixed;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid rgba(255, 255, 255, 0.95);
  box-shadow:
    0 0 0 1.5px rgba(0, 0, 0, 0.45),
    0 4px 18px rgba(0, 0, 0, 0.4);
  cursor: grab;
  z-index: 999999;
  touch-action: none;
  background: #eee;
}

.magnifier-lens.dragging {
  cursor: grabbing;
}

.magnifier-content {
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  transform: scale(2);
  pointer-events: none;
  will-change: transform;
}
</style>
