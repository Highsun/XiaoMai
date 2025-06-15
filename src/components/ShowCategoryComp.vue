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
        :id="item.id"
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
import { useRouter } from 'vue-router'
import ShowCard from '../components/ShowCardComp.vue'

defineProps({
  title: {
    type: String,
    required: true,
  },
  shows: {
    type: Array,
    default: () => [],
  },
})

const router = useRouter()
function goToCategory() {
  router.push('/category')
}
</script>

<style scoped>
/* 最外层容器，给个 max-width 并水平居中 */
.category-container {
  margin: 24px auto;
  padding: 0 16px; /* 给左右留点内边距，避免贴边 */
  max-width: 1200px; /* 根据你的设计稿决定宽度 */
}

/* 标题区 */
.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.category-title {
  font-size: 20px;
  font-weight: bold;
}
.more-link {
  font-size: 14px;
  color: #3bc586;
  cursor: pointer;
}

/* 关键：卡片列表 */
.card-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* 水平居中每一行 */
  gap: 16px;
}

/* 如果你还想让整体内容垂直方向也居中（多行情况下），可以加上： */
/* align-content: center;  */
/* 但通常不需要，默认每行会紧凑排列。 */
</style>
