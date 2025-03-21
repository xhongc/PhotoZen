<template>
  <div class="mx-auto px-4 py-4 h-screen-header">
    <div class="max-w-full mx-auto">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <button @click="router.back()" class="text-gray-500 hover:text-gray-700 mr-2">
          <i class="fas fa-arrow-left"></i>
        </button>
        <h1 class="text-xl font-bold">编辑照片</h1>
        </div>
        <!-- 功能栏 -->
        <div class="flex items-center space-x-4">
          <!-- 信息 -->
          <button @click="toggleInfoPanel" class="text-gray-400 hover:text-gray-700 p-2 rounded-full focus:outline-none">
            <i class="fas fa-info-circle"></i>
          </button>
          <!-- 收藏 -->
          <button class="text-gray-400 hover:text-gray-700 p-2 rounded-full focus:outline-none">
            <i class="fas fa-star"></i>
          </button>
          <!-- 复制 -->
          <button @click="copyToClipboard" class="text-gray-400 hover:text-gray-700 p-2 rounded-full focus:outline-none">
            <i class="fas fa-copy"></i>
          </button>
          <!-- 删除 -->
          <button class="text-gray-400 hover:text-gray-700 p-2 rounded-full focus:outline-none">
            <i class="fas fa-trash-alt"></i>
          </button>
          <!-- 下载 -->
          <button class="text-gray-400 hover:text-gray-700 p-2 rounded-full focus:outline-none">
            <i class="fas fa-download"></i>
          </button>
          <!-- 分享 -->
          <button class="text-gray-400 hover:text-gray-700 p-2 rounded-full focus:outline-none">
            <i class="fas fa-share-alt"></i>
          </button>
          <!-- 全屏 -->
          <button @click="toggleFullscreen" class="text-gray-400 hover:text-gray-700 p-2 rounded-full focus:outline-none">
            <i :class="isFullscreen ? 'fas fa-compress' : 'fas fa-expand'"></i>
          </button>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center items-center h-64">
        <i class="fas fa-spinner fa-spin text-4xl text-primary-500"></i>
      </div>

      <div v-else-if="error" class="text-center text-red-500 py-8">
        {{ error }}
      </div>

      <div v-else class="rounded-lg shadow p-2">
        <!-- 复制成功提示 -->
        <div v-if="copySuccess" class="fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50">
          已复制到剪贴板
        </div>
        <div class="flex" :class="{ 'fixed inset-0 z-50 bg-black': isFullscreen }">
          <!-- 左侧：照片预览 -->
          <div class="flex-1 relative" :class="{ 'w-full': isFullscreen }">
            <!-- 上一张按钮 -->
            <button @click="navigatePhoto('prev')" 
              class="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-75 focus:outline-none">
              <i class="fas fa-chevron-left"></i>
            </button>
            
            <div class="flex justify-center items-center h-full">
              <img :src="photo?.file_path" :alt="photo?.title" 
                class="w-auto h-screen-2header rounded-lg object-fit"
                :class="{ 'h-screen': isFullscreen }">
            </div>

            <!-- 下一张按钮 -->
            <button @click="navigatePhoto('next')"
              class="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-75 focus:outline-none">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>

          <!-- 右侧：编辑表单 -->
          <div v-if="!isFullscreen && showInfoPanel" class="space-y-6 w-2/12 p-4 bg-base-100 rounded-lg">
            <div>
              <label class="block text-sm font-medium text-gray-700">标题</label>
              <input type="text" v-model="form.title"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">描述</label>
              <textarea v-model="form.description" rows="3"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">拍摄时间</label>
              <input type="datetime-local" v-model="form.taken_time"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500">
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">标签</label>
              <div class="mt-1 flex flex-wrap gap-2">
                <span v-for="tag in form.tags" :key="tag"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                  {{ tag }}
                  <button @click="removeTag(tag)" class="ml-1 text-primary-600 hover:text-primary-800">
                    <i class="fas fa-times"></i>
                  </button>
                </span>
                <input type="text" v-model="newTag" @keyup.enter="addTag" placeholder="添加标签"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500">
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">位置</label>
              <input type="text" v-model="form.location"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500">
            </div>

            <div class="flex items-center">
              <input type="checkbox" v-model="form.is_favorite"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded">
              <label class="ml-2 block text-sm text-gray-900">添加到收藏</label>
            </div>

            <div class="flex justify-end space-x-4">
              <button @click="router.back()"
                class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                取消
              </button>
              <button @click="savePhoto"
                class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                保存
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted, getCurrentInstance } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { photoApi, type Photo } from '@/api/photos'
import notify from '@/components/notify'

const route = useRoute()
const router = useRouter()
const photo = ref<Photo | null>(null)
const loading = ref(true)
const error = ref('')
const newTag = ref('')
const photos = ref<Photo[]>([])
const currentIndex = ref(0)
const isFullscreen = ref(false)
const showInfoPanel = ref(true)
const copySuccess = ref(false)

const form = ref({
  title: '',
  description: '',
  taken_time: '',
  tags: [] as string[],
  location: '',
  is_favorite: false
})

// 获取照片详情
const fetchPhoto = async () => {
  try {
    loading.value = true
    const photoId = Number(route.params.id)
    photo.value = await photoApi.getPhoto(photoId)
    // 填充表单数据
    if (photo.value) {
      form.value = {
        title: photo.value.title || '',
        description: photo.value.description || '',
        taken_time: photo.value.taken_time || '',
        tags: photo.value.tags.map(tag => tag.name),
        location: typeof photo.value.location === 'string' ? photo.value.location : photo.value.location?.name || '',
        is_favorite: photo.value.is_favorite || false
      }
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取照片失败'
  } finally {
    loading.value = false
  }
}

// 获取照片列表
const fetchPhotos = async () => {
  try {
    const photoGroups = await photoApi.getPhotos()
    // 将所有照片展平到一个数组中
    photos.value = photoGroups.flatMap(group => group.photos)
    // 找到当前照片的索引
    const photoId = Number(route.params.id)
    currentIndex.value = photos.value.findIndex(p => p.id === photoId)
  } catch (e) {
    console.error('获取照片列表失败:', e)
  }
}

// 导航到上一张或下一张照片
const navigatePhoto = (direction: 'prev' | 'next') => {
  if (direction === 'prev' && currentIndex.value > 0) {
    currentIndex.value--
  } else if (direction === 'next' && currentIndex.value < photos.value.length - 1) {
    currentIndex.value++
  } else {
    return
  }
  
  const nextPhoto = photos.value[currentIndex.value]
  router.push(`/photos/${nextPhoto.id}/edit`)
}

// 添加标签
const addTag = () => {
  if (newTag.value.trim() && !form.value.tags.includes(newTag.value.trim())) {
    form.value.tags.push(newTag.value.trim())
    newTag.value = ''
  }
}

// 移除标签
const removeTag = (tag: string) => {
  form.value.tags = form.value.tags.filter(t => t !== tag)
}

// 保存照片
const savePhoto = async () => {
  try {
    if (!photo.value) return
    await photoApi.updatePhoto(photo.value.id, form.value)
    router.back()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '保存照片失败'
  }
}

// 切换全屏
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
    isFullscreen.value = true
  } else {
    document.exitFullscreen()
    isFullscreen.value = false
  }
}

// 监听全屏变化
const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement
}

// 切换信息面板
const toggleInfoPanel = () => {
  showInfoPanel.value = !showInfoPanel.value
}

// 复制到剪贴板
const copyToClipboard = async () => {
  try {
    if (!photo.value?.file_path) return
    // 通过后端 API 获取图片数据
    const response = await photoApi.getPhotoFile(photo.value.id)
    const blob = response
    
    // 创建 ClipboardItem
    const clipboardItem = new ClipboardItem({
      [blob.type]: blob
    })
    
    // 写入剪贴板
    await navigator.clipboard.write([clipboardItem])
    
    // 显示成功通知
    notify.myMsg.notify({
      content: '图片已复制到剪贴板',
      type: 'success',
      time: 4000
    })
  } catch (e) {
    console.error('复制失败:', e)
    // 显示错误通知
    notify.myMsg.notify({
      content: '复制失败，请重试',
      type: 'error',
      time: 2000
    })
  }
}

// 监听路由参数变化
watch(() => route.params.id, () => {
  fetchPhoto()
  fetchPhotos()
})

onMounted(() => {
  fetchPhoto()
  fetchPhotos()
  document.addEventListener('fullscreenchange', handleFullscreenChange)
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
})
</script>