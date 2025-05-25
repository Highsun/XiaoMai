<template>
  <div class="show-card">
    <img :src="img" :alt="name" class="show-image" />
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
      <button class="btn-purchase">{{ price }}元起</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// ShowCard 数据结构
defineProps({
  name: String,
  date: String,
  location: String,
  price: [String, Number],
  img: String,
})

const nameRef = ref(null)
const dateRef = ref(null)
const locationRef = ref(null)

function setupScroll(el) {
  const wrapper = el.parentElement
  const scrollDistance = el.scrollWidth - wrapper.clientWidth

  if (scrollDistance <= 0) return // 没有溢出

  let direction = -1
  let position = 0

  function animate() {
    position += direction * 1 // 每帧移动 px
    el.style.transform = `translateX(${position}px)`

    if (position <= -scrollDistance || position >= 0) {
      direction *= -1
      setTimeout(() => requestAnimationFrame(animate), 3000) // 到头停顿3秒
    } else {
      requestAnimationFrame(animate)
    }
  }

  requestAnimationFrame(animate)
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
  object-position: center 20%;
  object-fit: cover;
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

.show-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.show-date,
.show-location {
  font-size: 0.95rem;
  color: #666;
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
