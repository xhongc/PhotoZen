<template>
  <div class="w-full h-screen bg-gradient-to-r from-blue-50 to-indigo-50 flex items-center justify-center p-6 bg-base-200">
    <div class="bg-base-100 bg-opacity-70 backdrop-filter backdrop-blur-md rounded-xl shadow-lg p-8 w-full max-w-md">
      <div class="flex justify-center mb-8">
        <div class="flex items-center">
          <i class="fas fa-cloud text-primary-500 text-4xl mr-3"></i>
          <h1 class="text-3xl font-bold text-gray-800">PhotoZen</h1>
        </div>
      </div>

      <h2 class="text-2xl font-bold text-center text-gray-800 mb-8">欢迎回来</h2>

      <form class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">用户名:</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <i class="fas fa-user text-gray-400"></i>
            </div>
            <input id="username" name="username" type="text"
              class="pl-10 block w-full rounded-lg border-gray-300 bg-white bg-opacity-80 shadow-sm focus:border-primary-500 focus:ring-primary-500 focus:ring-2 h-12"
              placeholder="your username">
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">密码:</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <i class="fas fa-lock text-gray-400"></i>
            </div>
            <input id="password" name="password" type="password"
              class="pl-10 block w-full rounded-lg border-gray-300 bg-white bg-opacity-80 shadow-sm focus:border-primary-500 focus:ring-primary-500 focus:ring-2 h-12"
              placeholder="••••••••">
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" name="remember-me" type="checkbox"
              class="h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500">
            <label for="remember-me" class="ml-2 block text-sm text-gray-700">记住我</label>
          </div>
          <a href="#" class="text-sm font-medium text-primary-600 hover:text-primary-500">忘记密码?</a>
        </div>

        <div>
          <button type="submit"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            登录
          </button>
        </div>
      </form>
      <p class="mt-6 text-center text-sm text-gray-600">
        还没有账户?
        <a href="#" class="font-medium text-primary-600 hover:text-primary-500">注册新账户</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    // TODO: 实现登录逻辑
    console.log('登录信息：', { username: username.value, password: password.value })
    // 登录成功后跳转到首页
    router.push('/')
  } catch (error) {
    console.error('登录失败：', error)
  }
}
</script>