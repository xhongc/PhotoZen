import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const userRole = ref('')
  const username = ref('')
  const hasMsg = ref(false)

  /**
   * 设置用户角色
   * @param role 用户角色
   */
  function setUserRole(role: string) {
    userRole.value = role
  }

  /**
   * 设置用户名
   * @param name 用户名
   */
  function setUsername(name: string) {
    username.value = name
  }

  /**
   * 设置是否有消息
   * @param status 消息状态
   */
  function setHasMsg(status: boolean) {
    hasMsg.value = status
  }

  /**
   * 获取登录信息
   * @returns 登录信息结果
   */
  async function loginInfo() {
    // 这里应该调用API获取登录信息，这里模拟返回
    return {
      result: true,
      data: {
        role: 'V2',
        is_forever: true,
        username: 'admin',
        salt: 'salt123',
        hash: 'hash123',
        sys_dict: {
          mi_play_in_pl: 'true'
        }
      }
    }
  }

  /**
   * 获取通知列表
   * @returns 通知列表
   */
  async function getNotifications() {
    // 这里应该调用API获取通知列表，这里模拟返回
    return {
      result: true,
      data: {
        list: [
          {
            title: '系统通知',
            content: '欢迎使用Music Tag Web',
            update_at: '2023-01-01 12:00:00'
          },
          {
            title: '更新提示',
            content: '有新版本可用',
            update_at: '2023-01-02 12:00:00'
          }
        ],
        unread_count: 2
      }
    }
  }

  /**
   * 激活码激活
   * @param code 激活码
   * @returns 激活结果
   */
  async function activeCode(code: string) {
    // 这里应该调用API激活码，这里模拟返回
    if (code === 'VIP123') {
      return {
        result: true,
        data: {
          is_forever: true
        }
      }
    } else {
      return {
        result: false,
        msg: '激活码无效'
      }
    }
  }

  return {
    userRole,
    username,
    hasMsg,
    setUserRole,
    setUsername,
    setHasMsg,
    loginInfo,
    getNotifications,
    activeCode
  }
}) 