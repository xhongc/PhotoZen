<template>
  <!-- 主内容区 -->
  <main>
    <!-- 筛选工具栏 -->
    <div class="border-b border-base-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <!-- 时间筛选 -->
            <select
              class="block pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md">
              <option>全部时间</option>
              <option>最近30天</option>
              <option>最近90天</option>
              <option>最近一年</option>
              <option>自定义...</option>
            </select>

            <!-- 快速筛选标签 -->
            <div class="flex items-center space-x-2">
              <button class="px-3 py-1.5 bg-primary-50 text-primary-700 rounded-full text-sm hover:bg-primary-100">
                <i class="fas fa-heart mr-1"></i>
                收藏
              </button>
              <button class="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200">
                <i class="fas fa-user mr-1"></i>
                人物
              </button>
              <button class="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200">
                <i class="fas fa-map-marker-alt mr-1"></i>
                地点
              </button>
            </div>
          </div>

          <div class="flex items-center space-x-4">
            <!-- 排序方式 -->
            <select
              class="block pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md">
              <option>最新优先</option>
              <option>最早优先</option>
              <option>评分最高</option>
            </select>

            <!-- 视图切换 -->
            <div class="flex items-center space-x-2 border-l border-gray-200 pl-4">
              <button class="p-2 text-primary-600">
                <i class="fas fa-th-large"></i>
              </button>
              <button class="p-2 text-gray-400 hover:text-gray-500">
                <i class="fas fa-th"></i>
              </button>
              <button class="p-2 text-gray-400 hover:text-gray-500">
                <i class="fas fa-list"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 照片墙 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 2024年1月 -->
      <div class="mb-12">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-medium text-primary-600">2024年1月</h2>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-500">共124张照片</span>
            <button class="text-sm text-primary-600 hover:text-primary-700">
              <i class="fas fa-chevron-down"></i>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <!-- 照片项 -->
          <div class="group relative">
            <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-lg overflow-hidden">
              <img src="https://images.unsplash.com/photo-1482517967863-00e15c9b44be"
                class="w-full h-full object-cover group-hover:opacity-75 transition-opacity" alt="新年烟花">
              <div
                class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
                <div class="flex space-x-2">
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-heart"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-share-alt"></i>
                  </button>
                </div>
              </div>
            </div>
            <div class="mt-2">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-medium text-gray-900">新年烟花</h3>
                <div class="flex items-center">
                  <i class="fas fa-star text-yellow-400 text-xs"></i>
                  <span class="ml-1 text-xs text-gray-500">4.8</span>
                </div>
              </div>
              <p class="text-sm text-gray-500">2024-01-01</p>
            </div>
          </div>

          <!-- 更多照片... -->
        </div>
      </div>

      <!-- 2023年12月 -->
      <div class="mb-12">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-medium text-primary-600">2023年12月</h2>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-500">共156张照片</span>
            <button class="text-sm text-primary-600 hover:text-primary-700">
              <i class="fas fa-chevron-down"></i>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <!-- 照片项 -->
          <div class="group relative">
            <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-lg overflow-hidden">
              <img src="https://images.unsplash.com/photo-1482517967863-00e15c9b44be"
                class="w-full h-full object-cover group-hover:opacity-75 transition-opacity" alt="圣诞节">
              <div
                class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
                <div class="flex space-x-2">
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-heart"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-share-alt"></i>
                  </button>
                </div>
              </div>
            </div>
            <div class="mt-2">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-medium text-gray-900">圣诞节</h3>
                <div class="flex items-center">
                  <i class="fas fa-star text-yellow-400 text-xs"></i>
                  <span class="ml-1 text-xs text-gray-500">4.5</span>
                </div>
              </div>
              <p class="text-sm text-gray-500">2023-12-25</p>
            </div>
          </div>

          <!-- 更多照片... -->
        </div>
      </div>

      <!-- 2023年6月 -->
      <div class="mb-12">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-medium text-primary-600">2023年6月</h2>
          <div class="flex items-center space-x-2">
            <span class="text-sm text-gray-500">共89张照片</span>
            <button class="text-sm text-primary-600 hover:text-primary-700">
              <i class="fas fa-chevron-down"></i>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <!-- 照片项 -->
          <div class="group relative">
            <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-lg overflow-hidden">
              <img src="https://images.unsplash.com/photo-1523906834658-6e24ef2386f9"
                class="w-full h-full object-cover group-hover:opacity-75 transition-opacity" alt="威尼斯日落">
              <div
                class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
                <div class="flex space-x-2">
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-heart"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-share-alt"></i>
                  </button>
                </div>
              </div>
            </div>
            <div class="mt-2">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-medium text-gray-900">威尼斯日落</h3>
                <div class="flex items-center">
                  <i class="fas fa-star text-yellow-400 text-xs"></i>
                  <span class="ml-1 text-xs text-gray-500">4.5</span>
                </div>
              </div>
              <p class="text-sm text-gray-500">2023-06-15</p>
            </div>
          </div>

          <div class="group relative">
            <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-lg overflow-hidden">
              <img src="https://images.unsplash.com/photo-1516483638261-f4dbaf036963"
                class="w-full h-full object-cover group-hover:opacity-75 transition-opacity" alt="罗马广场">
              <div
                class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
                <div class="flex space-x-2">
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-heart"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-share-alt"></i>
                  </button>
                </div>
              </div>
            </div>
            <div class="mt-2">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-medium text-gray-900">罗马广场</h3>
                <div class="flex items-center">
                  <i class="fas fa-star text-yellow-400 text-xs"></i>
                  <span class="ml-1 text-xs text-gray-500">4.8</span>
                </div>
              </div>
              <p class="text-sm text-gray-500">2023-06-16</p>
            </div>
          </div>

          <!-- 更多照片... -->
        </div>
      </div>

      <!-- 加载更多按钮 -->
      <div class="flex justify-center mt-8">
        <button
          class="inline-flex items-center px-6 py-3 border border-gray-300 shadow-sm text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
          <i class="fas fa-spinner mr-2"></i>
          加载更多时间段
        </button>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PhotoGrid from '@/components/PhotoGrid.vue'
import { photoApi, type Photo } from '@/api/photos'

const photos = ref<Photo[]>([])
const loading = ref(true)
const error = ref('')

const fetchPhotos = async () => {
  try {
    photos.value = await photoApi.getPhotos()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取照片失败'
  } finally {
    loading.value = false
  }
}

</script>
