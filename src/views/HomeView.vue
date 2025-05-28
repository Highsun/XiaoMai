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
    <button class="btn-test" style="background: transparent; color: black">测试跳转到购票页</button>
  </router-link>

  <Footer />
</template>

<script setup>
import Navbar from '../components/NavbarComp.vue'
import HeroSection from '../components/HeroSectionComp.vue'
import ShowCategory from '../components/ShowCategoryComp.vue'
import ArtistCategory from '../components/ArtistCategoryComp.vue'
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

// 即将推出
const Upcomings = [
  {
    name: 'G.E.M. 邓紫棋 I AM GLORIA 世界巡回演唱会 2.0',
    date: '2025.07.05',
    location: '烟台市·烟台体育公园体育场',
    price: 380,
    img: new URL('../assets/images/homepage/upcomings/GEM.jpeg', import.meta.url).href,
  },
  {
    name: '孙燕姿《就在日落以后》演唱会',
    date: '2025.06.13/06.15',
    location: '北京市·国家体育场-鸟巢',
    price: 480,
    img: new URL('../assets/images/homepage/upcomings/SYZ.jpeg', import.meta.url).href,
  },
  {
    name: '汪苏泷 2025 巡回演唱会「十万伏特 2.0」',
    date: '2025.06.27-06.29',
    location: '太原市·山西体育中心体育场',
    price: 380,
    img: new URL('../assets/images/homepage/upcomings/WSL.jpeg', import.meta.url).href,
  },
  {
    name: '凤凰传奇「吉祥如意」2025 巡回演唱会',
    date: '2025.06.27-06.29',
    location: '天津市·天津奥林匹克中心体育场',
    price: 380,
    img: new URL('../assets/images/homepage/upcomings/FHCQ.jpeg', import.meta.url).href,
  },
]

// 艺术家
const Artists = [
  {
    name: '林俊杰',
    img: new URL('../assets/images/homepage/artists/JJ.JPG', import.meta.url).href,
    link: '/artist/jj',
  },
  {
    name: '周杰伦',
    img: new URL('../assets/images/homepage/artists/Jay.JPG', import.meta.url).href,
    link: '/artist/jay',
  },
  {
    name: '陶喆',
    img: new URL('../assets/images/homepage/artists/DT.JPG', import.meta.url).href,
    link: '/artist/dt',
  },
  {
    name: '王力宏',
    img: new URL('../assets/images/homepage/artists/WLH.JPG', import.meta.url).href,
    link: '/artist/wlh',
  },
  {
    name: '邓紫棋',
    img: new URL('../assets/images/homepage/artists/GEM.JPG', import.meta.url).href,
    link: '/artist/gem',
  },
  {
    name: '孙燕姿',
    img: new URL('../assets/images/homepage/artists/SYZ.JPG', import.meta.url).href,
    link: '/artist/syz',
  },
  {
    name: '五月天',
    img: new URL('../assets/images/homepage/artists/WYT.JPG', import.meta.url).href,
    link: '/artist/wyt',
  },
  {
    name: '单依纯',
    img: new URL('../assets/images/homepage/artists/SYC.JPG', import.meta.url).href,
    link: '/artist/syc',
  },
]
</script>

<style scoped>
.home-content {
  margin-top: 32px;
}
</style>
