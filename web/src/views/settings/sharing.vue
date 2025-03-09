<template>
  <div class="sharing-settings">
    <h1 class="text-2xl font-semibold text-primary-600">分享与权限</h1>
    <!-- 分享与权限内容将在这里实现 -->
    <!-- 主内容区 -->
    <main class="flex-1 overflow-auto">
      <div class="py-6">
        <div class="max-w-full">
          <!-- 快速分享 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-medium text-gray-800">快速分享</h2>
                <button type="button"
                  class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  <i class="fas fa-share-alt mr-2"></i>
                  创建分享
                </button>
              </div>

              <!-- 分享选项 -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- 链接分享 -->
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-4">
                    <i class="fas fa-link text-primary-500 text-xl mr-3"></i>
                    <h3 class="text-lg font-medium text-gray-800">链接分享</h3>
                  </div>
                  <p class="text-gray-600 text-sm mb-4">创建安全的分享链接，可设置访问密码和有效期</p>
                  <button class="text-primary-600 hover:text-primary-500 text-sm font-medium">
                    创建链接 →
                  </button>
                </div>

                <!-- 二维码分享 -->
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-4">
                    <i class="fas fa-qrcode text-primary-500 text-xl mr-3"></i>
                    <h3 class="text-lg font-medium text-gray-800">二维码分享</h3>
                  </div>
                  <p class="text-gray-600 text-sm mb-4">生成相册二维码，方便手机扫码查看</p>
                  <button class="text-primary-600 hover:text-primary-500 text-sm font-medium">
                    生成二维码 →
                  </button>
                </div>

                <!-- 社交分享 -->
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-4">
                    <i class="fas fa-share-nodes text-primary-500 text-xl mr-3"></i>
                    <h3 class="text-lg font-medium text-gray-800">社交分享</h3>
                  </div>
                  <p class="text-gray-600 text-sm mb-4">分享到微信、QQ等社交平台</p>
                  <button class="text-primary-600 hover:text-primary-500 text-sm font-medium">
                    社交分享 →
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- 家庭共享 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-medium text-gray-800">家庭共享</h2>
                <button type="button"
                  class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  <i class="fas fa-user-plus mr-2"></i>
                  邀请家庭成员
                </button>
              </div>

              <!-- 家庭成员列表 -->
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
                <!-- 成员1 -->
                <div class="text-center">
                  <div class="relative">
                    <img class="w-20 h-20 rounded-full mx-auto mb-2"
                      src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=200"
                      alt="用户头像">
                    <span
                      class="absolute bottom-2 right-2 w-4 h-4 bg-green-400 border-2 border-white rounded-full"></span>
                  </div>
                  <h3 class="text-gray-800 font-medium">爸爸</h3>
                  <p class="text-gray-500 text-sm">管理员</p>
                </div>

                <!-- 成员2 -->
                <div class="text-center">
                  <div class="relative">
                    <img class="w-20 h-20 rounded-full mx-auto mb-2"
                      src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=200"
                      alt="用户头像">
                    <span
                      class="absolute bottom-2 right-2 w-4 h-4 bg-green-400 border-2 border-white rounded-full"></span>
                  </div>
                  <h3 class="text-gray-800 font-medium">妈妈</h3>
                  <p class="text-gray-500 text-sm">编辑者</p>
                </div>

                <!-- 添加成员按钮 -->
                <div class="text-center">
                  <button
                    class="w-20 h-20 rounded-full mx-auto mb-2 border-2 border-dashed border-gray-300 flex items-center justify-center hover:border-primary-500 hover:text-primary-500">
                    <i class="fas fa-plus text-2xl"></i>
                  </button>
                  <h3 class="text-gray-800 font-medium">添加成员</h3>
                  <p class="text-gray-500 text-sm">邀请新成员</p>
                </div>
              </div>
            </div>
          </section>

          <!-- 协作管理 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-medium text-gray-800">协作管理</h2>
                <div class="flex space-x-4">
                  <button type="button"
                    class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                    <i class="fas fa-history mr-2"></i>
                    活动记录
                  </button>
                  <button type="button"
                    class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                    <i class="fas fa-cog mr-2"></i>
                    权限设置
                  </button>
                </div>
              </div>

              <!-- 协作相册列表 -->
              <div class="space-y-4">
                <!-- 相册1 -->
                <div class="bg-gray-50 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                      <img src="https://images.unsplash.com/photo-1516483638261-f4dbaf036963" alt="相册封面"
                        class="w-16 h-16 object-cover rounded-lg">
                      <div>
                        <h3 class="text-gray-800 font-medium">家庭旅行相册</h3>
                        <p class="text-gray-500 text-sm">最近更新：2024-01-15</p>
                      </div>
                    </div>
                    <div class="flex items-center space-x-4">
                      <div class="flex -space-x-2">
                        <img class="w-8 h-8 rounded-full border-2 border-white"
                          src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=100"
                          alt="用户头像">
                        <img class="w-8 h-8 rounded-full border-2 border-white"
                          src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=100"
                          alt="用户头像">
                      </div>
                      <button class="text-gray-400 hover:text-gray-500">
                        <i class="fas fa-ellipsis-v"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 相册2 -->
                <div class="bg-gray-50 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                      <img src="https://images.unsplash.com/photo-1538428494232-9c0d8a3ab403" alt="相册封面"
                        class="w-16 h-16 object-cover rounded-lg">
                      <div>
                        <h3 class="text-gray-800 font-medium">宝宝成长相册</h3>
                        <p class="text-gray-500 text-sm">最近更新：2024-01-10</p>
                      </div>
                    </div>
                    <div class="flex items-center space-x-4">
                      <div class="flex -space-x-2">
                        <img class="w-8 h-8 rounded-full border-2 border-white"
                          src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=100"
                          alt="用户头像">
                        <img class="w-8 h-8 rounded-full border-2 border-white"
                          src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=100"
                          alt="用户头像">
                        <div
                          class="w-8 h-8 rounded-full border-2 border-white bg-gray-200 flex items-center justify-center text-xs text-gray-500">
                          +2</div>
                      </div>
                      <button class="text-gray-400 hover:text-gray-500">
                        <i class="fas fa-ellipsis-v"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// 分享与权限相关逻辑
</script>