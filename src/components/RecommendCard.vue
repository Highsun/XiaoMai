<template>
  <div class="recommend-card">
    <img :src="getPoster(concert.poster)" alt="poster" class="recommend-img" />
    <div class="recommend-info">
      <div class="recommend-name">{{ concert.name }}</div>
      <div class="recommend-date">{{ concert.date }}</div>
      <div class="recommend-price">{{ concert.price }}</div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  concert: Object
})

function getPoster(name) {
  // 实际开发中改为服务器路径
  return `/static/poster/${name}`
}
</script>

<style scoped>
.recommend-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f1f1f1;
}
.recommend-img {
  width: 54px;
  height: 72px;
  border-radius: 8px;
  object-fit: cover;
  background: #f7f7f7;
}
.recommend-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.recommend-name {
  font-size: 15px;
  color: #34495e;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.recommend-date, .recommend-price {
  font-size: 13px;
  color: #3bc586;
}
</style>
