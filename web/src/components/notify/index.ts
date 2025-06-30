import { createApp } from 'vue'
import type { App } from 'vue'
import myNotify from './Notify.vue'

interface NotifyOptions {
    content: string;
    type: 'success' | 'error' | 'warning';
    time?: number;
    url?: string;
    title?: string;
}

interface NotifyData {
    notifyFlag: boolean;
    time: number;
    content: string;
    url: string;
    title: string;
    type: 'success' | 'error' | 'warning';
    timer: number | null;
    timeFlag: boolean;
}

// 创建通知节点
const notifyWrap: HTMLDivElement = document.createElement('div');
notifyWrap.className = "notify-wrap";
notifyWrap.style.cssText = "position: fixed; right: 0px; top: 90px; transition-duration: .5s;";
document.body.appendChild(notifyWrap);

const myMsg = {
    /**
     * 通知框
     * @param options 通知选项
     */
    notify: (options: NotifyOptions): void => {
        const {
            content = '',
            type,
            time = 1500,
            url = '',
            title = ''
        } = options;

        const titleMap: Record<'success' | 'error' | 'warning', string> = {
            success: '创建成功！',
            error: '创建失败！',
            warning: '发生警告！'
        };

        // 创建 Vue 3 组件实例
        const notifyApp = createApp(myNotify, {
            time,
            content,
            url,
            title: title || titleMap[type],
            type,
            onTimeFlagChange: () => {
                notifyApp.unmount();
            }
        });

        // 创建挂载点
        const mountNode = document.createElement('div');
        notifyWrap.appendChild(mountNode);

        // 挂载组件
        notifyApp.mount(mountNode);
    }
}

// 注册插件
function register(app: App): void {
    app.config.globalProperties.$myMsg = myMsg;
}

export default {
    myMsg,
    register
} 