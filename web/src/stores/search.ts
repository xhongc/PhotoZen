import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSearchStore = defineStore('search', () => {
  const searchTerm = ref('')

  /**
   * 设置搜索关键字
   * @param term 搜索关键字
   */
  function setSearchTerm(term: string) {
    searchTerm.value = term
  }

  /**
   * 获取搜索建议
   * @param term 搜索关键字
   * @returns 搜索结果
   */
  async function searchSuggestions(term: string) {
    // 这里应该调用API获取搜索建议，这里模拟返回
    return {
      result: true,
      data: {
        artists: [
          {
            id: 1,
            name: '周杰伦',
            albumCount: 12
          },
          {
            id: 2,
            name: '林俊杰',
            albumCount: 10
          }
        ],
        albums: [
          {
            id: 1,
            name: '七里香',
            year: '2004',
            artist: '周杰伦'
          },
          {
            id: 2,
            name: '叶惠美',
            year: '2003',
            artist: '周杰伦'
          }
        ],
        tracks: [
          {
            id: 1,
            title: '七里香',
            year: '2004',
            artist: '周杰伦',
            album: '七里香'
          },
          {
            id: 2,
            title: '晴天',
            year: '2003',
            artist: '周杰伦',
            album: '叶惠美'
          }
        ]
      }
    }
  }

  return {
    searchTerm,
    setSearchTerm,
    searchSuggestions
  }
}) 