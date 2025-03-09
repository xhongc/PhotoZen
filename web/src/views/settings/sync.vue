<template>
  <div class="sync-settings">
    <h1 class="text-2xl font-semibold text-primary-600 mb-6">同步设置</h1>
    <!-- 同步设置内容将在这里实现 -->
    <!-- 主要内容区域 -->
    <main class="max-w-full">
      <!-- 同步状态概览 -->
      <div class="bg-white rounded-lg shadow-sm mb-6">
        <div class="px-6 py-5 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-medium text-gray-900">同步状态</h2>
            <div class="flex items-center space-x-4">
              <span
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                <span class="w-2 h-2 mr-2 rounded-full bg-green-500"></span>
                同步正常
              </span>
              <button type="button"
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                <i class="fas fa-sync-alt mr-2"></i>
                立即同步
              </button>
            </div>
          </div>
        </div>
        <div class="px-6 py-5">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <i class="fas fa-clock text-primary-500 text-xl mr-3"></i>
                  <div>
                    <p class="text-sm font-medium text-gray-900">上次同步</p>
                    <p class="text-sm text-gray-500">2024-03-20 15:30</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <i class="fas fa-images text-primary-500 text-xl mr-3"></i>
                  <div>
                    <p class="text-sm font-medium text-gray-900">已同步照片</p>
                    <p class="text-sm text-gray-500">1,234 张</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <i class="fas fa-hdd text-primary-500 text-xl mr-3"></i>
                  <div>
                    <p class="text-sm font-medium text-gray-900">已用空间</p>
                    <p class="text-sm text-gray-500">2.5 GB / 10 GB</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 同步设置选项 -->
      <div class="bg-white rounded-lg shadow-sm mb-6">
        <div class="px-6 py-5 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">同步设置</h2>
        </div>
        <div class="px-6 py-5">
          <div class="space-y-6">
            <!-- 自动同步开关 -->
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-sm font-medium text-gray-900">自动同步</h3>
                <p class="text-sm text-gray-500">开启后将自动同步新增的照片</p>
              </div>
              <button type="button"
                class="bg-primary-600 relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                role="switch" aria-checked="true">
                <span aria-hidden="true"
                  class="translate-x-5 pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"></span>
              </button>
            </div>

            <!-- 同步文件夹 -->
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-3">同步文件夹</h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div class="flex items-center">
                    <i class="fas fa-folder text-primary-500 text-xl mr-3"></i>
                    <span class="text-sm text-gray-700">相机胶卷</span>
                  </div>
                  <button class="text-gray-400 hover:text-gray-500">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </div>
                <button type="button"
                  class="w-full flex items-center justify-center px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg text-sm font-medium text-gray-600 hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  <i class="fas fa-plus mr-2"></i>
                  添加文件夹
                </button>
              </div>
            </div>

            <!-- 同步选项 -->
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-3">同步选项</h3>
              <div class="space-y-3">
                <div class="flex items-center">
                  <input type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                  <label class="ml-3 text-sm text-gray-700">仅在 Wi-Fi 网络下同步</label>
                </div>
                <div class="flex items-center">
                  <input type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                  <label class="ml-3 text-sm text-gray-700">同步原始照片（RAW 格式）</label>
                </div>
                <div class="flex items-center">
                  <input type="checkbox"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
                  <label class="ml-3 text-sm text-gray-700">保留照片 EXIF 信息</label>
                </div>
              </div>
            </div>

            <!-- 同步频率 -->
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-3">同步频率</h3>
              <select
                class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 rounded-md">
                <option>实时同步</option>
                <option>每小时</option>
                <option>每天</option>
                <option>每周</option>
                <option>手动同步</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- 同步历史记录 -->
      <div class="bg-white rounded-lg shadow-sm">
        <div class="px-6 py-5 border-b border-gray-200">
          <h2 class="text-lg font-medium text-gray-900">同步历史</h2>
        </div>
        <div class="px-6 py-5">
          <div class="space-y-4">
            <div class="flex items-center justify-between py-3 border-b border-gray-200">
              <div class="flex items-center">
                <i class="fas fa-check-circle text-green-500 text-xl mr-3"></i>
                <div>
                  <p class="text-sm font-medium text-gray-900">成功同步 15 张照片</p>
                  <p class="text-sm text-gray-500">2024-03-20 15:30</p>
                </div>
              </div>
              <span class="text-sm text-gray-500">32 MB</span>
            </div>
            <div class="flex items-center justify-between py-3 border-b border-gray-200">
              <div class="flex items-center">
                <i class="fas fa-check-circle text-green-500 text-xl mr-3"></i>
                <div>
                  <p class="text-sm font-medium text-gray-900">成功同步 8 张照片</p>
                  <p class="text-sm text-gray-500">2024-03-19 10:15</p>
                </div>
              </div>
              <span class="text-sm text-gray-500">18 MB</span>
            </div>
            <div class="flex items-center justify-between py-3">
              <div class="flex items-center">
                <i class="fas fa-exclamation-circle text-yellow-500 text-xl mr-3"></i>
                <div>
                  <p class="text-sm font-medium text-gray-900">部分同步失败（3/12 张）</p>
                  <p class="text-sm text-gray-500">2024-03-18 20:45</p>
                </div>
              </div>
              <span class="text-sm text-gray-500">25 MB</span>
            </div>
          </div>
          <div class="mt-4 text-center">
            <button type="button"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
              查看更多历史记录
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// 同步设置相关逻辑
</script>