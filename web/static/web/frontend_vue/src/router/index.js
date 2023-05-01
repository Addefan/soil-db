import { createRouter, createWebHistory } from 'vue-router'
import PlantsView from '@/pages/PlantsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/plants',
      name: 'plants',
      component: PlantsView
    }
  ]
})

export default router
