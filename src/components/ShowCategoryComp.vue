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
import { useRouter } from 'vue-router'

defineProps({
  title: String,
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
