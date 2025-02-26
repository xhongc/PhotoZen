<template>
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">上传照片</h2>
      <div 
        class="upload-zone border-2 border-dashed border-primary rounded-lg p-8 text-center cursor-pointer"
        @dragover.prevent
        @drop.prevent="handleDrop"
        @click="fileInput?.click()"
      >
        <input
          type="file"
          ref="fileInput"
          @change="handleFileSelect"
          multiple
          accept="image/*"
          class="hidden"
        />
        <div class="text-lg mb-2">拖拽照片到这里或点击上传</div>
        <div class="text-sm text-base-content/60">支持 JPG、PNG、WebP 格式</div>
      </div>
      
      <!-- Upload Progress -->
      <div v-if="uploadingFiles.length > 0" class="mt-4">
        <div v-for="file in uploadingFiles" :key="file.name" class="mb-2">
          <div class="flex items-center gap-2">
            <div class="flex-1">
              <div class="text-sm font-medium">{{ file.name }}</div>
              <progress class="progress progress-primary w-full" :value="file.progress" max="100"></progress>
            </div>
            <button class="btn btn-ghost btn-sm" @click="cancelUpload(file)">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Ref } from 'vue'
import { photoApi } from '@/api/photos'

const emit = defineEmits<{
  (e: 'upload-success'): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const uploadingFiles = ref<{ name: string; progress: number; cancel: () => void }[]>([])

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    uploadFiles(Array.from(target.files))
  }
}

const handleDrop = (event: DragEvent) => {
  const files = event.dataTransfer?.files
  if (files) {
    uploadFiles(Array.from(files))
  }
}

const uploadFiles = async (files: File[]) => {
  for (const file of files) {
    const uploadingFile = {
      name: file.name,
      progress: 0,
      cancel: () => {} // Will be assigned below
    }
    uploadingFiles.value.push(uploadingFile)

    try {
      await photoApi.uploadPhoto(file, (progress) => {
        uploadingFile.progress = progress
      })
      // Remove file from uploading list when complete
      uploadingFiles.value = uploadingFiles.value.filter(f => f !== uploadingFile)
      emit('upload-success')
    } catch (error) {
      console.error('Upload failed:', error)
      // Keep file in list with error state if needed
    }
  }
}

const cancelUpload = (file: { name: string; progress: number; cancel: () => void }) => {
  file.cancel()
  uploadingFiles.value = uploadingFiles.value.filter(f => f !== file)
}
</script>
