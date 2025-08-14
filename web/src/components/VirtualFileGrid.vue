<template>
  <div style="height: 100%; display: flex; flex-direction: column;">
    <div style="flex: 1; min-height: 0; padding: 24px;">
      <SimpleVirtualList 
        :items="chunkedFiles"
        :item-height="240"
        :get-key="(index) => `row-${index}`"
      >
        <template #default="{ item: rowFiles }">
          <div class="grid grid-cols-4 gap-4 mb-4">
            <div v-for="file in rowFiles" :key="file.path"
              class="bg-base-100 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow cursor-pointer"
              :class="{ 'bg-base-200': file.path === currentPreviewPath }" 
              @click="$emit('fileClick', file)"
              :data-file-path="file.path">
              <div class="aspect-square mb-2 flex items-center justify-center">
                <i v-if="file.type === 'directory'" class="fas fa-folder text-yellow-400 text-4xl"></i>
                <LazyImage v-else-if="file.mime.startsWith('image/')" :src="file.url"
                  class="w-full h-full object-cover rounded" 
                  quality="medium" :priority="false" />
              </div>
              <div class="text-sm font-medium text-primary-600 truncate">{{ file.basename }}</div>
              <div class="text-xs text-gray-500">{{ formatDate(file.lastmod) }}</div>
            </div>
            <!-- 补齐空白格子 -->
            <div v-for="n in (4 - rowFiles.length)" :key="`empty-${n}`" class="invisible"></div>
          </div>
        </template>
      </SimpleVirtualList>
    </div>
    
    <!-- 状态栏 -->
    <div class="bg-base-100 border-t border-base-200 px-6 py-3 text-sm text-gray-500" style="flex-shrink: 0;">
      共 {{ files.length }} 个项目（{{ files.filter(f => f.type === 'directory').length }} 个文件夹，{{ files.filter(f => f.type === 'file').length }} 个文件）
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SimpleVirtualList from './SimpleVirtualList.vue'
import LazyImage from './LazyImage.vue'
import type { WebDAVFile } from '@/api/webdav'

interface Props {
  files: WebDAVFile[]
  currentPreviewPath: string
}

const props = defineProps<Props>()

defineEmits<{
  fileClick: [file: WebDAVFile]
}>()

// 将文件按每行4个分组，用于网格布局的虚拟滚动
const chunkedFiles = computed(() => {
  const chunks = []
  for (let i = 0; i < props.files.length; i += 4) {
    chunks.push(props.files.slice(i, i + 4))
  }
  return chunks
})

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>