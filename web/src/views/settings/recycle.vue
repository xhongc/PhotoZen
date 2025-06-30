<template>
    <!-- 右侧内容 -->
    <div class="flex-1 overflow-y-auto">
        <!-- 主内容区 -->
        <main class="flex-1">
            <div>
                <!-- 页面标题和操作按钮 -->
                <div class="mb-6">
                    <div class="flex justify-between items-center">
                        <div>
                            <h1 class="text-2xl font-semibold">回收站</h1>
                            <p class="mt-1 text-sm text-gray-500">项目将在删除30天后被永久删除</p>
                        </div>
                        <div class="flex space-x-3">
                            <button
                                @click="handleRestoreBatch"
                                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-base-100 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                                <i class="fas fa-trash-restore mr-2"></i>
                                恢复所选
                            </button>
                            <button
                                @click="handleDeleteBatch"
                                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
                                <i class="fas fa-trash-alt mr-2"></i>
                                永久删除所选
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 回收站内容 -->
                <div>
                    <div class="bg-base-100 rounded-lg shadow-sm">
                        <div class="border-b border-gray-200 px-6 py-4">
                            <div class="flex items-center">
                                <input type="checkbox"
                                    :checked="selectedItems.length === recycleList.length"
                                    @change="toggleSelectAll"
                                    class="h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500">
                                <span class="ml-3 text-sm text-gray-500">全选</span>
                                <span class="ml-4 text-sm text-gray-500">共 {{ totalCount }} 个项目</span>
                            </div>
                        </div>

                        <!-- 表格容器 -->
                        <div class="overflow-x-auto">
                            <!-- 列表视图 -->
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-base-200">
                                    <tr>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
                                            <span class="sr-only">选择</span>
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            名称
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            原位置
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            删除时间
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            剩余时间
                                        </th>
                                        <th scope="col" class="relative px-6 py-3">
                                            <span class="sr-only">操作</span>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-base-100 divide-y divide-gray-200">
                                    <tr v-for="item in recycleList" :key="item.path">
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <input type="checkbox"
                                                :checked="selectedItems.some(i => i.path === item.path)"
                                                @change="toggleSelect(item)"
                                                class="h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500">
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="flex items-center">
                                                <img v-if="item.preview_url" class="h-10 w-10 rounded object-cover"
                                                    :src="item.preview_url"
                                                    :alt="item.name">
                                                <div v-else class="h-10 w-10 rounded bg-gray-100 flex items-center justify-center">
                                                    <i class="fas fa-file text-gray-400"></i>
                                                </div>
                                                <div class="ml-4">
                                                    <div class="text-sm font-medium text-gray-900">{{ item.name }}</div>
                                                    <div class="text-sm text-gray-500">{{ formatFileSize(item.size) }}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="text-sm text-gray-900">{{ item.original_path }}</div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {{ item.delete_time }}
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="flex items-center">
                                                <div :class="[
                                                    'text-sm',
                                                    item.remaining_days <= 5 ? 'text-red-600' : 'text-yellow-600'
                                                ]">
                                                    剩余 {{ item.remaining_days }} 天
                                                </div>
                                                <div class="ml-2 w-16 bg-gray-200 rounded-full h-2">
                                                    <div :class="[
                                                        'h-2 rounded-full',
                                                        item.remaining_days <= 5 ? 'bg-red-600' : 'bg-yellow-600'
                                                    ]" :style="{ width: `${(item.remaining_days / 30) * 100}%` }"></div>
                                                </div>
                                            </div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button @click="handleRestore(item)" class="text-primary-600 hover:text-primary-900 mr-3">恢复</button>
                                            <button @click="handleDelete(item)" class="text-red-600 hover:text-red-900">删除</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        <!-- 分页 -->
                        <div
                            class="bg-base-100 px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
                            <div class="flex-1 flex justify-between sm:hidden">
                                <button
                                    @click="handlePageChange(currentPage - 1)"
                                    :disabled="currentPage === 1"
                                    class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-base-100 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                                    上一页
                                </button>
                                <button
                                    @click="handlePageChange(currentPage + 1)"
                                    :disabled="currentPage * pageSize >= totalCount"
                                    class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-base-100 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                                    下一页
                                </button>
                            </div>
                            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                                <div>
                                    <p class="text-sm text-gray-700">
                                        显示第 <span class="font-medium">{{ (currentPage - 1) * pageSize + 1 }}</span> 到
                                        <span class="font-medium">{{ Math.min(currentPage * pageSize, totalCount) }}</span>
                                        项，共 <span class="font-medium">{{ totalCount }}</span> 项
                                    </p>
                                </div>
                                <div>
                                    <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                                        aria-label="Pagination">
                                        <button
                                            @click="handlePageChange(currentPage - 1)"
                                            :disabled="currentPage === 1"
                                            class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-base-100 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                                            <span class="sr-only">上一页</span>
                                            <i class="fas fa-chevron-left"></i>
                                        </button>
                                        <button
                                            v-for="page in Math.ceil(totalCount / pageSize)"
                                            :key="page"
                                            @click="handlePageChange(page)"
                                            :class="[
                                                'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                                                currentPage === page
                                                    ? 'z-10 bg-primary-50 border-primary-500 text-primary-600'
                                                    : 'bg-base-100 border-gray-300 text-gray-500 hover:bg-gray-50'
                                            ]">
                                            {{ page }}
                                        </button>
                                        <button
                                            @click="handlePageChange(currentPage + 1)"
                                            :disabled="currentPage * pageSize >= totalCount"
                                            class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-base-100 text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                                            <span class="sr-only">下一页</span>
                                            <i class="fas fa-chevron-right"></i>
                                        </button>
                                    </nav>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { recycleApi, type RecycleItem } from '@/api/recycle'
import { formatFileSize } from '@/utils/format'

// 状态定义
const loading = ref(false)
const recycleList = ref<RecycleItem[]>([])
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedItems = ref<RecycleItem[]>([])

// 加载回收站列表
const loadRecycleList = async () => {
    try {
        loading.value = true
        const res = await recycleApi.getRecycleList(currentPage.value, pageSize.value)
        recycleList.value = res.data.items
        totalCount.value = res.data.total_count
    } catch (error) {
        console.error('加载回收站列表失败:', error)
    } finally {
        loading.value = false
    }
}

// 恢复文件
const handleRestore = async (item: RecycleItem) => {
    try {
        await recycleApi.restoreFile(item.path)
        loadRecycleList()
    } catch (error) {
        console.error('恢复文件失败:', error)
    }
}

// 批量恢复文件
const handleRestoreBatch = async () => {
    if (selectedItems.value.length === 0) {
        return
    }

    try {
        await recycleApi.restoreFilesBatch(selectedItems.value.map(item => item.path))
        selectedItems.value = []
        loadRecycleList()
    } catch (error) {
        console.error('批量恢复文件失败:', error)
    }
}

// 永久删除文件
const handleDelete = async (item: RecycleItem) => {
    try {
        
        
        await recycleApi.deleteFile(item.path)
        loadRecycleList()
    } catch (error) {
        if (error !== 'cancel') {
            console.error('删除文件失败:', error)
        }
    }
}

// 批量永久删除
const handleDeleteBatch = async () => {
    if (selectedItems.value.length === 0) {
        return
    }

    try {
        
        await recycleApi.deleteFilesBatch(selectedItems.value.map(item => item.path))
        selectedItems.value = []
        loadRecycleList()
    } catch (error) {
        if (error !== 'cancel') {
            console.error('批量删除文件失败:', error)
        }
    }
}

// 选择/取消选择文件
const toggleSelect = (item: RecycleItem) => {
    const index = selectedItems.value.findIndex(i => i.path === item.path)
    if (index === -1) {
        selectedItems.value.push(item)
    } else {
        selectedItems.value.splice(index, 1)
    }
}

// 全选/取消全选
const toggleSelectAll = () => {
    if (selectedItems.value.length === recycleList.value.length) {
        selectedItems.value = []
    } else {
        selectedItems.value = [...recycleList.value]
    }
}

// 页码改变
const handlePageChange = (page: number) => {
    currentPage.value = page
    loadRecycleList()
}

// 每页条数改变
const handleSizeChange = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
    loadRecycleList()
}

// 初始化
onMounted(() => {
    loadRecycleList()
})
</script>