import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import type { LoginResponse } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<LoginResponse['user'] | null>(() => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  })

  const setAuth = (response: LoginResponse) => {
    token.value = response.token
    user.value = response.user
    localStorage.setItem('token', response.token)
    localStorage.setItem('user', JSON.stringify(response.user))
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.token}`
  }

  const clearAuth = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
  }

  const initAuth = () => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
    }
  }

  return {
    token,
    user,
    setAuth,
    clearAuth,
    initAuth
  }
}) 