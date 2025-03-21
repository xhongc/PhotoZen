import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/home/index.vue'
import settingsRoutes from './settings'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
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
      path: '/photos/:id/edit',
      name: 'photo-edit',
      component: () => import('../views/photos/PhotoEditView.vue'),
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
      path: '/file',
      name: 'file',
      component: () => import('../views/file/index.vue'),
    },
    {
      path: '/expore',
      name: 'expore',
      component: () => import('../views/expore/index.vue'),
    },
    ...settingsRoutes
  ],
})

export default router
