/**
 * 通用存储工具函数
 */

/**
 * 清除所有本地存储
 */
export const clearStore = () => {
  localStorage.clear()
  sessionStorage.clear()
  
  // 清除所有cookie
  const cookies = document.cookie.split(";")
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i]
    const eqPos = cookie.indexOf("=")
    const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie
    document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/"
  }
}

/**
 * 设置本地存储
 * @param {string} key 键名
 * @param {any} value 值
 */
export const setLocalStore = (key, value) => {
  if (typeof value === 'object') {
    value = JSON.stringify(value)
  }
  localStorage.setItem(key, value)
}

/**
 * 获取本地存储
 * @param {string} key 键名
 * @returns {any} 存储值
 */
export const getLocalStore = (key) => {
  let value = localStorage.getItem(key)
  try {
    value = JSON.parse(value)
    return value
  } catch (error) {
    return value
  }
}

/**
 * 删除本地存储
 * @param {string} key 键名
 */
export const removeLocalStore = (key) => {
  localStorage.removeItem(key)
} 