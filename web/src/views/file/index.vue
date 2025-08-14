<template>
  <div class="flex flex-col h-screen-header w-full">
    <!-- 导航栏 -->
    <header class="shadow-sm">
      <div class="min-w-full px-4">
        <div class="flex items-center justify-between h-16">
          <!-- 导航路径 -->
          <div class="flex items-center space-x-2 text-sm flex-1">
            <button class="p-1.5 rounded hover:bg-base-100" @click="navigateBack">
              <i class="fas fa-arrow-left text-gray-600"></i>
            </button>
            <button class="p-1.5 rounded hover:bg-base-100" @click="navigateForward">
              <i class="fas fa-arrow-right text-gray-600"></i>
            </button>
            <button class="p-1.5 rounded hover:bg-base-100" @click="navigateDown">
              <i class="fas fa-arrow-down text-gray-600"></i>
            </button>
            <div class="h-4 w-px bg-base-300 mx-2"></div>
            <div class="flex items-center bg-base-100 border rounded-md px-3 py-1.5 flex-1">
              <i class="fas fa-folder text-gray-400 mr-2"></i>
              <div class="flex items-center space-x-1 text-sm">
                <button class="hover:text-primary-600" @click="navigateTo('/')">media</button>
                <template v-for="(segment, index) in pathSegments" :key="index">
                  <span class="text-gray-400">/</span>
                  <button class="hover:text-primary-600" @click="navigateToSegment(index)">
                    {{ segment }}
                  </button>
                </template>
              </div>
            </div>
          </div>

          <!-- 搜索框 -->
          <div class="flex items-center ml-4">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-search text-gray-400"></i>
              </div>
              <input type="text" v-model="searchQuery"
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
            <label
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded cursor-pointer">
              <i class="fas fa-upload mr-2"></i>
              上传
              <input type="file" class="hidden" multiple @change="handleUpload" accept="image/*">
            </label>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              新建文件夹
            </button>
            <button @click="handleScanLibrary"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-search mr-2"></i>
              扫描入库
            </button>
            <button @click="handleGenerateThumbnails"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-image mr-2"></i>
              生成缩略图
            </button>
            <button @click="handleCheckDuplicates"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-copy mr-2"></i>
              重复检查
            </button>
            <button @click="handleBackupUpload"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-cloud-upload-alt mr-2"></i>
              备份上传
            </button>
            <button @click="handleFaceRecognition"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-user mr-2"></i>
              人像识别
            </button>
            <button @click="handleClipAnalysis"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-brain mr-2"></i>
              CLIP识别
            </button>
            <button @click="handleOcrAnalysis"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-text-height mr-2"></i>
              OCR识别
            </button>
            <button @click="handleVideoTranscode"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-video mr-2"></i>
              视频转码
            </button>
          </div>

          <div class="flex items-center space-x-2">
            <button class="p-1.5 rounded" :class="viewMode === 'list' ? 'text-gray-700' : 'text-gray-400'"
              @click="toggleViewMode('list')">
              <i class="fas fa-list"></i>
            </button>
            <button class="p-1.5 rounded" :class="viewMode === 'grid' ? 'text-gray-700' : 'text-gray-400'"
              @click="toggleViewMode('grid')">
              <i class="fas fa-th-large"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 上传进度条 -->
    <div v-if="isUploading" class="fixed bottom-0 left-0 right-0 p-2">
      <div class="max-w-full">
        <div class="flex items-center justify-between">
          <span class="text-sm">正在上传...</span>
          <span class="text-sm">{{ uploadProgress }}%</span>
        </div>
        <div class="w-full bg-neutral bg-opacity-20 rounded-full h-1.5 mt-1">
          <div class="bg-primary h-1.5 rounded-full" :style="{ width: `${uploadProgress}%` }"></div>
        </div>
      </div>
    </div>

    <!-- 任务进度条 -->
    <div v-if="isProcessing" class="fixed bottom-0 left-0 right-0 p-4 bg-white shadow-lg border-t">
      <div class="max-w-4xl mx-auto">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center">
            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary mr-2"></div>
            <span class="text-sm font-medium">{{ taskMessage || '正在处理...' }}</span>
          </div>
          <div class="flex items-center">
            <span class="text-sm text-gray-500 mr-2">{{ taskProgress }}%</span>
            <button @click="isProcessing = false" class="text-gray-400 hover:text-gray-600">
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div class="bg-primary h-2 rounded-full transition-all duration-300" 
               :style="{ width: `${taskProgress}%` }"></div>
        </div>
      </div>
    </div>

    <!-- 任务结果弹窗 -->
    <div v-if="taskResults && taskResults.duplicate_groups" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-96 overflow-y-auto">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">重复文件检查结果</h3>
          <button @click="taskResults = null" class="text-gray-400 hover:text-gray-600">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="space-y-4">
          <div v-for="(group, index) in taskResults.duplicate_groups" :key="index" 
               class="border rounded-lg p-3">
            <div class="text-sm font-medium text-gray-700 mb-2">
              原始文件: {{ group.original }}
            </div>
            <div class="text-xs text-gray-500 mb-1">
              文件大小: {{ formatFileSize(group.size) }}
            </div>
            <div class="text-xs text-red-600">
              重复文件 ({{ group.duplicates.length }}个):
            </div>
            <ul class="text-xs text-gray-600 ml-4">
              <li v-for="duplicate in group.duplicates" :key="duplicate">
                {{ duplicate }}
              </li>
            </ul>
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
              <i class="fas fa-folder-open mr-2 text-yellow-400"></i>
              <span class="text-sm">{{ pathSegments[pathSegments.length - 1] }}</span>
            </div>
            <div v-for="file in files.filter(f => f.type === 'directory')" :key="file.path"
              class="flex items-center py-1.5 px-4 rounded hover:bg-base-200 cursor-pointer"
              :class="{ 'bg-blue-50 text-blue-600': currentPath === file.path }" @click="navigateTo(file.path)">
              <i class="fas fa-folder text-yellow-400 mr-2"></i>
              <span class="text-sm">{{ file.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧文件列表 -->
      <div class="flex-1 overflow-hidden">
        <!-- 列表视图 -->
        <div v-if="viewMode === 'list'" class="h-full flex flex-col">
          <!-- 表头 -->
          <div class="bg-base-100 border-b border-base-200 px-6 py-3">
            <div class="flex items-center">
              <div class="w-5/12 text-xs font-medium text-gray-500 uppercase tracking-wider">名称</div>
              <div class="w-2/12 text-xs font-medium text-gray-500 uppercase tracking-wider">修改日期</div>
              <div class="w-2/12 text-xs font-medium text-gray-500 uppercase tracking-wider">类型</div>
              <div class="w-2/12 text-xs font-medium text-gray-500 uppercase tracking-wider">大小</div>
              <div class="w-1/12 text-xs font-medium text-gray-500 uppercase tracking-wider text-right">操作</div>
            </div>
          </div>
          <!-- 虚拟列表内容 -->
          <div class="flex-1">
            <VirtualFileList
              :files="files"
              :view-mode="viewMode"
              :current-preview-path="currentPreviewPath"
              @file-click="handleFileClick"
              @delete="handleDelete"
            />
          </div>
          <!-- 状态栏 -->
          <div class="bg-base-100 border-t border-base-200 px-6 py-3 text-sm text-gray-500">
            共 {{ files.length }} 个项目（{{ files.filter(f => f.type === 'directory').length }} 个文件夹，{{ files.filter(f => f.type === 'file').length }} 个文件）
          </div>
        </div>

        <!-- 网格视图 -->
        <div v-else class="h-full">
          <VirtualFileGrid
            :files="files"
            :current-preview-path="currentPreviewPath"
            @file-click="handleFileClick"
          />
        </div>
      </div>
      <!-- 添加图片预览组件 -->
      <ImagePreview v-model:show="showImagePreview" :image-url="previewImageUrl" :image-list="previewImageList"
        v-model:current-index="previewCurrentIndex"
        @update:show="(val) => { showImagePreview = val; if (!val) handlePreviewClose(); }" />
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import { webdavApi, type WebDAVFile } from '@/api/webdav'
import { 
  fileApi, 
  type ScanLibraryRequest,
  type GenerateThumbnailsRequest,
  type CheckDuplicatesRequest,
  type BackupUploadRequest,
  type FaceRecognitionRequest,
  type ClipAnalysisRequest,
  type OcrAnalysisRequest,
  type VideoTranscodeRequest,
  type TaskStatusResponse
} from '@/api/file'
import { useRouter } from 'vue-router'
import ImagePreview from '@/components/ImagePreview.vue'
import LazyImage from '@/components/LazyImage.vue'
import VirtualFileList from '@/components/VirtualFileList.vue'
import VirtualFileGrid from '@/components/VirtualFileGrid.vue'
import notify from '@/components/notify'

const router = useRouter()

// 定义API返回的数据结构
interface WebDAVResponse {
  name: string | null;
  path: string;
  children: Array<{
    name: string;
    is_collection: boolean;
    path: string;
    url: string;
    last_modified: string;
    type: 'file' | 'directory';
  }>;
}

// 状态定义
const currentPath = ref('/')
const files = ref<WebDAVFile[]>([])
const loading = ref(false)
const viewMode = ref<'list' | 'grid'>('list')
const searchQuery = ref('')
const uploadProgress = ref(0)
const isUploading = ref(false)

// 工具栏功能状态管理
const currentTask = ref<string | null>(null)
const taskProgress = ref(0)
const taskMessage = ref('')
const isProcessing = ref(false)
const taskResults = ref<any>(null)

// 添加当前预览图片的路径
const currentPreviewPath = ref('')

// 计算当前预览的文件
const currentPreviewFile = computed(() => {
  return files.value.find(f => f.path === currentPreviewPath.value)
})

// 导航历史
const navigationHistory = ref<string[]>(['/'])
const currentHistoryIndex = ref(0)

// 计算路径分段
const pathSegments = computed(() => {
  return currentPath.value.split('/').filter(Boolean)
})

// 图片预览相关状态
const showImagePreview = ref(false)
const previewImageUrl = ref('')
const previewImageList = ref<string[]>([])
const previewCurrentIndex = ref(0)

// 初始化 WebDAV 配置
onMounted(async () => {
  try {
    // 从localStorage或vuex获取认证信息
    const token = localStorage.getItem('token')
    if (!token) {
      // 如果没有token，重定向到登录页
      window.location.href = '/login'
      return
    }

    // 设置WebDAV配置
    webdavApi.setConfig({
      username: token,
      password: '' // 使用token作为认证方式
    })

    // 测试连接
    await loadDirectory(currentPath.value)
  } catch (error: any) {
    console.error('初始化失败:', error)
    // 如果认证失败，重定向到登录页
    window.location.href = '/login'
  }
})

// 加载目录内容
const loadDirectory = async (path: string) => {
  try {
    loading.value = true
    const response = await webdavApi.listDirectory(path)
    const webDAVResponse = response as unknown as WebDAVResponse
    // 处理返回的数据结构
    const newFiles = webDAVResponse.children.map(item => ({
      name: item.name,
      path: item.path,
      url: item.url,
      type: item.type,
      basename: item.name,
      lastmod: item.last_modified,
      mime: item.type === 'directory' ? 'directory' : 'image/jpeg',
      size: 0,
      etag: '' // 添加必需的etag字段
    }))
    
    // 分批渲染文件，避免一次性渲染大量文件导致卡顿
    files.value = []
    await nextTick()
    
    const batchSize = 50
    for (let i = 0; i < newFiles.length; i += batchSize) {
      const batch = newFiles.slice(i, i + batchSize)
      files.value.push(...batch)
      await nextTick()
      
      // 小延迟让浏览器有时间渲染
      if (i + batchSize < newFiles.length) {
        await new Promise(resolve => setTimeout(resolve, 10))
      }
    }
  } catch (error: any) {
    console.error('加载目录失败:', error)
    // 如果是认证错误，重定向到登录页
    if (error.response?.status === 401) {
      window.location.href = '/login'
    }
  } finally {
    loading.value = false
  }
}

// 导航操作
const navigateTo = (path: string) => {
  // 更新当前路径
  currentPath.value = path

  // 更新导航历史
  if (currentHistoryIndex.value < navigationHistory.value.length - 1) {
    // 如果在历史记录中间，删除当前位置之后的所有记录
    navigationHistory.value = navigationHistory.value.slice(0, currentHistoryIndex.value + 1)
  }
  navigationHistory.value.push(path)
  currentHistoryIndex.value = navigationHistory.value.length - 1

  // 加载新目录内容
  loadDirectory(path + '/')
}

const navigateBack = () => {
  if (currentHistoryIndex.value > 0) {
    currentHistoryIndex.value--
    const previousPath = navigationHistory.value[currentHistoryIndex.value]
    currentPath.value = previousPath
    loadDirectory(previousPath)
  }
}

const navigateForward = () => {
  if (currentHistoryIndex.value < navigationHistory.value.length - 1) {
    currentHistoryIndex.value++
    const nextPath = navigationHistory.value[currentHistoryIndex.value]
    currentPath.value = nextPath
    loadDirectory(nextPath)
  }
}

const navigateUp = () => {
  const parentPath = currentPath.value.split('/').slice(0, -1).join('/') || '/'
  navigateTo(parentPath)
}

// 刷新当前目录
const navigateDown = () => {
  loadDirectory(currentPath.value)
}

// 文件上传处理
const handleUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  try {
    isUploading.value = true
    uploadProgress.value = 0

    for (const file of input.files) {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('path', currentPath.value)

      const xhr = new XMLHttpRequest()
      xhr.open('POST', '/api/files/upload')
      xhr.setRequestHeader('Authorization', `Bearer ${localStorage.getItem('token')}`)

      // 处理上传进度
      xhr.upload.onprogress = (event: ProgressEvent) => {
        if (event.lengthComputable) {
          uploadProgress.value = Math.round((event.loaded * 100) / event.total)
        }
      }

      // 处理响应
      await new Promise<void>((resolve, reject) => {
        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve()
          } else {
            reject(new Error(xhr.responseText))
          }
        }
        xhr.onerror = () => reject(new Error('上传失败'))
        xhr.send(formData)
      })

      const result = JSON.parse(xhr.responseText)
      console.log('上传成功:', result)
      notify.myMsg.notify({
        content: '上传成功',
        type: 'success',
        time: 4000
      })
    }
    // 刷新文件列表
    await loadDirectory(currentPath.value)
  } catch (error: any) {
    notify.myMsg.notify({
      content: '上传失败',
      type: 'error',
      time: 4000
    })
  } finally {
    isUploading.value = false
    uploadProgress.value = 0
    // 清空input，允许重复上传相同文件
    if (input) {
      input.value = ''
    }
  }
}


const handleCreateDirectory = async () => {
  const name = prompt('请输入文件夹名称:')
  if (!name) return

  try {
    await webdavApi.createDirectory(`${currentPath.value}/${name}`)
    loadDirectory(currentPath.value)
  } catch (error) {
    console.error('创建文件夹失败:', error)
  }
}

const handleDelete = async (path: string) => {
  try {
    await fileApi.deleteFile(path).then(res => {
      if (res.data.result) {
        loadDirectory(currentPath.value)
        notify.myMsg.notify({
          title: '删除成功',
          content: '文件已移入回收站',
          type: 'success',
          time: 2000
        })
      } else {
        notify.myMsg.notify({
          title: '删除失败',
          content: res.data.msg,
          type: 'error',
          time: 4000
        })
      }
    })
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 切换视图模式
const toggleViewMode = (mode: 'list' | 'grid') => {
  viewMode.value = mode
}

// 格式化文件大小
const formatFileSize = (size: number) => {
  if (size === 0) return '--'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let index = 0
  while (size >= 1024 && index < units.length - 1) {
    size /= 1024
    index++
  }
  return `${size.toFixed(1)} ${units[index]}`
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 导航到指定层级
const navigateToSegment = (index: number) => {
  const path = '/' + pathSegments.value.slice(0, index + 1).join('/')
  navigateTo(path)
}

// 处理文件点击事件
const handleFileClick = (file: WebDAVFile) => {
  if (file.type === 'directory') {
    navigateTo(file.path)
  } else if (file.mime.startsWith('image/')) {
    // 获取当前目录下的所有图片文件
    const imageFiles = files.value.filter(f => f.mime.startsWith('image/'))
    previewImageList.value = imageFiles.map(f => "http://127.0.0.1:8000/api/fsdav/" + f.path)
    previewCurrentIndex.value = imageFiles.findIndex(f => f.path === file.path)
    currentPreviewPath.value = file.path
    showImagePreview.value = true
  }
}

// 添加滚动定位方法
const scrollToFile = (filePath: string) => {
  const fileElement = document.querySelector(`[data-file-path="${filePath}"]`)
  if (fileElement) {
    fileElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

// 处理预览关闭
const handlePreviewClose = () => {
  if (previewImageList.value && previewCurrentIndex.value !== undefined) {
    const currentImagePath = previewImageList.value[previewCurrentIndex.value]
    const filePath = currentImagePath.replace('http://127.0.0.1:8000/api/fsdav/', '')
    currentPreviewPath.value = filePath
    scrollToFile(filePath)
  }
}

// =============工具栏功能处理方法=============

// 通用任务状态监控
const monitorTask = async (taskId: string) => {
  currentTask.value = taskId
  isProcessing.value = true
  
  const checkStatus = async () => {
    try {
      const response = await fileApi.getTaskStatus(taskId)
      const status = response.data
      
      taskProgress.value = status.progress
      taskMessage.value = status.message || ''
      
      if (status.status === 'completed') {
        taskResults.value = status.result
        isProcessing.value = false
        notify.myMsg.notify({
          title: '任务完成',
          content: status.message || '操作已完成',
          type: 'success',
          time: 3000
        })
      } else if (status.status === 'failed') {
        isProcessing.value = false
        notify.myMsg.notify({
          title: '任务失败',
          content: status.message || '操作失败',
          type: 'error',
          time: 4000
        })
      } else {
        // 继续监控
        setTimeout(checkStatus, 2000)
      }
    } catch (error) {
      console.error('监控任务状态失败:', error)
      isProcessing.value = false
    }
  }
  
  checkStatus()
}

// 扫描入库
const handleScanLibrary = async () => {
  try {
    const response = await fileApi.scanLibrary({
      path: currentPath.value,
      recursive: true
    })
    
    const result = response.data
    
    if (result.task_id) {
      monitorTask(result.task_id)
    }
    
    notify.myMsg.notify({
      title: '扫描入库',
      content: `发现 ${result.processed} 张图片，导入 ${result.imported} 张`,
      type: 'success',
      time: 3000
    })
    
    if (result.errors.length > 0) {
      console.error('扫描错误:', result.errors)
    }
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '扫描失败',
      content: error.response?.data?.message || '扫描入库操作失败',
      type: 'error',
      time: 4000
    })
  }
}

// 生成缩略图
const handleGenerateThumbnails = async () => {
  try {
    const response = await fileApi.generateThumbnails({
      path: currentPath.value,
      sizes: [200, 400, 800]
    })
    
    const result = response.data
    
    if (result.task_id) {
      monitorTask(result.task_id)
    }
    
    notify.myMsg.notify({
      title: '生成缩略图',
      content: `生成 ${result.generated} 个，跳过 ${result.skipped} 个`,
      type: 'success',
      time: 3000
    })
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '生成失败',
      content: error.response?.data?.message || '生成缩略图失败',
      type: 'error',
      time: 4000
    })
  }
}

// 重复检查
const handleCheckDuplicates = async () => {
  try {
    const response = await fileApi.checkDuplicates({
      path: currentPath.value
    })
    
    const result = response.data
    
    notify.myMsg.notify({
      title: '重复检查',
      content: `发现 ${result.total_duplicates} 个重复文件，可节省 ${formatFileSize(result.space_saved)} 空间`,
      type: 'success',
      time: 5000
    })
    
    // 这里可以显示详细的重复文件列表
    taskResults.value = result
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '检查失败',
      content: error.response?.data?.message || '重复检查失败',
      type: 'error',
      time: 4000
    })
  }
}

// 备份上传
const handleBackupUpload = async () => {
  const destination = prompt('请输入备份目标路径:')
  if (!destination) return
  
  try {
    const response = await fileApi.backupUpload({
      source: currentPath.value,
      destination: destination,
      compression: true
    })
    
    const result = response.data
    
    if (result.task_id) {
      monitorTask(result.task_id)
    }
    
    notify.myMsg.notify({
      title: '备份上传',
      content: `备份任务已启动，预估大小: ${formatFileSize(result.estimated_size || 0)}`,
      type: 'success',
      time: 3000
    })
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '备份失败',
      content: error.response?.data?.message || '备份上传失败',
      type: 'error',
      time: 4000
    })
  }
}

// 人像识别
const handleFaceRecognition = async () => {
  try {
    const response = await fileApi.faceRecognition({
      path: currentPath.value,
      create_albums: true
    })
    
    const result = response.data
    
    if (result.task_id) {
      monitorTask(result.task_id)
    }
    
    notify.myMsg.notify({
      title: '人像识别',
      content: `检测到 ${result.faces_detected} 张人脸，识别出 ${result.persons.length} 个人物`,
      type: 'success',
      time: 4000
    })
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '识别失败',
      content: error.response?.data?.message || '人像识别失败',
      type: 'error',
      time: 4000
    })
  }
}

// CLIP识别
const handleClipAnalysis = async () => {
  try {
    const response = await fileApi.clipAnalysis({
      path: currentPath.value,
      confidence_threshold: 0.5
    })
    
    const result = response.data
    
    if (result.task_id) {
      monitorTask(result.task_id)
    }
    
    notify.myMsg.notify({
      title: 'CLIP识别',
      content: `识别出标签: ${result.tags.join(', ')}`,
      type: 'success',
      time: 4000
    })
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '识别失败',
      content: error.response?.data?.message || 'CLIP识别失败',
      type: 'error',
      time: 4000
    })
  }
}

// OCR识别
const handleOcrAnalysis = async () => {
  try {
    const response = await fileApi.ocrAnalysis({
      path: currentPath.value,
      language: 'zh'
    })
    
    const result = response.data
    
    if (result.task_id) {
      monitorTask(result.task_id)
    }
    
    notify.myMsg.notify({
      title: 'OCR识别',
      content: `识别文字: ${result.text.substring(0, 50)}...`,
      type: 'success',
      time: 4000
    })
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '识别失败',
      content: error.response?.data?.message || 'OCR识别失败',
      type: 'error',
      time: 4000
    })
  }
}

// 视频转码
const handleVideoTranscode = async () => {
  const format = prompt('请输入目标格式 (mp4/avi/mkv):', 'mp4')
  if (!format) return
  
  try {
    const response = await fileApi.videoTranscode({
      path: currentPath.value,
      format: format,
      quality: 'medium'
    })
    
    const result = response.data
    
    if (result.task_id) {
      monitorTask(result.task_id)
    }
    
    notify.myMsg.notify({
      title: '视频转码',
      content: `转码任务已启动，预估时间: ${result.estimated_time || 0} 分钟`,
      type: 'success',
      time: 3000
    })
    
  } catch (error: any) {
    notify.myMsg.notify({
      title: '转码失败',
      content: error.response?.data?.message || '视频转码失败',
      type: 'error',
      time: 4000
    })
  }
}

</script>