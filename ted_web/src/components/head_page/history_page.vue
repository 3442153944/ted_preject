<template>
  <div class="history_page">
    <div class="content">
      <div class="title">历史记录</div>
      <div class="item_list">
        <div class="item" v-for="(item, index) in watch_his" :key="index">
          <div class="video_box" @click="to_content(item.watch_his_video_id)">
            <video :src="'http://localhost:8000/static/video/' + item.video_file_path" preload="auto"
              :poster="'http://localhost:8000/static/img/img/' + item.video_cover_path"
              @loadedmetadata="get_video_duration($event, item.watch_his_video_id)" muted='true'
              v-on:mouseenter="play_video($event)" v-on:mouseout="pause_video($event)"></video>
            <div class="video_duration">{{ format_video_time(durationMap[item.watch_his_video_id]) }}</div>
          </div>
          <div class="video_info">
            <span style="font-weight: bold;">{{ item.title }}</span>
            <span>{{ item.introduce }}</span>
            <span>{{ format_time(item.watch_his_time) }}</span>
            <div class="user_info">
              <div class="avatar" @click="to_other_user_center(item.author_info.id)">
                <img :src="'http://localhost:8000/static/img/thumbnail/' + item.author_info.avatar_path + '.png'">
              </div>
              <span>{{ item.author_info.username }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="check_point" ref="check_point"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import get_watch_his from './get_watch_his';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

//滚动加载
let check_point = ref(null);
let limit = ref(5);
let offset = ref(0);
let total = ref(0);
let obs = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting) {
    offset.value += limit.value;
    if (offset.value >= total.value) {
      return;
    }
    let res = await get_watch_his(limit.value, offset.value);
    if (res.status === 200) {
      watch_his.value = watch_his.value.concat(res.data);
      // 清除author_id为空以及author_info为空的记录
      watch_his.value = watch_his.value.filter(item => item.author_id && item.author_info);
      //通过watch_his_id去重
      watch_his.value = watch_his.value.filter(
        (item, index, self) =>
          index === self.findIndex(
            (t) => t.watch_his_video_id === item.watch_his_video_id
          )
      )
    } else {
      console.warn(res.msg);
    }
  }
}, {
  root: null,
  rootMargin: '200px',
  threshold: 0
})

let watch_his = ref([]);
let durationMap = ref({}); // 用于存储视频的时长

onMounted(async function () {
  let res = await get_watch_his();
  if (res.status === 200) {
    watch_his.value = res.data;
    total.value = res.total;
  } else {
    console.warn(res.msg);
  }
  // 清除author_id为空以及author_info为空的记录
  watch_his.value = watch_his.value.filter(item => item.author_id && item.author_info);
  obs.observe(check_point.value);
});

//卸载obs
onUnmounted(() => {
  obs.disconnect();
});

// 格式化时间
function format_time(time) {
  let date = new Date(time);
  let year = date.getFullYear();
  let month = date.getMonth() + 1;
  let day = date.getDate();
  return `${year}年${month}月${day}日`;
}

// 获取视频时长
function get_video_duration(event, videoId) {
  let video = event.target;
  durationMap.value[videoId] = video.duration; // 保存视频时长
}

// 格式化视频时间
function format_video_time(time) {
  if (!time) return '0:00';
  let min = Math.floor(time / 60);
  let sec = Math.floor(time % 60).toString().padStart(2, '0');
  return `${min}:${sec}`;
}

//视频开始播放
function play_video(e) {
  e.target.play();
}
// 视频暂停播放
function pause_video(e) {
  e.target.pause();
}

// 内容跳转
const to_content = (id) => {
  router.push('/content_page');
  store.commit('set_video_id', id);
};

// 其他用户的用户中心跳转
const to_other_user_center = (id) => {
  router.push('/other_user_center');
  store.commit('set_other_user_id', id);
};
</script>

<style scoped>
.history_page {
  width: 85%;
  height: auto;
  display: flex;
  flex-direction: column;
  margin: auto;
}

.content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 18px;
  font-weight: 600;
  display: flex;
}

.item_list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.item {
  display: flex;
  gap: 10px;
}

.video_box {
  display: flex;
  width: 300px;
  height: 100%;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
}

.video_box video {
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.video_duration {
  position: absolute;
  bottom: 5px;
  right: 5px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 2px 5px;
  border-radius: 5px;
}

.video_info {
  display: flex;
  width: fit-content;
  flex-direction: column;
  gap: 10px;
}

.user_info {
  display: flex;
  gap: 10px;
  align-items: center;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.check_point{
  display: block;
  width: 1px;
  height: 1px;
  margin: -1px;
  overflow: hidden;
}
</style>