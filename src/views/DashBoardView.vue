<template>
  <Navbar />

  <!-- TODO: 全部弄完之后记得组件化 -->
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
              <h2>{{ welcome }} {{ username }}{{ marker }}</h2>
              <div class="personal-info">
                <h4 style="grid-column: 1 / -1; margin: 16px 0">编辑账号信息</h4>
                <div class="form-group" v-for="field in fields" :key="field.key">
                  <label :for="field.key">{{ field.label }}</label>
                  <!-- 性别 -->
                  <select
                    v-if="field.key === 'gender'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    :style="{ color: formData.gender ? '#333' : '#aaa' }"
                  >
                    <option disabled value="">请选择性别</option>
                    <option value="男">男</option>
                    <option value="女">女</option>
                    <option value="保密">保密</option>
                  </select>
                  <!-- 出生日期 -->
                  <input
                    v-else-if="field.key === 'birthday'"
                    type="date"
                    :id="field.key"
                    v-model="formData[field.key]"
                    :max="today"
                  />
                  <!-- TODO: “国家和地区”改为三栏联合选择框 -->
                  <!-- 普通输入框 -->
                  <input
                    v-else
                    type="text"
                    :id="field.key"
                    :placeholder="`请输入${field.label}`"
                    v-model="formData[field.key]"
                  />
                </div>
              </div>
              <div class="form-actions">
                <button class="save-btn" @click="saveChanges">保存修改</button>
                <button class="cancel-btn" @click="cancelChanges">取消</button>
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
              <!-- TODO: 配送地址，观演人管理，订阅管理，修改邮箱、手机号、密码，注销账号 -->
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
import Navbar from '../components/NavbarComp.vue'
import Footer from '../components/FooterComp.vue'

import { ref, reactive } from 'vue'

const view = ref('account')
const welcome = ref('亲爱的')
const username = ref('小麦用户_89757')
const marker = ref('，')

function logout() {
  // TODO: 添加清除用户登录状态的逻辑
  view.value = 'account'
  welcome.value = '这里空空如也呢，先登录吧'
  username.value = ''
  marker.value = '！'
  alert('已退出登录')
}

// TODO: 全靠我们伟大的后端了
const fields = [
  { key: 'name', label: '姓名' },
  { key: 'gender', label: '性别' },
  { key: 'birthday', label: '出生日期' },
  { key: 'email', label: '国家与地区' },
]

const formData = reactive({})
const originalData = {}

fields.forEach((field) => {
  formData[field.key] = ''
  originalData[field.key] = ''
})

const today = new Date().toISOString().split('T')[0]

function saveChanges() {
  alert('保存成功')
  // TODO: 接入后端数据库
  fields.forEach((field) => {
    originalData[field.key] = formData[field.key]
  })
}

function cancelChanges() {
  fields.forEach((field) => {
    formData[field.key] = originalData[field.key]
  })
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

/* 左侧边栏 */
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

/* 个人信息 */
.personal-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0px 24px;
  margin-top: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 14px;
  margin-bottom: 6px;
  color: #333;
}

.form-group input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #42b983;
}

.form-group select {
  display: block;
  width: 100%;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
  color: #333;
  background-color: #fff;
  appearance: none;
}

.form-group select:focus {
  outline: none;
  border-color: #42b983;
}

.form-group input[type='date'] {
  height: 36px;
}

.form-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.save-btn,
.cancel-btn {
  padding: 10px 20px;
  width: auto;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  text-align: center;
  transition: background 0.3s;
}

.save-btn {
  background-color: #42b983;
  color: white;
}

.save-btn:hover {
  background-color: #369c74;
}

.cancel-btn {
  background-color: #f0f0f0;
  color: #333;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}
</style>
