<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-opacity-75 bg-base-100" @click="close">
    <!-- 上一张/下一张按钮 - 固定在屏幕两侧 -->
    <button v-if="imageList?.length > 1" 
      class="fixed left-4 top-1/2 -translate-y-1/2 text-white hover:text-gray-300 bg-black bg-opacity-30 p-3 rounded-full z-50"
      @click.stop="prevImage">
      <i class="fas fa-chevron-left text-3xl"></i>
    </button>
    <button v-if="imageList?.length > 1"
      class="fixed right-4 top-1/2 -translate-y-1/2 text-white hover:text-gray-300 bg-black bg-opacity-30 p-3 rounded-full z-50"
      @click.stop="nextImage">
      <i class="fas fa-chevron-right text-3xl"></i>
    </button>

    <!-- 图片容器 -->
    <div class="relative max-w-4xl max-h-[90vh]">
      <img :src="currentImageUrl" class="max-w-full max-h-[90vh] object-contain" alt="预览图片">
      
      <!-- 关闭按钮 -->
      <button class="absolute top-4 right-4 text-white hover:text-gray-300" @click="close">
        <i class="fas fa-times text-2xl"></i>
      </button>

      <!-- 图片计数器 -->
      <div v-if="imageList?.length > 1" class="absolute bottom-4 left-1/2 -translate-x-1/2 text-white bg-black bg-opacity-30 px-3 py-1 rounded-full text-sm">
        {{ (currentIndex ?? 0) + 1 }} / {{ imageList.length }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  show: boolean
  imageUrl: string
  imageList?: string[]
  currentIndex?: number
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'update:currentIndex', value: number): void
}>()

// 计算当前图片URL
const currentImageUrl = computed(() => {
  if (props.imageList && props.currentIndex !== undefined) {
    return props.imageList[props.currentIndex]
  }
  return props.imageUrl
})

// 上一张图片
const prevImage = () => {
  if (!props.imageList || props.currentIndex === undefined) return
  const newIndex = props.currentIndex > 0 ? props.currentIndex - 1 : props.imageList.length - 1
  emit('update:currentIndex', newIndex)
}

// 下一张图片
const nextImage = () => {
  if (!props.imageList || props.currentIndex === undefined) return
  const newIndex = props.currentIndex < props.imageList.length - 1 ? props.currentIndex + 1 : 0
  emit('update:currentIndex', newIndex)
}

// 键盘事件处理
const handleKeydown = (event: KeyboardEvent) => {
  if (!props.show) return
  
  switch (event.key) {
    case 'ArrowLeft':
      prevImage()
      break
    case 'ArrowRight':
      nextImage()
      break
    case 'Escape':
      close()
      break
  }
}

// 添加和移除键盘事件监听
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

const close = () => {
  emit('update:show', false)
}
</script> 