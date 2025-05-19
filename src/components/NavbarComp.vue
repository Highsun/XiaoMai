<template>
  <nav class="navbar">
    <!-- 左侧 Logo + 一级导航 -->
    <div class="navbar-left">
      <div class="logo-title" @click="goHome" style="cursor: pointer">
        <img src="../assets/logo.png" alt="logo" class="logo-img" />
        <span class="logo-text">小麦</span>
      </div>
      <ul class="nav-links">
        <li><a href="#">首页</a></li>
        <li><a href="#">分类</a></li>
      </ul>
    </div>

    <!-- 居中搜索框 -->
    <div class="navbar-center">
      <div class="search-box">
        <i class="fas fa-search search-icon"></i>
        <input type="text" placeholder="搜索演出/艺人" class="search-input" />
        <button class="search-button">搜 索</button>
      </div>
    </div>

    <!-- 右侧账号、设置、购物车 -->
    <div class="navbar-right">
      <button class="icon-btn" title="购物车">
        <i class="fas fa-shopping-cart"></i>
      </button>
      <button class="icon-btn" title="账号" @click="goToLogin">
        <i class="fas fa-user-circle"></i>
      </button>
      <button class="icon-btn" title="设置">
        <i class="fas fa-cog"></i>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function goHome() {
  router.push('/')
}

function goToLogin() {
  router.push('/login')
}
</script>

<style scoped>
.logo-img {
  height: 36px;
  width: 36px;
  margin-right: 8px;
}

.logo-text {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}
</style>
