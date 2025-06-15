<template>
  <!-- 右侧辅助信息 -->
  <div class="side-section">
    <div class="seat-map" disabled>观演须知</div>
    <div class="hints">
      <div v-for="(hint, index) in hints" :key="index" class="hint-item">
        <div class="hint-header">
          <div class="hint-icon" :class="hint.type">
            <i v-if="hint.type === 'ok'" class="fas fa-check-circle"></i>
            <i v-else-if="hint.type === 'no'" class="fas fa-times-circle"></i>
          </div>
          <h4 class="hint-title">{{ hint.title }}</h4>
        </div>
        <p class="hint-text">{{ hint.text }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const hints = [
  {
    type: 'no',
    title: '条件退',
    text: '本项目支持有条件退款，若需要收取退票手续费，将以用户实际支付票款为基准收取。基于项目主办方提供的退票政策不同，具体可支持用户申请退款的情形请详见该项目详情页退票政策相关说明或公告。',
  },
  {
    type: 'ok',
    title: '实名制购票和入场',
    text: '本项目需实名制购票及入场，购票完成后观演人信息不可更改，须购票时填写的实名观演人携带本人有效证件验证入场。',
  },
  {
    type: 'no',
    title: '不支持选座',
    text: '本项目不支持自主选座，同一个订单优先连座。',
  },
  {
    type: 'ok',
    title: '电子票',
    text: '通过身份证验票入场。',
  },
  {
    type: 'ok',
    title: '电子发票',
    text: '本项目支持开具电子发票。需要在演出开始前在订单详情页提交发票申请，一般演出结束后1个月左右开具并发送至您的邮箱。',
  },
]
</script>
