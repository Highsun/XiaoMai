<template>
  <nav class="navbar">
    <!-- 左侧 Logo + 一级导航 -->
    <div class="navbar-left">
      <div class="logo-title" @click="goHome" style="cursor: pointer">
        <!-- TODO: 添加小麦LOGO -->
        <img src="../assets/logo.png" alt="logo" class="logo-img" />
        <span class="logo-text">小麦</span>
      </div>
      <ul class="nav-links">
        <li><a href="#" @click.prevent="goHome">首页</a></li>
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
      <div class="dropdown-wrapper" ref="menuRef">
        <button class="icon-btn" @click="toggleMenu">
          <i class="fas fa-user-circle"></i>
        </button>
        <transition name="fade-slide">
          <div class="dropdown-menu" v-if="menuOpen">
            <div class="dropdown-arrow"></div>
            <ul>
              <li><a href="#" @click.prevent="goToDashBoard">个人中心</a></li>
              <li><a href="#" @click.prevent="goToLogin">登录</a></li>
            </ul>
          </div>
        </transition>
      </div>
      <button class="icon-btn" title="设置">
        <i class="fas fa-cog"></i>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

// LOGO跳转主页
function goHome() {
  router.push('/')
}

// 账号下拉菜单
import { ref, onMounted, onBeforeUnmount } from 'vue'
const menuOpen = ref(false)
const menuRef = ref(null)

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function handleClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    menuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
})

// 跳转登陆
function goToLogin() {
  router.push('/login')
}

// 跳转个人中心
function goToDashBoard() {
  router.push('/dashboard')
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
