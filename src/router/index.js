import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import BuyTicketsView from '../views/BuyTicketsView.vue' // FIXME: Test
import DashBoardView from '../views/DashBoardView.vue'
import PayView from '../views/PayView.vue'

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
  // FIXME: Test
  {
    path: '/buy-tickets',
    name: 'BuyTickets',
    component: BuyTicketsView,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashBoardView,
  },
  {
  path: '/category',
  name: 'Category',
  component: () => import('@/views/CategoryView.vue')
  },
  {
    path: '/pay',
    name: 'Pay',
    component: PayView,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  }
})


export default router
