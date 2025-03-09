<template>
  <div class="help-settings">
    <h1 class="text-2xl font-semibold text-primary-600 mb-6">帮助与反馈</h1>
    <!-- 帮助与反馈内容将在这里实现 -->
    <!-- 主要内容区域 -->
    <main class="max-w-full">
      <!-- 搜索框 -->
      <div class="px-4 sm:px-0 mb-8">
        <div class="relative">
          <input type="text"
            class="w-full pl-12 pr-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            placeholder="搜索帮助文档...">
          <div class="absolute left-4 top-3.5 text-gray-400">
            <i class="fas fa-search text-lg"></i>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- 左侧常见问题区域 -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-5 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">常见问题</h2>
            </div>
            <div class="px-6 py-5">
              <div class="space-y-6">
                <!-- 问题分类 -->
                <div class="space-y-4">
                  <h3 class="text-sm font-medium text-gray-900">账号与安全</h3>
                  <div class="space-y-2">
                    <a href="#" class="block text-sm text-gray-600 hover:text-primary-500">如何修改登录密码？</a>
                    <a href="#" class="block text-sm text-gray-600 hover:text-primary-500">忘记密码怎么办？</a>
                    <a href="#" class="block text-sm text-gray-600 hover:text-primary-500">如何开启两步验证？</a>
                  </div>
                </div>
                <div class="space-y-4">
                  <h3 class="text-sm font-medium text-gray-900">照片管理</h3>
                  <div class="space-y-2">
                    <a href="#" class="block text-sm text-gray-600 hover:text-primary-500">如何创建相册？</a>
                    <a href="#" class="block text-sm text-gray-600 hover:text-primary-500">照片备份方式有哪些？</a>
                    <a href="#" class="block text-sm text-gray-600 hover:text-primary-500">如何共享照片给他人？</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧反馈表单 -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow">
            <div class="px-6 py-5 border-b border-gray-200">
              <h2 class="text-lg font-medium text-gray-900">提交反馈</h2>
            </div>
            <div class="px-6 py-5">
              <form class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">反馈类型</label>
                  <select
                    class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 rounded-md">
                    <option>功能建议</option>
                    <option>问题反馈</option>
                    <option>其他</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">反馈内容</label>
                  <textarea rows="4"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"></textarea>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">联系方式（选填）</label>
                  <input type="email"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500">
                </div>
                <div>
                  <button type="submit"
                    class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                    提交反馈
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- 联系客服 -->
          <div class="mt-8 bg-white rounded-lg shadow">
            <div class="px-6 py-5">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <i class="fas fa-headset text-primary-500 text-xl mr-3"></i>
                  <div>
                    <h3 class="text-sm font-medium text-gray-900">在线客服</h3>
                    <p class="text-sm text-gray-500">工作时间：9:00 - 18:00</p>
                  </div>
                </div>
                <button
                  class="inline-flex items-center px-4 py-2 border border-primary-500 text-sm font-medium rounded-md text-primary-600 hover:bg-primary-50">
                  联系客服
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 用户指南区域 -->
      <div class="mt-8">
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-5 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">新手指南</h2>
          </div>
          <div class="px-6 py-5">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="p-4 border border-gray-200 rounded-lg">
                <div class="flex items-center mb-4">
                  <i class="fas fa-cloud-upload-alt text-primary-500 text-xl mr-3"></i>
                  <h3 class="text-sm font-medium text-gray-900">快速上手</h3>
                </div>
                <p class="text-sm text-gray-500">了解如何快速上传和管理您的照片</p>
                <a href="#"
                  class="mt-3 inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-500">
                  查看教程 <i class="fas fa-arrow-right ml-2"></i>
                </a>
              </div>
              <div class="p-4 border border-gray-200 rounded-lg">
                <div class="flex items-center mb-4">
                  <i class="fas fa-share-alt text-primary-500 text-xl mr-3"></i>
                  <h3 class="text-sm font-medium text-gray-900">照片分享</h3>
                </div>
                <p class="text-sm text-gray-500">学习如何安全地分享照片给亲朋好友</p>
                <a href="#"
                  class="mt-3 inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-500">
                  查看教程 <i class="fas fa-arrow-right ml-2"></i>
                </a>
              </div>
              <div class="p-4 border border-gray-200 rounded-lg">
                <div class="flex items-center mb-4">
                  <i class="fas fa-shield-alt text-primary-500 text-xl mr-3"></i>
                  <h3 class="text-sm font-medium text-gray-900">隐私保护</h3>
                </div>
                <p class="text-sm text-gray-500">了解如何保护您的照片和个人信息</p>
                <a href="#"
                  class="mt-3 inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-500">
                  查看教程 <i class="fas fa-arrow-right ml-2"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// 帮助与反馈相关逻辑
</script>