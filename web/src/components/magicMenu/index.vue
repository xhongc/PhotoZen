<template>
    <div>
        <!--      头部菜单      -->
        <top-header></top-header>
        <!--      内容区域      -->
        <container></container>
    </div>
</template>

<script lang="ts" setup>
import topHeader from './header.vue'
import container from './container.vue'
import { ref } from 'vue'

const title = ref('音乐标签Web版')
const headerTitle = ref('')
const imgSrc = ref('')
</script>

<style scoped>
.monitor-logo {
    width: 32px;
    height: 32px;
}

.monitor-logo-icon {
    width: 32px;
    height: 32px;
}
</style>
