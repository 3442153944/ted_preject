<template>
    <div class="index_item">
        <div class="content">
            <div class="top_video" v-if="video_info">
                <div class="video_box" v-if="video_info.video_file_path">
                    <video :src="'http://localhost:8000/static/video/' + video_info.video_file_path"
                        :poster="'http://localhost:8000/static/img/img/' + video_info.video_cover_path"
                        ref="video_file"></video>
                    <div class="time_box">
                        <span>{{ video_long_time }}</span>
                    </div>
                </div>
                <div class="video_info" >
                    <div>{{ video_info.title }}</div>
                    <div class="play_info" v-if="video_info.video_file_path">
                        <span>
                            <img src="http://localhost:8000/static/svg/播放.svg" alt="player" class="icon">
                            {{ video_info.watch_count }}
                        </span>
                        <span>
                            {{ video_info.create_time }}
                        </span>
                    </div>
                    <div class="edit_top_video">
                        <span class="edit_top_ed"
                            @click="float_video_list_box_show = !float_video_list_box_show">编辑置顶</span>
                        <span class="edit_top_ca" @click="del_top" v-if="video_info.video_file_path" >取消置顶</span>
                    </div>
                </div>
            </div>
            <div class="add_top_video" v-else>
                <div class="add_btn" @click="float_video_list_box_show = true">
                    <img src="http://localhost:8000/static/svg/新增.svg" alt="新增" class="icon" style="width:50px;height:50px;">
                    <span>新增一个置顶视频</span>
                </div>
            </div>
            <div class="float_video_list_box" v-if="float_video_list_box_show">
                <user_video_list :video_list="props.user_info.data.user_videos"
                    @close_page="float_video_list_box_show = false" @page_reload="reload()"></user_video_list>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import get_video_info from '../js/get_video_info';
import user_video_list from './user_video_list.vue';
import update_top_video from '../js/update_top_video';

const store = useStore();
const router = useRouter();

let video_file = ref(null)
let video_long_time = ref(null)
let float_video_list_box_show = ref(false)

//获取视频时长
function get_video_long_time() {
    video_file.value.addEventListener('loadedmetadata', function () {
        let duration = video_file.value.duration;
        let hour = Math.floor(duration / 3600);
        let minute = Math.floor((duration % 3600) / 60);
        let second = Math.floor(duration % 60);

        // 如果小时为0，则不显示小时
        let formattedTime = '';
        if (hour > 0) {
            formattedTime += (hour < 10 ? '0' : '') + hour + ':';
        }
        formattedTime += (minute < 10 ? '0' : '') + minute + ':';
        formattedTime += (second < 10 ? '0' : '') + second;

        video_long_time.value = formattedTime;
    });
}


const props = defineProps({
    user_info: Object
})

let video_info = ref({})
let user_info = ref({})

async function del_top() {
    let res = await update_top_video(null, 'del')
    console.log(res)
    store.commit('set_global_msg',res.status?'取消置顶成功':`失败${res.msg}`)
    setTimeout(function () {
        window.location.reload()
    },1000)
}

function reload() {
    window.location.reload()
}

onMounted(async function () {
    console.log(props.user_info)
    user_info.value = props.user_info.data.user_info
    if (user_info.value.top_video) {
        let res = await get_video_info(user_info.value.top_video)
        video_info.value = res.data
        console.log(video_info.value)
        nextTick(function () {
            get_video_long_time()
        })
    }
    else{
        video_info.value = {}
        console.log('没有置顶视频')
    }

})

</script>

<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.content {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
}

.top_video {
    width: auto;
    height: auto;
    max-height: 300px;
    display: flex;
    position: relative;
    gap: 20px;
}

.top_video video {
    width: auto;
    max-width: 400px;
    max-height: 300px;
    height: auto;
    object-fit: cover;
}

.video_box {
    position: relative;
}

.time_box {
    position: absolute;
    padding: 3px 5px;
    background-color: rgba(196, 196, 196, 0.5);
    right: 5px;
    bottom: 5px;
    border-radius: 5px;
}

.video_info {
    display: flex;
    gap: 20px;
    flex-direction: column;
}

.play_info {
    width: auto;
    display: flex;
    gap: 10px;
    align-items: center;
}

.play_info span {
    display: flex;
    align-items: center;
    gap: 5px;
}

.edit_top_video {
    display: flex;
    gap: 20px;
    align-items: center;
}

.edit_top_ed {
    background-color: rgba(0, 150, 220, 1);
    color: white;
    padding: 5px 10px;
    transition: all 0.2s ease-in-out;
    border-radius: 5px;
    border: 1px solid rgba(1, 1, 1, 0.2);
}

.edit_top_ca {
    background-color: rgba(255, 255, 255, 1);
    color: black;
    padding: 5px 10px;
    border-radius: 5px;
    transition: all 0.2s ease-in-out;
    border: 1px solid rgba(1, 1, 1, 0.2);
}

.edit_top_ed:hover,
.edit_top_ca:hover {
    cursor: pointer;
    border: 1px solid rgba(0, 150, 220, 1);
    transform: scale(1.02) translateY(-1px);
}

.float_video_list_box {
    position: fixed;
    top: 0px;
    left: 0px;
}
.add_top_video{
    width:200px;
    height: 200px;
    display: flex;
    flex-direction: column;
    padding:5px;
    align-items: center;
    justify-content: center;
}
.add_btn{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap:10px;
    cursor: pointer;
    justify-content: center;
}

</style>