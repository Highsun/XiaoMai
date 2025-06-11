<template>
  <div class="delete-account-container">
    <div>
      <button class="delete-btn" @click="showConfirm = true">注销账号</button>
    </div>

    <transition name="fade">
      <div v-if="showConfirm" class="confirm-overlay">
        <div class="confirm-box">
          <h3>确认注销？</h3>
          <p>
            注销后您将无法再登录此账号，您的所有数据将被清空（未使用的演出门票也将无法继续使用）。
          </p>
          <div class="btn-group">
            <button @click="confirmDelete" class="confirm">确认注销</button>
            <button @click="showConfirm = false" class="cancel">取消</button>
          </div>
        </div>
      </div>
    </transition>

    <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showConfirm = ref(false)
const successMessage = ref('')

function confirmDelete() {
  showConfirm.value = false
  // TODO: 在这里调用后端API进行账号注销
  setTimeout(() => {
    successMessage.value = '您的账号已成功注销，感谢您的使用，再会！'
    setTimeout(() => {
      window.location.href = '/login'
    }, 2000)
  }, 500)
}
</script>

<style scoped>
.delete-account-container {
  margin: 0 auto;
  margin-bottom: 12px;
}

.delete-btn {
  background: none;
  border: none;
  color: #e74c3c;
  font-size: 14px;
  padding: 0;
  cursor: pointer;
  border-radius: 0;
  text-align: left;
  width: auto;
  display: inline-block;
}

.delete-btn:hover {
  text-decoration: underline;
  color: #c0392b;
}

.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.confirm-box {
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
  max-width: 360px;
  text-align: center;
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.15);
}

.confirm-box h3 {
  font-size: 16px;
  margin-bottom: 10px;
}

.confirm-box p {
  font-size: 14px;
  color: #333;
  margin-bottom: 20px;
}

.btn-group {
  gap: 24px;
  display: flex;
  justify-content: space-around;
}

.confirm,
.cancel {
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.confirm {
  background-color: #e74c3c;
  color: white;
}

.cancel {
  background-color: #ddd;
  color: #333;
}

.success-msg {
  margin-top: 12px;
  font-size: 14px;
  color: #42b983;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.35s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
