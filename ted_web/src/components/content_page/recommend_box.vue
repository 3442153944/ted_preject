<template>
  <div class="recommend_box">
    <div class="content">
        <div class="video_recommend">
            <h2>接下来观看</h2>
            <div class="recommend_list">
                <!-- 推荐视频列表，使用v-for循环 -->
                <div class="recommend_item" v-for="(video, index) in recommend_video_list" :key="index"
                    @mouseenter="playRecommendVideo(index)" @mouseleave="pauseRecommendVideo(index)">
                    <div class="recommend_video_box" @click="jump_link(video.video_id)">
                        <!-- 推荐视频播放器 -->
                        <video ref="recommendRefs" class="recommend-video" 
                        :src="'http://localhost:8000/static/video/'+video.video_file_path" muted
                            @timeupdate="updateRecommendTime(index)" preload="auto" 
                            :poster="'http://localhost:8000/static/img/img/'+video.video_cover_path"></video>
                        <div class="time">
                            <span>{{ remainingTimes[index] }} 秒</span>
                        </div>
                    </div>
                    <div class="recommend_info">
                        <div class="recommend_time">
                            <span>{{ video.create_time }}</span>
                        </div>
                        <div class="recommend_title">
                            <span>{{ video.title }}</span>
                        </div>
                        <div class="recommend_speaker">
                            <span>{{video.username}}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router';
import get_recommend_video from './js/get_recommend_video'

const store = useStore()
const router = useRouter()

let recommend_video_list=ref([])

//进入推荐视频页面
function jump_link(video_id){
    router.push('/content_page')
    store.commit('set_video_id',video_id)
    console.log(video_id)
}

// 主视频的播放路径
const video_path = ref('src/assets/video/v1.mp4')

// 推荐视频列表（动态加载）
const videoList = ref([])

// 剩余时间数组
const remainingTimes = ref([])

// 引用推荐视频的 DOM 元素
const recommendRefs = ref([])

// 模拟动态加载视频数据
function fetchVideoList() {
    // 这里用模拟数据替代实际请求
    const fetchedVideos = [
        { src: video_path.value, date: '2024-03-03' },
        { src: video_path.value, date: '2024-03-04' },
        { src: video_path.value, date: '2024-03-05' },
        // 可以继续添加更多视频
        { src: video_path.value, date: '2024-03-05' },
        { src: video_path.value, date: '2024-03-05' },
    ]

    videoList.value = fetchedVideos
    remainingTimes.value = Array(fetchedVideos.length).fill(0)
}

// 鼠标移入时播放推荐视频
function playRecommendVideo(index) {
    if (recommendRefs.value[index]) {
        recommendRefs.value[index].play()
    }
}

// 鼠标移出时暂停推荐视频
function pauseRecommendVideo(index) {
    if (recommendRefs.value[index]) {
        recommendRefs.value[index].pause()
    }
}

// 更新推荐视频的剩余时间
function updateRecommendTime(index) {
    const video = recommendRefs.value[index]
    if (video) {
        remainingTimes.value[index] = Math.floor(video.duration - video.currentTime)
    }
}

onMounted(async () => {
    fetchVideoList() // 动态加载视频数据
    // 通过 refs 获取视频引用
    recommendRefs.value = []
    recommend_video_list.value = await get_recommend_video()
    recommend_video_list.value=recommend_video_list.value.data
    console.log(recommend_video_list.value)
    //剩余时间初始化
    remainingTimes.value = Array(recommend_video_list.value.length).fill(0)
})
</script>

<style scoped>
.recommend_box{
    height: 100%;
    max-height: 100%;
    overflow-y: auto;
}
.video_recommend {
    margin-top: 40px;
    display: flex;
    flex-direction: column;
    width: 100%;
}
.recommend_list {
    display: flex;
    gap: 20px;
    flex-direction: column;
}

.recommend_item {
    width: 250px;
    cursor: pointer;
}

.recommend_video_box {
    position: relative;
    width: 100%;
    height: 140px;
    background-color: #000;
}

.recommend-video {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.time {
    position: absolute;
    bottom: 5px;
    right: 10px;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 3px 8px;
    font-size: 12px;
    border-radius: 3px;
    z-index: 2;
}
</style>