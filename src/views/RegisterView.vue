<template>
  <div class="auth-page">
    <img class="background-img" src="../assets/images/poster.jpg" alt="poster" />

    <div class="logo-area" @click="goHome" style="cursor: pointer">
      <!-- TODO: 添加小麦LOGO -->
      <img src="../assets/logo.png" alt="logo" class="logo-img" />
      <span class="logo-text">小麦</span>
    </div>

    <div class="auth-box">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister" novalidate>
        <div class="form-group" :class="{ error: errors.username }">
          <label for="username">用户名</label>
          <input
            v-model="username"
            id="username"
            type="text"
            placeholder="请输入用户名"
            @focus="clearError('username')"
          />
          <p v-if="errors.username" class="error-msg">{{ errors.username }}</p>
        </div>

        <div class="form-group" :class="{ error: errors.email }">
          <label for="email">邮箱</label>
          <input
            v-model="email"
            id="email"
            type="email"
            placeholder="请输入邮箱"
            @focus="clearError('email')"
          />
          <p v-if="errors.email" class="error-msg">{{ errors.email }}</p>
        </div>

        <div class="form-group" :class="{ error: errors.password }">
          <label for="password">密码</label>
          <input
            v-model="password"
            id="password"
            type="password"
            placeholder="请输入密码"
            @focus="clearError('password')"
          />
          <p v-if="errors.password" class="error-msg">{{ errors.password }}</p>
        </div>

        <div class="form-group" :class="{ error: errors.confirmPassword }">
          <label for="confirmPassword">确认密码</label>
          <input
            v-model="confirmPassword"
            id="confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            @focus="clearError('confirmPassword')"
          />
          <p v-if="errors.confirmPassword" class="error-msg">{{ errors.confirmPassword }}</p>
        </div>

        <button type="submit">注册</button>

        <p class="hint">
          已有账号？
          <a href="#" @click.prevent="goToLogin">点击登录</a>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const router = useRouter()

// 点击LOGO跳转到首页
function goHome() {
  router.push('/')
}

function clearError(field) {
  errors[field] = ''
}

function handleRegister() {
  // 清空所有错误提示
  Object.keys(errors).forEach((key) => {
    errors[key] = ''
  })

  // 依次验证，遇到第一个错误就返回提示
  if (!username.value.trim()) {
    errors.username = '用户名不能为空'
    return
  }

  if (!email.value.trim()) {
    errors.email = '邮箱不能为空'
    return
  } else if (!validateEmail(email.value)) {
    errors.email = '请输入正确的邮箱格式'
    return
  }

  if (!password.value) {
    errors.password = '密码不能为空'
    return
  }

  if (!confirmPassword.value) {
    errors.confirmPassword = '请确认密码'
    return
  }

  if (password.value !== confirmPassword.value) {
    errors.confirmPassword = '两次输入的密码不一致'
    return
  }

  // TODO: 添加后端注册逻辑
  console.log('注册信息:', {
    username: username.value,
    email: email.value,
    password: password.value,
  })

  alert('注册成功，请登录')
  router.push('/login')
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

function goToLogin() {
  router.push('/login')
}
</script>
