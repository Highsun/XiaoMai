import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// fontawesome 图标库
import '@fortawesome/fontawesome-free/css/all.min.css'

// CSS 样式表
import './assets/styles/base.css'
import './assets/styles/auth.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
