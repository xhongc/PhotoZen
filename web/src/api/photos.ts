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
  album_id?: number
}

export interface PhotoGroup {
  date_key: string
  photos: Photo[]
}

export interface PhotoRatingParams {
  rating: number
  comment?: string
}

export interface PhotoUpdateParams {
  title?: string
  description?: string
  taken_time?: string
  tags?: string[]
  location?: string
  is_favorite?: boolean
}

export interface MetadataField {
  name: string
  value: any
  editable: boolean
  field_type?: string
}

export interface PhotoMetadata {
  basic_info: Record<string, any>
  exif_data: Record<string, MetadataField>
  custom_fields: Record<string, MetadataField>
}

export interface ExifData {
  data: Record<string, any>
}

export interface CustomFieldData {
  key: string
  name: string
  value: string
  field_type: 'text' | 'number' | 'date' | 'boolean' | 'json'
}

export interface CustomFieldUpdate {
  value: string
}

export interface ExifFieldUpdate {
  tag: string
  value: string
}

export interface GPSCoordinates {
  latitude: number
  longitude: number
}

export interface CameraInfo {
  make: string
  model: string
  software: string
  lens_model: string
}

export interface ShootingParameters {
  aperture: any
  shutter_speed: any
  iso: any
  focal_length: any
  flash: any
  white_balance: any
  exposure_mode: any
  metering_mode: any
}

export interface MetadataResponse {
  success: boolean
  message: string
  data?: Record<string, any>
}

export const photoApi = {
  // 获取照片列表
  getPhotos(params?: PhotoListParams): Promise<PhotoGroup[]> {
    return api.get('/photos', { params }).then(response => response.data)
  },

  // 获取单个照片
  getPhoto(id: number): Promise<Photo> {
    return api.get(`/photos/${id}`).then(response => response.data)
  },

  // 更新照片
  updatePhoto(id: number, data: PhotoUpdateParams): Promise<Photo> {
    return api.put(`/photos/${id}`, data).then(response => response.data)
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
  },

  // 获取照片文件
  getPhotoFile(id: number): Promise<Blob> {
    return api.get(`/photos/${id}/file`, { responseType: 'blob' }).then(response => response.data)
  },

  // === 元数据相关 API ===
  // 获取照片完整元数据
  getMetadata(id: number): Promise<PhotoMetadata> {
    return api.get(`/photos/${id}/metadata`).then(response => response.data)
  },

  // 获取EXIF数据
  getExifData(id: number): Promise<ExifData> {
    return api.get(`/photos/${id}/metadata/exif`).then(response => response.data)
  },

  // 更新EXIF字段
  updateExifField(id: number, data: ExifFieldUpdate): Promise<MetadataResponse> {
    return api.put(`/photos/${id}/metadata/exif`, data).then(response => response.data)
  },

  // 添加自定义字段
  addCustomField(id: number, data: CustomFieldData): Promise<any> {
    return api.post(`/photos/${id}/metadata/custom`, data).then(response => response.data)
  },

  // 更新自定义字段
  updateCustomField(id: number, key: string, data: CustomFieldUpdate): Promise<MetadataResponse> {
    return api.put(`/photos/${id}/metadata/custom/${key}`, data).then(response => response.data)
  },

  // 删除自定义字段
  deleteCustomField(id: number, key: string): Promise<MetadataResponse> {
    return api.delete(`/photos/${id}/metadata/custom/${key}`).then(response => response.data)
  },

  // 获取GPS坐标
  getGPSCoordinates(id: number): Promise<GPSCoordinates | null> {
    return api.get(`/photos/${id}/metadata/gps`).then(response => response.data)
  },

  // 获取相机信息
  getCameraInfo(id: number): Promise<CameraInfo> {
    return api.get(`/photos/${id}/metadata/camera`).then(response => response.data)
  },

  // 获取拍摄参数
  getShootingParameters(id: number): Promise<ShootingParameters> {
    return api.get(`/photos/${id}/metadata/shooting`).then(response => response.data)
  },

  // 获取所有自定义字段
  getCustomFields(id: number): Promise<any[]> {
    return api.get(`/photos/${id}/metadata/custom`).then(response => response.data)
  }
}
