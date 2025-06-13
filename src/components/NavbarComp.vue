<template>
  <nav class="navbar">
    <!-- 左侧 Logo + 一级导航 -->
    <div class="navbar-left">
      <div class="logo-title" @click="goHome" style="cursor: pointer">
        <img src="../assets/logo.png" alt="logo" class="logo-img" />
        <span class="logo-text">小麦</span>
      </div>
      <ul class="nav-links">
        <li><a href="#" @click.prevent="goHome">首页</a></li>
        <li><a href="#" @click.prevent="goToCategory">分类</a></li>
      </ul>
    </div>

    <!-- 居中搜索框 -->
    <div class="navbar-center">
      <div class="search-box">
        <i class="fas fa-search search-icon"></i>
        <input
          type="text"
          v-model="searchInput"
          @keyup.enter="doSearch"
          placeholder="搜索演出/艺人"
          class="search-input"
        />
        <button class="search-button" @click="doSearch">搜 索</button>
      </div>
    </div>

    <!-- 右侧账号、设置、购物车 -->
    <div class="navbar-right">
      <button class="icon-btn" title="收藏夹" @click="goToFavorites">
        <i class="fa-solid fa-star"></i>
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
      <button class="icon-btn" title="设置" @click="goToSettings">
        <i class="fas fa-cog"></i>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 账号菜单控制
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

// 跳转函数
function goHome() {
  router.push('/')
}

function goToCategory() {
  router.push('/category')
}

function goToFavorites() {
  router.push('/favorites')
}

function goToLogin() {
  router.push('/login')
}

function goToDashBoard() {
  router.push('/dashboard')
}

function goToSettings() {
  router.push({ name: 'Dashboard', query: { view: 'settings' } })
}

// 搜索输入框状态，与路由 q 参数同步
const searchInput = ref(route.query.q?.toString() || '')

// 监听路由 q 变化，保持输入框同步（浏览器前进后退）
watch(
  () => route.query.q,
  (newQ) => {
    const val = newQ?.toString() || ''
    if (val !== searchInput.value) {
      searchInput.value = val
    }
  },
)

// 监听输入框变化，如果清空且路由有 q，自动删除 q，恢复无查询参数分类页
watch(searchInput, (newVal) => {
  if (newVal.trim() === '' && route.query.q) {
    const newQuery = { ...route.query }
    delete newQuery.q
    router.replace({ path: '/category', query: newQuery })
  }
})

// 执行搜索：输入框有内容时跳转带 q 参数路由
function doSearch() {
  const val = searchInput.value.trim()
  if (val) {
    router.push({ path: '/category', query: { q: val } })
  }
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
