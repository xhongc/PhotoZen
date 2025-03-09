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
                                <dt class="text-sm font-medium text-gray-500 truncate">总照片数</dt>
                                <dd class="text-lg font-semibold text-primary-600">12,361</dd>
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
                                <dt class="text-sm font-medium text-gray-500 truncate">相册数</dt>
                                <dd class="text-lg font-semibold text-primary-600">56</dd>
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
                                <dt class="text-sm font-medium text-gray-500 truncate">收藏数</dt>
                                <dd class="text-lg font-semibold text-primary-600">284</dd>
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
                                <dt class="text-sm font-medium text-gray-500 truncate">存储空间</dt>
                                <dd class="text-lg font-semibold text-primary-600">45.8 GB</dd>
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
                    <!-- 示例照片项 -->
                    <div class="group relative">
                        <div class="aspect-w-1 aspect-h-1 rounded-lg overflow-hidden">
                            <img src="https://images.unsplash.com/photo-1682687220742-aba13b6e50ba" alt=""
                                class="object-cover">
                            <div
                                class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-opacity">
                            </div>
                        </div>
                        <p class="mt-2 text-sm text-gray-500">2024-03-20</p>
                    </div>
                    <!-- 更多照片项... -->
                </div>
            </div>
        </div>

        <!-- 今日回忆 -->
        <div class="bg-base-100 shadow rounded-lg mb-6">
            <div class="px-4 py-5 border-b border-base-200 sm:px-6">
                <div class="flex items-center justify-between">
                    <h3 class="text-lg leading-6 font-medium text-base-900">今日回忆</h3>
                    <span class="text-sm text-primary-600">2年前的今天</span>
                </div>
            </div>
            <div class="px-4 py-5 sm:p-6">
                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                    <div class="relative rounded-lg overflow-hidden">
                        <img src="https://images.unsplash.com/photo-1682687220742-aba13b6e50ba" alt=""
                            class="w-full h-48 object-cover">
                        <div class="absolute bottom-0 left-0 right-0 px-4 py-2 bg-gradient-to-t from-black">
                            <p class="text-white text-sm">2022年3月20日</p>
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

<style>
@media (min-width: 1024px) {
    .about {
        min-height: 100vh;
        display: flex;
        align-items: center;
    }
}
</style>