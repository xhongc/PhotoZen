import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/about/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
    },
    {
      path: '/photos',
      name: 'photos',
      component: () => import('../views/photos/PhotosView.vue'),
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('../views/photos/UploadView.vue'),
    },
    {
      path: '/albums',
      name: 'albums',
      component: () => import('../views/albums/AlbumsView.vue'),
    },
    {
      path: '/tags',
      name: 'tags',
      component: () => import('../views/tags/TagsView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/about/AboutView.vue'),
    },
  ],
})

export default router
