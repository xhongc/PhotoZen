<template>
  <div class="container mx-auto px-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div v-for="photo in photos" :key="photo.id" class="card bg-base-100 shadow-xl">
        <figure class="relative aspect-square">
          <img :src="photo.url" :alt="photo.title" class="w-full h-full object-cover" />
        </figure>
        <div class="card-body p-4">
          <h3 class="card-title text-sm">{{ photo.title || '未命名照片' }}</h3>
          <p class="text-xs text-gray-500">{{ formatDate(photo.created_at) }}</p>
          <div class="card-actions justify-end mt-2">
            <button class="btn btn-sm btn-primary" @click="handleView(photo)">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
              </svg>
              查看
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 照片预览模态框 -->
    <dialog ref="viewDialog" class="modal">
      <div class="modal-box max-w-4xl">
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>
        <div v-if="selectedPhoto" class="p-4">
          <img :src="selectedPhoto.url" :alt="selectedPhoto.title" class="w-full h-auto rounded-lg" />
          <div class="mt-4">
            <h3 class="text-lg font-semibold">{{ selectedPhoto.title || '未命名照片' }}</h3>
            <p class="text-sm text-gray-600">{{ formatDate(selectedPhoto.created_at) }}</p>
            <div class="flex gap-2 mt-2" v-if="selectedPhoto.tags && selectedPhoto.tags.length">
              <span v-for="tag in selectedPhoto.tags" :key="tag" class="badge badge-primary">{{ tag }}</span>
            </div>
          </div>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>关闭</button>
      </form>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Photo {
  id: number
  url: string
  title?: string
  created_at: string
  tags?: string[]
}

const props = defineProps<{
  photos: Photo[]
}>()

const viewDialog = ref<HTMLDialogElement | null>(null)
const selectedPhoto = ref<Photo | null>(null)

const handleView = (photo: Photo) => {
  selectedPhoto.value = photo
  viewDialog.value?.showModal()
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
</style>
