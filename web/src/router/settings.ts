import type { RouteRecordRaw } from 'vue-router';

const settingsRoutes: RouteRecordRaw[] = [
    {
        path: '/settings',
        component: () => import('@/views/settings/index.vue'),
        children: [
            {
                path: '',
                name: 'settings',
                redirect: '/settings/account',
                meta: {
                    fatherName: 'settings'
                }
            },
            {
                path: 'account',
                name: 'SettingsAccount',
                component: () => import('@/views/settings/account.vue'),
                meta: {
                    title: '账户信息',
                    fatherName: 'settings'
                }
            },
            {
                path: 'notifications',
                name: 'SettingsNotifications',
                component: () => import('@/views/settings/notifications.vue'),
                meta: {
                    title: '消息通知',
                    fatherName: 'settings'
                }
            },
            {
                path: 'privacy',
                name: 'SettingsPrivacy',
                component: () => import('@/views/settings/privacy.vue'),
                meta: {
                    title: '隐私与安全',
                    fatherName: 'settings'
                }
            },
            {
                path: 'storage',
                name: 'SettingsStorage',
                component: () => import('@/views/settings/storage.vue'),
                meta: {
                    title: '存储管理',
                    fatherName: 'settings'
                }
            },
            {
                path: 'sync',
                name: 'SettingsSync',
                component: () => import('@/views/settings/sync.vue'),
                meta: {
                    title: '同步设置',
                    fatherName: 'settings'
                }
            },
            {
                path: 'recycle',
                name: 'SettingsRecycle',
                component: () => import('@/views/settings/recycle.vue'),
                meta: {
                    title: '回收站',
                    fatherName: 'settings'
                }
            },
            {
                path: 'sharing',
                name: 'SettingsSharing',
                component: () => import('@/views/settings/sharing.vue'),
                meta: {
                    title: '分享与权限',
                    fatherName: 'settings'
                }
            },
            {
                path: 'permissions',
                name: 'SettingsPermissions',
                component: () => import('@/views/settings/permissions.vue'),
                meta: {
                    title: '权限管理',
                    fatherName: 'settings'
                }
            },
            {
                path: 'help',
                name: 'SettingsHelp',
                component: () => import('@/views/settings/help.vue'),
                meta: {
                    title: '帮助与反馈',
                    fatherName: 'settings'
                }
            }
        ]
    }
];

export default settingsRoutes; 