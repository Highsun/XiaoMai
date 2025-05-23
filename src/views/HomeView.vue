<template>
  <div>
    <Navbar />
    <div class="home-content">
      <!-- TODO: 主页内容 -->
      <main></main>
      <!-- 主页置顶全屏海报 -->
      <HeroSection />
      <!-- 滚动推荐 -->
      <!-- 热卖中 -->
      <!-- 即将推出 -->
      <!-- 分类预览 -->
      <!-- 艺术家 -->

      <!-- 新闻 -->
    </div>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '../components/NavbarComp.vue'
import HeroSection from '../components/HeroSectionComp.vue'

import Footer from '../components/FooterComp.vue'
</script>

<style scoped>
main {
  margin-top: 32px;
}
</style>
