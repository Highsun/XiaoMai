<template>
  <div>
    <button @click="goToLogin" style="width: 60px; margin: 20px auto auto 20px">账号</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function goToLogin() {
  router.push('/login')
}
</script>
