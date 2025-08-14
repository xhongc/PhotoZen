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
          <div v-if="!isFullscreen && showInfoPanel" class="w-2/12 p-4 bg-base-100 rounded-lg">
            <!-- 标签页切换 -->
            <div class="border-b border-gray-200 mb-4">
              <nav class="-mb-px flex space-x-8">
                <button 
                  @click="activeTab = 'basic'" 
                  :class="[
                    'py-2 px-1 border-b-2 font-medium text-sm',
                    activeTab === 'basic' 
                      ? 'border-primary-500 text-primary-600' 
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  ]">
                  基本信息
                </button>
                <button 
                  @click="activeTab = 'metadata'"
                  :class="[
                    'py-2 px-1 border-b-2 font-medium text-sm',
                    activeTab === 'metadata' 
                      ? 'border-primary-500 text-primary-600' 
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  ]">
                  元数据
                </button>
              </nav>
            </div>

            <!-- 基本信息标签页 -->
            <div v-show="activeTab === 'basic'" class="space-y-6">
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

            <!-- 元数据标签页 -->
            <div v-show="activeTab === 'metadata'" class="space-y-6">
              <div v-if="metadataLoading" class="text-center py-4">
                <i class="fas fa-spinner fa-spin text-primary-500"></i>
                <p class="text-sm text-gray-500 mt-2">加载元数据...</p>
              </div>

              <div v-else-if="metadata" class="space-y-4">
                <!-- EXIF数据部分 -->
                <div class="border border-gray-200 rounded-lg p-3">
                  <h3 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
                    <i class="fas fa-camera mr-2"></i>
                    EXIF信息
                  </h3>
                  
                  <!-- 相机信息 -->
                  <div v-if="cameraInfo" class="mb-4">
                    <h4 class="text-xs font-medium text-gray-600 mb-2">相机信息</h4>
                    <div class="space-y-1 text-xs">
                      <div><span class="text-gray-500">制造商:</span> {{ cameraInfo.make }}</div>
                      <div><span class="text-gray-500">型号:</span> {{ cameraInfo.model }}</div>
                      <div><span class="text-gray-500">软件:</span> {{ cameraInfo.software }}</div>
                      <div><span class="text-gray-500">镜头:</span> {{ cameraInfo.lens_model }}</div>
                    </div>
                  </div>

                  <!-- 拍摄参数 -->
                  <div v-if="shootingParams" class="mb-4">
                    <h4 class="text-xs font-medium text-gray-600 mb-2">拍摄参数</h4>
                    <div class="space-y-1 text-xs">
                      <div><span class="text-gray-500">光圈:</span> {{ shootingParams.aperture }}</div>
                      <div><span class="text-gray-500">快门:</span> {{ shootingParams.shutter_speed }}</div>
                      <div><span class="text-gray-500">ISO:</span> {{ shootingParams.iso }}</div>
                      <div><span class="text-gray-500">焦距:</span> {{ shootingParams.focal_length }}</div>
                    </div>
                  </div>

                  <!-- GPS坐标 -->
                  <div v-if="gpsCoordinates" class="mb-4">
                    <h4 class="text-xs font-medium text-gray-600 mb-2">GPS坐标</h4>
                    <div class="text-xs">
                      <div><span class="text-gray-500">纬度:</span> {{ gpsCoordinates.latitude.toFixed(6) }}</div>
                      <div><span class="text-gray-500">经度:</span> {{ gpsCoordinates.longitude.toFixed(6) }}</div>
                    </div>
                  </div>

                  <!-- 可编辑EXIF字段 -->
                  <div v-if="editableExifFields.length > 0" class="mb-4">
                    <h4 class="text-xs font-medium text-gray-600 mb-2">可编辑EXIF字段</h4>
                    <div class="space-y-2">
                      <div v-for="field in editableExifFields" :key="field.key" class="flex items-center space-x-2">
                        <span class="text-xs text-gray-500 w-20 truncate" :title="field.name">{{ field.name }}:</span>
                        <input
                          type="text"
                          v-model="field.value"
                          @blur="updateExifField(field.key, String(field.value))"
                          class="flex-1 text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:border-primary-500"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 自定义字段部分 -->
                <div class="border border-gray-200 rounded-lg p-3">
                  <div class="flex items-center justify-between mb-3">
                    <h3 class="text-sm font-medium text-gray-700 flex items-center">
                      <i class="fas fa-tags mr-2"></i>
                      自定义字段
                    </h3>
                    <button 
                      @click="showAddFieldModal = true"
                      class="text-xs text-primary-600 hover:text-primary-700">
                      <i class="fas fa-plus mr-1"></i>添加
                    </button>
                  </div>
                  
                  <div v-if="customFields.length === 0" class="text-xs text-gray-500 text-center py-4">
                    暂无自定义字段
                  </div>
                  
                  <div v-else class="space-y-2">
                    <div v-for="field in customFields" :key="field.key" class="flex items-center space-x-2">
                      <span class="text-xs text-gray-500 w-20 truncate" :title="field.name">{{ field.name }}:</span>
                      <input
                        type="text"
                        v-model="field.value"
                        @blur="updateCustomField(field.key, field.value)"
                        class="flex-1 text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:border-primary-500"
                      />
                      <button 
                        @click="deleteCustomField(field.key)" 
                        class="text-red-500 hover:text-red-700">
                        <i class="fas fa-trash text-xs"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 添加自定义字段的模态框 -->
            <div v-if="showAddFieldModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
              <div class="bg-white rounded-lg p-6 w-96">
                <h3 class="text-lg font-medium mb-4">添加自定义字段</h3>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">字段名称</label>
                    <input 
                      type="text" 
                      v-model="newCustomField.name"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      placeholder="输入字段名称">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">字段键名</label>
                    <input 
                      type="text" 
                      v-model="newCustomField.key"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      placeholder="输入唯一键名">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">字段类型</label>
                    <select 
                      v-model="newCustomField.field_type"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500">
                      <option value="text">文本</option>
                      <option value="number">数字</option>
                      <option value="date">日期</option>
                      <option value="boolean">布尔值</option>
                      <option value="json">JSON</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">字段值</label>
                    <input 
                      type="text" 
                      v-model="newCustomField.value"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                      placeholder="输入初始值">
                  </div>
                </div>
                <div class="flex justify-end space-x-4 mt-6">
                  <button 
                    @click="showAddFieldModal = false"
                    class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                    取消
                  </button>
                  <button 
                    @click="addCustomField"
                    class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-primary-600 hover:bg-primary-700">
                    添加
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  photoApi, 
  type Photo, 
  type PhotoMetadata,
  type CameraInfo,
  type ShootingParameters,
  type GPSCoordinates,
  type CustomFieldData,
  type MetadataField
} from '@/api/photos'
import notify from '@/components/notify'
import type { WebDAVFile } from '@/api/webdav'

const props = defineProps<{
  photo: WebDAVFile | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

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

// 元数据相关状态
const activeTab = ref('basic')
const metadata = ref<PhotoMetadata | null>(null)
const metadataLoading = ref(false)
const cameraInfo = ref<CameraInfo | null>(null)
const shootingParams = ref<ShootingParameters | null>(null)
const gpsCoordinates = ref<GPSCoordinates | null>(null)
const customFields = ref<any[]>([])
const showAddFieldModal = ref(false)
const newCustomField = ref({
  key: '',
  name: '',
  value: '',
  field_type: 'text' as 'text' | 'number' | 'date' | 'boolean' | 'json'
})

// 计算可编辑的EXIF字段
const editableExifFields = computed(() => {
  if (!metadata.value?.exif_data) return []
  return Object.entries(metadata.value.exif_data)
    .filter(([_, field]) => field.editable)
    .map(([key, field]) => ({ key, ...field }))
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
    emit('close')
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

// === 元数据相关功能 ===

// 获取元数据
const fetchMetadata = async () => {
  if (!photo.value) return
  
  try {
    metadataLoading.value = true
    
    // 并行获取所有元数据
    const [metadataData, cameraData, shootingData, gpsData, customData] = await Promise.all([
      photoApi.getMetadata(photo.value.id),
      photoApi.getCameraInfo(photo.value.id).catch(() => null),
      photoApi.getShootingParameters(photo.value.id).catch(() => null),
      photoApi.getGPSCoordinates(photo.value.id).catch(() => null),
      photoApi.getCustomFields(photo.value.id).catch(() => [])
    ])
    
    metadata.value = metadataData
    cameraInfo.value = cameraData
    shootingParams.value = shootingData
    gpsCoordinates.value = gpsData
    customFields.value = customData
    
  } catch (e) {
    console.error('获取元数据失败:', e)
    notify.myMsg.notify({
      content: '获取元数据失败',
      type: 'error',
      time: 2000
    })
  } finally {
    metadataLoading.value = false
  }
}

// 更新EXIF字段
const updateExifField = async (tag: string, value: string) => {
  if (!photo.value) return
  
  try {
    const response = await photoApi.updateExifField(photo.value.id, { tag, value })
    if (response.success) {
      notify.myMsg.notify({
        content: 'EXIF字段更新成功',
        type: 'success',
        time: 2000
      })
      // 重新获取元数据
      fetchMetadata()
    } else {
      throw new Error(response.message)
    }
  } catch (e) {
    console.error('更新EXIF字段失败:', e)
    notify.myMsg.notify({
      content: `更新EXIF字段失败: ${e instanceof Error ? e.message : '未知错误'}`,
      type: 'error',
      time: 3000
    })
  }
}

// 添加自定义字段
const addCustomField = async () => {
  if (!photo.value || !newCustomField.value.key || !newCustomField.value.name) return
  
  try {
    await photoApi.addCustomField(photo.value.id, newCustomField.value)
    
    notify.myMsg.notify({
      content: '自定义字段添加成功',
      type: 'success',
      time: 2000
    })
    
    // 重置表单
    newCustomField.value = {
      key: '',
      name: '',
      value: '',
      field_type: 'text'
    }
    showAddFieldModal.value = false
    
    // 重新获取自定义字段
    fetchMetadata()
    
  } catch (e) {
    console.error('添加自定义字段失败:', e)
    notify.myMsg.notify({
      content: `添加自定义字段失败: ${e instanceof Error ? e.message : '未知错误'}`,
      type: 'error',
      time: 3000
    })
  }
}

// 更新自定义字段
const updateCustomField = async (key: string, value: string) => {
  if (!photo.value) return
  
  try {
    const response = await photoApi.updateCustomField(photo.value.id, key, { value })
    if (response.success) {
      notify.myMsg.notify({
        content: '自定义字段更新成功',
        type: 'success',
        time: 2000
      })
    } else {
      throw new Error(response.message)
    }
  } catch (e) {
    console.error('更新自定义字段失败:', e)
    notify.myMsg.notify({
      content: `更新自定义字段失败: ${e instanceof Error ? e.message : '未知错误'}`,
      type: 'error',
      time: 3000
    })
  }
}

// 删除自定义字段
const deleteCustomField = async (key: string) => {
  if (!photo.value) return
  
  try {
    const response = await photoApi.deleteCustomField(photo.value.id, key)
    if (response.success) {
      notify.myMsg.notify({
        content: '自定义字段删除成功',
        type: 'success',
        time: 2000
      })
      // 重新获取自定义字段
      fetchMetadata()
    } else {
      throw new Error(response.message)
    }
  } catch (e) {
    console.error('删除自定义字段失败:', e)
    notify.myMsg.notify({
      content: `删除自定义字段失败: ${e instanceof Error ? e.message : '未知错误'}`,
      type: 'error',
      time: 3000
    })
  }
}

// 监听路由参数变化
watch(() => route.params.id, () => {
  fetchPhoto()
  fetchPhotos()
})

// 监听activeTab变化，切换到元数据标签时获取元数据
watch(() => activeTab.value, (newTab) => {
  if (newTab === 'metadata' && photo.value && !metadata.value) {
    fetchMetadata()
  }
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