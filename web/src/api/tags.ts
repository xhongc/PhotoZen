import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export interface Tag {
  id: number
  name: string
  photos_count?: number
}

export const tagApi = {
  // 获取标签列表
  getTags(): Promise<Tag[]> {
    return api.get('/tags').then(response => response.data)
  },

  // 获取单个标签详情
  getTag(id: number): Promise<Tag> {
    return api.get(`/tags/${id}`).then(response => response.data)
  },

  // 创建标签
  createTag(data: { name: string }): Promise<Tag> {
    return api.post('/tags', data).then(response => response.data)
  },

  // 删除标签
  deleteTag(id: number): Promise<void> {
    return api.delete(`/tags/${id}`)
  },

  // 获取标签下的照片
  getTagPhotos(id: number): Promise<any[]> {
    return api.get(`/tags/${id}/photos`).then(response => response.data)
  },

  // 为照片添加标签
  addTagToPhoto(photoId: number, tagName: string): Promise<void> {
    return api.post(`/photos/${photoId}/tags/${tagName}`)
  },

  // 从照片中移除标签
  removeTagFromPhoto(photoId: number, tagId: number): Promise<void> {
    return api.delete(`/photos/${photoId}/tags/${tagId}`)
  }
}