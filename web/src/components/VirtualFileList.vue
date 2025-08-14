<template>
  <SimpleVirtualList 
    :items="files"
    :item-height="itemHeight"
    :get-key="(index) => files[index]?.path || index"
  >
    <template #default="{ item: file }">
      <div class="hover:bg-base-200 transition-colors"
           :class="{ 'bg-base-200': file.path === currentPreviewPath }" 
           @click="$emit('fileClick', file)"
           :data-file-path="file.path">
        
        <!-- 列表视图 -->
        <div v-if="viewMode === 'list'" class="flex items-center px-6 py-4 border-b border-base-200">
          <!-- 名称列 (5/12) -->
          <div class="w-5/12 flex items-center">
            <i v-if="file.type === 'directory'" class="fas fa-folder text-yellow-400 mr-3"></i>
            <LazyImage v-else-if="file.mime.startsWith('image/')" :src="file.url"
              class="w-8 h-8 rounded object-cover mr-3" width="32" height="32" 
              quality="low" :priority="false" />
            <span class="text-sm text-primary-600 truncate">{{ file.basename }}</span>
          </div>
          <!-- 修改日期列 (2/12) -->
          <div class="w-2/12 text-sm text-gray-500">{{ formatDate(file.lastmod) }}</div>
          <!-- 类型列 (2/12) -->
          <div class="w-2/12 text-sm text-gray-500">{{ file.type === 'directory' ? '文件夹' : file.mime }}</div>
          <!-- 大小列 (2/12) -->
          <div class="w-2/12 text-sm text-gray-500">{{ formatFileSize(file.size) }}</div>
          <!-- 操作列 (1/12) -->
          <div class="w-1/12 text-right">
            <button class="text-gray-400 hover:text-gray-500" @click.stop="$emit('delete', file.path)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>

        <!-- 网格视图 -->
        <div v-else class="p-4">
          <div class="bg-base-100 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow cursor-pointer"
               :class="{ 'bg-base-200': file.path === currentPreviewPath }">
            <div class="aspect-square mb-2 flex items-center justify-center">
              <i v-if="file.type === 'directory'" class="fas fa-folder text-yellow-400 text-4xl"></i>
              <LazyImage v-else-if="file.mime.startsWith('image/')" :src="file.url"
                class="w-full h-full object-cover rounded" 
                quality="medium" :priority="false" />
            </div>
            <div class="text-sm font-medium text-primary-600 truncate">{{ file.basename }}</div>
            <div class="text-xs text-gray-500">{{ formatDate(file.lastmod) }}</div>
          </div>
        </div>
      </div>
    </template>
  </SimpleVirtualList>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SimpleVirtualList from './SimpleVirtualList.vue'
import LazyImage from './LazyImage.vue'
import type { WebDAVFile } from '@/api/webdav'

interface Props {
  files: WebDAVFile[]
  viewMode: 'list' | 'grid'
  currentPreviewPath: string
}

const props = defineProps<Props>()

defineEmits<{
  fileClick: [file: WebDAVFile]
  delete: [path: string]
}>()

// 根据视图模式动态计算行高
const itemHeight = computed(() => {
  return props.viewMode === 'list' ? 60 : 200 // 列表视图60px，网格视图200px
})

// 格式化文件大小
const formatFileSize = (size: number) => {
  if (size === 0) return '--'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let index = 0
  while (size >= 1024 && index < units.length - 1) {
    size /= 1024
    index++
  }
  return `${size.toFixed(1)} ${units[index]}`
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>