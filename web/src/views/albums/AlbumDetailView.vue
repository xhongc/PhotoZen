<template>
  <main class="flex-1 h-screen-header overflow-y-auto">
    <div class="py-6">
      <!-- 页面标题 -->
      <div class="px-6 mb-6 flex items-center justify-between ml-2">
        <div class="flex items-center">
          <button @click="router.back()" class="text-gray-500 hover:text-gray-700 mr-4">
            <i class="fas fa-arrow-left"></i>
          </button>
          <h2 class="text-xl font-semibold text-primary-600">{{ album?.name || '相册详情' }}</h2>
        </div>
        <div class="flex items-center space-x-4">
          <button @click="handleEditAlbum" class="btn btn-sm btn-outline">
            <i class="fas fa-edit mr-1"></i>编辑相册
          </button>
          <button @click="handleDeleteAlbum" class="btn btn-sm btn-error">
            <i class="fas fa-trash mr-1"></i>删除相册
          </button>
        </div>
      </div>

      <!-- 相册信息 -->
      <div v-if="album" class="px-6 mb-6">
        <div class="bg-base-100 rounded-lg shadow-sm p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-600">{{ album.description || '暂无描述' }}</p>
              <p class="text-sm text-gray-500 mt-1">
                创建于 {{ formatDate(album.created_time) }}
                <span class="mx-2">·</span>
                {{ album.photos_count }} 张照片
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 照片列表 -->
      <PhotosView :album-id="albumId" />
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { albumApi, type Album } from '@/api/albums'
import PhotosView from '@/views/photos/PhotosView.vue'

const router = useRouter()
const route = useRoute()
const albumId = Number(route.params.id)
const album = ref<Album | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(() => {
  fetchAlbum()
})

const fetchAlbum = async () => {
  try {
    loading.value = true
    album.value = await albumApi.getAlbum(albumId)
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取相册信息失败'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const handleEditAlbum = () => {
  // TODO: 实现编辑相册功能
  console.log('编辑相册:', album.value)
}

const handleDeleteAlbum = async () => {
  if (!confirm('确定要删除这个相册吗？此操作不可恢复。')) {
    return
  }
  try {
    await albumApi.deleteAlbum(albumId)
    router.push('/albums')
  } catch (e) {
    error.value = e instanceof Error ? e.message : '删除相册失败'
  }
}
</script> 