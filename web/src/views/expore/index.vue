<template>
    <!-- 主内容区 -->
    <main class="flex-1 overflow-auto">
        <div class="py-6">
            <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
                <h1 class="text-2xl font-semibold text-primary-600 mb-6">智能分类</h1>

                <!-- AI 照片分类 -->
                <section class="mb-10">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-xl font-medium text-primary-600">AI 照片分类</h2>
                        <button class="text-sm font-medium text-primary-600 hover:text-primary-500">查看全部</button>
                    </div>

                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <!-- 人物 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden group">
                            <div class="relative aspect-w-16 aspect-h-12">
                                <img src="https://images.unsplash.com/photo-1521119989659-a83eee488004?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1023"
                                    alt="人物"
                                    class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                <div
                                    class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                </div>
                                <div class="absolute bottom-0 left-0 right-0 p-4">
                                    <p class="text-white font-medium">人物</p>
                                    <p class="text-white/80 text-sm">128张照片</p>
                                </div>
                            </div>
                        </div>
                        <!-- 风景 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden group">
                            <div class="relative aspect-w-16 aspect-h-12">
                                <img src="https://images.unsplash.com/photo-1511884642898-4c92249e20b6?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1470"
                                    alt="风景"
                                    class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                <div
                                    class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                </div>
                                <div class="absolute bottom-0 left-0 right-0 p-4">
                                    <p class="text-white font-medium">风景</p>
                                    <p class="text-white/80 text-sm">94张照片</p>
                                </div>
                            </div>
                        </div>

                        <!-- 美食 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden group">
                            <div class="relative aspect-w-16 aspect-h-12">
                                <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1470"
                                    alt="美食"
                                    class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                <div
                                    class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                </div>
                                <div class="absolute bottom-0 left-0 right-0 p-4">
                                    <p class="text-white font-medium">美食</p>
                                    <p class="text-white/80 text-sm">67张照片</p>
                                </div>
                            </div>
                        </div>

                        <!-- 建筑 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden group">
                            <div class="relative aspect-w-16 aspect-h-12">
                                <img src="https://images.unsplash.com/photo-1487958449943-2429e8be8625?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1470"
                                    alt="建筑"
                                    class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                <div
                                    class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                </div>
                                <div class="absolute bottom-0 left-0 right-0 p-4">
                                    <p class="text-white font-medium">建筑</p>
                                    <p class="text-white/80 text-sm">53张照片</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- 时间与地点归档 -->
                <section class="mb-10">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-xl font-medium text-primary-600">时间与地点归档</h2>
                        <div class="flex space-x-2">
                            <button type="button"
                                class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                                <i class="fas fa-calendar-alt mr-1.5"></i>
                                按时间
                            </button>
                            <button type="button"
                                class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                                <i class="fas fa-map-marker-alt mr-1.5"></i>
                                按地点
                            </button>
                        </div>
                    </div>

                    <!-- 时间轴 -->
                    <div class="bg-base-100 rounded-lg shadow-sm p-6">
                        <div class="space-y-8">
                            <!-- 2023年 -->
                            <div>
                                <h3 class="text-lg font-medium text-primary-600 mb-4">2023年</h3>
                                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <!-- 十月 -->
                                    <div class="bg-base-100 border border-base-200 rounded-lg overflow-hidden group">
                                        <div class="relative aspect-w-16 aspect-h-12">
                                            <img src="https://images.unsplash.com/photo-1521119989659-a83eee488004?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1023"
                                                alt="2023年10月"
                                                class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                            <div
                                                class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                            </div>
                                            <div class="absolute bottom-0 left-0 right-0 p-4">
                                                <p class="text-white font-medium">10月</p>
                                                <p class="text-white/80 text-sm">42张照片</p>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- 九月 -->
                                    <div class="bg-base-100 border border-base-200 rounded-lg overflow-hidden group">
                                        <div class="relative aspect-w-16 aspect-h-12">
                                            <img src="https://images.unsplash.com/photo-1521119989659-a83eee488004?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1023"
                                                alt="2023年9月"
                                                class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                            <div
                                                class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                            </div>
                                            <div class="absolute bottom-0 left-0 right-0 p-4">
                                                <p class="text-white font-medium">9月</p>
                                                <p class="text-white/80 text-sm">58张照片</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- 地点视图 (默认隐藏) -->
                            <div class="hidden">
                                <h3 class="text-lg font-medium text-gray-900 mb-4">按地点</h3>
                                <div class="aspect-w-16 aspect-h-9 mb-4">
                                    <div class="w-full h-full rounded-lg bg-gray-200 flex items-center justify-center">
                                        <p class="text-gray-500">世界地图将在此处显示</p>
                                    </div>
                                </div>
                                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    <!-- 北京 -->
                                    <div class="bg-base-100 border border-base-200 rounded-lg overflow-hidden group">
                                        <div class="relative aspect-w-16 aspect-h-12">
                                            <img src="https://images.unsplash.com/photo-1599571234909-29ed5d1321d6?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1000"
                                                alt="北京"
                                                class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                            <div
                                                class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                            </div>
                                            <div class="absolute bottom-0 left-0 right-0 p-4">
                                                <p class="text-white font-medium">北京</p>
                                                <p class="text-white/80 text-sm">65张照片</p>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- 上海 -->
                                    <div class="bg-base-100 border border-base-200 rounded-lg overflow-hidden group">
                                        <div class="relative aspect-w-16 aspect-h-12">
                                            <img src="https://images.unsplash.com/photo-1538428494232-9c0d8a3ab403?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=1000"
                                                alt="上海"
                                                class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                                            <div
                                                class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent">
                                            </div>
                                            <div class="absolute bottom-0 left-0 right-0 p-4">
                                                <p class="text-white font-medium">上海</p>
                                                <p class="text-white/80 text-sm">47张照片</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- 人脸识别 -->
                <section class="mb-10">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-xl font-medium text-primary-600">人脸识别</h2>
                        <button class="text-sm font-medium text-primary-600 hover:text-primary-500 flex items-center">
                            <i class="fas fa-user-plus mr-1"></i>
                            添加人物
                        </button>
                    </div>

                    <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
                        <!-- 家人1 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden text-center group">
                            <div class="relative aspect-w-1 aspect-h-1 mb-2">
                                <img src="https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=500"
                                    alt="小雨"
                                    class="w-full h-full object-cover rounded-full object-center group-hover:opacity-90 transition-opacity mx-auto p-2">
                            </div>
                            <div class="p-2">
                                <p class="font-medium text-primary-600">小雨</p>
                                <p class="text-gray-500 text-sm">43张照片</p>
                            </div>
                        </div>

                        <!-- 家人2 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden text-center group">
                            <div class="relative aspect-w-1 aspect-h-1 mb-2">
                                <img src="https://images.unsplash.com/photo-1599566150163-29194dcaad36?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=500"
                                    alt="小明"
                                    class="w-full h-full object-cover rounded-full object-center group-hover:opacity-90 transition-opacity mx-auto p-2">
                            </div>
                            <div class="p-2">
                                <p class="font-medium text-primary-600">小明</p>
                                <p class="text-gray-500 text-sm">38张照片</p>
                            </div>
                        </div>

                        <!-- 家人3 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden text-center group">
                            <div class="relative aspect-w-1 aspect-h-1 mb-2">
                                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=500"
                                    alt="小红"
                                    class="w-full h-full object-cover rounded-full object-center group-hover:opacity-90 transition-opacity mx-auto p-2">
                            </div>
                            <div class="p-2">
                                <p class="font-medium text-primary-600">小红</p>
                                <p class="text-gray-500 text-sm">29张照片</p>
                            </div>
                        </div>

                        <!-- 朋友1 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden text-center group">
                            <div class="relative aspect-w-1 aspect-h-1 mb-2">
                                <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&q=80&w=500"
                                    alt="老王"
                                    class="w-full h-full object-cover rounded-full object-center group-hover:opacity-90 transition-opacity mx-auto p-2">
                            </div>
                            <div class="p-2">
                                <p class="font-medium text-primary-600">老王</p>
                                <p class="text-gray-500 text-sm">18张照片</p>
                            </div>
                        </div>

                        <!-- 未识别人脸 -->
                        <div class="bg-base-100 rounded-lg shadow-sm overflow-hidden text-center">
                            <div class="relative aspect-w-1 aspect-h-1 mb-2">
                                <div
                                    class="w-full h-full flex items-center justify-center bg-base-200 rounded-full p-2 mx-auto">
                                    <i class="fas fa-question text-3xl text-base-100 h-80"></i>
                                </div>
                            </div>
                            <div class="p-2">
                                <p class="font-medium text-primary-600">未识别的人脸</p>
                                <p class="text-gray-500 text-sm">请标记</p>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </main>
</template>

<script setup lang="ts">

</script>