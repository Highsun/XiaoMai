<template>
  <div class="subscription-container">
    <h2 class="msg-title">消息订阅与推送</h2>

    <div class="toggle-wrapper">
      <label class="switch">
        <input type="checkbox" v-model="isSubscribed" />
        <span class="slider"></span>
      </label>
      <span class="toggle-label">
        {{ isSubscribed ? '已开启，您将通过邮件接收我们的推送消息' : '已关闭' }}
      </span>
    </div>

    <transition name="fade-slide">
      <div v-if="isSubscribed" class="checkbox-group">
        <p style="font-size: 15px; margin-bottom: 10px">请选择您想接收的消息内容：</p>
        <label class="checkbox-item">
          <input type="checkbox" v-model="subscriptions.websiteUpdate" />
          <span>网站更新</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" v-model="subscriptions.newOrInterestedEvents" />
          <span>新上架 / 已订阅的演出</span>
        </label>
        <label class="checkbox-item">
          <input type="checkbox" v-model="subscriptions.personalRelatedEvents" />
          <span>您的订单、支付凭证等</span>
        </label>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isSubscribed = ref(false)

const subscriptions = ref({
  websiteUpdate: false,
  newOrInterestedEvents: false,
  personalRelatedEvents: false,
})
</script>

<style scoped>
.subscription-container {
  width: 100%;
  margin: 0 auto;
  margin-bottom: 12px;
  background-color: #fff;
}

.msg-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: left;
}

.toggle-wrapper {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 28px;
  margin-right: 12px;
  margin-bottom: 0;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 34px;
}

.slider::before {
  position: absolute;
  content: '';
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #42b983;
}

input:checked + .slider::before {
  transform: translateX(22px);
}

.toggle-label {
  font-size: 15px;
  color: #333;
  line-height: 28px;
  display: inline-block;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  padding: 0 12px;
  gap: 10px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 14px;
  white-space: nowrap;
}

.checkbox-item input {
  width: 14px;
  height: 14px;
  cursor: pointer;
}

.checkbox-item span {
  font-weight: lighter;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
