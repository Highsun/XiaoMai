<template>
  <div class="artist-card" @click="goToLink">
    <div class="overlay">
      <span class="artist-name">{{ name }}</span>
    </div>
    <img :src="img" :alt="name" />
  </div>
</template>

<script setup>
defineProps({
  name: String,
  img: String,
  link: String,
})

function goToLink() {
  console.log('跳转艺人详情页')
}
</script>

<style scoped>
.artist-card {
  position: relative;
  width: 160px;
  height: 160px;
  min-width: 160px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.artist-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.artist-card:hover {
  transform: scale(1.05);
}

.overlay {
  position: absolute;
  inset: 0;
  backdrop-filter: blur(4px);
  background-color: rgba(0, 0, 0, 0.4);
  opacity: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.3s ease;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  text-align: center;
}

.artist-card:hover .overlay {
  opacity: 1;
}
</style>
