import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// 将所有 axios 请求都指向后端 API
axios.defaults.baseURL = 'http://localhost:8888'

// fontawesome 图标库
import '@fortawesome/fontawesome-free/css/all.min.css'

// CSS 样式表
import './assets/styles/base.css'
import './assets/styles/fonts.css'
import './assets/styles/auth.css'
import './assets/styles/navbar.css'
import './assets/styles/hero.css'
import './assets/styles/category_container.css'
import './assets/styles/footer.css'
import './assets/styles/buy_tickets_comps.css'
import './assets/styles/concert_info.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
