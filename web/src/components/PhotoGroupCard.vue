<template>
  <div :id="`month-${group.date_key}`">
    <!-- 分组标题 -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-medium text-primary-600">{{ group.date_key }}</h2>
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-500">共{{ group.photos.length }}张照片</span>
        <button v-if="isSelectMode" @click="$emit('toggleGroupSelection', group.date_key)"
          class="text-sm text-primary-600 hover:text-primary-700">
          {{ isGroupSelected ? '取消全选' : '全选' }}
        </button>
        <button v-if="group.photos.length > 5" @click="$emit('toggleGroup', group.date_key)"
          class="text-sm text-primary-600 hover:text-primary-700">
          <i :class="['fas', isGroupExpanded ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
        </button>
      </div>
    </div>

    <!-- 网格视图 -->
    <div v-if="currentView === 'grid'"
      class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <div v-for="photo in displayPhotos"
        :key="photo.id" class="group relative photo-item" :data-date="photo.taken_time"
        :data-photo-id="photo.id">
        <!-- 选择框 -->
        <div v-if="isSelectMode" class="absolute top-2 left-2 z-10">
          <input type="checkbox" :checked="selectedPhotos.includes(photo.id)"
            @change="$emit('togglePhotoSelection', photo.id)"
            class="w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 checkbox">
        </div>
        <div
          class="w-full md:h-[180px] 2xl:h-[300px] h-[180px] cursor-pointer"
          @click="isSelectMode && $emit('togglePhotoSelection', photo.id)">
          <LazyImage 
            :src="photo.thumbnail_path" 
            :alt="photo.title"
            :class="[isSelectMode && selectedPhotos.includes(photo.id) ? 'brightness-75 p-2' : 'opacity-100', 'w-full h-full object-cover group-hover:opacity-75 transition-opacity'].join(' ')"
            width="100%"
            height="100%"
          />
          <div v-if="!isSelectMode"
            class="absolute inset-0 bg-black bg-opacity-0 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
            <div class="flex space-x-2">
              <button
                :class="['p-2 rounded-full', photo.is_favorite ? 'bg-primary-500 text-white' : 'bg-white text-gray-700 hover:text-gray-900']"
                @click="$emit('toggleFavorite', photo.id)">
                <i class="fas fa-heart"></i>
              </button>
              <button @click.stop="$emit('editPhoto', photo.id)"
                class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
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
    <div v-else-if="currentView === 'masonry'">
      <MasonryGrid 
        :items="group.photos" 
        :gap="16"
        :min-column-width="200"
      >
        <template #default="{ item: photo }">
          <div class="group relative photo-item" 
            :data-date="photo.taken_time"
            :data-photo-id="photo.id">
            <!-- 选择框 -->
            <div v-if="isSelectMode" class="absolute top-2 left-2 z-10">
              <input type="checkbox" :checked="selectedPhotos.includes(Number(photo.id))"
                @change="$emit('togglePhotoSelection', Number(photo.id))"
                class="w-5 h-5 text-primary-600 rounded border-gray-300 focus:ring-primary-500 checkbox">
            </div>
            <div class="rounded-lg overflow-hidden cursor-pointer"
              @click="isSelectMode && $emit('togglePhotoSelection', Number(photo.id))">
              <LazyImage 
                :src="photo.thumbnail_path" 
                :alt="photo.title"
                :class="[isSelectMode && selectedPhotos.includes(Number(photo.id)) ? 'brightness-75 p-2' : 'opacity-100', 'w-full object-cover group-hover:opacity-75 transition-opacity'].join(' ')"
                width="100%"
              />
              <div v-if="!isSelectMode"
                class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity flex items-center justify-center opacity-0 group-hover:opacity-100">
                <div class="flex space-x-2">
                  <button
                    :class="['p-2 rounded-full', photo.is_favorite ? 'bg-primary-500 text-white' : 'bg-white text-gray-700 hover:text-gray-900']"
                    @click="$emit('toggleFavorite', Number(photo.id))">
                    <i class="fas fa-heart"></i>
                  </button>
                  <button @click.stop="$emit('editPhoto', Number(photo.id))"
                    class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="p-2 bg-white rounded-full text-gray-700 hover:text-gray-900">
                    <i class="fas fa-share-alt"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </template>
      </MasonryGrid>
    </div>

    <!-- 列表视图 -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
      <div v-for="photo in displayPhotos"
        :key="photo.id"
        class="flex items-center space-x-3 p-3 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <!-- 选择框 -->
        <div v-if="isSelectMode" class="flex-shrink-0">
          <input type="checkbox" :checked="selectedPhotos.includes(photo.id)"
            @change="$emit('togglePhotoSelection', photo.id)"
            class="w-4 h-4 text-primary-600 rounded border-gray-300 focus:ring-primary-500 checkbox">
        </div>
        <div class="w-16 h-16 flex-shrink-0 cursor-pointer photo-item" :data-photo-id="photo.id"
          @click="isSelectMode && $emit('togglePhotoSelection', photo.id)">
          <LazyImage 
            :src="photo.thumbnail_path" 
            :alt="photo.title"
            :class="[isSelectMode && selectedPhotos.includes(photo.id) ? 'brightness-75' : 'opacity-100', 'w-full h-full object-cover rounded'].join(' ')"
            width="64px"
            height="64px"
          />
        </div>
        <div class="flex-1 min-w-0">
          <h3 class="text-sm font-medium text-gray-900 truncate">{{ photo.title || '未命名照片' }}</h3>
          <p class="text-xs text-gray-500 truncate">{{ formatDate(photo.taken_time || new Date().toISOString()) }}</p>
        </div>
        <div class="flex items-center space-x-1 flex-shrink-0">
          <button
            :class="['p-1.5 rounded-full', photo.is_favorite ? 'bg-primary-500 text-white' : 'bg-gray-100 text-gray-700 hover:text-gray-900']"
            @click="$emit('toggleFavorite', photo.id)">
            <i class="fas fa-heart text-xs"></i>
          </button>
          <button @click.stop="$emit('editPhoto', photo.id)"
            class="p-1.5 bg-gray-100 rounded-full text-gray-700 hover:text-gray-900">
            <i class="fas fa-edit text-xs"></i>
          </button>
          <button class="p-1.5 bg-gray-100 rounded-full text-gray-700 hover:text-gray-900">
            <i class="fas fa-share-alt text-xs"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import LazyImage from '@/components/LazyImage.vue'
import MasonryGrid from '@/components/MasonryGrid.vue'
import type { PhotoGroup } from '@/api/photos'

interface Props {
  group: PhotoGroup
  currentView: 'grid' | 'masonry' | 'list'
  isSelectMode: boolean
  selectedPhotos: number[]
  expandedGroups: Set<string>
}

const props = defineProps<Props>()

defineEmits<{
  toggleGroup: [dateKey: string]
  toggleGroupSelection: [dateKey: string]
  togglePhotoSelection: [photoId: number]
  toggleFavorite: [photoId: number]
  editPhoto: [photoId: number]
}>()

// 计算是否展开
const isGroupExpanded = computed(() => {
  return props.expandedGroups.has(props.group.date_key)
})

// 计算是否全选
const isGroupSelected = computed(() => {
  return props.group.photos.every(photo => props.selectedPhotos.includes(photo.id))
})

// 根据展开状态显示照片
const displayPhotos = computed(() => {
  if (props.currentView === 'masonry') {
    return props.group.photos // 瀑布流总是显示所有照片
  }
  return isGroupExpanded.value ? props.group.photos : props.group.photos.slice(0, 5)
})

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>