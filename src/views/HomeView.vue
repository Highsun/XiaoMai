<template>
  <Navbar />
  <div class="home-content">
    <!-- 主页轮播宣传海报 -->
    <HeroSection />

    <!-- 热卖中：只取有 img 的前 8 条 -->
    <ShowCategory title="热卖中🔥" :shows="hotShowsLimited" />

    <!-- 即将推出：只取有 img 的前 4 条 -->
    <ShowCategory title="即将推出🔜" :shows="upcomingShowsLimited" />

    <!-- 艺术家 -->
    <ArtistCategory title="艺术家" :artists="Artists" />
  </div>

  <Footer />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

import Navbar from '../components/NavbarComp.vue'
import HeroSection from '../components/HeroSectionComp.vue'
import ShowCategory from '../components/ShowCategoryComp.vue'
import ArtistCategory from '../components/ArtistCategoryComp.vue'
import Footer from '../components/FooterComp.vue'

// —— 响应式数据 ——
const HotShows = ref([])
const Upcomings = ref([])
const Artists = ref([])

// —— 工具函数 ——
function beautifyDate(str) {
  if (!str) return ''
  const m = str.match(/^(\d{4}-\d{2}-\d{2})(?:-(\d{4}-\d{2}-\d{2}))?$/)
  if (!m) return str.replace(/-/g, '.')
  const s = m[1].replace(/-/g, '.')
  const e = m[2] ? m[2].replace(/-/g, '.') : ''
  return e && s !== e ? `${s} - ${e}` : s
}

function beautifyPrice(p) {
  if (typeof p === 'string') return p
  if (Array.isArray(p) && p.length > 0) {
    if (p.length === 1) return `${p[0]}元`
    return `${Math.min(...p)}-${Math.max(...p)}元`
  }
  return ''
}

// —— 计算属性：限量展示 ——
const hotShowsLimited = computed(() => HotShows.value.filter((s) => Boolean(s.img)).slice(0, 8))

const upcomingShowsLimited = computed(() =>
  Upcomings.value.filter((s) => Boolean(s.img)).slice(0, 4),
)

onMounted(async () => {
  try {
    // 拉热卖中
    const hotRes = await axios.get('/api/shows/hot')
    if (hotRes.data.code === 0) {
      HotShows.value = hotRes.data.data.map((item) => ({
        id: item.id,
        name: item.title,
        date: beautifyDate(
          item.start_date && item.end_date
            ? `${item.start_date}-${item.end_date}`
            : item.start_date,
        ),
        location: item.location,
        price: beautifyPrice(item.price),
        img: item.image_url ? item.image_url : '',
      }))
    } else {
      console.warn('加载热卖演出失败：', hotRes.data.message)
    }

    // 拉即将推出
    const upRes = await axios.get('/api/shows/upcoming')
    if (upRes.data.code === 0) {
      Upcomings.value = upRes.data.data.map((item) => ({
        id: item.id,
        name: item.title,
        date: beautifyDate(
          item.start_date && item.end_date
            ? `${item.start_date}-${item.end_date}`
            : item.start_date,
        ),
        location: item.location,
        price: beautifyPrice(item.price),
        img: item.image_url ? item.image_url : '',
      }))
    } else {
      console.warn('加载即将推出演出失败：', upRes.data.message)
    }

    // 拉艺术家
    const artRes = await axios.get('/api/artists/')
    if (artRes.data.code === 0) {
      Artists.value = artRes.data.data.map((item) => ({
        id: item.id,
        name: item.name,
        img: item.image_url,
        link: item.link,
      }))
    } else {
      console.warn('加载艺术家信息失败：', artRes.data.message)
    }
  } catch (err) {
    console.error('加载数据失败：', err)
  }
})
</script>

<style scoped>
.home-content {
  margin-top: 32px;
}
</style>
