<template>
    <div class="index_page">
        <div class="content">
            <h2>主页</h2>
            <div class="item">
                <div class="title" v-if="top_video_info">
                    <span>置顶视频</span>
                </div>
                <div class="video_list" v-if="top_video_info">
                    <div class="video_top_item">
                        <video :src="'http://localhost:8000/static/video/' + top_video_info.video_file_path"
                            preload="auto" :poster="'http://localhost:8000/static/img/img/' +
                                (top_video_info.video_cover_path ?
                                    top_video_info.video_cover_path : '102718099_p0.png')" ref="top_video" 
                                    @click="to_video_content(top_video_info.id)" >
                        </video>
                        <div class="video_info">
                            <div class="video_title">
                                <span>{{ top_video_info.title }}</span>
                            </div>
                            <div class="play_info">
                                <div class="play_count">
                                    <img src="http://localhost:8000/static/svg/播放.svg" alt="播放" class="icon">
                                    <span>{{ top_video_info.watch_count }}</span>
                                </div>
                                <div class="time">
                                    <img src="http://localhost:8000/static/svg/时间.svg" alt="时间" class="icon">
                                    <span>{{ format_time(top_video_info.create_time) }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="title" v-if="user_info.data.user_videos.length > 0">
                    <span>投稿的作品</span>
                </div>
                <div class="video_list" v-if="user_info.data.user_videos.length > 0">
                    <div class="video_item" v-for="(item, index) in user_info.data.user_videos.slice(0, 6)"
                        :key="index">
                        <div v-if="index <= 6" class="video_item_1">
                            <video :src="'http://localhost:8000/static/video/' + item.video_file_path" preload="auto"
                                :poster="'http://localhost:8000/static/img/img/' +
                                    (item.video_cover_path ?
                                        item.video_cover_path : '102718099_p0.png')" @click="to_video_content(item.id)" >
                            </video>
                            <div class="video_info">
                                <div class="video_title">
                                    <span>{{ item.title }}</span>
                                </div>
                                <div class="play_info">
                                    <div class="play_count">
                                        <img src="http://localhost:8000/static/svg/播放.svg" alt="播放" class="icon">
                                        <span>{{ item.watch_count }}</span>
                                    </div>
                                    <div class="time">
                                        <img src="http://localhost:8000/static/svg/时间.svg" alt="时间" class="icon">
                                        <span>{{ format_time(item.create_time) }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <span>用户没有投稿的视频</span>
                </div>
                <div class="title" v-if="user_info.data.collected_videos.length > 0">
                    <span>收藏的作品</span>
                </div>
                <div class="video_list" v-if="user_info.data.collected_videos.length > 0">
                    <div class="video_item" v-for="(item, index) in user_info.data.collected_videos.slice(0, 6)"
                        :key="index">
                        <div v-if="index <= 6" class="video_item_1">
                            <video :src="'http://localhost:8000/static/video/' + item.video_file_path" :poster="'http://localhost:8000/static/img/img/' +
                                (item.video_cover_path ? item.video_cover_path : '102718099_p0.png')" 
                                @click="to_video_content(item.id)">
                            </video>
                            <div class="video_info">
                                <div class="video_title">
                                    <span>{{ item.title }}</span>
                                </div>
                                <div class="play_info">
                                    <div class="play_count">
                                        <img src="http://localhost:8000/static/svg/播放.svg" alt="播放" class="icon">
                                        <span>{{ item.watch_count }}</span>
                                    </div>
                                    <div class="time">
                                        <img src="http://localhost:8000/static/svg/时间.svg" alt="时间" class="icon">
                                        <span>{{ format_time(item.create_time) }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <span>用户没有收藏的视频</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, onMounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import get_video_info from '../js/get_video_info';

const router = useRouter();
const store = useStore();

let top_video_info = ref()

const props = defineProps({
    user_info: {
        type: Object,
        default: () => { }
    }
})

async function get_top_video_info() {
    if (props.user_info && props.user_info.data) {
        let result = await get_video_info(props.user_info.data.user_info.top_video)
        console.log(result)
        top_video_info.value = result.data
    }
    else {
        console.log('没有用户信息')
    }
}

//格式化时间
function format_time(time) {
    if (!time) return ''; // 处理空时间

    // 将字符串解析为 Date 对象
    const date = new Date(time.replace(/-/g, '/')); // 替换 '-' 为 '/' 以确保跨浏览器兼容性

    // 提取年、月、日、小时、分钟和秒
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份从 0 开始，需要 +1
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');
    const second = String(date.getSeconds()).padStart(2, '0');

    // 返回格式化后的字符串
    return `${year}年${month}月${day}日 ${hour}时${minute}分`;
}

//视频内容页跳转
const to_video_content = (id) => {
    router.push('content_page')
    store.commit('set_video_id', id)
}

onMounted(async () => {
    await nextTick()
    if (props.user_info.data) {
        await get_top_video_info()
    }
})

</script>

<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.index_page {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    gap: 20px;
    margin-bottom: 20px;
}

.content {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
}

.item {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
}

.title {
    font-size: 18px;
    font-weight: bold;
}

.video_list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    width: 100%;
}

.video_top_item {
    width: 500px;
    height: 300px;
    display: flex;
    position: relative;
    flex-direction: column;
    gap: 10px;
    cursor: pointer;
}

.video_top_item video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 5px;
}

.video_item {
    width: calc(100% / 3 - 20px);
    height: 300px;
    display: flex;
    max-width: 500px;
    max-height: 500px;
    min-width: 300px;
    min-height: 200px;
    cursor: pointer;
}

.video_item video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 5px;
}

.video_item_1 {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.video_info {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.play_info {
    display: flex;
    gap: 5px;
    justify-content: space-between;
    align-items: center;
}

.play_count {
    display: flex;
    align-items: center;
    gap: 5px;
}

.time {
    display: flex;
    align-items: center;
    gap: 5px;
}
</style>