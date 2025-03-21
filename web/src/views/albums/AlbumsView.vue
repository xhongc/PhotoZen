<template>
  <main class="flex-1 overflow-hidden">
    <div class="py-6">
      <!-- 页面标题 -->
      <div class="px-6 mb-6 flex items-center justify-between ml-2">
        <h2 class="text-xl font-semibold text-primary-600">我的相册</h2>
      </div>

      <!-- 相册分类 -->
      <div class="px-6 mb-4">
        <div class="bg-base-100 rounded-lg shadow-sm p-4 mb-6">
          <h3 class="text-lg font-medium text-primary-600 mb-4">系统相册</h3>
          <div class="grid grid-cols-4 gap-4">
            <!-- 最近添加 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1374&auto=format&fit=crop"
                  alt="最近添加" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">最近添加</h4>
                  <p class="text-gray-200 text-sm">108 张照片</p>
                </div>
              </div>
            </div>

            <!-- 收藏 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1374&auto=format&fit=crop"
                  alt="收藏" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">收藏</h4>
                  <p class="text-gray-200 text-sm">24 张照片</p>
                </div>
              </div>
            </div>

            <!-- 人物 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1374&auto=format&fit=crop"
                  alt="人物" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">人物</h4>
                  <p class="text-gray-200 text-sm">56 张照片</p>
                </div>
              </div>
            </div>

            <!-- 地点 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1374&auto=format&fit=crop"
                  alt="地点" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">地点</h4>
                  <p class="text-gray-200 text-sm">12 个地点</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-base-100 rounded-lg shadow-sm p-4">
          <h3 class="text-lg font-medium text-primary-600 mb-4">自定义相册</h3>
          <div class="grid grid-cols-4 gap-4">
            <!-- 旅行 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1501555088652-021faa106b9b?q=80&w=1473&auto=format&fit=crop"
                  alt="旅行" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">旅行</h4>
                  <p class="text-gray-200 text-sm">64 张照片</p>
                </div>
              </div>
              <div
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-1">
                <button
                  class="p-1.5 bg-white bg-opacity-70 backdrop-filter backdrop-blur-sm rounded-full text-gray-700 hover:text-gray-900 focus:outline-none">
                  <i class="fas fa-ellipsis-h"></i>
                </button>
              </div>
            </div>

            <!-- 家庭 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1511895426328-dc8714191300?q=80&w=1470&auto=format&fit=crop"
                  alt="家庭" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">家庭</h4>
                  <p class="text-gray-200 text-sm">32 张照片</p>
                </div>
              </div>
              <div
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-1">
                <button
                  class="p-1.5 bg-white bg-opacity-70 backdrop-filter backdrop-blur-sm rounded-full text-gray-700 hover:text-gray-900 focus:outline-none">
                  <i class="fas fa-ellipsis-h"></i>
                </button>
              </div>
            </div>

            <!-- 美食 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=1470&auto=format&fit=crop"
                  alt="美食" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">美食</h4>
                  <p class="text-gray-200 text-sm">18 张照片</p>
                </div>
              </div>
              <div
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-1">
                <button
                  class="p-1.5 bg-white bg-opacity-70 backdrop-filter backdrop-blur-sm rounded-full text-gray-700 hover:text-gray-900 focus:outline-none">
                  <i class="fas fa-ellipsis-h"></i>
                </button>
              </div>
            </div>

            <!-- 宠物 -->
            <div class="relative group overflow-hidden rounded-lg shadow-sm">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1560807707-8cc77767d783?q=80&w=1470&auto=format&fit=crop"
                  alt="宠物" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">宠物</h4>
                  <p class="text-gray-200 text-sm">27 张照片</p>
                </div>
              </div>
              <div
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-1">
                <button
                  class="p-1.5 bg-white bg-opacity-70 backdrop-filter backdrop-blur-sm rounded-full text-gray-700 hover:text-gray-900 focus:outline-none">
                  <i class="fas fa-ellipsis-h"></i>
                </button>
              </div>
            </div>

            <!-- 新建相册卡片 -->
            <div
              class="border-2 border-dashed border-base-300 rounded-lg flex items-center justify-center h-40 cursor-pointer hover:border-primary-400 transition-colors duration-300">
              <div class="text-center">
                <div class="flex justify-center">
                  <div class="rounded-full bg-primary-100 text-primary-600 p-3">
                    <i class="fas fa-plus"></i>
                  </div>
                </div>
                <h4 class="mt-2 font-medium text-primary-600">新建相册</h4>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
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

</script>