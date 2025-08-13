<template>
    <!-- 主内容区 -->
    <main class="max-w-full mx-auto py-6 sm:px-6 lg:px-8">
        <!-- 统计概览 -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-4 mb-6">
            <div class="bg-base-100 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 bg-base-200 rounded-md p-3">
                            <i class="fas fa-image text-primary-600 text-xl"></i>
                        </div>
                        <div class="ml-5 w-0 flex-1">
                            <dl>
                                <div class="text-sm font-medium text-gray-500 truncate">总照片数</div>
                                <div class="text-lg font-semibold text-primary-600">{{ homeData?.total_photos }}</div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-base-100 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
                            <i class="fas fa-folder text-green-600 text-xl"></i>
                        </div>
                        <div class="ml-5 w-0 flex-1">
                            <dl>
                                <div class="text-sm font-medium text-gray-500 truncate">相册数</div>
                                <div class="text-lg font-semibold text-primary-600">{{ homeData?.total_albums }}</div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-base-100 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 bg-blue-100 rounded-md p-3">
                            <i class="fas fa-heart text-blue-600 text-xl"></i>
                        </div>
                        <div class="ml-5 w-0 flex-1">
                            <dl>
                                <div class="text-sm font-medium text-gray-500 truncate">收藏数</div>
                                <div class="text-lg font-semibold text-primary-600">{{ homeData?.total_favorites }}</div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-base-100 overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <div class="flex items-center">
                        <div class="flex-shrink-0 bg-purple-100 rounded-md p-3">
                            <i class="fas fa-cloud text-purple-600 text-xl"></i>
                        </div>
                        <div class="ml-5 w-0 flex-1">
                            <dl>
                                <div class="text-sm font-medium text-gray-500 truncate">存储空间</div>
                                <div class="text-lg font-semibold text-primary-600">{{ homeData?.storage_space }}</div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 最近上传 -->
        <div class="bg-base-100 shadow rounded-lg mb-6">
            <div class="px-4 py-5 border-b border-base-200 sm:px-6">
                <div class="flex items-center justify-between">
                    <h3 class="text-lg leading-6 font-medium text-base-900">最近上传</h3>
                    <a href="/albums/recent"
                        class="text-primary-600 hover:text-primary-700 text-sm font-medium">查看全部</a>
                </div>
            </div>
            <div class="px-4 py-5 sm:p-6">
                <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
                    <div class="group relative" v-for="photo in recentPhotos" :key="photo.id">
                        <div class="aspect-w-1 aspect-h-1 rounded-lg overflow-hidden w-full md:h-[160px] 2xl:h-[260px] h-[160px]">
                            <img :src="photo.thumbnail_path" alt=""
                                class="object-cover w-full h-full group-hover:scale-105 transition-all duration-300 cursor-pointer">
                        </div>
                        <p class="mt-2 text-sm text-gray-500">{{ photo.taken_time }}</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 今日回忆 -->
        <div class="bg-base-100 shadow rounded-lg mb-6" v-if="memoriesData && memoriesData.memories.length > 0">
            <div class="px-4 py-5 border-b border-base-200 sm:px-6">
                <div class="flex items-center justify-between">
                    <h3 class="text-lg leading-6 font-medium text-base-900">今日回忆</h3>
                    <span class="text-sm text-primary-600" v-if="memoriesData.memories.length > 0">
                        {{ memoriesData.memories[0].years_ago }}年前的今天
                    </span>
                </div>
            </div>
            <div class="px-4 py-5 sm:p-6">
                <div v-for="yearMemory in memoriesData.memories" :key="yearMemory.year" class="mb-6 last:mb-0">
                    <div class="flex items-center justify-between mb-3">
                        <h4 class="text-md font-medium text-base-700">{{ yearMemory.year }}年 ({{ yearMemory.years_ago }}年前)</h4>
                        <span class="text-sm text-gray-500">{{ yearMemory.photos.length }}张照片</span>
                    </div>
                    <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
                        <div v-for="photo in yearMemory.photos" :key="photo.id" class="relative rounded-lg overflow-hidden group cursor-pointer">
                            <img :src="photo.thumbnail_path" :alt="photo.title"
                                class="w-full h-24 object-cover group-hover:scale-105 transition-all duration-300">
                            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-all duration-300">
                                <div class="absolute bottom-0 left-0 right-0 p-2">
                                    <p class="text-white text-xs truncate">{{ photo.title }}</p>
                                    <p class="text-white/80 text-xs">{{ formatDate(photo.taken_time) }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 智能相册推荐 -->
        <div class="bg-base-100 shadow rounded-lg">
            <div class="px-4 py-5 border-b border-base-200 sm:px-6">
                <div class="flex items-center justify-between">
                    <h3 class="text-lg leading-6 font-medium text-base-900">智能相册</h3>
                    <a href="/albums/smart" class="text-primary-600 hover:text-primary-700 text-sm font-medium">查看全部</a>
                </div>
            </div>
            <div class="px-4 py-5 sm:p-6">
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <div class="relative rounded-lg overflow-hidden group cursor-pointer">
                        <img src="https://images.unsplash.com/photo-1682687220742-aba13b6e50ba" alt=""
                            class="w-full h-32 object-cover">
                        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent">
                            <div class="absolute bottom-0 left-0 right-0 p-4">
                                <p class="text-white font-medium">人物</p>
                                <p class="text-white/80 text-sm">128张照片</p>
                            </div>
                        </div>
                    </div>
                    <!-- 更多智能相册... -->
                </div>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { homeApi, type HomeData, type MemoriesData } from '@/api/home'
import { photoApi, type Photo } from '@/api/photos'

const homeData = ref<HomeData>()
const recentPhotos = ref<Photo[]>([])
const memoriesData = ref<MemoriesData>()

onMounted(async () => {
    await Promise.all([
        fetchHomeData(),
        fetchRecentPhotos(),
        fetchTodayMemories()
    ])
})

const fetchHomeData = async () => {
    try {
        const response = await homeApi.getHome()
        homeData.value = response
    } catch (error) {
        console.error('获取首页数据失败:', error)
    }
}

const fetchRecentPhotos = async () => {
    try {
        const response = await photoApi.getPhotos(
            {
                group_by: 'item',
                'sort_by': '-taken_time',
                page_size: 5
            }
        )
        recentPhotos.value = response[0].photos
    } catch (error) {
        console.error('获取最近照片失败:', error)
    }
}

const fetchTodayMemories = async () => {
    try {
        const response = await homeApi.getTodayMemories()
        memoriesData.value = response
    } catch (error) {
        console.error('获取今日回忆失败:', error)
    }
}

const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    })
}
</script>

<style>
@media (min-width: 1024px) {
    .about {
        min-height: 100vh;
        display: flex;
        align-items: center;
    }
}
</style>