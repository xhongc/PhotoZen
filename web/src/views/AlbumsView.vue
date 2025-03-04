<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-2xl font-bold">我的相册</h1>
        <button class="btn btn-primary" @click="openCreateAlbumModal">
          创建相册
        </button>
      </div>
      
      <div v-if="loading" class="flex justify-center items-center min-h-[200px]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>
      <div v-else-if="error" class="alert alert-error">
        {{ error }}
      </div>
      <div v-else-if="albums.length === 0" class="text-center py-12">
        <div class="text-lg mb-4">暂无相册</div>
        <button class="btn btn-primary" @click="openCreateAlbumModal">创建第一个相册</button>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div v-for="album in albums" :key="album.id" class="card bg-base-100 shadow-xl">
          <figure class="relative aspect-square bg-gray-100">
            <img 
              v-if="album.cover_photo" 
              :src="album.cover_photo.url" 
              :alt="album.name" 
              class="w-full h-full object-cover" 
            />
            <div v-else class="flex items-center justify-center w-full h-full text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </figure>
          <div class="card-body p-4">
            <h3 class="card-title text-sm">{{ album.name }}</h3>
            <p class="text-xs text-gray-500">{{ album.photos_count || 0 }}张照片</p>
            <div class="card-actions justify-end mt-2">
              <button class="btn btn-sm btn-outline" @click="viewAlbum(album)">
                查看
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建相册模态框 -->
    <dialog ref="createAlbumDialog" class="modal">
      <div class="modal-box">
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>
        <h3 class="font-bold text-lg mb-4">创建新相册</h3>
        <form @submit.prevent="createAlbum">
          <div class="form-control w-full">
            <label class="label">
              <span class="label-text">相册名称</span>
            </label>
            <input 
              type="text" 
              v-model="newAlbum.name" 
              placeholder="输入相册名称" 
              class="input input-bordered w-full" 
              required
            />
          </div>
          <div class="form-control w-full mt-4">
            <label class="label">
              <span class="label-text">相册描述</span>
            </label>
            <textarea 
              v-model="newAlbum.description" 
              placeholder="输入相册描述（可选）" 
              class="textarea textarea-bordered w-full"
            ></textarea>
          </div>
          <div class="modal-action">
            <button type="button" class="btn" @click="closeCreateAlbumModal">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="creating">创建</button>
          </div>
        </form>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>关闭</button>
      </form>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

interface Photo {
  id: number
  url: string
  title?: string
}

interface Album {
  id: number
  name: string
  description: string
  created_time: string
  updated_time: string
  photos_count?: number
  cover_photo?: Photo
}

const router = useRouter()
const albums = ref<Album[]>([])
const loading = ref(true)
const error = ref('')
const createAlbumDialog = ref<HTMLDialogElement | null>(null)
const creating = ref(false)

const newAlbum = ref({
  name: '',
  description: ''
})

const fetchAlbums = async () => {
  loading.value = true
  error.value = ''
  try {
    // 这里应该调用API获取相册列表
    // 暂时使用模拟数据
    albums.value = [
      {
        id: 1,
        name: '家庭照片',
        description: '家庭生活的美好瞬间',
        created_time: '2023-01-01T00:00:00Z',
        updated_time: '2023-01-01T00:00:00Z',
        photos_count: 12,
        cover_photo: {
          id: 1,
          url: 'https://picsum.photos/id/1/300/300',
          title: '家庭照片'
        }
      },
      {
        id: 2,
        name: '旅行记忆',
        description: '旅行中的精彩瞬间',
        created_time: '2023-02-01T00:00:00Z',
        updated_time: '2023-02-01T00:00:00Z',
        photos_count: 24,
        cover_photo: {
          id: 2,
          url: 'https://picsum.photos/id/10/300/300',
          title: '旅行照片'
        }
      },
      {
        id: 3,
        name: '美食记录',
        description: '记录美食与生活',
        created_time: '2023-03-01T00:00:00Z',
        updated_time: '2023-03-01T00:00:00Z',
        photos_count: 8,
        cover_photo: {
          id: 3,
          url: 'https://picsum.photos/id/20/300/300',
          title: '美食照片'
        }
      }
    ]
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取相册失败'
  } finally {
    loading.value = false
  }
}

const openCreateAlbumModal = () => {
  newAlbum.value = {
    name: '',
    description: ''
  }
  createAlbumDialog.value?.showModal()
}

const closeCreateAlbumModal = () => {
  createAlbumDialog.value?.close()
}

const createAlbum = async () => {
  if (!newAlbum.value.name) return
  
  creating.value = true
  try {
    // 这里应该调用API创建相册
    // 暂时使用模拟数据
    const newAlbumData = {
      id: albums.value.length + 1,
      name: newAlbum.value.name,
      description: newAlbum.value.description,
      created_time: new Date().toISOString(),
      updated_time: new Date().toISOString(),
      photos_count: 0
    }
    
    albums.value.unshift(newAlbumData)
    closeCreateAlbumModal()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '创建相册失败'
  } finally {
    creating.value = false
  }
}

const viewAlbum = (album: Album) => {
  router.push(`/albums/${album.id}`)
}

onMounted(fetchAlbums)
</script>