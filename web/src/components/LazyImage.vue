<template>
  <div class="lazy-image-container" :style="{ width: containerWidth, height: containerHeight }">
    <div v-if="!loaded && !error" class="lazy-placeholder">
      <div class="skeleton-loader"></div>
    </div>
    <img
      v-show="loaded && !error"
      ref="imageRef"
      :src="imageSrc"
      :alt="alt"
      :class="imageClass"
      @load="onLoad"
      @error="onError"
    />
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
  alt?: string
  class?: string
  width?: string | number
  height?: string | number
  placeholder?: string
  threshold?: number
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  class: '',
  width: '100%',
  height: 'auto',
  placeholder: '',
  threshold: 0.1
})

const imageRef = ref<HTMLImageElement>()
const loaded = ref(false)
const error = ref(false)
const inView = ref(false)

const containerWidth = computed(() => {
  return typeof props.width === 'number' ? `${props.width}px` : props.width
})

const containerHeight = computed(() => {
  return typeof props.height === 'number' ? `${props.height}px` : props.height
})

const imageSrc = computed(() => {
  return inView.value ? props.src : ''
})

const imageClass = computed(() => {
  return [
    props.class,
    'transition-opacity duration-300',
    loaded.value ? 'opacity-100' : 'opacity-0'
  ].filter(Boolean).join(' ')
})

let observer: IntersectionObserver | null = null

const onLoad = () => {
  loaded.value = true
  error.value = false
}

const onError = () => {
  error.value = true
  loaded.value = false
}

onMounted(() => {
  if (imageRef.value) {
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
        rootMargin: '50px'
      }
    )

    observer.observe(imageRef.value.parentElement!)
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
}

.lazy-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.skeleton-loader {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: inherit;
}

.error-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>