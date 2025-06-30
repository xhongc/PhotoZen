<template>
  <main class="flex-1 h-screen-header overflow-y-auto">
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
                <img src="https://images.unsplash.com/photo-1501555088652-021faa106b9b?q=80&w=1473&auto=format&fit=crop"
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
                <img src="https://images.unsplash.com/photo-1501555088652-021faa106b9b?q=80&w=1473&auto=format&fit=crop"
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
                <img src="https://images.unsplash.com/photo-1501555088652-021faa106b9b?q=80&w=1473&auto=format&fit=crop"
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
                <img src="https://images.unsplash.com/photo-1501555088652-021faa106b9b?q=80&w=1473&auto=format&fit=crop"
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
            <div class="relative group overflow-hidden rounded-lg shadow-sm" v-for="album in albums" :key="album.id"
              @click="viewAlbum(album)">
              <div class="aspect-w-16 aspect-h-9 bg-gray-200">
                <img src="https://images.unsplash.com/photo-1501555088652-021faa106b9b?q=80&w=1473&auto=format&fit=crop"
                  alt="旅行" class="w-full h-40 2xl:h-60 object-cover">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60">
                </div>
                <div class="absolute inset-x-0 bottom-0 p-4">
                  <h4 class="text-white font-medium">{{ album.name }}</h4>
                  <p class="text-gray-200 text-sm">{{ album.photos_count }} 张照片</p>
                </div>
              </div>
              <div
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-1">
                <button
                  class="p-1.5 bg-white bg-opacity-70 backdrop-filter backdrop-blur-sm rounded-full text-gray-700 hover:text-gray-900 focus:outline-none"
                  @click.stop="handleAlbumMenu(album)">
                  <i class="fas fa-ellipsis-h"></i>
                </button>
              </div>
            </div>
            <!-- 新建相册卡片 -->
            <div
              class="border-2 border-dashed border-base-300 rounded-lg flex items-center justify-center h-40 cursor-pointer hover:border-primary-400 transition-colors duration-300"
              @click="openCreateAlbumModal">
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
  <dialog ref="createAlbumDialog" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h3 class="text-lg font-bold">新建相册</h3>
      <div class="mt-2">
        <div>相册名称:</div>
        <input type="text" placeholder="请输入相册名称" class="input input-bordered input-sm w-full max-w-xs mt-1"
          v-model="newAlbum.name" />
        <div class="mt-2">相册描述:</div>
        <textarea placeholder="请输入相册描述" class="textarea textarea-bordered textarea-sm w-full max-w-xs mt-1"
          v-model="newAlbum.description"></textarea>
      </div>
      <div class="modal-action">
        <form method="dialog">
          <button class="btn btn-ghost btn-sm mr-2">取消</button>
          <button class="btn btn-primary btn-sm" @click="createAlbum">创建</button>
        </form>
      </div>
    </div>
  </dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { albumApi, type Album } from '@/api/albums'

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

onMounted(() => {
  fetchAlbums()
})


const fetchAlbums = async () => {
  loading.value = true
  error.value = ''
  try {
    albums.value = await albumApi.getAlbums()
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
    await albumApi.createAlbum(newAlbum.value)
    fetchAlbums()
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

const handleAlbumMenu = (album: Album) => {
  // TODO: 实现相册菜单功能
  console.log('相册菜单:', album)
}

</script>