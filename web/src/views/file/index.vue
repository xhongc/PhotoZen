<template>
    <div class="flex flex-col h-screen-header w-full">
        <!-- 导航栏 -->
        <header class="shadow-sm">
            <div class="min-w-full px-4">
                <div class="flex items-center justify-between h-16">
                    <!-- 导航路径 -->
                    <div class="flex items-center space-x-2 text-sm flex-1">
                        <button class="p-1.5 rounded hover:bg-base-100">
                            <i class="fas fa-arrow-left text-gray-600"></i>
                        </button>
                        <button class="p-1.5 rounded hover:bg-base-100">
                            <i class="fas fa-arrow-right text-gray-600"></i>
                        </button>
                        <button class="p-1.5 rounded hover:bg-base-100">
                            <i class="fas fa-arrow-up text-gray-600"></i>
                        </button>
                        <div class="h-4 w-px bg-base-300 mx-2"></div>
                        <div class="flex items-center bg-base-100 border rounded-md px-3 py-1.5 flex-1">
                            <i class="fas fa-folder text-gray-400 mr-2"></i>
                            <input type="text" value="/Photos/2023/Summer Vacation"
                                class="w-full text-sm focus:outline-none bg-transparent" readonly>
                        </div>
                    </div>

                    <!-- 搜索框 -->
                    <div class="flex items-center ml-4">
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <i class="fas fa-search text-gray-400"></i>
                            </div>
                            <input type="text"
                                class="block w-64 pl-10 pr-3 py-2 border border-base-300 rounded-md text-sm placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                                placeholder="搜索文件...">
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <!-- 工具栏 -->
        <div class="bg-base-100 border-t border-b border-base-200">
            <div class="min-w-7xl mx-auto px-4">
                <div class="flex items-center justify-between h-12">
                    <div class="flex items-center space-x-4">
                        <button
                            class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
                            <i class="fas fa-upload mr-2"></i>
                            上传
                        </button>
                        <button
                            class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
                            <i class="fas fa-folder-plus mr-2"></i>
                            新建文件夹
                        </button>
                    </div>

                    <div class="flex items-center space-x-2">
                        <button class="p-1.5 rounded text-gray-700 hover:bg-gray-100">
                            <i class="fas fa-list"></i>
                        </button>
                        <button class="p-1.5 rounded text-gray-400 hover:bg-gray-100">
                            <i class="fas fa-th-large"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 主内容区 -->
        <div class="flex-1 flex overflow-hidden">
            <!-- 左侧目录树 -->
            <div class="w-64 bg-base-100 border-r border-base-200 overflow-y-auto">
                <div class="p-4">
                    <div class="space-y-0.5">
                        <div class="flex items-center py-1.5 px-2 rounded hover:bg-base-200 cursor-pointer">
                            <i class="fas fa-chevron-down w-4 text-gray-400 mr-1"></i>
                            <i class="fas fa-folder text-yellow-400 mr-2"></i>
                            <span class="text-sm">Photos</span>
                        </div>
                        <div class="ml-6">
                            <div class="flex items-center py-1.5 px-2 rounded hover:bg-base-200 cursor-pointer">
                                <i class="fas fa-chevron-down w-4 text-gray-400 mr-1"></i>
                                <i class="fas fa-folder text-yellow-400 mr-2"></i>
                                <span class="text-sm">2023</span>
                            </div>
                            <div class="ml-6">
                                <div
                                    class="flex items-center py-1.5 px-2 rounded bg-blue-50 text-blue-600 cursor-pointer">
                                    <i class="fas fa-folder text-yellow-400 mr-2 ml-5"></i>
                                    <span class="text-sm">Summer Vacation</span>
                                </div>
                                <div class="flex items-center py-1.5 px-2 rounded hover:bg-base-200 cursor-pointer">
                                    <i class="fas fa-folder text-yellow-400 mr-2 ml-5"></i>
                                    <span class="text-sm">Family</span>
                                </div>
                            </div>
                            <div class="flex items-center py-1.5 px-2 rounded hover:bg-base-200 cursor-pointer">
                                <i class="fas fa-chevron-right w-4 text-gray-400 mr-1"></i>
                                <i class="fas fa-folder text-yellow-400 mr-2"></i>
                                <span class="text-sm">2022</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 右侧文件列表 -->
            <div class="flex-1 overflow-y-auto">
                <div class="p-6">
                    <!-- 列表视图 -->
                    <table class="min-w-full divide-y divide-base-200 bg-base-100 shadow-sm rounded-lg">
                        <thead>
                            <tr class="bg-base-100">
                                <th scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-5/12">
                                    名称</th>
                                <th scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-2/12">
                                    修改日期</th>
                                <th scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-2/12">
                                    类型</th>
                                <th scope="col"
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-2/12">
                                    大小</th>
                                <th scope="col"
                                    class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-1/12">
                                    操作</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-base-200">
                            <!-- 文件夹 -->
                            <tr class="hover:bg-base-200">
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <i class="fas fa-folder text-yellow-400 mr-3"></i>
                                        <span class="text-sm text-primary-600">Venice</span>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2023/07/15</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">文件夹</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--</td>
                                <td class="px-6 py-4 whitespace-nowrap text-right">
                                    <button class="text-gray-400 hover:text-gray-500">
                                        <i class="fas fa-ellipsis-h"></i>
                                    </button>
                                </td>
                            </tr>

                            <!-- 图片文件 -->
                            <tr class="hover:bg-base-200">
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <img src="https://images.unsplash.com/photo-1499678329028-101435549a4e"
                                            class="w-8 h-8 rounded object-cover mr-3">
                                        <span class="text-sm text-primary-600">IMG_001.jpg</span>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2023/07/15</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">JPEG 图片</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">3.5 MB</td>
                                <td class="px-6 py-4 whitespace-nowrap text-right">
                                    <button class="text-gray-400 hover:text-gray-500">
                                        <i class="fas fa-ellipsis-h"></i>
                                    </button>
                                </td>
                            </tr>

                            <tr class="hover:bg-base-200">
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="flex items-center">
                                        <img src="https://images.unsplash.com/photo-1516483638261-f4dbaf036963"
                                            class="w-8 h-8 rounded object-cover mr-3">
                                        <span class="text-sm text-primary-600">IMG_002.jpg</span>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2023/07/15</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">JPEG 图片</td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">2.8 MB</td>
                                <td class="px-6 py-4 whitespace-nowrap text-right">
                                    <button class="text-gray-400 hover:text-gray-500">
                                        <i class="fas fa-ellipsis-h"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- 状态栏 -->
                    <div class="mt-4 text-sm text-gray-500">
                        共 3 个项目（1 个文件夹，2 个文件）
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
</script>