<template>
  <!-- 左侧海报 -->
  <div class="poster-section">
    <img :src="posterUrl" alt="poster" class="poster-image" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const posterUrl = ref('')

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await axios.get(`/api/shows/${id}`)
    if (res.data.code === 0) {
      posterUrl.value = res.data.data.image_url
    } else {
      console.warn('获取演出信息失败:', res.data.message)
    }
  } catch (err) {
    console.error('请求出错:', err)
  }
})
</script>
