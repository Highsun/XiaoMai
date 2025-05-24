<template>
  <section class="category-container">
    <!-- 标题 + 浏览更多 -->
    <div class="category-header">
      <h2 class="category-title">{{ title }}</h2>
      <a class="more-link" @click.prevent="goToCategory">浏览更多</a>
    </div>

    <!-- 卡片列表 -->
    <div class="card-list">
      <ShowCard
        v-for="(item, index) in shows"
        :key="index"
        :name="item.name"
        :date="item.date"
        :location="item.location"
        :price="item.price"
        :img="item.img"
      />
    </div>
  </section>
</template>

<script setup>
import ShowCard from '../components/ShowCardComp.vue'

defineProps({
  title: String,
  shows: {
    type: Array,
    default: () => [],
  },
})

function goToCategory() {
  // TODO: 跳转到分类页的逻辑
  console.log('跳转分类页')
}
</script>

<style scoped>
.category-container {
  margin: 40px auto;
  padding: 0 16px;
  max-width: 1200px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.category-title {
  font-size: 1.6rem;
  font-weight: bold;
  color: #333;
}

.more-link {
  color: #333;
  margin-bottom: 16px;
  text-decoration: none;
  cursor: pointer;
  white-space: nowrap;
  transition: color 0.2s ease;
}

.more-link:hover {
  color: #42b983;
}

.card-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}
</style>
