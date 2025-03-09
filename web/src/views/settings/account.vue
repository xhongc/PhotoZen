<template>
  <!-- 右侧内容 -->
  <div class="flex-1 overflow-y-auto py-6 px-8">
    <div class="max-w-full mx-auto">
      <h1 class="text-2xl font-semibold text-gray-900 mb-6">账户信息</h1>

      <!-- 个人信息卡片 -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex items-center space-x-6">
          <div class="flex-shrink-0">
            <div class="relative">
              <img class="h-24 w-24 rounded-full"
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                alt="用户头像">
              <div class="absolute bottom-0 right-0">
                <button
                  class="bg-white rounded-full p-1 shadow-md text-gray-600 hover:text-gray-800 focus:outline-none">
                  <i class="fas fa-camera"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium text-gray-800">陈小明</h3>
            <p class="text-gray-500">user@example.com</p>
            <p class="text-gray-500 text-sm mt-1">会员类型：标准用户</p>
            <button
              class="mt-2 inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900 focus:ring-primary-500">
              升级至专业版
            </button>
          </div>
        </div>
      </div>

      <!-- 基本信息表单 -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h2 class="text-lg font-medium text-gray-800 mb-4">基本信息</h2>
        <form class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="col-span-1">
              <label for="first-name" class="block text-sm font-medium text-gray-700">姓名</label>
              <input type="text" name="first-name" id="first-name" value="陈小明"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
            </div>
            <div class="col-span-1">
              <label for="nickname" class="block text-sm font-medium text-gray-700">昵称</label>
              <input type="text" name="nickname" id="nickname" value="照片控"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">电子邮箱</label>
            <input type="email" name="email" id="email" value="user@example.com"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
          </div>

          <div>
            <label for="phone" class="block text-sm font-medium text-gray-700">手机号码</label>
            <input type="tel" name="phone" id="phone" value="138****1234"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm">
          </div>

          <div>
            <label for="bio" class="block text-sm font-medium text-gray-700">个人简介</label>
            <textarea id="bio" name="bio" rows="3"
              class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              placeholder="介绍一下自己吧...">热爱摄影，喜欢记录生活中的美好瞬间。</textarea>
          </div>

          <div class="pt-2">
            <button type="submit"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
              保存更改
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 账户信息相关逻辑
</script>