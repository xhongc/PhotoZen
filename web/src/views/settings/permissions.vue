<template>
  <div class="permissions-settings">
    <h1 class="text-2xl font-semibold text-primary-600 mb-6">权限管理</h1>
    <!-- 权限管理内容将在这里实现 -->
    <!-- 权限管理界面 -->
    <div class="mb-6">
      <!-- 用户权限管理 -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-medium text-gray-800">用户权限</h2>
          <button
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            <i class="fas fa-plus mr-2"></i>
            添加用户
          </button>
        </div>

        <!-- 用户列表 -->
        <div class="mt-4">
          <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">用户</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">角色</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">相册权限</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">功能权限</th>
                  <th scope="col" class="relative py-3.5 pl-3 pr-4">
                    <span class="sr-only">操作</span>
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 bg-white">
                <!-- 用户1 -->
                <tr>
                  <td class="whitespace-nowrap py-4 pl-4 pr-3">
                    <div class="flex items-center">
                      <img class="h-8 w-8 rounded-full"
                        src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e" alt="">
                      <div class="ml-4">
                        <div class="font-medium text-gray-900">张三</div>
                        <div class="text-gray-500">zhangsan@example.com</div>
                      </div>
                    </div>
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      管理员
                    </span>
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    <span>全部相册</span>
                  </td>
                  <td class="px-3 py-4 text-sm text-gray-500">
                    <span>全部权限</span>
                  </td>
                  <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium">
                    <button class="text-primary-600 hover:text-primary-900">编辑</button>
                  </td>
                </tr>

                <!-- 用户2 -->
                <tr>
                  <td class="whitespace-nowrap py-4 pl-4 pr-3">
                    <div class="flex items-center">
                      <img class="h-8 w-8 rounded-full" src="https://images.unsplash.com/photo-1550525811-e5869dd03032"
                        alt="">
                      <div class="ml-4">
                        <div class="font-medium text-gray-900">李四</div>
                        <div class="text-gray-500">lisi@example.com</div>
                      </div>
                    </div>
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      编辑者
                    </span>
                  </td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                    <span>家庭相册, 旅行相册</span>
                  </td>
                  <td class="px-3 py-4 text-sm text-gray-500">
                    <span>上传, 编辑, 删除</span>
                  </td>
                  <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium">
                    <button class="text-primary-600 hover:text-primary-900">编辑</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 角色管理 -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-medium text-gray-800">角色管理</h2>
          <button
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            <i class="fas fa-plus mr-2"></i>
            创建角色
          </button>
        </div>

        <!-- 角色列表 -->
        <div class="space-y-4">
          <!-- 管理员角色 -->
          <div class="border rounded-lg p-4">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 mr-2">
                  管理员
                </span>
                <span class="text-sm text-gray-500">系统最高权限角色</span>
              </div>
              <button class="text-primary-600 hover:text-primary-900 text-sm font-medium">
                编辑权限
              </button>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">功能权限</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    相册管理
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    用户管理
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    系统设置
                  </li>
                </ul>
              </div>
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">相册权限</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    查看所有相册
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    编辑所有相册
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    删除所有相册
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- 编辑者角色 -->
          <div class="border rounded-lg p-4">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2">
                  编辑者
                </span>
                <span class="text-sm text-gray-500">可以编辑指定相册</span>
              </div>
              <button class="text-primary-600 hover:text-primary-900 text-sm font-medium">
                编辑权限
              </button>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">功能权限</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    上传照片
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    编辑照片
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-times text-red-500 mr-2"></i>
                    系统设置
                  </li>
                </ul>
              </div>
              <div>
                <h4 class="text-sm font-medium text-gray-700 mb-2">相册权限</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    查看指定相册
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-check text-green-500 mr-2"></i>
                    编辑指定相册
                  </li>
                  <li class="flex items-center">
                    <i class="fas fa-times text-red-500 mr-2"></i>
                    删除相册
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 权限管理相关逻辑
</script>