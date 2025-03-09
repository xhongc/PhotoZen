<template>
  <div class="notifications-settings">
    <h1 class="text-2xl font-semibold text-primary-600 mb-6">消息通知</h1>
    <!-- 消息通知内容将在这里实现 -->
    <!-- 消息通知页面 -->
    <!-- 主要内容区域 -->
    <main class="max-w-full">
      <!-- 消息类型切换 -->
      <div class="bg-white rounded-lg shadow-sm mb-6">
        <div class="px-4 sm:px-6 lg:px-8">
          <nav class="flex space-x-8" aria-label="消息类型">
            <button
              class="border-primary-500 text-primary-600 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm">
              全部消息
              <span class="ml-2 py-0.5 px-2 bg-primary-100 text-primary-600 rounded-full text-xs">12</span>
            </button>
            <button
              class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm">
              系统通知
              <span class="ml-2 py-0.5 px-2 bg-gray-100 text-gray-600 rounded-full text-xs">5</span>
            </button>
            <button
              class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm">
              互动消息
              <span class="ml-2 py-0.5 px-2 bg-gray-100 text-gray-600 rounded-full text-xs">7</span>
            </button>
          </nav>
        </div>
      </div>

      <!-- 消息列表 -->
      <div class="bg-white rounded-lg shadow-sm">
        <div class="divide-y divide-gray-200">
          <!-- 未读系统通知 -->
          <div class="p-4 sm:px-6 hover:bg-gray-50 cursor-pointer relative">
            <div class="absolute top-4 left-4 w-2 h-2 bg-primary-500 rounded-full"></div>
            <div class="ml-6">
              <div class="flex justify-between">
                <div class="flex items-center">
                  <i class="fas fa-bell text-primary-500 text-xl mr-3"></i>
                  <p class="text-sm font-medium text-gray-900">存储空间即将用完</p>
                </div>
                <time class="text-sm text-gray-500">10分钟前</time>
              </div>
              <div class="mt-2 text-sm text-gray-500 ml-7">
                您的存储空间已使用90%，建议及时清理或升级存储空间。
              </div>
            </div>
          </div>

          <!-- 已读互动消息 -->
          <div class="p-4 sm:px-6 hover:bg-gray-50 cursor-pointer">
            <div class="flex justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <img class="h-10 w-10 rounded-full"
                    src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    alt="">
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">张三</p>
                  <p class="text-sm text-gray-500">评论了您的照片</p>
                </div>
              </div>
              <time class="text-sm text-gray-500">2小时前</time>
            </div>
            <div class="mt-2 text-sm text-gray-500 ml-13">
              "这张照片拍得真不错，光线处理很自然！"
            </div>
            <!-- 照片预览 -->
            <div class="mt-2 ml-13">
              <img class="h-20 w-20 object-cover rounded-lg"
                src="https://images.unsplash.com/photo-1500531279542-fc8490c8ea4d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1351&q=80"
                alt="">
            </div>
          </div>

          <!-- 系统通知 -->
          <div class="p-4 sm:px-6 hover:bg-gray-50 cursor-pointer">
            <div class="flex justify-between">
              <div class="flex items-center">
                <i class="fas fa-sync text-green-500 text-xl mr-3"></i>
                <p class="text-sm font-medium text-gray-900">同步完成</p>
              </div>
              <time class="text-sm text-gray-500">昨天</time>
            </div>
            <div class="mt-2 text-sm text-gray-500 ml-7">
              已成功同步 25 张新照片到云端。
            </div>
          </div>

          <!-- 互动消息 -->
          <div class="p-4 sm:px-6 hover:bg-gray-50 cursor-pointer">
            <div class="flex justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <img class="h-10 w-10 rounded-full"
                    src="https://images.unsplash.com/photo-1550525811-e5869dd03032?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                    alt="">
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900">李四</p>
                  <p class="text-sm text-gray-500">点赞了您的相册</p>
                </div>
              </div>
              <time class="text-sm text-gray-500">2天前</time>
            </div>
            <div class="mt-2 text-sm text-gray-500 ml-13">
              "我的旅行记录"
            </div>
          </div>
        </div>

        <!-- 加载更多 -->
        <div class="px-4 py-4 sm:px-6 text-center">
          <button type="button"
            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            加载更多
            <i class="fas fa-chevron-down ml-2"></i>
          </button>
        </div>
      </div>

      <!-- 空状态 -->
      <div class="hidden mt-6 text-center">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100">
          <i class="fas fa-bell text-gray-400 text-2xl"></i>
        </div>
        <h3 class="mt-2 text-sm font-medium text-gray-900">暂无消息</h3>
        <p class="mt-1 text-sm text-gray-500">
          您现在没有任何未读消息。
        </p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// 消息通知相关逻辑
</script>