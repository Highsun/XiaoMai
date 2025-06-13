<template>
  <Navbar />
  <div class="home-content">
    <!-- 主页轮播宣传海报 -->
    <HeroSection />

    <!-- 热卖中 -->
    <ShowCategory title="热卖中🔥" :shows="HotShows" />

    <!-- 即将推出 -->
    <ShowCategory title="即将推出🔜" :shows="Upcomings" />

    <!-- 艺术家 -->
    <ArtistCategory title="艺术家" :artists="Artists" />
  </div>

  <!-- FIXME: Test -->
  <router-link to="/buy-tickets" class="btn-link">
    <button class="btn-test" style="background: transparent; color: black">
      测试跳转到购票页
    </button>
  </router-link>

  <Footer />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import Navbar from '../components/NavbarComp.vue'
import HeroSection from '../components/HeroSectionComp.vue'
import ShowCategory from '../components/ShowCategoryComp.vue'
import ArtistCategory from '../components/ArtistCategoryComp.vue'
import Footer from '../components/FooterComp.vue'

// 响应式数据
const HotShows = ref([])
const Upcomings = ref([])
const Artists = ref([])

/**
 * 将后端 show 数据格式化为组件需要的 props
 */
function formatShowList(data) {
  return data.map((item) => ({
    name: item.title,
    date:
      item.start_date === item.end_date
        ? item.start_date
        : `${item.start_date} - ${item.end_date}`,
    location: item.location,
    price: parseInt(item.price, 10),
    img: item.image_url,
  }))
}

/**
 * 将后端 artist 数据格式化为组件需要的 props
 */
function formatArtistList(data) {
  return data.map((item) => ({
    id: item.id,
    name: item.name,
    img: item.image_url,
    link: item.link,
  }))
}

onMounted(async () => {
  // 同时请求热卖和即将推出
  try {
    const [hotRes, upcomingRes] = await Promise.all([
      axios.get('http://localhost:8888/api/shows/hot'),
      axios.get('http://localhost:8888/api/shows/upcoming'),
    ])

    if (hotRes.data.code === 0) {
      HotShows.value = formatShowList(hotRes.data.data)
    } else {
      console.warn('加载热卖演出失败：', hotRes.data.message)
    }

    if (upcomingRes.data.code === 0) {
      Upcomings.value = formatShowList(upcomingRes.data.data)
    } else {
      console.warn('加载即将推出演出失败：', upcomingRes.data.message)
    }
  } catch (err) {
    console.error('加载演出信息失败：', err)
  }

  // 请求艺术家列表
  try {
    const artistsRes = await axios.get('http://localhost:8888/api/artists/')
    if (artistsRes.data.code === 0) {
      Artists.value = formatArtistList(artistsRes.data.data)
    } else {
      console.warn('加载艺术家信息失败：', artistsRes.data.message)
    }
  } catch (err) {
    console.error('加载艺术家信息失败：', err)
  }
})
</script>

<style scoped>
.home-content {
  margin-top: 32px;
}
</style>
