import api from './axios'

export interface HomeData {
  total_photos: number
  total_albums: number
  total_favorites: number
  storage_space: string
}

export interface MemoryPhoto {
  id: number
  title: string
  thumbnail_path: string
  taken_time: string
  description: string
}

export interface YearMemory {
  year: number
  years_ago: number
  photos: MemoryPhoto[]
}

export interface MemoriesData {
  memories: YearMemory[]
  success: boolean
}

export const homeApi = {
  getHome(): Promise<HomeData> {
    return api.get('/home/').then(response => response.data)
  },
  getTodayMemories(): Promise<MemoriesData> {
    return api.get('/home/memories').then(response => response.data)
  }
}

