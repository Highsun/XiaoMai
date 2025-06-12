<template>
  <div class="pay-container">
    <div class="pay-card">
      <div class="pay-header">
        <span
          >请在 <span class="countdown">{{ countdownText }}</span> 内完成支付，否则订单将取消</span
        >
      </div>
      <div class="pay-order-info">
        <div>票务：{{ orderInfo.ticketName }}</div>
        <div>订单号：{{ orderInfo.orderId }}</div>
        <div>
          支付金额：<span class="pay-amount">￥{{ orderInfo.amount }}</span>
        </div>
      </div>
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
      <div class="pay-options">
        <button class="pay-back-btn" @click="router.push('/')">返回首页</button>
        <button class="pay-btn" :disabled="countdown === 0" @click="handlePay">下一步</button>
      </div>
      <div v-if="countdown === 0" class="pay-expired-tip">订单已超时，请返回重新下单。</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const orderInfo = ref({
  ticketName: route.query.ticketName || '小麦演唱会门票',
  city: route.query.city || '',
  session: route.query.session || '',
  price: route.query.price || 0,
  label: route.query.label || '',
  quantity: route.query.quantity || 1,
  amount: route.query.total || 0,
  orderId: Date.now().toString(),
})

const payMethod = ref('alipay')
const countdown = ref(5 * 60 + 0)

// 倒计时
const countdownText = computed(() => {
  const min = String(Math.floor(countdown.value / 60)).padStart(2, '0')
  const sec = String(countdown.value % 60).padStart(2, '0')
  return `${min}分${sec}秒`
})

let timer = null
onMounted(() => {
  timer = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value -= 1
    } else {
      clearInterval(timer)
    }
  }, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

// 支付逻辑
function handlePay() {
  if (countdown.value === 0) {
    alert('订单已超时，请重新下单')
    router.push('/category') // 返回首页
    return
  }
  // 模拟支付跳转成功
  alert(`支付成功！您选择了${payMethod.value === 'alipay' ? '支付宝' : '微信'}。`)
  // 这里可跳转到订单详情或订单成功页
  router.push('/dashboard')
}
</script>

<style scoped>
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
