import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import BuyTicketsView from '../views/BuyTicketsView.vue' // FIXME: Test
import DashBoardView from '../views/DashBoardView.vue'
import PayView from '../views/PayView.vue'
import FavoritesView from '../views/FavoritesView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/buy-tickets/:id',
    name: 'BuyTickets',
    component: BuyTicketsView,
    props: true,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashBoardView,
  },
  {
    path: '/category',
    name: 'Category',
    component: () => import('@/views/CategoryView.vue'),
  },
  {
    path: '/pay',
    name: 'Pay',
    component: PayView,
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: FavoritesView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { left: 0, top: 0 }
  },
})

// 每次路由完成后，再次把页面拉到最顶部
router.afterEach(() => {
  window.scrollTo(0, 0)
})

export default router
