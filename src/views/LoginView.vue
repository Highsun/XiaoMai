<template>
  <div class="auth-page">
    <img class="background-img" src="../assets/images/poster.jpg" alt="poster" />

    <div class="logo-area" @click="goHome" style="cursor: pointer">
      <!-- TODO: 添加小麦LOGO -->
      <img src="../assets/logo.png" alt="logo" class="logo-img" />
      <span class="logo-text">小麦</span>
    </div>

    <div class="auth-box">
      <h2>登录</h2>
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

const account = ref('')
const password = ref('')
const showPassword = ref(false)

const errors = reactive({
  account: '',
  password: '',
})

const router = useRouter()

// 点击LOGO跳转到首页
function goHome() {
  router.push('/')
}

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}

function clearError(field) {
  errors[field] = ''
}

function handleLogin() {
  // 清空所有错误提示
  Object.keys(errors).forEach((key) => {
    errors[key] = ''
  })

  // 依次验证，遇到第一个错误就返回提示
  if (!account.value.trim()) {
    errors.account = '请输入用户名或邮箱'
    return
  }
  if (!password.value) {
    errors.password = '请输入密码'
    return
  }

  // TODO: 添加后端登录验证

  router.push('/')
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
</style>
