import axios from 'axios'

export interface LoginResponse {
  token: string
  user: {
    id: number
    username: string
    email: string
    is_active: boolean
  }
  token_exp_date: string
}

export interface LoginRequest {
  username: string
  password: string
}

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await axios.post<LoginResponse>('/api/auth/login', data)
    return response.data
  },

  logout: async () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
  },

  refreshToken: async (token: string) => {
    const response = await axios.post('/api/auth/api-token-refresh', {
      refresh: token
    })
    return response.data
  }
} 