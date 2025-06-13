<template>
  <!-- 左侧海报 -->
  <div class="poster-section">
    <img :src="posterUrl" alt="poster" class="poster-image" />
  </div>
</template>

<script setup>
const posterUrl = 'backend/uploads/concerts/poster.png' // 修改为后端路径
</script>
