import api from './axios'

export interface Location {
  latitude: number
  longitude: number
  name: string
}

export interface Tag {
  id: number
  name: string
}

export interface Photo {
  id: number
  title: string
  description: string
  file_path: string
  thumbnail_path: string
  upload_time: string
  taken_time?: string
  size: number
  width: number
  height: number
  format: string
  location?: Location
  rating?: number
  is_favorite: boolean
  tags: Tag[]
}

export interface PhotoListResponse {
  count: number
  results: Photo[]
}

export interface PhotoListParams {
  time_filter?: string
  start_date?: Date
  end_date?: Date
  tags?: string[]
  location?: string
  favorites_only?: boolean
  sort_by?: string
  page?: number
  page_size?: number
  group_by?: string
}

export interface PhotoGroup {
  date_key: string
  photos: Photo[]
}

export interface PhotoRatingParams {
  rating: number
  comment?: string
}

export const photoApi = {
  // 获取照片列表
  getPhotos(params?: PhotoListParams): Promise<PhotoGroup[]> {
    return api.get('/photos', { params }).then(response => response.data)
  },

  // 上传照片
  uploadPhoto(file: File, onProgress?: (progress: number) => void) {
    const formData = new FormData()
    formData.append('photo', file)

    return api.post('/photos', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = (progressEvent.loaded * 100) / progressEvent.total
          onProgress(Math.round(progress))
        }
      },
    }).then(response => response.data)
  },

  // 删除照片
  deletePhoto(id: number) {
    return api.delete(`/photos/${id}`)
  },

  // 切换收藏状态
  toggleFavorite(id: number): Promise<Photo> {
    return api.post(`/photos/${id}/favorite`).then(response => response.data)
  },

  // 评分照片
  ratePhoto(id: number, data: PhotoRatingParams): Promise<Photo> {
    return api.post(`/photos/${id}/rate`, data).then(response => response.data)
  }
}
