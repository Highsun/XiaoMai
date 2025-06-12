<template>
  <div class="faq-container">
    <h2 class="faq-title">常见问题 Q&A</h2>

    <div v-for="(item, index) in faqs" :key="index" class="faq-item">
      <div class="faq-question" @click="toggle(index)">
        <span>{{ item.question }}</span>
        <i :class="['fas', expanded[index] ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
      </div>

      <div :class="['faq-answer', { expanded: expanded[index] }]">
        <div class="answer-content">
          {{ item.answer }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const faqs = ref([
  {
    question: '我如何修改账户的密码？',
    answer: '您可以在“账号设置 -> 修改密码”中修改您的登录密码。',
  },
  {
    question: '我在哪里查看购票记录？',
    answer: '请前往“历史订单”页面查看历史购票记录，有的效门票将会被收录在“我的票夹”中。',
  },
  {
    question: '我何时能够收到退款？',
    answer: '申请退票成功后，退款会在3-5个工作日内原路退回。如有疑问请联系客服。',
  },
])

const expanded = ref(faqs.value.map(() => false))

function toggle(index) {
  expanded.value[index] = !expanded.value[index]
}
</script>

<style scoped>
.faq-container {
  margin-bottom: 20px;
}

.faq-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: left;
}

.faq-item {
  border-bottom: 1px solid #eee;
  padding: 12px 0;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
}

.faq-question i {
  font-size: 14px;
  transition:
    color 0.3s ease,
    transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.faq-question:hover i {
  color: #42b983;
}

.faq-answer {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  transition: all 0.4s ease;
}

.faq-answer.expanded {
  max-height: 200px;
  opacity: 1;
}

.answer-content {
  margin-top: 8px;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}
</style>
