<template>
  <div ref="scrollContainer" @scroll="onScroll" style="width: 100%; height: 100%; overflow-y: auto; overflow-x: hidden;">
    <div :style="{ height: totalHeight + 'px', position: 'relative' }">
      <div 
        v-for="(item, index) in visibleItems" 
        :key="getKey(item.index)"
        :style="{
          position: 'absolute',
          top: item.top + 'px',
          left: '0',
          width: '100%'
        }"
      >
        <slot :item="items[item.index]" :index="item.index" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'

interface Props {
  items: any[]
  itemHeight: number
  containerHeight?: number
  buffer?: number
  getKey?: (index: number) => string | number
}

const props = withDefaults(defineProps<Props>(), {
  containerHeight: 600,
  buffer: 5,
  getKey: (index: number) => index
})

const scrollContainer = ref<HTMLElement>()
const scrollTop = ref(0)

const totalHeight = computed(() => props.items.length * props.itemHeight)

const containerHeight = computed(() => {
  if (scrollContainer.value) {
    return scrollContainer.value.clientHeight
  }
  return props.containerHeight
})

const visibleStartIndex = computed(() => {
  return Math.floor(scrollTop.value / props.itemHeight)
})

const visibleEndIndex = computed(() => {
  return Math.min(
    visibleStartIndex.value + Math.ceil(containerHeight.value / props.itemHeight) + props.buffer,
    props.items.length - 1
  )
})

const actualStartIndex = computed(() => {
  return Math.max(0, visibleStartIndex.value - props.buffer)
})

const actualEndIndex = computed(() => {
  return Math.min(props.items.length - 1, visibleEndIndex.value + props.buffer)
})

const visibleItems = computed(() => {
  const items = []
  for (let i = actualStartIndex.value; i <= actualEndIndex.value; i++) {
    items.push({
      index: i,
      top: i * props.itemHeight
    })
  }
  return items
})

const onScroll = () => {
  if (scrollContainer.value) {
    scrollTop.value = scrollContainer.value.scrollTop
  }
}

const updateScrollPosition = () => {
  if (scrollContainer.value) {
    scrollTop.value = scrollContainer.value.scrollTop
  }
}

onMounted(() => {
  nextTick(() => {
    updateScrollPosition()
    // 监听容器大小变化
    if (scrollContainer.value) {
      const resizeObserver = new ResizeObserver(() => {
        // 当容器大小改变时，重新计算
        nextTick(() => {
          updateScrollPosition()
        })
      })
      resizeObserver.observe(scrollContainer.value)
      
      // 在组件卸载时清理
      onBeforeUnmount(() => {
        resizeObserver.disconnect()
      })
    }
  })
})

onBeforeUnmount(() => {
  if (scrollContainer.value) {
    scrollContainer.value.removeEventListener('scroll', onScroll)
  }
})
</script>