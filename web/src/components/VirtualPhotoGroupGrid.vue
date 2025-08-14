<template>
  <SimpleVirtualList 
    :items="photoGroups"
    :item-height="getEstimatedHeight()"
    :get-key="(index) => photoGroups[index]?.date_key || index"
  >
    <template #default="{ item: group }">
      <div class="mb-12 px-4 sm:px-6 lg:px-8">
        <PhotoGroupCard
          :group="group"
          :current-view="currentView"
          :is-select-mode="isSelectMode"
          :selected-photos="selectedPhotos"
          :expanded-groups="expandedGroups"
          @toggle-group="$emit('toggleGroup', $event)"
          @toggle-group-selection="$emit('toggleGroupSelection', $event)"
          @toggle-photo-selection="$emit('togglePhotoSelection', $event)"
          @toggle-favorite="$emit('toggleFavorite', $event)"
          @edit-photo="$emit('editPhoto', $event)"
        />
      </div>
    </template>
  </SimpleVirtualList>
</template>

<script setup lang="ts">
import SimpleVirtualList from './SimpleVirtualList.vue'
import PhotoGroupCard from './PhotoGroupCard.vue'
import type { PhotoGroup } from '@/api/photos'

interface Props {
  photoGroups: PhotoGroup[]
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

// 根据视图类型估算高度
const getEstimatedHeight = () => {
  switch (props.currentView) {
    case 'grid':
      return 400 // 标题 + 网格布局的估算高度
    case 'masonry':
      return 500 // 瀑布流可能更高
    case 'list':
      return 300 // 列表视图相对较矮
    default:
      return 400
  }
}
</script>