<template>
  <div>
    <Navbar />
    <div class="home-content">
      <!-- TODO: 主页内容 -->
      <!-- 主页轮播宣传海报 -->
      <HeroSection />

      <!-- 热卖中 -->
      <ShowCategory title="热卖中🔥" :shows="HotShows" />
      <!-- 即将推出 -->
      <!-- 分类预览 -->
      <!-- 艺术家 -->

      <!-- 新闻 -->
      <Footer />
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/NavbarComp.vue'
import HeroSection from '../components/HeroSectionComp.vue'
import ShowCategory from '../components/ShowCategoryComp.vue'
import Footer from '../components/FooterComp.vue'

// 热卖中
const HotShows = [
  {
    name: 'JJ20 FINAL LAP 世界巡回演唱会',
    date: '2025.06.28-07.13',
    location: '北京市·国家体育场-鸟巢',
    price: 380,
    img: new URL('../assets/images/homepage/hot_shows/JJ.HEIC', import.meta.url).href,
  },
  {
    name: '周杰伦《嘉年华》巡回演唱会',
    date: '2025.06.27-06.29',
    location: '中国香港·香港启德体育园主场馆',
    price: 1100,
    img: new URL('../assets/images/homepage/hot_shows/Jay.HEIC', import.meta.url).href,
  },
  {
    name: '陶喆 Soul Power II 世界巡回演唱会',
    date: '2025.08.09-08.10',
    location: '深圳市·深圳湾体育中心“春茧”体育场',
    price: 380,
    img: new URL('../assets/images/homepage/hot_shows/DT.HEIC', import.meta.url).href,
  },
  {
    name: '王力宏「最好的地方」巡回演唱会',
    date: '2025.07.05-07.06',
    location: '苏州市·苏州奥林匹克体育中心体育馆',
    price: 480,
    img: new URL('../assets/images/homepage/hot_shows/WLH.HEIC', import.meta.url).href,
  },
]
</script>

<style scoped>
.home-content {
  margin-top: 32px;
}
</style>
