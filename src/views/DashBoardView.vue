<template>
  <Navbar />

  <div class="dashboard-wrapper">
    <div class="dashboard-container">
      <!-- 左侧侧边栏 -->
      <div class="sidebar card">
        <div class="sidebar-content">
          <ul>
            <li :class="{ active: view === 'account' }" @click="changeView('account')">
              <i class="fa-solid fa-user icon-fixed"></i>
              <span>我的账号</span>
            </li>
            <li
              :class="[{ active: view === 'tickets' }, { 'sidebar-disabled': !userStore.isLoggedIn }]"
              @click="userStore.isLoggedIn && changeView('tickets')"
            >
              <i class="fa-solid fa-ticket icon-fixed"></i>
              <span>我的票夹</span>
            </li>
            <li
              :class="[{ active: view === 'orders' }, { 'sidebar-disabled': !userStore.isLoggedIn }]"
              @click="userStore.isLoggedIn && changeView('orders')"
            >
              <i class="fa-solid fa-receipt icon-fixed"></i>
              <span>历史订单</span>
            </li>
            <li
              :class="[{ active: view === 'settings' }, { 'sidebar-disabled': !userStore.isLoggedIn }]"
              @click="userStore.isLoggedIn && changeView('settings')"
            >
              <i class="fa-solid fa-sliders icon-fixed"></i>
              <span>账号设置</span>
            </li>
            <li
              :class="{ active: view === 'help' }"
              @click="changeView('help')"
            >
              <i class="fa-solid fa-circle-info icon-fixed"></i>
              <span>帮助中心</span>
            </li>
          </ul>
        </div>
        <div class="sidebar-footer" v-if="userStore.isLoggedIn">
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
            <!-- 账号信息 -->
            <div v-if="view === 'account'">
              <h2>
                {{ userStore.isLoggedIn ? '亲爱的 ' + userStore.username + '，' : '这里空空如也呢，先登录吧！' }}
              </h2>
              <h4 style="grid-column: 1 / -1; margin: 32px 0 16px 0">您可以在此处编辑个人信息</h4>
              <div :class="['info-edit-panel', { 'disabled-panel': !userStore.isLoggedIn }]">
                <PersonalInfo :disabled="!userStore.isLoggedIn" />
              </div>
            </div>

            <!-- 我的票夹 -->
            <div v-else-if="view === 'tickets'" class="ticket-section">
              <h2>
                {{ userStore.isLoggedIn ? '亲爱的 ' + userStore.username + '，' : '这里空空如也呢，先登录吧！' }}
              </h2>
              <h4 style="grid-column: 1 / -1; margin: 32px 0 16px 0">以下是您已订购的演出</h4>
              <div class="ticket-tabs">
                <button
                  v-for="tab in tabs"
                  :key="tab"
                  @click="activeTab = tab"
                  :class="['ticket-tab', { active: activeTab === tab }]"
                >
                  {{ tab }}
                </button>
              </div>
              <div v-for="ticket in filteredTickets" :key="ticket.id" class="ticket-item">
                <div class="ticket-left">
                  <img :src="ticket.avatar" alt="avatar" class="ticket-avatar" />
                  <span class="ticket-artist">{{ ticket.artist }}</span>
                </div>
                <div class="ticket-center">
                  <div><i class="fa-solid fa-calendar-days"></i> {{ ticket.time }}</div>
                  <div><i class="fa-solid fa-location-dot"></i> {{ ticket.venue }}</div>
                  <div><i class="fa-solid fa-chair"></i> {{ ticket.seat }}</div>
                  <div><i class="fa-solid fa-tag"></i> ￥{{ ticket.price }}</div>
                </div>
                <!-- 只有未使用状态下显示下拉和二维码 -->
                <div
                  v-if="ticket.ticket_status === '未使用'"
                  class="ticket-dropdown-container"
                  @click.stop
                >
                  <button
                    class="ticket-details-button"
                    @click="toggleDropdown(ticket.id)"
                    title="下载入场凭证"
                  >
                    <i class="fas fa-ellipsis-v"></i>
                  </button>
                  <transition name="dropdown-fade">
                    <div
                      v-if="dropdownOpenId === ticket.id"
                      class="ticket-dropdown"
                      :id="`qr-container-${ticket.id}`"
                    >
                      <div class="ticket-qr-title">
                        <div class="ticket-qr-header">
                          <img src="../assets/logo.png" alt="logo" class="ticket-logo" />
                          <div>
                            <p style="color: #666">小麦</p>
                            <p style="font-size: 10px; color: #666">全球领先的票务代理</p>
                          </div>
                        </div>
                        <h4>扫码入场</h4>
                      </div>
                      <div class="ticket-qr-wrapper">
                        <img :src="ticket.qr" alt="qr-code" class="ticket-qr" />
                        <a
                          href="#"
                          @click.prevent="downloadTicketAsImage(ticket.id)"
                          class="ticket-download"
                        >
                          下载入场凭证
                        </a>
                      </div>
                      <div class="ticket-info">
                        <div><strong>座位：</strong>{{ ticket.seat }}</div>
                        <div><strong>票价：</strong>￥{{ ticket.price }}</div>
                        <div><strong>XMT-ID：</strong>{{ ticket.id }}</div>
                      </div>
                    </div>
                  </transition>
                </div>
                <!-- 已使用/已过期：不显示下拉和二维码，按钮也不显示 -->
              </div>
            </div>

            <!-- 历史订单 -->
            <div v-else-if="view === 'orders'">
              <h2>
                {{ userStore.isLoggedIn ? '亲爱的 ' + userStore.username + '，' : '这里空空如也呢，先登录吧！' }}
              </h2>
              <h4 style="grid-column: 1 / -1; margin: 32px 0 16px 0">以下是您的历史订单</h4>
              <div class="ticket-tabs">
                <button
                  v-for="tab in history_tabs"
                  :key="tab"
                  @click="activeTab = tab"
                  :class="['ticket-tab', { active: activeTab === tab }]"
                >
                  {{ tab }}
                </button>
              </div>
              <div v-for="ticket in filteredTickets" :key="ticket.id" class="ticket-item">
                <div class="ticket-left">
                  <img :src="ticket.avatar" alt="avatar" class="ticket-avatar" />
                  <span class="ticket-artist">{{ ticket.artist }}</span>
                </div>
                <div class="ticket-center">
                  <div><i class="fa-solid fa-calendar-days"></i> {{ ticket.time }}</div>
                  <div><i class="fa-solid fa-tag"></i> ￥{{ ticket.price }}</div>
                  <div>订单创建时间: {{ ticket.createtime }}</div>
                </div>
                <div class="go-to-perform-detail">
                  <button class="ticket-details-button" title="查看详情">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                  </button>
                </div>
              </div>
            </div>

            <!-- 账号设置 -->
            <div v-else-if="view === 'settings'">
              <h2>
                {{ userStore.isLoggedIn ? '亲爱的 ' + userStore.username + '，' : '这里空空如也呢，先登录吧！' }}
              </h2>
              <h4 style="grid-column: 1 / -1; margin: 32px 0 16px 0">在此查看或更改您的账号设置</h4>
              <MessageSubscription />
              <SpectatorManager />
              <ChangePassword />
              <DeleteAccount />
            </div>

            <!-- 帮助中心 -->
            <div v-else-if="view === 'help'">
              <h4 style="grid-column: 1 / -1; margin: 32px 0 16px 0">我们可以如何帮助您？</h4>
              <FastQA />
              <CustomerService />
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>

  <Footer />
</template>

<script setup>
import Navbar from '../components/NavbarComp.vue'
import Footer from '../components/FooterComp.vue'
import MessageSubscription from '../components/account_settings_comps/MessageSubscription.vue'
import SpectatorManager from '../components/account_settings_comps/SpectatorManager.vue'
import ChangePassword from '../components/account_settings_comps/ChangePassword.vue'
import DeleteAccount from '../components/account_settings_comps/DeleteAccount.vue'
import PersonalInfo from '@/components/my_account_comps/PersonalInfo.vue'
import FastQA from '@/components/help_center_comps/FastQ&A.vue'
import CustomerService from '@/components/help_center_comps/CustomerService.vue'

import { userStore } from '@/stores/userStore.js'
import { ref, watchEffect, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import html2canvas from 'html2canvas'

const router = useRouter()
const route = useRoute()

const isLoggedIn = ref(!!localStorage.getItem('access_token'))

window.addEventListener('storage', () => {
  isLoggedIn.value = !!localStorage.getItem('access_token')
})
watchEffect(() => {
  isLoggedIn.value = !!localStorage.getItem('access_token')
})

// 登出
function logout() {
  userStore.logout()
  router.push('/')
}

const view = ref('account')
const tabs = ['未使用', '已使用', '已过期']
const history_tabs = ['交易成功', '已取消']
const activeTab = ref('未使用')

// 订单英文状态转中文
const statusMap = {
  'paid': '交易成功',
  'cancelled': '已取消'
}

// 票夹&订单数据
const tickets = ref([])

// 过滤
const filteredTickets = computed(() => {
  if (view.value === 'tickets') {
    return tickets.value.filter(
      ticket =>
        ticket.ticket_status === activeTab.value &&
        ticket.order_status === 'paid'
    )
  }
  if (view.value === 'orders') {
    // 显示所有订单
    return tickets.value.filter(
      ticket => statusMap[ticket.order_status] === activeTab.value
    )
  }
  return []
})


// 下拉菜单控制
const dropdownOpenId = ref(null)
function toggleDropdown(id) {
  dropdownOpenId.value = dropdownOpenId.value === id ? null : id
}
function handleClickOutside(event) {
  const dropdowns = document.querySelectorAll('.ticket-dropdown-container')
  let clickedInside = false
  dropdowns.forEach((container) => {
    if (container.contains(event.target)) {
      clickedInside = true
    }
  })
  if (!clickedInside) {
    dropdownOpenId.value = null
  }
}

// 下载核销二维码为图片
async function downloadTicketAsImage(ticketId) {
  const el = document.getElementById(`qr-container-${ticketId}`)
  if (!el) return
  const originalBorderImage = el.style.borderImage
  const originalBorder = el.style.border
  el.style.borderImage = 'none'
  el.style.border = 'none'
  try {
    const canvas = await html2canvas(el, {
      backgroundColor: '#ffffff',
      scale: 4,
    })
    const link = document.createElement('a')
    link.href = canvas.toDataURL('image/png')
    link.download = `XMTicket-${ticketId}.png`
    link.click()
  } catch (error) {
    console.error('下载失败:', error)
  } finally {
    el.style.borderImage = originalBorderImage
    el.style.border = originalBorder
  }
}

// 数据请求：获取票夹和订单数据
async function fetchTickets() {
  if (!userStore.isLoggedIn) {
    tickets.value = []
    return
  }
  try {
    const res = await axios.get('/api/orders/my-tickets', {
      headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
    })
    if (res.data.code === 0 && Array.isArray(res.data.data)) {
      tickets.value = res.data.data
    } else {
      tickets.value = []
    }
  } catch (err) {
    console.error('获取票夹失败', err)
    tickets.value = []
  }
}

// 切换视图时同步页面信息
function changeView(targetView) {
  view.value = targetView
  if (targetView === 'tickets') {
    activeTab.value = tabs[0]
    fetchTickets()
  } else if (targetView === 'orders') {
    activeTab.value = history_tabs[0]
    fetchTickets()
  }
}

// 首次挂载拉取
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  if (route.query.view) {
    view.value = route.query.view
  }
  fetchTickets()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

</script>

<style scoped>
/* 你的全部样式，无任何变动 */
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
  background-color: #e6f9f2;
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
.ticket-tabs {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  margin-bottom: 1rem;
}
.ticket-tabs button {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: white;
  color: #333;
  white-space: nowrap;
  cursor: pointer;
  width: auto;
  min-width: 0;
  flex: 0 0 auto;
}
.ticket-tabs button.active {
  background-color: #42b983;
  color: white;
  border-color: #42b983;
}
.ticket-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
  position: relative;
}
.ticket-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.ticket-left img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}
.ticket-center {
  flex: 3;
  display: flex;
  flex-direction: row;
  padding: 0 48px;
  gap: 32px;
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}
.ticket-details-button {
  color: #42b983;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}
.ticket-dropdown-container {
  position: relative;
}
.ticket-dropdown {
  position: absolute;
  right: 36px;
  top: 12px;
  width: 240px;
  background: white;
  border: 2px solid;
  border-image: linear-gradient(135deg, #42b983, #6a5af9, #ff4d4f, #f9d423) 1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  padding: 16px;
  z-index: 100;
}
.ticket-qr-title {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
.ticket-qr-header {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
}
.ticket-qr-title h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 10px auto;
  text-align: center;
}
.ticket-qr-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}
.ticket-qr {
  width: 128px;
  height: 128px;
  object-fit: contain;
  margin-bottom: 8px;
}
.ticket-download {
  display: inline-block;
  font-size: 13px;
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
}
.ticket-download:hover {
  text-decoration: underline;
}
.ticket-info {
  text-align: center;
  font-size: 13px;
  color: #333;
  line-height: 1.6;
}
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: opacity 0.3s ease;
}
.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
}
.dropdown-fade-enter-to,
.dropdown-fade-leave-from {
  opacity: 1;
}
.go-to-perform-detail {
  position: relative;
}
.disabled-panel {
  pointer-events: none;
  opacity: 0.5;
  filter: grayscale(60%);
}
.sidebar-disabled {
  color: #bbb !important;
  pointer-events: none !important;
  background: none !important;
  cursor: not-allowed !important;
  font-weight: normal !important;
}
.sidebar-disabled i {
  color: #bbb !important;
}
</style>
