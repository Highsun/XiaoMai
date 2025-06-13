<template>
  <div class="password-change-container">
    <h2 class="change-password-title">修改密码</h2>

    <div class="password-container">
      <div class="cp-form-group">
        <label>旧密码</label>
        <input type="password" v-model="oldPassword" placeholder="请输入旧密码" />
      </div>
      <div class="cp-form-group">
        <label>新密码</label>
        <input type="password" v-model="newPassword" placeholder="请输入新密码（至少6位）" />
      </div>
      <div class="cp-form-group">
        <label>确认新密码</label>
        <input type="password" v-model="confirmPassword" placeholder="请再次输入新密码" />
      </div>
    </div>

    <p class="error-msg" v-if="error">{{ error }}</p>
    <p class="success-msg" v-if="success">{{ success }}</p>

    <div>
      <button class="submit-btn" @click="submitChange">提交修改</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { changePassword } from '@/services/auth'

const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const error = ref('')
const success = ref('')

async function submitChange() {
  error.value = ''
  success.value = ''

  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    error.value = '请填写所有字段'
    return
  }

  if (newPassword.value.length < 6) {
    error.value = '新密码必须至少6位'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    error.value = '两次输入的新密码不一致'
    return
  }

  try {
    const res = await changePassword({
      old_password: oldPassword.value,
      new_password: newPassword.value,
      confirm_password: confirmPassword.value
    })
    success.value = res.msg || '密码修改成功！'
    // 清空字段
    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (err) {
    const msg = err.response?.data?.msg || '修改失败，请重试'
    error.value = msg
  }
}
</script>

<style scoped>
.password-change-container {
  margin: 0 auto;
  margin-bottom: 12px;
}

.change-password-title {
  font-size: 16px;
  font-weight: bold;
  text-align: left;
  margin-bottom: 12px;
}

.password-container {
  display: flex;
  gap: 16px;
}

.cp-form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: 0;
}

label {
  margin-bottom: 6px;
  font-size: 14px;
  color: #333;
}

input {
  padding: 8px 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.submit-btn {
  width: auto;
  display: block;
  margin-top: 12px;
  margin-left: auto;
  background-color: #42b983;
  color: white;
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover {
  background-color: #369d6f;
}

.error-msg {
  font-size: 13px;
  margin-bottom: 10px;
}

.success-msg {
  color: #42b983;
  font-size: 13px;
  margin-top: 4px;
  margin-bottom: 10px;
}
</style>
