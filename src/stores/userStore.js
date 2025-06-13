import { reactive } from 'vue'

export const userStore = reactive({
  isLoggedIn: !!localStorage.getItem('access_token'),
  username: localStorage.getItem('username') || '',
  login(token, name) {
    localStorage.setItem('access_token', token)
    if (name) localStorage.setItem('username', name)
    userStore.isLoggedIn = true
    if (name) userStore.username = name
  },
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('username')
    userStore.isLoggedIn = false
    userStore.username = ''
  }
})

// 支持多标签页同步
window.addEventListener('storage', () => {
  userStore.isLoggedIn = !!localStorage.getItem('access_token')
  userStore.username = localStorage.getItem('username') || ''
})
