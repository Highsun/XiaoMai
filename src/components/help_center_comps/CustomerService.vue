<template>
  <h2 class="customer-service-title">联系客服</h2>
  <div class="customer-service">
    <div class="service-box" @click="showModal('complaint')">
      <i class="fas fa-exclamation-circle icon"></i>
      <span>演出投诉</span>
    </div>
    <div class="service-box" @click="showModal('chat')">
      <i class="fas fa-comments icon"></i>
      <span>在线客服</span>
    </div>
    <div class="service-box" @click="showModal('phone')">
      <i class="fas fa-phone icon"></i>
      <span>电话咨询</span>
    </div>

    <!-- 演出投诉弹窗 -->
    <transition name="fade">
      <div v-if="activeModal === 'complaint'" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>提交投诉</h3>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>
          <div class="modal-body">
            <input type="text" placeholder="您的称呼" />
            <input type="email" placeholder="邮箱地址" />
            <textarea rows="6" placeholder="请输入投诉内容..."></textarea>
          </div>
          <div class="modal-footer">
            <button class="submit">发送</button>
            <button class="cancel" @click="closeModal">取消</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 在线客服弹窗 -->
    <transition name="fade">
      <div v-if="activeModal === 'chat'" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>在线客服</h3>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>
          <div class="modal-body chat-body">
            <div class="chat-message">您好，请问有什么可以帮您？</div>
            <!-- 用户聊天输入框 -->
            <input type="text" placeholder="请输入问题..." />
          </div>
        </div>
      </div>
    </transition>

    <!-- 电话咨询弹窗 -->
    <transition name="fade">
      <div v-if="activeModal === 'phone'" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>电话咨询</h3>
            <button class="close-btn" @click="closeModal"><i class="fas fa-times"></i></button>
          </div>
          <div class="modal-body">
            <p>客服服务时间：工作日 9:00 - 17:00</p>
            <p>客服电话：400-820-3820</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeModal = ref(null)

function showModal(type) {
  activeModal.value = type
}

function closeModal() {
  activeModal.value = null
}
</script>

<style scoped>
.customer-service-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 20px;
  text-align: left;
}

.customer-service {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.service-box {
  width: 120px;
  height: 120px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.service-box:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.service-box .icon {
  font-size: 28px;
  margin: 16px auto;
  color: #42b983;
}

.service-box span {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  position: relative;
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 360px;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
}

/* 圆形关闭按钮 */
.close-btn {
  all: unset;
  position: absolute;
  top: 6px;
  right: 6px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #ddd;
  color: #333;
  font-size: 12px;
  border: none;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s;
}

.close-btn i {
  transform: translateY(-1px);
}

.close-btn:hover {
  color: white;
  background-color: #f44336;
}

.modal-header {
  text-align: center;
  font-size: 14px;
  margin-bottom: 12px;
}

.modal-body input,
.modal-body select,
.modal-body textarea {
  width: 100%;
  margin: 10px 0;
  padding: 8px;
  font-size: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}

.submit {
  background-color: #42b983;
  color: white;
  font-size: 14px;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  width: auto;
  min-width: 0;
  display: inline-block;
  white-space: nowrap;
}

.cancel {
  background-color: #ddd;
  color: #333;
  font-size: 14px;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  width: auto;
  min-width: 0;
  display: inline-block;
  white-space: nowrap;
}

.chat-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-message {
  background: #f5f5f5;
  padding: 10px;
  border-radius: 6px;
  font-size: 12px;
}

.modal-body p {
  font-size: 14px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
