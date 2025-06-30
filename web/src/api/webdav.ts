import api from './axios'

export interface fsdavConfig {
  username: string
  password: string
}

export interface WebDAVFile {
  name: string
  basename: string
  lastmod: string
  size: number
  type: string
  mime: string
  etag: string
  path: string
}

export const webdavApi = {
  // 配置 fsdav 客户端
  config: null as fsdavConfig | null,

  // 设置配置
  setConfig(config: fsdavConfig) {
    this.config = config
  },

  // 列出目录内容
  async listDirectory(path: string): Promise<any[]> {
    return api.get(`/fsdav${path}`, {
      headers: this._getAuthHeaders()
    }).then(response => response.data)
  },

  // 获取文件内容
  async getFile(path: string): Promise<Blob> {
    return api.get(`/fsdav/download`, {
      params: { path },
      headers: this._getAuthHeaders(),
      responseType: 'blob'
    }).then(response => response.data)
  },

  // 上传文件
  async uploadFile(path: string, file: File): Promise<void> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('path', path)
    
    return api.post(`/fsdav/upload`, formData, {
      headers: {
        ...this._getAuthHeaders(),
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 创建目录
  async createDirectory(path: string): Promise<void> {
    return api.put(`/fsdav/mkdir`, null, {
      params: { path },
      headers: this._getAuthHeaders()
    })
  },

  // 删除文件或目录
  async delete(path: string): Promise<void> {
    return api.delete(`/fsdav/delete`, {
      params: { path },
      headers: this._getAuthHeaders()
    })
  },

  // 移动文件或目录
  async move(from: string, to: string): Promise<void> {
    return api.put(`/fsdav/move`, null, {
      params: { from, to },
      headers: this._getAuthHeaders()
    })
  },

  // 复制文件或目录
  async copy(from: string, to: string): Promise<void> {
    return api.put(`/fsdav/copy`, null, {
      params: { from, to },
      headers: this._getAuthHeaders()
    })
  },

  // 获取认证头
  _getAuthHeaders() {
    if (!this.config) {
      throw new Error('fsdav config not set')
    }
    return {
      'Authorization': `Basic ${btoa(`${this.config.username}:${this.config.password}`)}`
    }
  }
}
