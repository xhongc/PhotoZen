<template>
    <transition name="slide-fade">
        <div v-if="isVisible" class="notify-container">
            <div role="alert" class="alert shadow-lg notify" :class="type">
                <div class="flex items-center flex-1">
                    <!-- 图标 -->
                    <div class="icon-wrapper mr-4">
                        <svg v-if="type === 'success'" class="h-6 w-6 fill-success" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
                            <path d="M512 832c-176.448 0-320-143.552-320-320S335.552 192 512 192s320 143.552 320 320-143.552 320-320 320m0-704C300.256 128 128 300.256 128 512s172.256 384 384 384 384-172.256 384-384S723.744 128 512 128"></path>
                            <path d="M619.072 429.088l-151.744 165.888-62.112-69.6a32 32 0 1 0-47.744 42.624l85.696 96a32 32 0 0 0 23.68 10.688h0.192c8.96 0 17.536-3.776 23.616-10.4l175.648-192a32 32 0 0 0-47.232-43.2"></path>
                        </svg>
                        <svg v-else-if="type === 'error'" class="h-6 w-6 fill-error" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
                            <path d="M676.053333 350.208l-1.152-1.152a25.6 25.6 0 0 0-36.181333 0L512 475.733333l-126.72-126.72a25.557333 25.557333 0 0 0-36.224 0 25.514667 25.514667 0 0 0 0 36.266667L475.818667 512 349.013333 638.72a25.514667 25.514667 0 0 0 0 36.138667l1.194667 1.152a25.6 25.6 0 0 0 36.224 0l126.72-126.72 126.72 126.72a25.6 25.6 0 1 0 36.181333-36.224l-126.72-126.72 126.72-126.72a25.6 25.6 0 0 0 0-36.181334"></path>
                        </svg>
                        <svg v-else class="h-6 w-6 fill-warning" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
                            <path d="M522.656 388.064a32 32 0 0 0-32 32v160a32 32 0 0 0 64 0v-160a32 32 0 0 0-32-32M522.656 676.064a32 32 0 1 0 0 64 32 32 0 0 0 0-64"></path>
                            <path d="M714.656 795.616H203.072l127.584-221.888 33.152-57.664 158.848-276.224 158.816 276.224 33.184 57.696 127.552 221.856h-127.552z m194.528-11.968L566.528 187.712c-10.144-17.6-26.112-27.712-43.872-27.712s-33.728 10.112-43.84 27.712L136.096 783.648c-10.048 17.568-10.784 36.48-1.92 51.84 8.896 15.328 25.6 24.128 45.824 24.128H865.344c20.16 0 36.864-8.8 45.76-24.128 8.896-15.36 8.192-34.24-1.92-51.84z"></path>
                        </svg>
                    </div>
                    <!-- 内容 -->
                    <div class="flex-1">
                        <h3 class="font-bold text-base">{{title}}</h3>
                        <div class="text-sm mt-1">{{content}}</div>
                    </div>
                </div>
                <!-- 操作按钮 -->
                <div class="flex items-center space-x-2">
                    <button v-if="url" 
                        class="btn btn-sm btn-primary" 
                        @click="handleRedirct(url)">
                        查看
                    </button>
                    <button class="btn btn-sm btn-ghost" @click="handleClose">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup lang="ts">
import { ref, onBeforeUnmount, onMounted } from 'vue'

interface Props {
  time: number
  content: string
  url: string
  title: string
  type: 'success' | 'error' | 'warning'
}

const props = defineProps<Props>()
const emit = defineEmits(['timeFlagChange'])

const isVisible = ref(true)
const timer = ref<number | null>(null)

// 设置定时器
onMounted(() => {
  timer.value = window.setTimeout(() => {
    handleClose()
  }, props.time)
})

// 组件卸载时清理定时器
onBeforeUnmount(() => {
  if (timer.value) {
    window.clearTimeout(timer.value)
  }
})

// 处理关闭
const handleClose = () => {
  isVisible.value = false
  emit('timeFlagChange', true)
}

// 处理跳转
const handleRedirct = (url: string) => {
  window.location.href = url
  handleClose()
}
</script>

<style scoped>
.slide-fade-leave-active {
    transition: all .2s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to{
    transform: translateX(10px);
    opacity: 0;
}
.notify-wrap{
    background-color: #1AFA29;
}
.my-notify{
    margin: 15px;
    width: 350px;
}

.notify {
    position: relative;
    animation: show cubic-bezier(.18, .89, .32, 1.28) .4s;
}
.notify .tip{
    height: 30px;
    margin-bottom: 5px;
    line-height: 30px;
}
.notify .tip span{
    line-height: 30px;
    font-size: 17px;
    font-weight: 600;
}
.notify .content{
    width: 320px;
    height: 30px;
    font-size: 15px;
}
@keyframes show{
    0%{
        right: -350px;
    }
    100%{
        right: 10px;
    }
}
</style>
