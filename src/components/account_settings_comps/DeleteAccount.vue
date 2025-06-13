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
    <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { deleteAccount } from '@/services/auth'
import axios from 'axios'

const showConfirm = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const router = useRouter()

async function confirmDelete() {
  showConfirm.value = false
  successMessage.value = ''
  errorMessage.value = ''
  try {
    const res = await deleteAccount()
    successMessage.value = res.data.msg || '您的账号已成功注销，感谢您的使用，再会！'
    // 清除本地登录状态
    localStorage.removeItem('access_token')
    delete axios.defaults.headers.common['Authorization']
    // 跳转登录页
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (err) {
    errorMessage.value = err.response?.data?.msg || '注销失败，请重试'
  }
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

.error-msg {
  margin-top: 12px;
  font-size: 14px;
  color: #e74c3c;
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
