<template>
    <!-- 主内容区 -->
    <main class="flex-1 overflow-hidden flex">
        <!-- 左侧导航 -->
        <div class="w-64 border-r border-base-300 sticky top-0 h-screen-header">
            <div class="h-full flex flex-col py-6">
                <div class="px-4">
                    <h2 class="text-lg font-medium text-primary-600">设置</h2>
                </div>
                <nav class="flex-1 px-8 space-y-1">
                    <router-link to="/settings/account"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/account' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-user-circle mr-3" :class="[$route.path === '/settings/account' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>账户信息</span>
                    </router-link>
                    <router-link to="/settings/notifications"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/notifications' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-bell mr-3" :class="[$route.path === '/settings/notifications' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>消息通知</span>
                    </router-link>
                    <router-link to="/settings/privacy"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/privacy' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-lock mr-3" :class="[$route.path === '/settings/privacy' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>隐私与安全</span>
                    </router-link>
                    <router-link to="/settings/storage"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/storage' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-hdd mr-3" :class="[$route.path === '/settings/storage' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>存储管理</span>
                    </router-link>
                    <router-link to="/settings/sync"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/sync' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-sync-alt mr-3" :class="[$route.path === '/settings/sync' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>同步设置</span>
                    </router-link>
                    <router-link to="/settings/appearance"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/appearance' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-palette mr-3" :class="[$route.path === '/settings/appearance' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>外观设置</span>
                    </router-link>
                    <router-link to="/settings/sharing"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/sharing' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-share-alt mr-3" :class="[$route.path === '/settings/sharing' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>分享与权限</span>
                    </router-link>
                    <router-link to="/settings/permissions"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/permissions' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-user-shield mr-3" :class="[$route.path === '/settings/permissions' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>权限管理</span>
                    </router-link>
                    <router-link to="/settings/help"
                        class="group flex items-center px-3 py-2 text-sm font-medium rounded-md"
                        :class="[$route.path === '/settings/help' ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900']">
                        <i class="fas fa-question-circle mr-3" :class="[$route.path === '/settings/help' ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500']"></i>
                        <span>帮助与反馈</span>
                    </router-link>
                </nav>
                <div class="mt-auto px-4 pt-4 border-t border-base-300">
                    <button @click="handleLogout"
                        class="text-red-600 hover:text-red-800 group flex items-center px-2 py-2 text-sm font-medium rounded-md w-full">
                        <i class="fas fa-sign-out-alt mr-3"></i>
                        <span>退出登录</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- 右侧内容 -->
        <div class="flex-1 overflow-y-auto h-screen-header py-6 px-8">
            <router-view></router-view>
        </div>
    </main>
</template>

<script setup lang="ts">
const handleLogout = () => {
    // 处理退出登录逻辑
    console.log('退出登录');
};
</script>