import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/yearly',
    name: 'yearly',
    component: () => import('@/views/Yearly.vue')
  },
  {
    path: '/monthly',
    name: 'monthly',
    component: () => import('@/views/Monthly.vue')
  },
  {
    path: '/category',
    name: 'category',
    component: () => import('@/views/Category.vue')
  },
  {
    path: '/time',
    name: 'time',
    component: () => import('@/views/Time.vue')
  },
  {
    path: '/insights',
    name: 'insights',
    component: () => import('@/views/Insights.vue')
  },
  {
    path: '/transactions',
    name: 'transactions',
    component: () => import('@/views/Transactions.vue')
  },
  {
    path: '/settings',
    name: 'settings',
    component: () => import('@/views/Settings.vue')
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router
