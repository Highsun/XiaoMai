<template>
  <div class="poster-section">
    <img :src="posterUrl" alt="poster" class="poster-image" />
  </div>
</template>

<script setup>
const posterUrl = '/backend/uploads/concerts/JJ20.jpeg'
</script>

<style scoped>
.poster-section {
  width: 100%;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  background: #f6f8f7;
}

.poster-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  object-position: center;
}
</style>
