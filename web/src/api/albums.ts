import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// Add request interceptor to handle authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export interface Album {
  id: number
  name: string
  description: string
  created_time: string
  updated_time: string
  photos_count?: number
  cover_photo?: {
    id: number
    url: string
    title?: string
  }
}

export const albumApi = {
  // 获取相册列表
  getAlbums(): Promise<Album[]> {
    return api.get('/albums').then(response => response.data)
  },

  // 获取单个相册详情
  getAlbum(id: number): Promise<Album> {
    return api.get(`/albums/${id}`).then(response => response.data)
  },

  // 创建相册
  createAlbum(data: { name: string; description?: string }): Promise<Album> {
    return api.post('/albums', data).then(response => response.data)
  },

  // 更新相册
  updateAlbum(id: number, data: { name?: string; description?: string }): Promise<Album> {
    return api.put(`/albums/${id}`, data).then(response => response.data)
  },

  // 删除相册
  deleteAlbum(id: number): Promise<void> {
    return api.delete(`/albums/${id}`)
  },

  // 获取相册中的照片
  getAlbumPhotos(id: number): Promise<any[]> {
    return api.get(`/albums/${id}/photos`).then(response => response.data)
  },

  // 添加照片到相册
  addPhotoToAlbum(albumId: number, photoId: number): Promise<void> {
    return api.post(`/photos/${photoId}/albums/${albumId}`)
  },

  // 从相册中移除照片
  removePhotoFromAlbum(albumId: number, photoId: number): Promise<void> {
    return api.delete(`/photos/${photoId}/albums/${albumId}`)
  }
}