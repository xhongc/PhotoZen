<template>
  <div class="masonry-container" ref="containerRef">
    <div
      v-for="(column, columnIndex) in columns"
      :key="columnIndex"
      class="masonry-column"
      :style="{ width: columnWidth }"
    >
      <slot
        v-for="item in column"
        :key="item.id"
        :item="item"
        :index="item.originalIndex"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'

interface MasonryItem {
  id: number | string
  originalIndex: number
  [key: string]: any
}

interface Props {
  items: any[]
  columnCount?: number
  gap?: number
  minColumnWidth?: number
}

const props = withDefaults(defineProps<Props>(), {
  columnCount: 0, // 0 means auto-calculate based on container width
  gap: 16,
  minColumnWidth: 250
})

const emit = defineEmits<{
  itemsArranged: [columns: MasonryItem[][]]
}>()

const containerRef = ref<HTMLElement>()
const columns = ref<MasonryItem[][]>([])
const actualColumnCount = ref(4)
const containerWidth = ref(0)
const resizeObserver = ref<ResizeObserver>()

const columnWidth = computed(() => {
  if (actualColumnCount.value === 0) return '100%'
  const totalGaps = (actualColumnCount.value - 1) * props.gap
  return `${(100 - (totalGaps / containerWidth.value * 100)) / actualColumnCount.value}%`
})

// 计算列数
const calculateColumnCount = () => {
  if (!containerRef.value) return 4
  
  const width = containerRef.value.offsetWidth
  containerWidth.value = width
  
  if (props.columnCount > 0) {
    return props.columnCount
  }
  
  // 根据容器宽度和最小列宽自动计算列数
  const availableWidth = width - props.gap * 2 // 留出边距
  const possibleColumns = Math.floor(availableWidth / (props.minColumnWidth + props.gap))
  return Math.max(1, Math.min(possibleColumns, 6)) // 限制在1-6列之间
}

// 分布项目到各列
const distributeItems = () => {
  if (!props.items.length) {
    columns.value = []
    return
  }

  actualColumnCount.value = calculateColumnCount()
  
  // 初始化列数组
  const newColumns: MasonryItem[][] = Array.from({ length: actualColumnCount.value }, () => [])
  const columnHeights = new Array(actualColumnCount.value).fill(0)
  
  // 将项目分配给当前高度最小的列
  props.items.forEach((item, index) => {
    const shortestColumnIndex = columnHeights.indexOf(Math.min(...columnHeights))
    
    const masonryItem: MasonryItem = {
      ...item,
      originalIndex: index
    }
    
    newColumns[shortestColumnIndex].push(masonryItem)
    
    // 根据图片尺寸估算高度，如果没有尺寸信息则使用默认值
    let estimatedHeight = 250 // 默认高度
    if (item.width && item.height) {
      // 基于图片宽高比计算高度
      const aspectRatio = item.height / item.width
      const columnWidthPx = (containerWidth.value - props.gap * (actualColumnCount.value - 1)) / actualColumnCount.value
      estimatedHeight = columnWidthPx * aspectRatio
    }
    
    columnHeights[shortestColumnIndex] += estimatedHeight + props.gap
  })
  
  columns.value = newColumns
  emit('itemsArranged', newColumns)
}

// 防抖函数
const debounce = (func: Function, wait: number) => {
  let timeout: number
  return (...args: any[]) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func.apply(null, args), wait) as any
  }
}

const debouncedDistribute = debounce(distributeItems, 150)

// 监听容器大小变化
const setupResizeObserver = () => {
  if (!containerRef.value) return
  
  resizeObserver.value = new ResizeObserver(debouncedDistribute)
  resizeObserver.value.observe(containerRef.value)
}

// 监听 items 变化
watch(() => props.items, () => {
  nextTick(() => {
    distributeItems()
  })
}, { deep: true })

onMounted(() => {
  nextTick(() => {
    setupResizeObserver()
    distributeItems()
  })
})

onUnmounted(() => {
  if (resizeObserver.value) {
    resizeObserver.value.disconnect()
  }
})

// 暴露方法给父组件
defineExpose({
  refresh: distributeItems
})
</script>

<style scoped>
.masonry-container {
  display: flex;
  align-items: flex-start;
  gap: v-bind('props.gap + "px"');
  width: 100%;
}

.masonry-column {
  display: flex;
  flex-direction: column;
  gap: v-bind('props.gap + "px"');
  flex-shrink: 0;
}

/* 优化性能 */
.masonry-container * {
  contain: layout style paint;
}
</style>