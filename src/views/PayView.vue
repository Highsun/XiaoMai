<template>
  <div class="pay-container">
    <div class="pay-card">
      <!-- 倒计时提示 -->
      <div class="pay-header">
        <span>
          请在 <span class="countdown">{{ countdownText }}</span> 内完成支付，否则订单将取消
        </span>
      </div>

      <!-- 订单信息 -->
      <div class="pay-order-info">
        <div>票务：{{ orderInfo.ticketName }}</div>
        <div>订单号：{{ serverOrderId ?? '——' }}</div>
        <div>
          支付金额：<span class="pay-amount">￥{{ orderInfo.amount }}</span>
        </div>
      </div>

      <!-- 支付方式 -->
      <div class="pay-method-title">选择支付平台</div>
      <div class="pay-methods">
        <div
          :class="['pay-method', { active: payMethod === 'alipay' }]"
          @click="payMethod = 'alipay'"
        >
          <img src="@/assets/images/pay/alipay.png" alt="支付宝" />
          <span>支付宝</span>
        </div>
        <div
          :class="['pay-method', { active: payMethod === 'wechat' }]"
          @click="payMethod = 'wechat'"
        >
          <img src="@/assets/images/pay/wechat.png" alt="微信" />
          <span>微信</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="pay-options">
        <button
          class="pay-back-btn"
          @click="cancelPayment"
          :disabled="processing"
        >
          返回首页
        </button>
        <button
          class="pay-btn"
          :disabled="countdown === 0 || processing || !serverOrderId"
          @click="handlePay"
        >
          <template v-if="processing">处理中...</template>
          <template v-else>下一步</template>
        </button>
      </div>

      <!-- 超时提示 -->
      <div v-if="countdown === 0" class="pay-expired-tip">
        订单已超时，请返回重新下单。
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const router        = useRouter()
const route         = useRoute()

// 从 URL query 拿到参数，并做类型转换
const orderInfo = {
  showId:     Number(route.query.show_id || 0),
  ticketName: route.query.ticketName || '小麦演唱会门票',
  session:    route.query.session    || '',
  quantity:   Number(route.query.quantity || 1),
  amount:     Number(route.query.total || 0),
}

// 后台返回的真实订单 ID
const serverOrderId = ref(null)

const payMethod  = ref('alipay')
const countdown  = ref(10 * 60)
const processing = ref(false)

const countdownText = computed(() => {
  const m = String(Math.floor(countdown.value / 60)).padStart(2, '0')
  const s = String(countdown.value % 60).padStart(2, '0')
  return `${m}分${s}秒`
})

let timer = null

onMounted(async () => {
  // 启动倒计时
  timer = setInterval(() => {
    if (countdown.value > 0) countdown.value--
    else clearInterval(timer)
  }, 1000)

  // 在后端创建订单，获取真正的 ID
  try {
    const res = await axios.post(
      '/api/payments/create',
      {
        show_id:  orderInfo.showId,
        amount:   orderInfo.amount,
        quantity: orderInfo.quantity,
        session:  orderInfo.session
      },
      {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token')
        }
      }
    )
    if (res.data.code === 0) {
      serverOrderId.value = res.data.order_id
    } else {
      console.error('创建订单返回错误', res.data)
    }
  } catch (err) {
    console.error('创建订单失败', err)
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

async function handlePay() {
  if (countdown.value === 0 || processing.value || !serverOrderId.value) return
  processing.value = true

  try {
    await axios.post(
      '/api/payments/complete',
      {
        order_id: serverOrderId.value,
        items: [
          {
            show_id:    orderInfo.showId,
            quantity:   orderInfo.quantity,
            unit_price: orderInfo.amount
          }
        ]
      },
      {
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token')
        }
      }
    )
    router.push({ path: '/dashboard', query: { view: 'tickets' } })
  } catch (err) {
    alert('支付失败，请重试')
    console.error('完成支付失败', err)
    processing.value = false
  }
}

async function cancelPayment() {
  if (!processing.value && serverOrderId.value) {
    try {
      await axios.post(
        '/api/payments/cancel',
        { order_id: serverOrderId.value },
        {
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token')
          }
        }
      )
    } catch (err) {
      console.error('取消订单失败', err)
    }
  }
  router.push('/')
}
</script>

<style scoped>
/* —— 以下样式保持不动 —— */
.pay-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f9fbfa;
  padding-top: 0;
}
.pay-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px rgba(80, 180, 120, 0.11);
  width: 500px;
  max-width: 96vw;
  padding: 34px 36px 32px 36px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.pay-header {
  background: #f8f7e8;
  color: #b98113;
  border-radius: 8px;
  padding: 12px 18px;
  font-size: 16px;
  margin-bottom: 10px;
}
.countdown {
  color: #fc5e19;
  font-weight: bold;
}
.pay-order-info {
  color: #444;
  font-size: 15px;
  line-height: 2;
}
.pay-amount {
  color: #34be69;
  font-size: 20px;
  font-weight: bold;
  margin-left: 4px;
}
.pay-method-title {
  font-weight: 600;
  margin: 8px 0 0 0;
  font-size: 15px;
  color: #333;
}
.pay-methods {
  display: flex;
  gap: 30px;
  margin-top: 4px;
}
.pay-method {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 14px 28px 10px 28px;
  background: #f3f5f7;
  border-radius: 12px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border 0.15s;
}
.pay-method img {
  width: 80px;
  height: 36px;
}
.pay-method span {
  font-size: 14px;
}
.pay-method.active {
  border: 2px solid #37ba77;
  background: #eafcf3;
}
.pay-options {
  display: flex;
  gap: 16px;
  margin-top: 10px;
}
.pay-btn {
  flex: 1;
  background: #37ba77;
  color: #fff;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  font-weight: 500;
  padding: 10px 0;
  transition: background 0.15s;
  cursor: pointer;
  width: 100%;
}
.pay-btn:hover {
  background: #2e8461;
}
.pay-expired-tip {
  color: #fd5353;
  text-align: center;
  margin-top: 12px;
  font-size: 15px;
  font-weight: 600;
}
.pay-back-btn {
  flex: 1;
  background: #f3f5f7;
  color: #37ba77;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  font-weight: 500;
  padding: 9px 0;
  cursor: pointer;
  width: 100%;
  transition:
    background 0.15s,
    color 0.15s;
}
.pay-back-btn:hover {
  background: #eafcf3;
  color: #238a57;
}
</style>
