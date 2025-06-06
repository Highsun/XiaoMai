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
                  <!-- 省份与城市 -->
                  <div
                    v-else-if="field.key === 'location'"
                    class="location-select-row"
                    style="display: flex; gap: 12px"
                  >
                    <!-- 省 -->
                    <select
                      v-model="selectedProvince"
                      @change="onProvinceChange"
                      id="province-select"
                    >
                      <option disabled value="">请选择省份</option>
                      <option v-for="province in provinces" :key="province" :value="province">
                        {{ province }}
                      </option>
                    </select>

                    <!-- 市 -->
                    <select
                      v-model="selectedCity"
                      @change="onCityChange"
                      :disabled="!selectedProvince"
                      id="city-select"
                    >
                      <option disabled value="">请选择城市</option>
                      <option v-for="city in cities" :key="city" :value="city">
                        {{ city }}
                      </option>
                    </select>

                    <!-- 区/县 -->
                    <select
                      v-model="selectedDistrict"
                      @change="onDistrictChange"
                      :disabled="!selectedCity"
                      id="district-select"
                    >
                      <option disabled value="">请选择区/县</option>
                      <option v-for="district in districts" :key="district" :value="district">
                        {{ district }}
                      </option>
                    </select>
                  </div>

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
            <!-- FIXME: CSS样式还要大改 -->
            <div v-else-if="view === 'tickets'" class="ticket-section">
              <h2 class="ticket-heading">亲爱的 {{ username }}，</h2>
              <h4 style="grid-column: 1 / -1; margin: 32px 0 16px 0">以下是您已订购的演出</h4>
              <!-- 分类切换按钮 -->
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
              <!-- 演出列表 -->
              <div v-for="ticket in filteredTickets" :key="ticket.id" class="ticket-item">
                <!-- 左侧头像+歌手名 -->
                <div class="ticket-left">
                  <img :src="ticket.avatar" alt="avatar" class="ticket-avatar" />
                  <span class="ticket-artist">{{ ticket.artist }}</span>
                </div>
                <!-- 中间票务信息部分 -->
                <div class="ticket-center">
                  <div><i class="fa-solid fa-calendar-days"></i> {{ ticket.time }}</div>
                  <div><i class="fa-solid fa-location-dot"></i> {{ ticket.venue }}</div>
                  <div><i class="fa-solid fa-chair"></i> {{ ticket.seat }}</div>
                  <div><i class="fa-solid fa-tag"></i> ￥{{ ticket.price }}</div>
                </div>
                <!-- 右侧“更多”按钮 -->
                <div class="ticket-dropdown-container">
                  <button class="ticket-details-button"><i class="fas fa-ellipsis-v"></i></button>
                  <!-- TODO: 跳转到票务核销二维码界面，提供核销码下载服务 -->
                </div>
              </div>
            </div>
            <div v-else-if="view === 'orders'">
              <h2>亲爱的 {{ username }}，</h2>
              <!-- TODO: 订单状态：全部、待付款、待收货、待评价、已过期 -->
            </div>
            <div v-else-if="view === 'settings'">
              <h2>亲爱的 {{ username }}，</h2>
              <!-- TODO: 观演人管理，订阅管理，修改邮箱、密码，注销账号 -->
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
import { ref, reactive, computed, onMounted } from 'vue'
import locationData from '../assets/data/location-L3.json'

const view = ref('account')
const welcome = ref('亲爱的')
const username = ref('小麦用户_89757')
const marker = ref('，')

// 登出
function logout() {
  view.value = 'account'
  welcome.value = '这里空空如也呢，先登录吧'
  username.value = ''
  marker.value = '！'
  alert('已退出登录')
}

// 我的账号
const fields = [
  { key: 'name', label: '姓名' },
  { key: 'gender', label: '性别' },
  { key: 'birthday', label: '出生日期' },
  { key: 'phone', label: '手机号' },
  { key: 'location', label: '省份与城市' },
  { key: 'address', label: '详细地址' },
]

// 表单初始值 TODO: 接入后端数据
const formData = reactive({
  name: '',
  gender: '保密',
  birthday: '',
  location: '',
})

// 保存原始数据（用于取消）
const originalData = {
  name: formData.name,
  gender: formData.gender,
  birthday: formData.birthday,
  location: formData.location,
}

// 地区数据
const provinces = Object.keys(locationData)

const selectedProvince = ref('')
const selectedCity = ref('')
const selectedDistrict = ref('')

// 地区列表
const cities = computed(() => {
  return selectedProvince.value ? Object.keys(locationData[selectedProvince.value]) : []
})

const districts = computed(() => {
  if (selectedProvince.value && selectedCity.value) {
    return locationData[selectedProvince.value][selectedCity.value] || []
  }
  return []
})

// 初始化省市区
onMounted(() => {
  initLocationFromString(formData.location)
})

// 监听地区变化
function onProvinceChange() {
  selectedCity.value = ''
  selectedDistrict.value = ''
  updateLocation()
}

function onCityChange() {
  selectedDistrict.value = ''
  updateLocation()
}

function onDistrictChange() {
  updateLocation()
}

// 更新 location 字符串
function updateLocation() {
  formData.location = [selectedProvince.value, selectedCity.value, selectedDistrict.value]
    .filter(Boolean)
    .join(' / ')
}

// 根据字符串回显省市区
function initLocationFromString(str) {
  const parts = str.split(' / ')
  selectedProvince.value = parts[0] || ''
  selectedCity.value = parts[1] || ''
  selectedDistrict.value = parts[2] || ''
}

// 日期限制（最大值设为今天）
const today = new Date().toISOString().split('T')[0]

// 保存修改
function saveChanges() {
  updateLocation()
  fields.forEach((field) => {
    originalData[field.key] = formData[field.key]
  })
  alert('保存成功')
}

// 取消修改，回滚数据
function cancelChanges() {
  fields.forEach((field) => {
    formData[field.key] = originalData[field.key]
  })
  initLocationFromString(formData.location)
}

// 我的票夹
const tabs = ['未使用', '已使用', '已过期']
const activeTab = ref('未使用')

// TODO: 接入后端数据
const tickets = ref([
  {
    id: 'T123',
    artist: '周杰伦',
    avatar: 'src/assets/images/homepage/artists/Jay.JPG',
    time: '2025-07-20 19:30',
    venue: '广州体育馆',
    seat: 'A区 3排 12号',
    price: 1100,
    status: '未使用',
    qr: '',
  },
  {
    id: 'T124',
    artist: '林俊杰',
    avatar: 'src/assets/images/homepage/artists/JJ.JPG',
    time: '2025-05-10 19:00',
    venue: '深圳大剧院',
    seat: 'B区 1排 8号',
    price: 1880,
    status: '未使用',
    qr: '',
  },
  {
    id: 'T125',
    artist: '陶喆',
    avatar: 'src/assets/images/homepage/artists/DT.JPG',
    time: '2025-04-01 18:00',
    venue: '北京工体',
    seat: 'C区 2排 5号',
    price: 780,
    status: '已使用',
    qr: '',
  },
  {
    id: 'T126',
    artist: '五月天',
    avatar: 'src/assets/images/homepage/artists/WYT.JPG',
    time: '2025-03-23 20:00',
    venue: '天津之眼',
    seat: 'D区 6排 19号',
    price: 580,
    status: '已过期',
    qr: '',
  },
])

const filteredTickets = computed(() =>
  tickets.value.filter((ticket) => ticket.status === activeTab.value),
)
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

/* 我的账号 */
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

.location-select-row select {
  flex: 1;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
  color: #333;
  background-color: #fff;
  appearance: none;
}

.location-select-row select:disabled {
  color: #aaa;
  background-color: #f9f9f9;
  cursor: not-allowed;
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

/* 我的票夹 */
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
  font-size: 1.5rem;
  cursor: pointer;
}
</style>
