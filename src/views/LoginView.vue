<template>
  <div class="auth-page">
    <img class="background-img" src="../assets/images/auth/poster.jpg" alt="poster" />

    <div class="logo-area" @click="goHome" style="cursor: pointer">
      <img src="../assets/logo.png" alt="logo" class="logo-img" />
      <span class="logo-text">小麦</span>
    </div>

    <div class="auth-box">
      <h2>登录</h2>

      <!-- 后端通用错误 -->
      <p v-if="generalError" class="error-msg">{{ generalError }}</p>

      <form @submit.prevent="handleLogin" novalidate>
        <div class="form-group" :class="{ error: errors.account }">
          <label for="account">账号</label>
          <input
            v-model="account"
            id="account"
            type="text"
            placeholder="请输入用户名或邮箱"
            @focus="clearError('account')"
          />
          <p v-if="errors.account" class="error-msg">{{ errors.account }}</p>
        </div>

        <div class="form-group" :class="{ error: errors.password }">
          <label for="password">密码</label>
          <div class="password-wrapper">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              id="password"
              placeholder="请输入密码"
              @focus="clearError('password')"
            />
            <i
              :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"
              class="toggle-password"
              @click="togglePasswordVisibility"
            ></i>
          </div>
          <p v-if="errors.password" class="error-msg">{{ errors.password }}</p>
        </div>

        <button type="submit">登录</button>

        <p class="hint">
          没有账号？
          <a href="#" @click.prevent="goToRegister">点击注册</a>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/auth'
import { userStore } from '@/stores/userStore.js'
import axios from 'axios'

const router = useRouter()

// 表单字段
const account      = ref('')
const password     = ref('')
const showPassword = ref(false)

// 字段级错误和通用错误
const errors = reactive({ account: '', password: '' })
const generalError = ref('')

function goHome() {
  router.push('/')
}

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}

function clearError(field) {
  errors[field]      = ''
  generalError.value = ''
}

async function handleLogin() {
  // 重置错误
  Object.keys(errors).forEach(k => (errors[k] = ''))
  generalError.value = ''

  // 前端校验
  if (!account.value.trim()) {
    errors.account = '请输入用户名或邮箱'
    return
  }
  if (!password.value) {
    errors.password = '请输入密码'
    return
  }

  // 调用后端登录接口
  try {
    const res = await login({
      account:  account.value,
      password: password.value
    })
    const token = res.data.access_token
    localStorage.setItem('access_token', token)

    // 新增部分：登录后用 token 获取用户名
    const userinfoRes = await axios.get('/api/auth/userinfo', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const username = userinfoRes.data.username

    // 用 userStore 记录全局状态
    userStore.login(token, username)

    router.push('/')
  } catch (err) {
    generalError.value = err.response?.data?.msg || '登录失败，请重试'
  }
}

function goToRegister() {
  router.push('/register')
}
</script>

<style scoped>
.logo-img {
  height: 40px;
  width: 40px;
  object-fit: contain;
  margin-right: 12px;
}
.logo-text {
  color: #fff;
  font-size: 1.8rem;
}
.error-msg {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 4px;
}
.password-wrapper {
  position: relative;
}
.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}
</style>
