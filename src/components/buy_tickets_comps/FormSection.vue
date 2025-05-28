<template>
  <div class="main-section">
    <h2 class="title">{{ title }}</h2>
    <p class="info">{{ currentCityData.date }}</p>
    <div class="venue-row">
      <span class="venue-text">{{ currentCityData.venue }}</span>
      <button class="map-btn" @click="toggleMap">
        <i class="fas fa-map-marker-alt"></i><span style="font-size: 1rem"> 在地图上查看</span>
      </button>
    </div>
    <transition name="map-fade">
      <div v-if="showMap" class="map-overlay">
        <div class="map-popup">
          <iframe :src="currentCityData.mapUrl" frameborder="0"></iframe>
        </div>
        <button class="close-icon" @click="toggleMap">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </transition>

    <div class="presale">
      {{ presaleNote }}
      <p>{{ presaleText }}</p>
    </div>

    <div class="options">
      <!-- 城市 -->
      <div class="option-group">
        <label>城市</label>
        <div class="radio-list">
          <label
            v-for="city in cities"
            :key="city"
            class="radio-button"
            :class="{ active: selectedCity === city }"
          >
            <input type="radio" v-model="selectedCity" :value="city" />
            {{ city }}
          </label>
        </div>
      </div>

      <!-- 场次 -->
      <div class="option-group">
        <label>场次</label>
        <div class="radio-list">
          <label
            v-for="session in currentCityData.sessions"
            :key="session"
            class="radio-button"
            :class="{ active: selectedSession === session }"
          >
            <input type="radio" v-model="selectedSession" :value="session" />
            {{ session }}
          </label>
        </div>
      </div>

      <!-- 票档 -->
      <div class="option-group">
        <label>票档</label>
        <div class="radio-list">
          <label
            v-for="tier in currentCityData.priceTiers"
            :key="tier.label + tier.price"
            class="radio-button"
            :class="{
              active: selectedTier.label === tier.label && selectedTier.price === tier.price,
            }"
          >
            <input type="radio" v-model="selectedTier" :value="tier" />
            {{ tier.label }}（{{ tier.price }}元）
          </label>
        </div>
      </div>

      <!-- 数量 -->
      <div class="option-group">
        <label>数量</label>
        <div class="quantity">
          <button @click="decreaseQty"><i class="fa-solid fa-minus"></i></button>
          <span>{{ quantity }} 张</span>
          <button @click="increaseQty"><i class="fa-solid fa-plus"></i></button>
          <small>每笔订单限购 {{ maxQuantity }} 张</small>
        </div>
      </div>
    </div>

    <div class="total">
      合计：<strong>{{ totalPrice }} 元</strong>
    </div>

    <div class="purchase-row">
      <p class="countdown-text">距开抢还有：{{ countdownText }}</p>
      <button class="buy-button" :disabled="!canBuy" @click="handleBuy">立即购买</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

// 全局数据
const title = 'JJ林俊杰 JJ20 FINAL LAP 世界巡回演唱会'
const presaleNote = '⚠️ 本商品为预售，正式开票后将第一时间配票'
const presaleText =
  '预售期间，由于主办未正式开票，下单后无法立即为您配票。一般于演出前1-2周开票，待正式开票后，请您通过订单详情页或者票夹详情，查看票品信息、取票方式等演出相关信息。'

// 城市数据
const cityData = {
  北京: {
    date: '2025.06.28-07.13',
    venue: '北京市·国家体育场-鸟巢',
    mapUrl: '',
    startTime: '2025-05-28T20:00:00',
    sessions: [
      '06.27 19:00',
      '06.28 19:00',
      '06.29 19:00',
      '07.04 19:00',
      '07.05 19:00',
      '07.06 19:00',
      '07.11 19:00',
      '07.12 19:00',
      '07.13 19:00',
    ],
    priceTiers: [
      { label: '看台', price: 380 },
      { label: '看台', price: 680 },
      { label: '看台', price: 980 },
      { label: '内场', price: 1380 },
      { label: '内场', price: 1580 },
      { label: '内场', price: 1880 },
    ],
  },
  韩国仁川: {
    date: '2025.06.14-06.15',
    venue: '韩国仁川·INSPIRE ARENA 迎仕柏综艺馆',
    mapUrl: '',
    startTime: '2025-04-22T11:00:00',
    sessions: ['06.14 19:00', '06.15 19:00'],
    priceTiers: [
      { label: '坐席', price: 590 },
      { label: '坐席', price: 990 },
      { label: '坐席', price: 1390 },
      { label: '坐席', price: 1690 },
      { label: '坐席', price: 2290 },
    ],
  },
}

const cities = Object.keys(cityData)
const selectedCity = ref(cities[0])

const currentCityData = computed(() => cityData[selectedCity.value])
const selectedSession = ref(currentCityData.value.sessions[0])
const selectedTier = ref(currentCityData.value.priceTiers[0])

// 切换城市时更新默认选项
watch(selectedCity, (newCity) => {
  selectedSession.value = cityData[newCity].sessions[0]
  selectedTier.value = cityData[newCity].priceTiers[0]
  restartCountdown()
})

// 数量与票价
const quantity = ref(1)
const maxQuantity = 4
function increaseQty() {
  if (quantity.value < maxQuantity) quantity.value++
}
function decreaseQty() {
  if (quantity.value > 1) quantity.value--
}
const totalPrice = computed(() => selectedTier.value.price * quantity.value)

// 地图弹窗
const showMap = ref(false)
function toggleMap() {
  showMap.value = !showMap.value
}

// 倒计时逻辑
const countdownText = ref('')
const canBuy = ref(false)
let timer = null

function pad(num) {
  return num.toString().padStart(2, '0')
}

function updateCountdown() {
  const start = new Date(currentCityData.value.startTime).getTime()
  const now = Date.now()
  const diff = start - now

  if (diff <= 0) {
    countdownText.value = '00天 00:00:00'
    canBuy.value = true
    clearInterval(timer)
    return
  }

  const totalSeconds = Math.floor(diff / 1000)
  const days = Math.floor(totalSeconds / 86400)
  const hours = Math.floor((totalSeconds % 86400) / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = totalSeconds % 60
  countdownText.value = `${pad(days)}天 ${pad(hours)}:${pad(minutes)}:${pad(seconds)}`
  canBuy.value = false
}

function restartCountdown() {
  if (timer) clearInterval(timer)
  updateCountdown()
  timer = setInterval(updateCountdown, 1000)
}

function handleBuy() {
  if (!canBuy.value) return
  alert('当前排队人数较多，请重试！')
}

onMounted(() => {
  restartCountdown()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>
