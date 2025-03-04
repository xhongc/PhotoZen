<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-2xl font-bold">我的照片</h1>
        <router-link to="/upload" class="btn btn-primary">
          上传照片
        </router-link>
      </div>
      
      <div v-if="loading" class="flex justify-center items-center min-h-[200px]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>
      <div v-else-if="error" class="alert alert-error">
        {{ error }}
      </div>
      <PhotoGrid v-else :photos="photos" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PhotoGrid from '@/components/PhotoGrid.vue'
import { photoApi, type Photo } from '@/api/photos'

const photos = ref<Photo[]>([])
const loading = ref(true)
const error = ref('')

const fetchPhotos = async () => {
  try {
    photos.value = await photoApi.getPhotos()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取照片失败'
  } finally {
    loading.value = false
  }
}

onMounted(fetchPhotos)
</script>
