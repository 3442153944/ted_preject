<template>
    <div class="user_video_list" v-if="video_list.length > 0">
        <div class="content">
            <div class="title">
                <span>请选择置顶的视频</span>
                <div class="close_btn" @click="colse_page">
                    <img src="http://localhost:8000/static/svg/退出.svg" alt="退出" class="icon">
                </div>
            </div>
            <div class="input_box">
                <div class="input">
                    <input placeholder="请输入想要搜索的视频" v-model="search_key">
                    <img src="http://localhost:8000/static/svg/搜索.svg" alt="搜索" class="icon">
                </div>
            </div>
            <div class="video_list">
                <div class="video_item" v-for="(item, index) in filtered_video_list" :key="index">
                    <div class="item" :class="selected_video.index == index ? 'item_choose_status' : ''"
                        @click="set_selected_video(index, item.id)">
                        <div class="video_cover">
                            <img :src="'http://localhost:8000/static/img/img/' + item.video_cover_path">
                        </div>
                        <div class="video_info">
                            <div class="title">
                                <span>{{ item.title }}</span>
                            </div>
                            <div class="watch_count">
                                <div class="count">
                                    <img class="icon" src="http://localhost:8000/static/svg/播放.svg">
                                    <span>{{ item.watch_count }}</span>
                                </div>
                                <div class="create_time">
                                    <span>{{ item.create_time }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="btn_box">
                <div class="sure_btn" @click="submit_update">
                    <span>确定</span>
                </div>
                <div class="cancel_btn" @click="colse_page">
                    <span>取消</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed } from "vue";
import update_top_video from "../js/update_top_video";
import { useStore } from "vuex";

const store = useStore();

const props = defineProps({
    video_list: Array
});

const emit = defineEmits(['update_user_info', 'close_page','page_reload']);

let colse_page = () => {
    emit('close_page');
};

let search_key = ref('');

// 选中的视频
let selected_video = ref({
    index: null,
    video_id: 0
});

// 过滤后的视频列表
const filtered_video_list = computed(() => {
    if (search_key.value.trim() === '') {
        return props.video_list;
    }
    return props.video_list.filter(item =>
        item.title.toLowerCase().includes(search_key.value.toLowerCase())
    );
});

// 设置选中的视频
function set_selected_video(index, video_id) {
    selected_video.value = {
        index: index,
        video_id: video_id
    };
}

// 提交更新的置顶视频
async function submit_update() {
    let res = await update_top_video(selected_video.value.video_id, 'update');
    if (res.status == 200) {
        emit('update_user_info');
        colse_page();
        emit('page_reload');
    }
    store.commit('set_global_msg',res.status?'更新置顶视频成功':`失败，${res.msg}`)
}
</script>


<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.user_video_list {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.1);
}

.content {
    width: 400px;
    height: auto;
    max-height: 800px;
    min-height: 100px;
    background-color: rgba(255, 255, 255, 1);
    margin: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-radius: 10px;
    padding: 5px;
    overflow-y: auto;
}

.title {
    width: auto;
    height: 35px;
    display: flex;
    justify-content: space-between;
    margin: 0px 10px;
    margin-top: 5px;
}

.close_btn {
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-content: center;
    align-items: center;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}

.close_btn:hover {
    transform: rotate(180deg);
    transform: scale(1.02);
    transform: translateY(-1px);
    background-color: rgba(133, 133, 133, 1);
    border-radius: 50%;
}

.btn_box {
    display: flex;
    height: 60px;
    gap: 20px;
    padding: 0 20px;
    justify-content: center;
    align-items: flex-end;
}

.sure_btn {
    padding: 10px 20px;
    display: flex;
    background-color: rgba(0, 150, 250, 1);
    cursor: pointer;
    color: white;
    border-radius: 10px;
    transition: all 0.3s ease-in-out;
}

.sure_btn:hover {
    background-color: rgba(0, 150, 250, 0.8);
    transform: scale(1.02) translateY(-1px);
}

.cancel_btn {
    padding: 10px 20px;
    display: flex;
    background-color: rgba(133, 133, 133, 1);
    cursor: pointer;
    color: white;
    border-radius: 10px;
    transition: all 0.3s ease-in-out;
}

.cancel_btn:hover {
    background-color: rgba(133, 133, 133, 0.8);
    transform: scale(1.02) translateY(-1px);
}

.input_box {
    display: flex;
    background-color: rgba(133, 133, 133, 0.5);
    width: 100%;
    border-radius: 10px;
}

.input {
    width: 100%;
    display: flex;
    gap: 5px;
    justify-content: center;
    align-items: center;
}

.input_box input {
    height: 35px;
    border-radius: 10px;
    outline: none;
    border: none;
    width: 100%;
    background: none;
    max-width: calc(100% - 40px);
}

.video_list {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
}

.video_item {
    height: 80px;
    display: flex;
    gap: 5px;
    max-height: 80px;
}

.item {
    display: flex;
    gap: 10px;
    align-items: center;
    cursor: pointer;
    border-radius: 10px;
    padding: 5px 10px;
    width: calc(100% - 20px);
}

.item_choose_status {
    background-color: rgba(0, 150, 220, 0.8);
    color: white;
}

.video_cover {
    width: 100px;
    height: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 100px;
}

.video_cover img {
    width: 100%;
    height: auto;
    max-height: 100px;
    object-fit: cover;
    border-radius: 5px;
}

.video_info {
    display: flex;
    gap: 8px;
    flex-direction: column;
}

.watch_count {
    display: flex;
    gap: 5px;
    font-size: 14px;
    color: rgba(133, 133, 133, 1);
    align-items: center;
}

.count {
    display: flex;
    align-items: center;
    gap: 5px;
}
</style>