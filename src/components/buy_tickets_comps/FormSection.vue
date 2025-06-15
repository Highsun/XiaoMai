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

    <!-- 登录提示文字 -->
    <div class="fav-feedback">
      <span v-if="showLoginPrompt" class="fav-msg login">请先登录</span>
    </div>

    <!-- 登录提示弹窗 -->
    <transition name="fade">
      <div v-if="showLoginPrompt" class="login-overlay">
        <div class="login-box">
          <p>请先登录后再进行此操作</p>
          <div class="login-actions">
            <button class="btn primary" @click="goLogin">去登录</button>
            <button class="btn cancel" @click="showLoginPrompt = false">取消</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const props = defineProps({ concert: { type: Object, required: true } })
const router = useRouter()

// — 上半部分：原有购票逻辑 —
const title = computed(() => props.concert.title)
const presaleNote = '⚠️ 本商品为预售，正式开票后将第一时间配票'
const presaleText =
  '预售期间，由于主办未正式开票，下单后无法立即为您配票。一般于演出前1-2周开票，待正式开票后，请您通过订单详情页或者票夹详情，查看票品信息、取票方式等演出相关信息。'
const currentCityData = computed(() => ({
  date:
    props.concert.start_date +
    (props.concert.end_date ? '-' + props.concert.end_date : ''),
  venue: props.concert.location,
  mapUrl: props.concert.map_url,
  startTime: props.concert.start_date + 'T00:00:00',
  priceTiers: props.concert.price_tiers || []
}))

const sessions = computed(() => props.concert.sessions || [])
const selectedSession = ref(null)
watch(
  sessions,
  v => { if (v.length && !selectedSession.value) selectedSession.value = v[0] },
  { immediate: true }
)

const selectedTier = ref(null)
watch(
  () => currentCityData.value.priceTiers,
  v => { if (v.length && !selectedTier.value) selectedTier.value = v[0] },
  { immediate: true }
)

const quantity = ref(1)
const maxQuantity = 4
function increaseQty() { if (quantity.value < maxQuantity) quantity.value++ }
function decreaseQty() { if (quantity.value > 1) quantity.value-- }

const totalPrice = computed(() =>
  (selectedTier.value?.price || 0) * quantity.value
)

const showMap = ref(false)
function toggleMap() { showMap.value = !showMap.value }

const countdownText = ref('')
const canBuy = ref(false)
let timer = null
function pad(n) { return n.toString().padStart(2, '0') }
function updateCountdown() {
  const start = new Date(currentCityData.value.startTime).getTime()
  const diff = start - Date.now()
  if (diff <= 0) {
    countdownText.value = '00天 00:00:00'
    canBuy.value = true
    clearInterval(timer)
    return
  }
  const s = Math.floor(diff / 1000)
  const d = Math.floor(s / 86400)
  const h = Math.floor((s % 86400) / 3600)
  const m = Math.floor((s % 3600) / 60)
  const ss = s % 60
  countdownText.value = `${pad(d)}天 ${pad(h)}:${pad(m)}:${pad(ss)}`
  canBuy.value = false
}
function restartCountdown() {
  clearInterval(timer)
  updateCountdown()
  timer = setInterval(updateCountdown, 1000)
}
onMounted(() => restartCountdown())
onUnmounted(() => clearInterval(timer))

function handleBuy() {
  if (!canBuy.value) return
  if (!localStorage.getItem('access_token')) {
    showLoginPrompt.value = true
    return
  }
  router.push({
    name: 'Pay',
    query: {
      show_id: String(props.concert.id),
      ticketName: title.value,
      session: selectedSession.value,
      price: selectedTier.value.price,
      label: selectedTier.value.label,
      quantity: quantity.value,
      total: totalPrice.value
    }
  })
}

// — 下半部分：收藏夹逻辑 & 登录提示 —
const favPending       = ref(false)
const hasFav           = ref(false)
const showLoginPrompt  = ref(false)

function goLogin() {
  showLoginPrompt.value = false
  router.push({ name: 'Login' })
}

async function checkIfFav() {
  favPending.value = true
  try {
    const res = await axios.get('/api/favorites/is_fav', {
      params: { show_id: props.concert.id },
      headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') }
    })
    hasFav.value = res.data.code === 0 && res.data.data.is_fav
  } catch {
    // 未登录时不报错
  }
  favPending.value = false
}

async function addToFavorites() {
  favPending.value = true
  try {
    await axios.post('/api/favorites/add',
      { show_id: props.concert.id },
      { headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') } }
    )
    hasFav.value = true
  } catch {}
  favPending.value = false
}

async function removeFromFavorites() {
  favPending.value = true
  try {
    await axios.post('/api/favorites/remove',
      { show_id: props.concert.id },
      { headers: { Authorization: 'Bearer ' + localStorage.getItem('access_token') } }
    )
    hasFav.value = false
  } catch {}
  favPending.value = false
}

function handleFavoriteClick() {
  if (!localStorage.getItem('access_token')) {
    showLoginPrompt.value = true
    return
  }
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
.favorite-btn,
.buy-button {
  width: 140px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}
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

/* 登录提示文字 */
.fav-feedback {
  margin-top: 8px;
  min-height: 18px;
}
.fav-msg.login {
  font-size: 0.85rem;
  color: #e67e22;
}

/* 登录弹窗覆盖层 */
.login-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.login-box {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  text-align: center;
  min-width: 260px;
}
.login-box p {
  margin-bottom: 16px;
  font-size: 1rem;
  color: #333;
}
.login-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 8px;
}
.login-actions .btn {
  flex: 1;
  padding: 8px 0;
  border-radius: 6px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.login-actions .btn.primary {
  background: #26ad62;
  color: #fff;
  border: 1px solid #26ad62;
}
.login-actions .btn.primary:hover {
  background: #1f9855;
}
.login-actions .btn.cancel {
  background: #fff;
  color: #333;
  border: 1px solid #ccc;
}
.login-actions .btn.cancel:hover {
  background: #f0f0f0;
}

/* 渐入动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
