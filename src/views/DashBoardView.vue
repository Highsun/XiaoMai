<template>
  <Navbar />

  <div class="dashboard-wrapper">
    <div class="dashboard-container">
      <!-- 左侧侧边栏 -->
      <div class="sidebar card">
        <div class="sidebar-content">
          <ul>
            <li :class="{ active: view === 'account' }" @click="view = 'account'">
              <i class="fa-solid fa-user icon-fixed"></i>
              <span>我的账号</span>
            </li>
            <li :class="{ active: view === 'tickets' }" @click="view = 'tickets'">
              <i class="fa-solid fa-ticket icon-fixed"></i>
              <span>我的票夹</span>
            </li>
            <li :class="{ active: view === 'orders' }" @click="view = 'orders'">
              <i class="fa-solid fa-receipt icon-fixed"></i>
              <span>历史订单</span>
            </li>
            <li :class="{ active: view === 'settings' }" @click="view = 'settings'">
              <i class="fa-solid fa-sliders icon-fixed"></i>
              <span>账号设置</span>
            </li>
            <li :class="{ active: view === 'help' }" @click="view = 'help'">
              <i class="fa-solid fa-circle-info icon-fixed"></i>
              <span>帮助中心</span>
            </li>
          </ul>
        </div>
        <div class="sidebar-footer">
          <button class="logout-btn" @click="logout">
            <i class="fa-solid fa-right-from-bracket icon-fixed"></i>
            <span>退出登录</span>
          </button>
        </div>
      </div>

      <!-- 右侧主内容区域 -->
      <div class="dashboard-content card">
        <Transition name="fade" mode="out-in">
          <div :key="view">
            <div v-if="view === 'account'">
              <h2>欢迎回来，{{ username }}！</h2>
              <div class="personal-info">
                <!-- TODO: 个人信息修改表单 -->
              </div>
            </div>
            <div v-else-if="view === 'tickets'">
              <h2>亲爱的 {{ username }}，</h2>
              <!-- TODO: 分类展示：未使用、已使用 -->
            </div>
            <div v-else-if="view === 'orders'">
              <h2>亲爱的 {{ username }}，</h2>
              <!-- TODO: 订单状态：全部、待付款、待收货、待评价、已过期 -->
            </div>
            <div v-else-if="view === 'settings'">
              <h2>亲爱的 {{ username }}，</h2>
              <!-- TODO: 配送地址、观演人管理、订阅管理、修改密码、注销账号 -->
            </div>
            <div v-else-if="view === 'help'">
              <h2>亲爱的 {{ username }}，</h2>
              <!-- TODO: 在线客服、用户反馈 -->
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>

  <Footer />
</template>

<script setup>
import { ref } from 'vue'
import Navbar from '../components/NavbarComp.vue'
import Footer from '../components/FooterComp.vue'

const view = ref('account')

function logout() {
  alert('已退出登录')
}
</script>

<style scoped>
.dashboard-wrapper {
  margin-top: 64px;
  background-color: #f8f8f8;
  min-height: calc(100vh - 64px);
  display: flex;
  justify-content: center;
  align-items: stretch;
  padding: 20px 60px;
}

.dashboard-container {
  display: flex;
  gap: 24px;
  flex: 1;
}

.card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  padding: 24px;
}

.sidebar {
  width: 220px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  min-height: calc(100vh - 104px);
}

.sidebar-content {
  flex: 1;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
}

.sidebar li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  font-size: 14px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

.sidebar li:hover,
.sidebar li.active {
  background-color: #e6f0ff;
  font-weight: bold;
}

.icon-fixed {
  width: 20px;
  text-align: center;
}

.sidebar-footer {
  margin-top: auto;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: transparent;
  color: #333;
  border: none;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  width: 100%;
  font-size: 14px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  color: white;
  background-color: #ff4d4f;
}

.dashboard-content {
  flex: 1;
}

.dashboard-content h2 {
  text-align: left;
  margin-bottom: 16px;
  font-size: 24px;
  color: #333;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
