import api from './axios'

export interface RecycleItem {
  name: string
  path: string
  original_path: string
  size: number
  delete_time: string
  remaining_days: number
  mime_type?: string
  preview_url?: string
}

export interface RecycleListResponse {
  items: RecycleItem[]
  total_count: number
  page: number
  page_size: number
}

export interface BatchOperationRequest {
  paths: string[]
}

export const recycleApi = {
  // 获取回收站列表
  getRecycleList: (page: number = 1, pageSize: number = 20) => {
    return api.get<RecycleListResponse>('/files/recycle', {
      params: { page, page_size: pageSize }
    })
  },

  // 恢复单个文件
  restoreFile: (path: string) => {
    return api.post('/files/recycle/restore', { path })
  },

  // 批量恢复文件
  restoreFilesBatch: (paths: string[]) => {
    return api.post('/files/recycle/restore-batch', { paths })
  },

  // 永久删除单个文件
  deleteFile: (path: string) => {
    return api.delete('/files/recycle/delete', { data: { path } })
  },

  // 批量永久删除文件
  deleteFilesBatch: (paths: string[]) => {
    return api.delete('/files/recycle/delete-batch', { data: { paths } })
  }
}
