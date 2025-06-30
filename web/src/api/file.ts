import api from './axios'



export const fileApi = {
  // 删除文件或文件夹
  deleteFile(path: string) {
    return api.delete(`/files/delete`, {
      data: {
        path
      }
    })
  }
}
