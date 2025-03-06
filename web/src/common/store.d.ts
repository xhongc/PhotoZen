/**
 * 清除所有本地存储
 */
export function clearStore(): void;

/**
 * 设置本地存储
 * @param key 键名
 * @param value 值
 */
export function setLocalStore(key: string, value: any): void;

/**
 * 获取本地存储
 * @param key 键名
 * @returns 存储值
 */
export function getLocalStore(key: string): any;

/**
 * 删除本地存储
 * @param key 键名
 */
export function removeLocalStore(key: string): void; 