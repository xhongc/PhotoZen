<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-2xl font-bold">上传照片</h1>
        <router-link to="/photos" class="btn btn-outline">
          返回照片列表
        </router-link>
      </div>

      <div class="max-w-2xl mx-auto">
        <PhotoUpload @upload-success="handleUploadSuccess" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import PhotoUpload from '@/components/PhotoUpload.vue'

const router = useRouter()

const handleUploadSuccess = () => {
  // 上传成功后跳转到照片列表页面
  router.push('/photos')
}
</script>
