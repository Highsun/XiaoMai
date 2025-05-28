<template>
  <!-- 左侧海报 -->
  <div class="poster-section">
    <img :src="posterUrl" alt="poster" class="poster-image" />
  </div>
</template>

<script setup>
const posterUrl = 'src/assets/images/buy_tickets/JJ20 FINAL LAP/poster.HEIC' // TODO: 接入数据库
</script>
