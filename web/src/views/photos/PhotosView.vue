<template>
  <!-- 主内容区 -->
  <main class="h-screen-header overflow-y-auto" ref="photoView">
    <!-- 筛选工具栏 -->
    <div class="border-b border-base-200">
      <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8 pt-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <!-- 时间筛选 -->
            <div class="relative ml-8">
              <input type="date" v-model="filters.time_filter"
                class="block pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md" />
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <i class="fas fa-calendar text-gray-400"></i>
              </div>
            </div>
          </div>

          <div class="flex items-center space-x-4">
            <!-- 视图切换 -->
            <div class="flex items-center space-x-2 border-l border-gray-200 pl-4">
              <button @click="handleViewChange('grid')"
                :class="['p-2', currentView === 'grid' ? 'text-primary-600' : 'text-gray-400 hover:text-gray-500']">
                <i class="fas fa-th-large"></i>
              </button>
              <button @click="handleViewChange('masonry')"
                :class="['p-2', currentView === 'masonry' ? 'text-primary-600' : 'text-gray-400 hover:text-gray-500']">
                <i class="fas fa-th"></i>
              </button>
              <button @click="handleViewChange('list')"
                :class="['p-2', currentView === 'list' ? 'text-primary-600' : 'text-gray-400 hover:text-gray-500']">
                <i class="fas fa-list"></i>
              </button>
            </div>
            <!-- 选择模式切换 -->
            <button @click="toggleSelectMode"
              :class="['p-2', isSelectMode ? 'text-primary-600' : 'text-gray-400 hover:text-gray-500']">
              <i class="fas fa-check-square"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 批量操作工具栏 -->
    <div v-if="isSelectMode" class="bg-white border-b border-gray-200 fixed top-3 left-0 right-0 z-10 rounded-xl">
      <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-600">已选择 {{ selectedPhotos.length }} 张照片</span>
            <button @click="selectAll" class="text-sm text-primary-600 hover:text-primary-700">
              {{ isAllSelected ? '取消全选' : '全选' }}
            </button>
          </div>
          <div class="flex items-center space-x-2">
              <button @click="batchAddToFavorites" class="px-3 py-1 bg-neutral-content text-neutral rounded-md">
              <i class="fas fa-heart mr-1"></i>添加到收藏
            </button>
            <button @click="batchAddToAlbum" class="px-3 py-1 bg-neutral-content text-neutral rounded-md">
              <i class="fas fa-folder-plus mr-1"></i>添加到相册
            </button>
            <button @click="batchDelete" class="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600">
              <i class="fas fa-trash mr-1"></i>删除
            </button>
            <button @click="toggleSelectMode" class="px-3 py-1 bg-neutral-content text-neutral rounded-md">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex">
      <!-- 照片墙 -->
      <div class="flex-1 px-4 sm:px-6 lg:px-8 py-8">
        <div class="max-w-7xl mx-auto">
          <template v-if="loading">
            <div class="flex justify-center items-center h-64">
              <i class="fas fa-spinner fa-spin text-4xl text-primary-500"></i>
            </div>
          </template>

          <template v-else-if="error">
            <div class="text-center text-red-500 py-8">
              {{ error }}
            </div>
          </template>

          <template v-else>
            <div v-for="(item, index) in photos" :key="index" :id="`month-${index}`" class="mb-12">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-medium text-primary-600">{{ item.date_key }}</h2>
                <div class="flex items-center space-x-2">
                  <span class="text-sm text-gray-500">共{{ item.photos.length }}张照片</span>
                  <button v-if="isSelectMode" @click="toggleGroupSelection(item.date_key)"
                    class="text-sm text-primary-600 hover:text-primary-700">
                    {{ isGroupSelected(item.date_key) ? '取消全选' : '全选' }}
                  </button>
                  <button v-if="item.photos.length > 5" @click="toggleGroup(item.date_key)"
                    class="text-sm text-primary-600 hover:text-primary-700">
                    <i :class="['fas', isGroupExpanded(item.date_key) ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
                  </button>
                </div>
              </div>

              <!-- 网格视图 -->
              <div v-if="currentView === 'grid'"
                class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                <div v-for="photo in (isGroupExpanded(item.date_key) ? item.photos : item.photos.slice(0, 5))"
                  :key="photo.id" class="group relative photo-item" :data-date="photo.taken_time" :data-photo-id="photo.id">
                  <!-- 选择框 -->
                  <div v-if="isSelectMode" class="absolute top-2 left-2 z-10">
                    <input type="checkbox" 
                      v-model="selectedPhotos" 
                      :value="photo.id"
                      class="w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 checkbox">
                  </div>
                  <div class="aspect-w-1 aspect-h-1 bg-gray-200 rounded-lg overflow-hidden cursor-pointer"
                    @click="isSelectMode && togglePhotoSelection(photo.id)">
                    <img :src="photo.thumbnail_path" :alt="photo.title"
                      :class="[isSelectMode && selectedPhotos.includes(photo.id) ? 'opacity-75' : 'opacity-100', 'w-full h-full object-cover group-hover:opacity-75 transition-opacity']">
                    <div
                      v-if="!isSelectMode"
                      class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
                      <div class="flex space-x-2">
                        <button
                          :class="['p-2 rounded-full', photo.is_favorite ? 'bg-primary-500 text-white' : 'bg-white text-gray-700 hover:text-gray-900']">
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
                </div>
              </div>

              <!-- 瀑布流视图 -->
              <div v-else-if="currentView === 'masonry'" class="columns-2 sm:columns-3 md:columns-4 lg:columns-5 gap-4">
                <div v-for="photo in item.photos" :key="photo.id"
                  class="group relative photo-item mb-4 break-inside-avoid" :data-date="photo.taken_time" :data-photo-id="photo.id">
                  <!-- 选择框 -->
                  <div v-if="isSelectMode" class="absolute top-2 left-2 z-10">
                    <input type="checkbox" 
                      v-model="selectedPhotos" 
                      :value="photo.id"
                      class="w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 checkbox">
                  </div>
                  <div class="bg-gray-200 rounded-lg overflow-hidden cursor-pointer"
                    @click="isSelectMode && togglePhotoSelection(photo.id)">
                    <img :src="photo.thumbnail_path" :alt="photo.title"
                      :class="[isSelectMode && selectedPhotos.includes(photo.id) ? 'opacity-75' : 'opacity-100', 'w-full object-cover group-hover:opacity-75 transition-opacity']">
                    <div
                      v-if="!isSelectMode"
                      class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
                      <div class="flex space-x-2">
                        <button
                          :class="['p-2 rounded-full', photo.is_favorite ? 'bg-primary-500 text-white' : 'bg-white text-gray-700 hover:text-gray-900']">
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
                </div>
              </div>

              <!-- 列表视图 -->
              <div v-else class="space-y-4">
                <div v-for="photo in (isGroupExpanded(item.date_key) ? item.photos : item.photos.slice(0, 5))"
                  :key="photo.id"
                  class="flex items-center space-x-4 p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
                  <!-- 选择框 -->
                  <div v-if="isSelectMode" class="flex items-center space-x-2">
                    <input type="checkbox" 
                      v-model="selectedPhotos" 
                      :value="photo.id"
                      class="w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 checkbox">
                  </div>
                  <div class="w-24 h-24 flex-shrink-0 cursor-pointer photo-item" 
                    :data-photo-id="photo.id"
                    @click="isSelectMode && togglePhotoSelection(photo.id)">
                    <img :src="photo.thumbnail_path" 
                      :alt="photo.title" 
                      :class="[isSelectMode && selectedPhotos.includes(photo.id) ? 'opacity-75' : 'opacity-100', 'w-full h-full object-cover rounded']">
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-medium text-gray-900">{{ photo.title || '未命名照片' }}</h3>
                    <p class="text-sm text-gray-500">{{ formatDate(photo.taken_time || new Date().toISOString()) }}</p>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button
                      :class="['p-2 rounded-full', photo.is_favorite ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-700 hover:text-gray-900']">
                      <i class="fas fa-heart"></i>
                    </button>
                    <button class="p-2 bg-gray-100 rounded-full text-gray-700 hover:text-gray-900">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="p-2 bg-gray-100 rounded-full text-gray-700 hover:text-gray-900">
                      <i class="fas fa-share-alt"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 加载更多提示 -->
    <div v-if="hasMore" class="flex justify-center items-center py-4">
      <div v-if="isLoadingMore" class="flex items-center space-x-2">
        <i class="fas fa-spinner fa-spin text-primary-500"></i>
        <span class="text-gray-500">加载更多...</span>
      </div>
    </div>
    <button
            v-if="curScrollTop > 700"
            @click="scrollToTop"
            class="fixed bottom-8 right-8 bg-neutral-content hover:bg-accent hover: text-accent-content text-neutral font-bold py-2 px-4 rounded-full shadow-xl transition-colors duration-300"
        >
            <svg t="1730534469934" class="icon h-5 w-5 fill-current" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2399" width="200" height="200"><path d="M890.5 755.3L537.9 269.2c-12.8-17.6-39-17.6-51.7 0L133.5 755.3c-3.8 5.3-0.1 12.7 6.5 12.7h75c5.1 0 9.9-2.5 12.9-6.6L512 369.8l284.1 391.6c3 4.1 7.8 6.6 12.9 6.6h75c6.5 0 10.3-7.4 6.5-12.7z" p-id="2400"></path></svg>
        </button>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import PhotoGrid from '@/components/PhotoGrid.vue'
import { photoApi, type Photo, type PhotoListParams, type PhotoGroup } from '@/api/photos'

const photos = ref<PhotoGroup[]>([])
const loading = ref(true)
const error = ref('')
const selectedDate = ref('')
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth() + 1)
const months = ref<Array<{ year: number; month: number; id: string }>>([])
const hoveredMonth = ref<{ year: number; month: number } | null>(null)
const tooltipVisible = ref(false)
const tooltipPosition = ref({ x: 0, y: 0 })
const tooltipContent = ref('')
const expandedGroups = ref<Set<string>>(new Set())
const currentView = ref<'grid' | 'masonry' | 'list'>('grid')
const photoView = ref<HTMLElement | null>(null)
const curScrollTop = ref(0)

// 分页相关
const page = ref(1)
const pageSize = ref(50)
const hasMore = ref(true)
const isLoadingMore = ref(false)

// 筛选条件
const filters = ref<PhotoListParams>({
  time_filter: '',
  start_date: undefined,
  end_date: undefined,
  tags: [],
  location: '',
  favorites_only: false,
  sort_by: '-taken_time',
  page: 1,
  page_size: 20,
  group_by: 'day'
})

// 选择模式相关
const isSelectMode = ref(false)
const selectedPhotos = ref<number[]>([])
const isMouseDown = ref(false)
const isSelecting = ref(false)

// 获取照片列表
const fetchPhotos = async (isLoadMore = false) => {
  try {
    if (!isLoadMore) {
      loading.value = true
    } else {
      isLoadingMore.value = true
    }

    const response = await photoApi.getPhotos({
      ...filters.value,
      page: page.value,
      page_size: pageSize.value
    })

    if (isLoadMore) {
      // 合并新的照片数据
      photos.value = [...photos.value, ...response]
    } else {
      photos.value = response
      // 默认收起所有分组
      expandedGroups.value = new Set()
    }
    let resp_length = 0
    response.forEach(item => {
      resp_length += item.photos.length
    })
    console.log(resp_length, pageSize.value)
    // 判断是否还有更多数据
    hasMore.value = resp_length === pageSize.value
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取照片失败'
  } finally {
    loading.value = false
    isLoadingMore.value = false
  }
}
// 切换视图
const handleViewChange = (view: 'grid' | 'masonry' | 'list') => {
  currentView.value = view
  if (view === 'grid') {
    filters.value.group_by = 'day'
  } else if (view === 'masonry') {
    filters.value.group_by = 'month'
  } else {
  }
}
// 处理滚动加载
const handleScroll = () => {
  const scrollHeight = photoView.value?.scrollHeight || 0
  const scrollTop = photoView.value?.scrollTop || 0
  const clientHeight = photoView.value?.clientHeight || 0
  curScrollTop.value = scrollTop
  // 当滚动到距离底部100px时触发加载
  if (scrollTop + clientHeight >= scrollHeight - 50) {
    if (hasMore.value && !isLoadingMore.value) {
      page.value++
      fetchPhotos(true)
    }
  }
}
const scrollToTop = () => {
  photoView.value?.scrollTo({ top: 0, behavior: 'smooth' })
}
// 监听滚动事件
onMounted(() => {
  fetchPhotos()
  photoView.value?.addEventListener('scroll', handleScroll)
  window.addEventListener('mousedown', handleMouseDown)
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseup', handleMouseUp)
})

// 组件卸载时移除滚动监听
onUnmounted(() => {
  photoView.value?.removeEventListener('scroll', handleScroll)
  window.removeEventListener('mousedown', handleMouseDown)
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseup', handleMouseUp)
})

// 重置分页
const resetPagination = () => {
  page.value = 1
  hasMore.value = true
  photos.value = []
}

// 修改应用筛选条件的逻辑
const applyFilters = async () => {
  resetPagination()
  await fetchPhotos()
}

// 监听筛选条件变化
watch(filters, () => {
  applyFilters()
}, { deep: true })

// 切换分组展开状态
const toggleGroup = (dateKey: string) => {
  if (expandedGroups.value.has(dateKey)) {
    expandedGroups.value.delete(dateKey)
  } else {
    expandedGroups.value.add(dateKey)
  }
}

// 检查分组是否展开
const isGroupExpanded = (dateKey: string) => {
  return expandedGroups.value.has(dateKey)
}

// 判断是否显示年份标记
const shouldShowYear = (dateKey: string, index: number) => {
  if (index === 0) return true;
  const currentYear = getYear(dateKey);
  const prevYear = getYear(photos.value[index - 1].date_key);
  return currentYear !== prevYear;
}

// 从日期字符串中提取年份
const getYear = (dateKey: string) => {
  return dateKey.split('-')[0];
}

// 格式化日期为年月格式
const formatDateToYearMonth = (dateKey: string) => {
  const date = new Date(dateKey)
  return `${date.getFullYear()}年${date.getMonth() + 1}月`
}

// 滚动到指定月份
const scrollToMonth = (dateKey: string) => {
  const monthElement = document.getElementById(`month-${photos.value.findIndex(item => item.date_key === dateKey)}`)
  if (monthElement) {
    monthElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 切换选择模式
const toggleSelectMode = () => {
  isSelectMode.value = !isSelectMode.value
  if (!isSelectMode.value) {
    selectedPhotos.value = []
  }
}

// 全选/取消全选
const isAllSelected = computed(() => {
  return photos.value.length > 0 && selectedPhotos.value.length === photos.value.reduce((acc, group) => acc + group.photos.length, 0)
})

const selectAll = () => {
  if (isAllSelected.value) {
    selectedPhotos.value = []
  } else {
    selectedPhotos.value = photos.value.flatMap(group => group.photos.map(photo => photo.id))
  }
}

// 批量操作
const batchAddToFavorites = async () => {
  try {
    // 为每个选中的照片调用 toggleFavorite
    await Promise.all(selectedPhotos.value.map(id => photoApi.toggleFavorite(id)))
    // 更新本地状态
    photos.value.forEach(group => {
      group.photos.forEach(photo => {
        if (selectedPhotos.value.includes(photo.id)) {
          photo.is_favorite = true
        }
      })
    })
    // 退出选择模式
    isSelectMode.value = false
    selectedPhotos.value = []
  } catch (error) {
    console.error('添加到收藏失败:', error)
  }
}

const batchAddToAlbum = async () => {
  // TODO: 实现添加到相册的功能
  console.log('添加到相册:', selectedPhotos.value)
}

const batchDelete = async () => {
  if (!confirm(`确定要删除选中的 ${selectedPhotos.value.length} 张照片吗？`)) {
    return
  }
  try {
    // 为每个选中的照片调用 deletePhoto
    await Promise.all(selectedPhotos.value.map(id => photoApi.deletePhoto(id)))
    // 更新本地状态
    photos.value = photos.value.map(group => ({
      ...group,
      photos: group.photos.filter(photo => !selectedPhotos.value.includes(photo.id))
    })).filter(group => group.photos.length > 0)
    // 退出选择模式
    isSelectMode.value = false
    selectedPhotos.value = []
  } catch (error) {
    console.error('删除照片失败:', error)
  }
}

// 检查分组是否被全选
const isGroupSelected = (dateKey: string) => {
  const group = photos.value.find(item => item.date_key === dateKey)
  if (!group) return false
  return group.photos.every(photo => selectedPhotos.value.includes(photo.id))
}

// 切换分组选择状态
const toggleGroupSelection = (dateKey: string) => {
  const group = photos.value.find(item => item.date_key === dateKey)
  if (!group) return

  if (isGroupSelected(dateKey)) {
    // 取消全选：从选中列表中移除该分组的所有照片
    selectedPhotos.value = selectedPhotos.value.filter(id => 
      !group.photos.some(photo => photo.id === id)
    )
  } else {
    // 全选：添加该分组的所有照片到选中列表
    const groupPhotoIds = group.photos.map(photo => photo.id)
    selectedPhotos.value = [...new Set([...selectedPhotos.value, ...groupPhotoIds])]
  }
}

// 切换单张照片的选中状态
const togglePhotoSelection = (photoId: number) => {
  const index = selectedPhotos.value.indexOf(photoId)
  if (index === -1) {
    selectedPhotos.value.push(photoId)
  } else {
    selectedPhotos.value.splice(index, 1)
  }
}

// 鼠标事件处理
const handleMouseDown = (e: MouseEvent) => {
  if (!isSelectMode.value) return
  isMouseDown.value = true
  isSelecting.value = true
  // 如果点击的是图片，则切换该图片的选中状态
  const target = e.target as HTMLElement
  const photoItem = target.closest('.photo-item')
  if (photoItem) {
    const photoId = Number(photoItem.getAttribute('data-photo-id'))
    if (!isNaN(photoId)) {
      togglePhotoSelection(photoId)
    }
  }
}

const handleMouseMove = (e: MouseEvent) => {
  if (!isMouseDown.value || !isSelecting.value) return
  
  const target = e.target as HTMLElement
  const photoItem = target.closest('.photo-item')
  if (photoItem) {
    const photoId = Number(photoItem.getAttribute('data-photo-id'))
    if (!isNaN(photoId)) {
      // 如果照片未被选中，则选中它
      if (!selectedPhotos.value.includes(photoId)) {
        selectedPhotos.value.push(photoId)
      }
    }
  }
}

const handleMouseUp = () => {
  isMouseDown.value = false
  isSelecting.value = false
}
</script>

<style scoped>
.time-segment {
  transition: height 0.3s ease;
}

.time-segment:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* 全局禁用文本选择 */
* {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

/* 只允许照片项接收鼠标事件 */
.photo-item {
  pointer-events: auto;
}

/* 照片项内的所有元素都禁用鼠标事件 */
.photo-item * {
  pointer-events: none;
}

/* 允许复选框接收鼠标事件 */
.checkbox {
  pointer-events: auto;
}

/* 允许按钮接收鼠标事件 */
button {
  pointer-events: auto;
}

/* 允许输入框接收鼠标事件 */
input {
  pointer-events: auto;
}
</style>
