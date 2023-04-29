import { createRouter, createWebHistory } from 'vue-router'
// TODO сделайте отдельную страницу. Импортировать приложение - костыль
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/plants',
      name: 'plants',
      component: () => import("../App.vue")
    }
  ]
})

export default router
