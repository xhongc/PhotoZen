<template>
    <div id="container" class="bg-base-200">
        <router-view v-slot="{ Component }">
            <keep-alive :include="['PhotosView']">
                <component :is="Component" />
            </keep-alive>
        </router-view>
    </div>
</template>

<script setup lang="ts">
// 由于没有任何数据和方法,这里可以保持为空
</script>

<style scoped></style>
