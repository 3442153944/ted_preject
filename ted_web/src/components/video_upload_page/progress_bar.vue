<template>
    <div class="progress_bar">
        <div class="content" :style="{ width: Number(progress) + '%', backgroundColor: barColor }"></div>
    </div>
</template>

<script setup>
import { defineProps } from 'vue';

// 定义组件的属性
const props = defineProps({
    progress: {
        type: [Number,String],
        default: 0, // 初始进度
        validator: (value) => value >= 0 && value <= 100, // 确保进度值在 0 到 100 之间
    },
    barColor: {
        type: String,
        default: '#0080ff', // 默认颜色
    }
});
</script>

<style scoped>
.progress_bar {
    width: 100%;
    height: 5px;
    background-color: #f0f0f0;
    border-radius: 5px;
    overflow: hidden;
}

.content {
    height: 100%;
    width: 0%;
    min-width: 5px;
    transition: width 0.3s ease-in-out;
    /* 平滑过渡效果 */
}
</style>