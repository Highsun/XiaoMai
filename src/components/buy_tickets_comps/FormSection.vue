<template>
  <div class="main-section">
    <!-- 演出标题 & 日期 -->
    <h2 class="title">{{ title }}</h2>
    <p class="info">{{ currentCityData.date }}</p>

    <!-- 场馆 & 地图弹窗 -->
    <div class="venue-row">
      <span class="venue-text">{{ currentCityData.venue }}</span>
      <button class="map-btn" @click="toggleMap">
        <i class="fas fa-map-marker-alt" style="font-size: 16px"></i>
        <span style="font-size: 16px"> 在地图上查看</span>
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

    <!-- 预售信息 -->
    <div class="presale">
      {{ presaleNote }}
      <p>{{ presaleText }}</p>
    </div>

    <!-- 场次／票档／数量 选项 -->
    <div class="options">
      <div class="option-group">
        <label>场次</label>
        <div class="radio-list">
          <label
            v-for="session in sessions"
            :key="session"
            class="radio-button"
            :class="{ active: selectedSession === session }"
          >
            <input type="radio" v-model="selectedSession" :value="session" />
            {{ session }}
          </label>
        </div>
      </div>

      <div class="option-group">
        <label>票档</label>
        <div class="radio-list">
          <label
            v-for="tier in currentCityData.priceTiers"
            :key="tier.label + tier.price"
            class="radio-button"
            :class="{
              active:
                selectedTier.label === tier.label &&
                selectedTier.price === tier.price
            }"
          >
            <input type="radio" v-model="selectedTier" :value="tier" />
            {{ tier.label }}（{{ tier.price }}元）
          </label>
        </div>
      </div>

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

    <!-- 总价 -->
    <div class="total">
      合计：<strong>{{ totalPrice }} 元</strong>
    </div>

    <!-- 倒计时 + 按钮组 -->
    <div class="purchase-row">
      <p class="countdown-text">距开抢还有：{{ countdownText }}</p>
      <div class="button-group">
        <button
          class="favorite-btn"
          @click="handleFavoriteClick"
          :disabled="favPending"
        >
          <template v-if="favPending">处理中...</template>
          <template v-else-if="hasFav">取消收藏</template>
          <template v-else>加入收藏夹</template>
        </button>
        <button class="buy-button" :disabled="!canBuy" @click="handleBuy">
          立即购买
        </button>
      </div>
    </div>
    <div class="fav-feedback">
      <span v-if="favError" class="fav-msg error">{{ favError }}</span>
      <span v-else-if="favSuccess" class="fav-msg success">收藏成功</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

// Props：从父组件传入的演出对象
const props = defineProps({
  concert: { type: Object, required: true }
})
const router = useRouter()

// —————————————————————————————————
// 购票页原有逻辑（标题、倒计时、选项等）
// —————————————————————————————————

// 标题
const title = computed(() => props.concert.title)

// 预售信息
const presaleNote = '⚠️ 本商品为预售，正式开票后将第一时间配票'
const presaleText =
  '预售期间，由于主办未正式开票，下单后无法立即为您配票。一般于演出前1-2周开票，待正式开票后，请您通过订单详情页或者票夹详情，查看票品信息、取票方式等演出相关信息。'

// 当前城市数据封装
const currentCityData = computed(() => ({
  date:
    props.concert.start_date +
    (props.concert.end_date ? '-' + props.concert.end_date : ''),
  venue: props.concert.location,
  mapUrl: props.concert.map_url,
  startTime: props.concert.start_date + 'T00:00:00',
  priceTiers: props.concert.price_tiers || []
}))

// 场次列表
const sessions = computed(() => props.concert.sessions || [])
const selectedSession = ref(null)
watch(
  sessions,
  v => { if (v.length && !selectedSession.value) selectedSession.value = v[0] },
  { immediate: true }
)

// 票档列表
const selectedTier = ref(null)
watch(
  () => currentCityData.value.priceTiers,
  v => { if (v.length && !selectedTier.value) selectedTier.value = v[0] },
  { immediate: true }
)

// 数量
const quantity = ref(1)
const maxQuantity = 4
function increaseQty() { if (quantity.value < maxQuantity) quantity.value++ }
function decreaseQty() { if (quantity.value > 1) quantity.value-- }

// 计算总价
const totalPrice = computed(() =>
  (selectedTier.value?.price || 0) * quantity.value
)

// 地图弹窗
const showMap = ref(false)
function toggleMap() { showMap.value = !showMap.value }

// 倒计时 / 是否可购
const countdownText = ref('')
const canBuy = ref(false)
let timer = null
function pad(n) { return n.toString().padStart(2, '0') }
function updateCountdown() {
  const start = new Date(currentCityData.value.startTime).getTime()
  const diff  = start - Date.now()
  if (diff <= 0) {
    countdownText.value = '00天 00:00:00'
    canBuy.value = true
    clearInterval(timer)
    return
  }
  const s  = Math.floor(diff / 1000)
  const d  = Math.floor(s / 86400)
  const h  = Math.floor((s % 86400) / 3600)
  const m  = Math.floor((s % 3600) / 60)
  const ss = s % 60
  countdownText.value = `${pad(d)}天 ${pad(h)}:${pad(m)}:${pad(ss)}`
  canBuy.value = false
}
function restartCountdown() {
  clearInterval(timer)
  updateCountdown()
  timer = setInterval(updateCountdown, 1000)
}

// 立即购买
function handleBuy() {
  if (!canBuy.value) return
  router.push({
    name: 'Pay',
    query: {
      ticketName: title.value,
      session: selectedSession.value,
      price: selectedTier.value.price,
      label: selectedTier.value.label,
      quantity: quantity.value,
      total: totalPrice.value
    }
  })
}

onMounted(() => restartCountdown())
onUnmounted(() => clearInterval(timer))

// —————————————————————————————————
// 收藏夹逻辑
// —————————————————————————————————

const favPending = ref(false)
const favError   = ref('')
const favSuccess = ref(false)
const hasFav     = ref(false)

// 查询收藏状态
async function checkIfFav() {
  favPending.value = true
  favError.value   = ''
  try {
    const res = await axios.get('/api/favorites/is_fav', {
      params: { show_id: props.concert.id },
      headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
    })
    hasFav.value = res.data.code === 0 && res.data.data.is_fav
  } catch {
    favError.value = '无法获取收藏状态'
  }
  favPending.value = false
}

// 添加收藏
async function addToFavorites() {
  favError.value   = ''
  favSuccess.value = false
  favPending.value = true
  try {
    const res = await axios.post(
      '/api/favorites/add',
      { show_id: props.concert.id },
      { headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') } }
    )
    if (res.data.code === 0) {
      hasFav.value    = true
      favSuccess.value = true
    } else {
      favError.value  = res.data.msg || '收藏失败'
    }
  } catch {
    favError.value = '收藏失败，请稍后重试'
  }
  favPending.value = false
}

// 取消收藏
async function removeFromFavorites() {
  favError.value   = ''
  favSuccess.value = false
  favPending.value = true
  try {
    const res = await axios.post(
      '/api/favorites/remove',
      { show_id: props.concert.id },
      { headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') } }
    )
    if (res.data.code === 0) {
      hasFav.value     = false
      favSuccess.value = true
    } else {
      favError.value   = res.data.msg || '取消失败'
    }
  } catch {
    favError.value = '取消失败，请稍后重试'
  }
  favPending.value = false
}

// 切换收藏/取消
function handleFavoriteClick() {
  if (favPending.value) return
  hasFav.value ? removeFromFavorites() : addToFavorites()
}

onMounted(() => checkIfFav())
</script>

<style scoped>
.purchase-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
}

.countdown-text {
  font-size: 0.95rem;
  color: #555;
}

.button-group {
  display: flex;
  gap: 8px;
}

/* 收藏 & 购买 按钮通用 */
.favorite-btn,
.buy-button {
  width: 140px;
  height: 40px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 收藏按钮 */
.favorite-btn {
  background: #fff;
  color: #26ad62;
  border: 1px solid #26ad62;
}
.favorite-btn:hover:not(:disabled) {
  background: #f4fcef;
  transform: translateY(-1px);
}
.favorite-btn:disabled {
  background: #f7f7f7;
  border-color: #bbb;
  color: #bbb;
}

/* 购买按钮 */
.buy-button {
  background: #26ad62;
  color: #fff;
  border: none;
}
.buy-button:disabled {
  background: #ccc;
}
.buy-button:not(:disabled):hover {
  background: #1f9855;
  transform: translateY(-1px);
}

/* 反馈提示 */
.fav-feedback {
  margin-top: 8px;
  min-height: 18px;
}
.fav-msg {
  font-size: 0.85rem;
}
.fav-msg.error {
  color: #e74c3c;
}
.fav-msg.success {
  color: #27ae60;
}
</style>
