<template>
  <div class="double-col">
    <!-- left -->
    <div class="poster">
      <div class="poster-overlay">
        <img src="../assets/images/poster.jpg" alt="poster" />
        <!-- TODO: Add logo icon here -->
        <div class="logo"></div>
      </div>
    </div>

    <!-- right -->
    <div class="login-container">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input v-model="username" id="username" type="text" placeholder="请输入用户名" />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input v-model="password" id="password" type="password" placeholder="请输入密码" />
        </div>
        <button type="submit">登录</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')

function handleLogin() {
  if (!username.value || !password.value) {
    alert('用户名或密码错误')
    return
  }
  // TODO: Add login logic here
  console.log('登录信息:', {
    username: username.value,
    password: password.value,
  })
}
</script>

<style scoped>
.double-col {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

/* left */
.poster {
  flex: 1.15;
  position: relative;
  overflow: hidden;
}

.poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.6);
}
.logo {
  position: absolute;
  top: 50px;
  left: 50px;
}
.poster-overlay {
  width: 100%;
  height: 100%;
  position: relative;
}

/* right */
/* TODO: Alter color theme */
.login-container {
  flex: 1;
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #f8f9fa;
}

h2 {
  font-size: 1.6rem;
  margin-bottom: 2rem;
  text-align: center;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
}

input {
  width: 350px;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border 0.2s;
}
input:focus {
  border-color: #42b983;
  outline: none;
}

button {
  width: 350px;
  padding: 0.75rem;
  background-color: #42b983;
  border: none;
  color: white;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}
button:hover {
  background-color: #369c74;
}
</style>
