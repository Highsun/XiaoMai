<template>
  <div class="show-card">
    <img :src="getFullImgUrl(img)" :alt="name" class="show-image" />
    <div class="show-info">
      <div class="card-scroll-wrapper">
        <h3 class="card-scroll-text" ref="nameRef">{{ name }}</h3>
      </div>
      <div class="card-scroll-wrapper">
        <p class="card-scroll-text" ref="dateRef">{{ date }}</p>
      </div>
      <div class="card-scroll-wrapper">
        <p class="card-scroll-text" ref="locationRef">{{ location }}</p>
      </div>
      <router-link :to="`/buy-tickets/${id}`" class="btn-link">
        <button class="btn-purchase">{{ minPrice }}元起</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

// 接收父组件传入的 props
const props = defineProps({
  name: String,
  date: String,
  location: String,
  price: [String, Number],
  img: String,
})

// —— 修正后的 getFullImgUrl ——
// 如果 path 以 http:// 或 https:// 或者以 / 开头，直接返回；否则拼成 /uploads/xxx
function getFullImgUrl(path) {
  if (!path) return ''
  if (/^(https?:)?\/\//.test(path) || path.startsWith('/')) {
    return path
  }
  return `/uploads/${path}`
}

// 计算最低价
const minPrice = computed(() => {
  const p = props.price
  if (typeof p === 'number') return p
  const s = String(p)
  const nums = s
    .split(/[^0-9]+/)
    .map((t) => parseInt(t, 10))
    .filter((n) => !isNaN(n))
  return nums.length > 0 ? Math.min(...nums) : ''
})

// 原滚动文字逻辑不变
const nameRef = ref(null)
const dateRef = ref(null)
const locationRef = ref(null)
function setupScroll(el) {
  if (!el) return
  const wrapper = el.parentElement
  const distance = el.scrollWidth - wrapper.clientWidth
  if (distance <= 0) return
  let dir = -1,
    pos = 0
  function step() {
    pos += dir
    el.style.transform = `translateX(${pos}px)`
    if (pos <= -distance || pos >= 0) {
      dir = -dir
      setTimeout(() => requestAnimationFrame(step), 3000)
    } else {
      requestAnimationFrame(step)
    }
  }
  requestAnimationFrame(step)
}
onMounted(() => {
  ;[nameRef.value, dateRef.value, locationRef.value].forEach(setupScroll)
})
</script>

<style scoped>
.show-card {
  width: 100%;
  max-width: 260px;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}
.show-card:hover {
  transform: translateY(-10px);
}
.show-image {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  object-position: center 20%;
}
.show-info {
  text-align: center;
  padding: 1rem;
}
.card-scroll-wrapper {
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  position: relative;
  height: 1.5em;
}
.card-scroll-text {
  display: inline-block;
  transition: transform 0.2s linear;
  will-change: transform;
}
.btn-purchase {
  margin-top: 0.8rem;
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  font-size: 0.95rem;
  cursor: pointer;
}
.btn-purchase:hover {
  background-color: #369c74;
}
</style>
