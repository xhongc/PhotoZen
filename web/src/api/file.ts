import api from './axios'

// 工具栏功能相关的接口类型定义
export interface ScanLibraryRequest {
  path: string
  recursive?: boolean
}

export interface ScanLibraryResponse {
  processed: number
  imported: number
  errors: string[]
  task_id?: string
}

export interface GenerateThumbnailsRequest {
  path: string
  sizes?: number[]
}

export interface GenerateThumbnailsResponse {
  generated: number
  skipped: number
  errors: string[]
  task_id?: string
}

export interface CheckDuplicatesRequest {
  path: string
}

export interface DuplicateGroup {
  original: string
  duplicates: string[]
  size: number
}

export interface CheckDuplicatesResponse {
  duplicate_groups: DuplicateGroup[]
  total_duplicates: number
  space_saved: number
}

export interface BackupUploadRequest {
  source: string
  destination: string
  compression?: boolean
}

export interface BackupUploadResponse {
  task_id: string
  status: string
  estimated_size?: number
}

export interface FaceRecognitionRequest {
  path: string
  create_albums?: boolean
}

export interface FaceRecognitionResponse {
  faces_detected: number
  persons: string[]
  photos_processed: number
  task_id?: string
}

export interface ClipAnalysisRequest {
  path: string
  confidence_threshold?: number
}

export interface ClipAnalysisResponse {
  tags: string[]
  confidence_scores: number[]
  photos_processed: number
  task_id?: string
}

export interface OcrAnalysisRequest {
  path: string
  language?: string
}

export interface OcrAnalysisResponse {
  text: string
  confidence: number
  photos_processed: number
  task_id?: string
}

export interface VideoTranscodeRequest {
  path: string
  format?: string
  quality?: string
  resolution?: string
}

export interface VideoTranscodeResponse {
  task_id: string
  output_path: string
  estimated_time?: number
}

export interface TaskStatusResponse {
  task_id: string
  status: string // pending, running, completed, failed
  progress: number // 0-100
  message?: string
  result?: any
}

export const fileApi = {
  // 删除文件或文件夹
  deleteFile(path: string) {
    return api.delete(`/files/delete`, {
      data: {
        path
      }
    })
  },

  // =============工具栏功能 API 方法=============
  
  // 扫描入库
  scanLibrary(data: ScanLibraryRequest) {
    return api.post<ScanLibraryResponse>('/files/scan-library', data)
  },

  // 生成缩略图
  generateThumbnails(data: GenerateThumbnailsRequest) {
    return api.post<GenerateThumbnailsResponse>('/files/generate-thumbnails', data)
  },

  // 重复检查
  checkDuplicates(data: CheckDuplicatesRequest) {
    return api.post<CheckDuplicatesResponse>('/files/check-duplicates', data)
  },

  // 备份上传
  backupUpload(data: BackupUploadRequest) {
    return api.post<BackupUploadResponse>('/files/backup-upload', data)
  },

  // 人像识别
  faceRecognition(data: FaceRecognitionRequest) {
    return api.post<FaceRecognitionResponse>('/files/face-recognition', data)
  },

  // CLIP识别
  clipAnalysis(data: ClipAnalysisRequest) {
    return api.post<ClipAnalysisResponse>('/files/clip-analysis', data)
  },

  // OCR识别
  ocrAnalysis(data: OcrAnalysisRequest) {
    return api.post<OcrAnalysisResponse>('/files/ocr-analysis', data)
  },

  // 视频转码
  videoTranscode(data: VideoTranscodeRequest) {
    return api.post<VideoTranscodeResponse>('/files/video-transcode', data)
  },

  // 获取任务状态
  getTaskStatus(taskId: string) {
    return api.get<TaskStatusResponse>(`/files/task-status/${taskId}`)
  }
}
