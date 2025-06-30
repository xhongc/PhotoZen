import api from './axios'

export interface HomeData {
  total_photos: number
  total_albums: number
  total_favorites: number
  storage_space: string
}

export const homeApi = {
  getHome(): Promise<HomeData> {
    return api.get('/home/').then(response => response.data)
  }
}

