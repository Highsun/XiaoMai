<template>
  <div class="auth-page">
    <img class="background-img" src="../assets/images/auth/poster.jpg" alt="poster" />

    <div class="logo-area" @click="goHome" style="cursor: pointer">
      <img src="../assets/logo.png" alt="logo" class="logo-img" />
      <span class="logo-text">小麦</span>
    </div>

    <div class="auth-box">
      <h2>注册</h2>

      <!-- 后端通用错误 -->
      <p v-if="generalError" class="error-msg">{{ generalError }}</p>

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
            v-model="confirmPwd"
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/services/auth'

const router       = useRouter()
const username     = ref('')
const email        = ref('')
const password     = ref('')
const confirmPwd   = ref('')

// 字段级错误
const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})
// 后端通用错误
const generalError = ref('')

function goHome() {
  router.push('/')
}

function goToLogin() {
  router.push('/login')
}

function clearError(field) {
  errors[field]       = ''
  generalError.value  = ''
}

function validateEmail(val) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(val)
}

async function handleRegister() {
  // 1. 清空之前的错误
  Object.keys(errors).forEach(k => (errors[k] = ''))
  generalError.value = ''

  // 2. 前端校验
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
  if (!confirmPwd.value) {
    errors.confirmPassword = '请确认密码'
    return
  }
  if (password.value !== confirmPwd.value) {
    errors.confirmPassword = '两次输入的密码不一致'
    return
  }

  // 3. 调用后端注册接口
  try {
    await register({
      username:        username.value,
      email:           email.value,
      password:        password.value,
      confirmPassword: confirmPwd.value,
    })
    // 成功后跳转登录页
    router.push('/login')
  } catch (err) {
    // 400/401… 后端返回的 msg
    generalError.value = err.response?.data?.msg || '注册失败，请重试'
  }
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
  margin-bottom: 8px;
}
</style>
