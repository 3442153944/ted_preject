<template>
    <div class="other_user_center">
        <div class="content">
            <background :user_info="user_info"></background>

            <div class="change_page">
                <div class="change_item" @mouseover="updateBackItemPosition(0)" @mouseleave="resetBackItemPosition"
                    @click="page_index = 0">
                    <span>主页</span>
                </div>
                <div class="change_item" @mouseover="updateBackItemPosition(1)" @mouseleave="resetBackItemPosition"
                    @click="page_index = 1">
                    <span>视频</span>
                </div>
                <div class="change_item" @mouseover="updateBackItemPosition(2)" @mouseleave="resetBackItemPosition"
                    @click="page_index = 2">
                    <span>收藏</span>
                </div>
                <div class="change_item" @mouseover="updateBackItemPosition(3)" @mouseleave="resetBackItemPosition"
                    @click="page_index = 3">
                    <span>动态</span>
                </div>

                <!-- 背景随动的盒子 -->
                <div class="back_item" :style="{ left: `${backItemPosition}px` }"></div>
            </div>

            <div class="works">
                <index_page :user_info="user_info" v-if="page_index === 0 && user_info.data"></index_page>
                <submit_works :user_info="user_info" v-if="page_index === 1 && user_info.data"></submit_works>
                <collect_video :user_info="user_info" v-if="page_index === 2 && user_info.data"></collect_video>
                <dynamic_page :dynamic_list="user_info.data.dynamic_info" v-if="page_index === 3 && user_info.data"></dynamic_page>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import background from './components/background.vue'
import get_all_user_info from './js/get_all_userinfo'
import index_page from './components/index_page.vue'
import submit_works from './components/submit_works.vue'
import collect_video from './components/collect_works.vue'
import dynamic_page from './components/dynamic_page.vue'

const router = useRouter()
const store = useStore()

const props = defineProps({
    user_id: {
        type: [Number, String],
        default: ''
    }
})

let page_index = ref(0)
let user_id = computed(() => store.getters.other_user_id)
let user_info = ref({})
let backItemPosition = ref(0)  // `back_item` 的水平位置

watch(user_id, async (newVal) => {
    console.log('newVal', newVal)
    await get_user_info()
})

async function get_user_info() {
    let result = await get_all_user_info(user_id.value)
    user_info.value = result
    console.log('user_info', user_info.value)
}

function updateBackItemPosition(index) {
    const itemWidth = 70  // 每个选项的宽度
    backItemPosition.value = index * (itemWidth + 20)  // 根据索引计算位置，20px为间隔
}

function resetBackItemPosition() {
    // 重置位置为当前页面的 `page_index`
    updateBackItemPosition(page_index.value)
}

onMounted(async () => {
    await get_user_info()
    updateBackItemPosition(page_index.value)  // 初始化背景位置
})
</script>

<style scoped>
.other_user_center {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.change_page {
    width: 85vw;
    height: 35px;
    margin-top: 5px;
    margin-bottom: 10px;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    gap: 20px;
    position: relative;
}

.change_item {
    width: 70px;
    height: 30px;
    font-size: 18px;
    font-weight: bold;
    align-items: center;
    justify-content: center;
    display: flex;
    cursor: pointer;
}

.back_item {
    width: 70px;
    height: 30px;
    position: absolute;
    bottom: 0px;
    background-color: rgba(0, 150, 250, 0.2);
    border-bottom: 3px solid rgba(0, 150, 250, 1);
    transition: left 0.3s ease-in-out;
    /* 增加平滑移动效果 */
    pointer-events: none;
    border-radius: 5px 5px 0px 0px;
}

.works {
    width: 85vw;
    height: auto;
    display: flex;
    flex-direction: column;
    margin-left: auto;
    margin-right: auto;
    background-color: rgba(255, 255, 255, 1);
}
</style>