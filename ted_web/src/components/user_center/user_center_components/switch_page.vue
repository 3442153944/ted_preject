<template>
    <div class="switch_page">
        <div class="content">
            <!-- 使用 v-for 循环生成选项，并根据当前的 index 添加不同的 class -->
            <div v-for="(item, index) in pages" :key="index"
                :class="['switch_item', { switch_item_in: activePage === index }]" @mouseenter="switchPage(index)"
                ref="switch_items" @click="choose_page(item)">
                <span>{{ item }}</span>
            </div>
            <!-- 下划线，用 transform 和 width 来控制其移动和宽度 -->
            <div class="underline" :style="underlineStyle"></div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, computed, onMounted, nextTick ,defineEmits} from 'vue'

const props = defineProps({
    user_info: Object
})

const emit = defineEmits(['switch_page'])

function choose_page(item)
{
    emit('switch_page',item)
}

// 页面标签
const pages = ['主页', '投稿', '收藏','个人信息']
// 当前激活的页面索引
const activePage = ref(0)
// 存储各个 switch_item 的 DOM 引用
const switch_items = ref([])
// 下划线的宽度和位置
const underlineWidth = ref(0)
const underlineOffset = ref(0)

// 控制下划线的位置和宽度
function switchPage(index) {
    activePage.value = index
    // 在渲染完成后，获取对应 switch_item 的宽度和偏移量
    nextTick(() => {
        const item = switch_items.value[index]
        if (item) {
            underlineWidth.value = item.offsetWidth
            underlineOffset.value = item.offsetLeft
        }
    })
}

// 计算下划线样式，根据当前激活项的宽度和偏移量动态设置
const underlineStyle = computed(() => ({
    width: `${underlineWidth.value}px`,
    transform: `translateX(${underlineOffset.value}px)`
}))

// 初始化时获取默认选项的下划线样式
onMounted(() => {
    switchPage(0)
})
</script>

<style scoped>
.content {
    width: 100%;
    height: 60px;
    display: flex;
    gap: 10px;
    position: relative;
    /* 确保下划线在内部相对定位 */
}

.switch_item {
    width: auto;
    /* 宽度由内容决定 */
    height: 100%;
    display: flex;
    gap: 5px;
    align-items: center;
    justify-content: center;
    padding: 5px 10px;
    padding-bottom: 0px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    position: relative;
}

.switch_item_in {
    color:rgba(0, 150, 220, 1);
    transform: scale(1.02) translateX(0px);
}

.underline {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 2px;
    /* 宽度和位置由 JS 动态控制 */
    background-color: rgba(0, 150, 220, 1);
    transition: transform 0.3s ease-in-out, width 0.3s ease-in-out;
}
</style>