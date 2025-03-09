<template>
  <div class="storage-settings">
    <h1 class="text-2xl font-semibold text-primary-600">存储管理</h1>
    <!-- 存储管理内容将在这里实现 -->
    <!-- 主内容区 -->
    <main class="flex-1 overflow-auto">
      <div class="py-6">
        <div class="max-w-full">
          <!-- 存储空间概览 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <h2 class="text-xl font-medium text-gray-800 mb-4">存储空间概览</h2>

              <!-- 存储使用统计 -->
              <div class="mb-6">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center">
                    <span class="text-gray-700 text-sm">已使用：5.8GB / 20GB</span>
                    <span
                      class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      <i class="fas fa-exclamation-triangle mr-1"></i>
                      接近容量上限
                    </span>
                  </div>
                  <button class="text-sm font-medium text-primary-600 hover:text-primary-500">
                    升级存储
                  </button>
                </div>

                <!-- 进度条 -->
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-primary-600 h-2.5 rounded-full" style="width: 29%"></div>
                </div>
              </div>

              <!-- 存储类型分布 -->
              <div>
                <h3 class="text-sm font-medium text-gray-700 mb-3">存储类型分布</h3>
                <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
                  <!-- 照片 -->
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                        <i class="fas fa-image text-blue-500"></i>
                      </div>
                      <div>
                        <p class="text-sm font-medium text-gray-700">照片</p>
                        <p class="text-lg font-semibold text-gray-900">4.2GB</p>
                      </div>
                    </div>
                  </div>

                  <!-- 视频 -->
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center mr-3">
                        <i class="fas fa-video text-red-500"></i>
                      </div>
                      <div>
                        <p class="text-sm font-medium text-gray-700">视频</p>
                        <p class="text-lg font-semibold text-gray-900">1.5GB</p>
                      </div>
                    </div>
                  </div>

                  <!-- 编辑版本 -->
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center mr-3">
                        <i class="fas fa-edit text-purple-500"></i>
                      </div>
                      <div>
                        <p class="text-sm font-medium text-gray-700">编辑版本</p>
                        <p class="text-lg font-semibold text-gray-900">0.1GB</p>
                      </div>
                    </div>
                  </div>

                  <!-- 备份 -->
                  <div class="bg-gray-50 rounded-lg p-4">
                    <div class="flex items-center">
                      <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center mr-3">
                        <i class="fas fa-database text-green-500"></i>
                      </div>
                      <div>
                        <p class="text-sm font-medium text-gray-700">备份</p>
                        <p class="text-lg font-semibold text-gray-900">0.0GB</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 重复照片检测 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-medium text-gray-800">重复照片检测</h2>
                <button type="button"
                  class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  <i class="fas fa-search mr-2"></i>
                  开始检测
                </button>
              </div>

              <!-- 上次检测结果 -->
              <div class="mb-6">
                <div class="flex items-center text-sm text-gray-500 mb-4">
                  <i class="fas fa-history mr-1"></i>
                  <span>上次检测：2023年10月15日</span>
                </div>

                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center">
                    <span class="font-medium text-gray-900">检测到28组重复照片</span>
                    <span
                      class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                      可节省约 124MB
                    </span>
                  </div>
                  <button class="text-sm font-medium text-primary-600 hover:text-primary-500">
                    一键清理
                  </button>
                </div>
              </div>

              <!-- 重复照片预览 -->
              <div class="space-y-6">
                <!-- 第一组 -->
                <div class="border border-gray-200 rounded-lg overflow-hidden">
                  <div class="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center justify-between">
                    <div class="flex items-center">
                      <span class="font-medium text-gray-900">组 #1</span>
                      <span class="ml-2 text-sm text-gray-500">3张相似照片</span>
                    </div>
                    <div class="flex items-center space-x-2">
                      <button class="text-sm text-gray-700 hover:text-gray-900">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button class="text-sm text-gray-700 hover:text-gray-900">
                        <i class="fas fa-check-circle"></i>
                      </button>
                    </div>
                  </div>
                  <div class="p-4 grid grid-cols-3 gap-4">
                    <div class="relative group">
                      <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-md overflow-hidden">
                        <img
                          src="https://images.unsplash.com/photo-1603899122634-f086ca5f5ddd?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=400"
                          class="w-full h-full object-cover">
                        <div
                          class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                          <button class="p-1 bg-white rounded-full">
                            <i class="fas fa-check text-green-500"></i>
                          </button>
                        </div>
                      </div>
                      <div class="mt-2">
                        <p class="text-xs text-gray-500">2023/10/12 18:42</p>
                        <p class="text-xs text-gray-500">2.1MB</p>
                      </div>
                    </div>
                    <div class="relative group">
                      <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-md overflow-hidden">
                        <img
                          src="https://images.unsplash.com/photo-1603899122634-f086ca5f5ddd?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=400"
                          class="w-full h-full object-cover">
                        <div
                          class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                          <button class="p-1 bg-white rounded-full">
                            <i class="fas fa-check text-green-500"></i>
                          </button>
                        </div>
                      </div>
                      <div class="mt-2">
                        <p class="text-xs text-gray-500">2023/10/12 18:43</p>
                        <p class="text-xs text-gray-500">2.1MB</p>
                      </div>
                    </div>
                    <div class="relative group">
                      <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-md overflow-hidden">
                        <img
                          src="https://images.unsplash.com/photo-1603899122634-f086ca5f5ddd?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=400"
                          class="w-full h-full object-cover">
                        <div
                          class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                          <button class="p-1 bg-white rounded-full">
                            <i class="fas fa-check text-green-500"></i>
                          </button>
                        </div>
                      </div>
                      <div class="mt-2">
                        <p class="text-xs text-gray-500">2023/10/12 18:45</p>
                        <p class="text-xs text-gray-500">2.0MB</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 第二组 -->
                <div class="border border-gray-200 rounded-lg overflow-hidden">
                  <div class="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center justify-between">
                    <div class="flex items-center">
                      <span class="font-medium text-gray-900">组 #2</span>
                      <span class="ml-2 text-sm text-gray-500">2张相似照片</span>
                    </div>
                    <div class="flex items-center space-x-2">
                      <button class="text-sm text-gray-700 hover:text-gray-900">
                        <i class="fas fa-eye"></i>
                      </button>
                      <button class="text-sm text-gray-700 hover:text-gray-900">
                        <i class="fas fa-check-circle"></i>
                      </button>
                    </div>
                  </div>
                  <div class="p-4 grid grid-cols-3 gap-4">
                    <div class="relative group">
                      <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-md overflow-hidden">
                        <img
                          src="https://images.unsplash.com/photo-1606787366850-de6330128bfc?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=400"
                          class="w-full h-full object-cover">
                        <div
                          class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                          <button class="p-1 bg-white rounded-full">
                            <i class="fas fa-check text-green-500"></i>
                          </button>
                        </div>
                      </div>
                      <div class="mt-2">
                        <p class="text-xs text-gray-500">2023/10/05 12:32</p>
                        <p class="text-xs text-gray-500">3.4MB</p>
                      </div>
                    </div>
                    <div class="relative group">
                      <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-md overflow-hidden">
                        <img
                          src="https://images.unsplash.com/photo-1606787366850-de6330128bfc?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=400"
                          class="w-full h-full object-cover">
                        <div
                          class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                          <button class="p-1 bg-white rounded-full">
                            <i class="fas fa-check text-green-500"></i>
                          </button>
                        </div>
                      </div>
                      <div class="mt-2">
                        <p class="text-xs text-gray-500">2023/10/05 12:33</p>
                        <p class="text-xs text-gray-500">3.2MB</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 照片压缩 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <h2 class="text-xl font-medium text-gray-800 mb-4">照片压缩</h2>

              <!-- 压缩选项 -->
              <div class="mb-8">
                <div class="max-w-3xl">
                  <div class="mb-6">
                    <label class="block text-sm font-medium text-gray-700 mb-2">压缩质量</label>
                    <select
                      class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md">
                      <option>高质量 (90%) - 推荐</option>
                      <option>中等质量 (75%)</option>
                      <option>低质量 (60%)</option>
                      <option>自定义...</option>
                    </select>
                    <p class="mt-1 text-sm text-gray-500">高质量压缩可减小约40%文件大小，而肉眼几乎无法察觉画质差异</p>
                  </div>

                  <div class="flex items-center mb-4">
                    <input id="keep-original" name="keep-original" type="checkbox"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                    <label for="keep-original" class="ml-2 block text-sm text-gray-700">保留原图（占用更多空间）</label>
                  </div>

                  <div class="flex items-center mb-6">
                    <input id="compress-new" name="compress-new" type="checkbox"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" checked>
                    <label for="compress-new" class="ml-2 block text-sm text-gray-700">自动压缩新上传的照片</label>
                  </div>

                  <button type="button"
                    class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                    <i class="fas fa-compress-alt mr-2"></i>
                    压缩所有照片
                  </button>
                </div>
              </div>

              <!-- 压缩示例 -->
              <div>
                <h3 class="text-lg font-medium text-gray-700 mb-4">压缩效果示例</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- 原图 -->
                  <div>
                    <div class="aspect-w-4 aspect-h-3 bg-gray-200 rounded-md overflow-hidden mb-2">
                      <img
                        src="https://images.unsplash.com/photo-1505761671935-60b3a7427bad?ixlib=rb-1.2.1&auto=format&fit=crop&q=100&w=600"
                        class="w-full h-full object-cover">
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-sm font-medium text-gray-700">原图</span>
                      <span class="text-sm text-gray-500">4.8MB</span>
                    </div>
                  </div>

                  <!-- 压缩后 -->
                  <div>
                    <div class="aspect-w-4 aspect-h-3 bg-gray-200 rounded-md overflow-hidden mb-2">
                      <img
                        src="https://images.unsplash.com/photo-1505761671935-60b3a7427bad?ixlib=rb-1.2.1&auto=format&fit=crop&q=85&w=600"
                        class="w-full h-full object-cover">
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-sm font-medium text-gray-700">压缩后</span>
                      <div class="flex items-center">
                        <span class="text-sm text-gray-500">2.1MB</span>
                        <span
                          class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          节省 56%
                        </span>
                      </div>
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
// 存储管理相关逻辑
</script>