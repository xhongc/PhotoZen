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
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              扫描入库
            </button>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              生成缩略图
            </button>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              重复检查
            </button>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              备份上传
            </button>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              人像识别
            </button>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              CLIP识别
            </button>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
              OCR识别
            </button>
            <button @click="handleCreateDirectory"
              class="inline-flex items-center px-3 py-1.5 text-sm font-medium text-primary-700 hover:bg-gray-100 rounded">
              <i class="fas fa-folder-plus mr-2"></i>
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
      <div class="flex-1 overflow-y-auto">
        <div class="p-6">
          <!-- 列表视图 -->
          <table v-if="viewMode === 'list'"
            class="min-w-full divide-y divide-base-200 bg-base-100 shadow-sm rounded-lg">
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
              <tr v-for="file in files" :key="file.path" class="hover:bg-base-200"
                :class="{ 'bg-base-200': file.path === currentPreviewPath }" @click="handleFileClick(file)"
                :data-file-path="file.path">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <i v-if="file.type === 'directory'" class="fas fa-folder text-yellow-400 mr-3"></i>
                    <img v-else-if="file.mime.startsWith('image/')" :src="file.path"
                      class="w-8 h-8 rounded object-cover mr-3">
                    <span class="text-sm text-primary-600">{{ file.basename }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(file.lastmod) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ file.type === 'directory' ? '文件夹' :
                  file.mime }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatFileSize(file.size) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <button class="text-gray-400 hover:text-gray-500" @click.stop="handleDelete(file.path)">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- 网格视图 -->
          <div v-else class="grid grid-cols-4 gap-4">
            <div v-for="file in files" :key="file.path"
              class="bg-base-100 rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow cursor-pointer"
              :class="{ 'bg-base-200': file.path === currentPreviewPath }" @click="handleFileClick(file)"
              :data-file-path="file.path">
              <div class="aspect-square mb-2">
                <i v-if="file.type === 'directory'" class="fas fa-folder text-yellow-400 text-4xl"></i>
                <img v-else-if="file.mime.startsWith('image/')" :src="file.path"
                  class="w-full h-full object-cover rounded">
              </div>
              <div class="text-sm font-medium text-primary-600 truncate">{{ file.basename }}</div>
              <div class="text-xs text-gray-500">{{ formatDate(file.lastmod) }}</div>
            </div>
          </div>

          <!-- 状态栏 -->
          <div class="mt-4 text-sm text-gray-500">
            共 {{ files.length }} 个项目（{{files.filter(f => f.type === 'directory').length}} 个文件夹，{{files.filter(f =>
              f.type
            === 'file').length }} 个文件）
          </div>
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
import { ref, onMounted, computed } from 'vue'
import { webdavApi, type WebDAVFile } from '@/api/webdav'
import { fileApi } from '@/api/file'
import { useRouter } from 'vue-router'
import ImagePreview from '@/components/ImagePreview.vue'
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
    files.value = webDAVResponse.children.map(item => ({
      name: item.name,
      path: item.path,
      type: item.type,
      basename: item.name,
      lastmod: item.last_modified,
      mime: item.type === 'directory' ? 'directory' : 'image/jpeg',
      size: 0,
      etag: '' // 添加必需的etag字段
    }))
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

</script>