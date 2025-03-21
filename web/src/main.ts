import './input.css'
import './output.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import message from './components/notify'
const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(message.register)
// 初始化认证状态
const authStore = useAuthStore()
authStore.initAuth()

app.mount('#app')
