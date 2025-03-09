<template>
  <div class="privacy-settings">
    <h1 class="text-2xl font-semibold text-primary-600">隐私与安全</h1>
    <!-- 隐私与安全内容将在这里实现 -->
    <!-- 主内容区 -->
    <main class="flex-1 overflow-auto">
      <div class="py-6">
        <div class="max-w-full">
          <!-- 备份状态概览 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-medium text-gray-800">备份状态</h2>
                <button type="button"
                  class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  <i class="fas fa-sync-alt mr-2"></i>
                  立即备份
                </button>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- 上次备份 -->
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-2">
                    <i class="fas fa-clock text-primary-500 text-xl mr-3"></i>
                    <h3 class="text-lg font-medium text-gray-800">上次备份</h3>
                  </div>
                  <p class="text-gray-600">2024-01-15 15:30</p>
                  <p class="text-sm text-gray-500 mt-1">备份完成：1,234个文件</p>
                </div>

                <!-- 备份进度 -->
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-2">
                    <i class="fas fa-database text-primary-500 text-xl mr-3"></i>
                    <h3 class="text-lg font-medium text-gray-800">备份容量</h3>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2.5">
                    <div class="bg-primary-600 h-2.5 rounded-full" style="width: 45%"></div>
                  </div>
                  <p class="text-sm text-gray-500 mt-2">已使用：45.5GB / 100GB</p>
                </div>

                <!-- 备份设备 -->
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex items-center mb-2">
                    <i class="fas fa-laptop text-primary-500 text-xl mr-3"></i>
                    <h3 class="text-lg font-medium text-gray-800">备份设备</h3>
                  </div>
                  <p class="text-gray-600">3台设备已连接</p>
                  <button class="text-primary-600 hover:text-primary-500 text-sm font-medium mt-1">
                    管理设备 →
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- 自动备份设置 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <h2 class="text-xl font-medium text-gray-800 mb-6">自动备份设置</h2>

              <div class="space-y-6">
                <!-- 备份频率 -->
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-gray-800 font-medium">备份频率</h3>
                    <p class="text-sm text-gray-500">设置自动备份的时间间隔</p>
                  </div>
                  <select
                    class="mt-1 block w-48 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md">
                    <option>实时备份</option>
                    <option>每天</option>
                    <option>每周</option>
                    <option>每月</option>
                  </select>
                </div>

                <!-- 备份内容 -->
                <div>
                  <h3 class="text-gray-800 font-medium mb-4">备份内容</h3>
                  <div class="space-y-4">
                    <label class="flex items-center">
                      <input type="checkbox"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" checked>
                      <span class="ml-3">
                        <span class="text-gray-700">照片和视频</span>
                        <span class="text-sm text-gray-500 block">包括原始文件和编辑后的版本</span>
                      </span>
                    </label>
                    <label class="flex items-center">
                      <input type="checkbox"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" checked>
                      <span class="ml-3">
                        <span class="text-gray-700">相册结构</span>
                        <span class="text-sm text-gray-500 block">保持相册的组织方式和分类</span>
                      </span>
                    </label>
                    <label class="flex items-center">
                      <input type="checkbox"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" checked>
                      <span class="ml-3">
                        <span class="text-gray-700">元数据</span>
                        <span class="text-sm text-gray-500 block">包括标签、评分和注释</span>
                      </span>
                    </label>
                  </div>
                </div>

                <!-- 备份位置 -->
                <div>
                  <h3 class="text-gray-800 font-medium mb-4">备份位置</h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="border border-gray-200 rounded-lg p-4 flex items-center justify-between">
                      <div class="flex items-center">
                        <i class="fas fa-cloud text-primary-500 text-xl mr-3"></i>
                        <div>
                          <h4 class="text-gray-800 font-medium">云端备份</h4>
                          <p class="text-sm text-gray-500">自动同步到云端存储</p>
                        </div>
                      </div>
                      <label class="switch">
                        <input type="checkbox" checked>
                        <span class="slider round"></span>
                      </label>
                    </div>
                    <div class="border border-gray-200 rounded-lg p-4 flex items-center justify-between">
                      <div class="flex items-center">
                        <i class="fas fa-hdd text-primary-500 text-xl mr-3"></i>
                        <div>
                          <h4 class="text-gray-800 font-medium">本地备份</h4>
                          <p class="text-sm text-gray-500">备份到外部存储设备</p>
                        </div>
                      </div>
                      <label class="switch">
                        <input type="checkbox">
                        <span class="slider round"></span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 数据安全 -->
          <section class="mb-10">
            <div class="bg-white rounded-lg shadow-sm p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-medium text-gray-800">数据安全</h2>
                <button type="button"
                  class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  <i class="fas fa-shield-alt mr-2"></i>
                  安全检查
                </button>
              </div>

              <div class="space-y-6">
                <!-- 加密设置 -->
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-gray-800 font-medium">端到端加密</h3>
                    <p class="text-sm text-gray-500">为您的照片提供最高级别的保护</p>
                  </div>
                  <label class="switch">
                    <input type="checkbox" checked>
                    <span class="slider round"></span>
                  </label>
                </div>

                <!-- 访问控制 -->
                <div>
                  <h3 class="text-gray-800 font-medium mb-4">访问控制</h3>
                  <div class="space-y-4">
                    <label class="flex items-center">
                      <input type="checkbox"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" checked>
                      <span class="ml-3">
                        <span class="text-gray-700">双重认证</span>
                        <span class="text-sm text-gray-500 block">使用手机验证码进行二次确认</span>
                      </span>
                    </label>
                    <label class="flex items-center">
                      <input type="checkbox"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" checked>
                      <span class="ml-3">
                        <span class="text-gray-700">登录通知</span>
                        <span class="text-sm text-gray-500 block">新设备登录时发送通知</span>
                      </span>
                    </label>
                  </div>
                </div>

                <!-- 恢复选项 -->
                <div>
                  <h3 class="text-gray-800 font-medium mb-4">恢复选项</h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="border border-gray-200 rounded-lg p-4">
                      <div class="flex items-center mb-2">
                        <i class="fas fa-key text-primary-500 text-xl mr-3"></i>
                        <h4 class="text-gray-800 font-medium">恢复密钥</h4>
                      </div>
                      <p class="text-sm text-gray-500">用于恢复加密的照片</p>
                      <button class="text-primary-600 hover:text-primary-500 text-sm font-medium mt-2">
                        下载密钥 →
                      </button>
                    </div>
                    <div class="border border-gray-200 rounded-lg p-4">
                      <div class="flex items-center mb-2">
                        <i class="fas fa-history text-primary-500 text-xl mr-3"></i>
                        <h4 class="text-gray-800 font-medium">版本历史</h4>
                      </div>
                      <p class="text-sm text-gray-500">保留30天的文件历史</p>
                      <button class="text-primary-600 hover:text-primary-500 text-sm font-medium mt-2">
                        查看历史 →
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// 隐私与安全相关逻辑
</script>