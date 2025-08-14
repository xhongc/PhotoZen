<template>
  <div ref="containerRef" class="lazy-image-container" :style="{ width: containerWidth, height: containerHeight }">
    <!-- 预览图 -->
    <img
      v-if="thumbnailSrc && !fullImageLoaded && !error"
      :src="thumbnailSrc"
      :alt="alt"
      class="preview-image"
      @load="onThumbnailLoad"
      @error="onThumbnailError"
    />
    
    <!-- 骨架屏加载器 -->
    <div v-if="!thumbnailLoaded && !loaded && !error" class="lazy-placeholder">
      <div class="skeleton-loader"></div>
    </div>
    
    <!-- 完整图片 -->
    <img
      v-show="fullImageLoaded && !error"
      ref="imageRef"
      :src="imageSrc"
      :alt="alt"
      :class="imageClass"
      @load="onLoad"
      @error="onError"
    />
    
    <!-- 错误状态 -->
    <div v-if="error" class="error-placeholder">
      <i class="fas fa-exclamation-triangle text-gray-400"></i>
      <span class="text-xs text-gray-400 mt-1">加载失败</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'

interface Props {
  src: string
  thumbnailSrc?: string
  alt?: string
  class?: string
  width?: string | number
  height?: string | number
  placeholder?: string
  threshold?: number
  useWebdav?: boolean
  priority?: boolean
  quality?: 'low' | 'medium' | 'high'
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  class: '',
  width: '100%',
  height: 'auto',
  placeholder: '',
  threshold: 0.1,
  useWebdav: false,
  priority: false,
  quality: 'medium'
})

const imageRef = ref<HTMLImageElement>()
const loaded = ref(false)
const fullImageLoaded = ref(false)
const thumbnailLoaded = ref(false)
const error = ref(false)
const inView = ref(false)

const containerWidth = computed(() => {
  return typeof props.width === 'number' ? `${props.width}px` : props.width
})

const containerHeight = computed(() => {
  return typeof props.height === 'number' ? `${props.height}px` : props.height
})

const imageSrc = computed(() => {
  if (!inView.value && !props.priority) return ''
  
  let src = props.src
  
  // 根据质量设置添加缩略图参数
  if (props.quality !== 'high') {
    const qualityMap = {
      low: '?quality=30&resize=400x400',
      medium: '?quality=60&resize=800x800'
    }
    src += qualityMap[props.quality]
  }
  
  if (props.useWebdav) {
    return `/webdav/${src}`
  }
  
  return src
})

const imageClass = computed(() => {
  return [
    props.class,
    'transition-opacity duration-500 relative z-10',
    fullImageLoaded.value ? 'opacity-100' : 'opacity-0'
  ].filter(Boolean).join(' ')
})

let observer: IntersectionObserver | null = null

const onThumbnailLoad = () => {
  thumbnailLoaded.value = true
}

const onThumbnailError = () => {
  thumbnailLoaded.value = false
}

const onLoad = () => {
  loaded.value = true
  fullImageLoaded.value = true
  error.value = false
}

const onError = () => {
  error.value = true
  loaded.value = false
  fullImageLoaded.value = false
}

const containerRef = ref<HTMLDivElement>()

onMounted(() => {
  if (containerRef.value) {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !inView.value) {
            inView.value = true
            observer?.unobserve(entry.target)
          }
        })
      },
      {
        threshold: props.threshold,
        rootMargin: props.priority ? '0px' : '50px'
      }
    )

    observer.observe(containerRef.value)
  }
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.lazy-image-container {
  position: relative;
  overflow: hidden;
  background-color: #f5f5f5;
  border-radius: 0.5rem;
  contain: layout style paint;
  will-change: transform;
}

.preview-image {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(2px);
  transition: opacity 0.2s ease;
  z-index: 1;
  contain: layout style paint;
}

.lazy-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  contain: layout;
}

.skeleton-loader {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 2s infinite ease-in-out;
  border-radius: inherit;
  contain: strict;
}

.error-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
  contain: layout;
}

/* 使用硬件加速和GPU优化 */
img {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* 减少重绘 */
@media (prefers-reduced-motion: reduce) {
  .skeleton-loader {
    animation: none;
    background: #e0e0e0;
  }
  
  .preview-image {
    transition: none;
  }
}
</style>