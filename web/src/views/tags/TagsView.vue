<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-2xl font-bold">标签管理</h1>
        <button class="btn btn-primary" @click="openCreateTagModal">
          创建标签
        </button>
      </div>
      
      <div v-if="loading" class="flex justify-center items-center min-h-[200px]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>
      <div v-else-if="error" class="alert alert-error">
        {{ error }}
      </div>
      <div v-else-if="tags.length === 0" class="text-center py-12">
        <div class="text-lg mb-4">暂无标签</div>
        <button class="btn btn-primary" @click="openCreateTagModal">创建第一个标签</button>
      </div>
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="tag in tags" :key="tag.id" class="card bg-base-100 shadow-xl">
          <div class="card-body p-4">
            <h3 class="card-title text-sm">{{ tag.name }}</h3>
            <p class="text-xs text-gray-500">{{ tag.photos_count || 0 }}张照片</p>
            <div class="card-actions justify-end mt-2">
              <button class="btn btn-sm btn-outline" @click="viewTag(tag)">
                查看
              </button>
              <button class="btn btn-sm btn-error btn-outline" @click="confirmDeleteTag(tag)">
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建标签模态框 -->
    <dialog ref="createTagDialog" class="modal">
      <div class="modal-box">
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>
        <h3 class="font-bold text-lg mb-4">创建新标签</h3>
        <form @submit.prevent="createTag">
          <div class="form-control w-full">
            <label class="label">
              <span class="label-text">标签名称</span>
            </label>
            <input 
              type="text" 
              v-model="newTag.name" 
              placeholder="输入标签名称" 
              class="input input-bordered w-full" 
              required
            />
          </div>
          <div class="modal-action">
            <button type="button" class="btn" @click="closeCreateTagModal">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="creating">创建</button>
          </div>
        </form>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>关闭</button>
      </form>
    </dialog>

    <!-- 删除确认模态框 -->
    <dialog ref="deleteTagDialog" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">确认删除</h3>
        <p>确定要删除标签 "{{ tagToDelete?.name }}" 吗？</p>
        <p class="text-sm text-gray-500 mt-2">此操作不会删除关联的照片，但会移除照片上的此标签。</p>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn mr-2">取消</button>
            <button class="btn btn-error" @click="deleteTag" :disabled="deleting">删除</button>
          </form>
        </div>
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

interface Tag {
  id: number
  name: string
  photos_count?: number
}

const router = useRouter()
const tags = ref<Tag[]>([])
const loading = ref(true)
const error = ref('')
const createTagDialog = ref<HTMLDialogElement | null>(null)
const deleteTagDialog = ref<HTMLDialogElement | null>(null)
const creating = ref(false)
const deleting = ref(false)
const tagToDelete = ref<Tag | null>(null)

const newTag = ref({
  name: ''
})

const fetchTags = async () => {
  loading.value = true
  error.value = ''
  try {
    // 这里应该调用API获取标签列表
    // 暂时使用模拟数据
    tags.value = [
      {
        id: 1,
        name: '家庭',
        photos_count: 15
      },
      {
        id: 2,
        name: '旅行',
        photos_count: 24
      },
      {
        id: 3,
        name: '美食',
        photos_count: 8
      },
      {
        id: 4,
        name: '风景',
        photos_count: 12
      },
      {
        id: 5,
        name: '宠物',
        photos_count: 6
      },
      {
        id: 6,
        name: '节日',
        photos_count: 10
      }
    ]
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取标签失败'
  } finally {
    loading.value = false
  }
}

const openCreateTagModal = () => {
  newTag.value = {
    name: ''
  }
  createTagDialog.value?.showModal()
}

const closeCreateTagModal = () => {
  createTagDialog.value?.close()
}

const createTag = async () => {
  if (!newTag.value.name) return
  
  creating.value = true
  try {
    // 这里应该调用API创建标签
    // 暂时使用模拟数据
    const newTagData = {
      id: tags.value.length + 1,
      name: newTag.value.name,
      photos_count: 0
    }
    
    tags.value.unshift(newTagData)
    closeCreateTagModal()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '创建标签失败'
  } finally {
    creating.value = false
  }
}

const viewTag = (tag: Tag) => {
  router.push(`/tags/${tag.id}`)
}

const confirmDeleteTag = (tag: Tag) => {
  tagToDelete.value = tag
  deleteTagDialog.value?.showModal()
}

const deleteTag = async () => {
  if (!tagToDelete.value) return
  
  deleting.value = true
  try {
    // 这里应该调用API删除标签
    // 暂时使用模拟数据
    tags.value = tags.value.filter(t => t.id !== tagToDelete.value?.id)
    deleteTagDialog.value?.close()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '删除标签失败'
  } finally {
    deleting.value = false
    tagToDelete.value = null
  }
}

onMounted(fetchTags)
</script>