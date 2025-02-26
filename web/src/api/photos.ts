import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export interface Photo {
  id: number
  url: string
  title?: string
  created_at: string
  tags?: string[]
}

export const photoApi = {
  // 获取照片列表
  getPhotos(): Promise<Photo[]> {
    return api.get('/photos').then(response => response.data)
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
  }
}
