<template>
  <div class="my_video">
    <div class="content">
        <h2>我的视频</h2>
        <div class="video_list">
          <div class="item" v-for="(item,index) in video_list" :key="index">
            <div class="item_content">
              <div class="video_box"  @mouseleave="video_len = ''">
                <video :src="'http://localhost:8000/static/video/'+item.video_file_path" 
                :poster="'http://localhost:8000/static/img/img/'+item.video_cover_path"
                 @mouseenter="get_video_len($event)"></video>
                <div class="video_tiem" v-if="video_len">
                  <span>{{ video_len }}</span>
                </div>
              </div>
              <div class="video_title">
                <span>{{item.title}}</span>
              </div>
              <div class="video_play_data">
                <span style="display: flex;align-items: center;gap:10px;">
                  <img src="http://localhost:8000/static/svg/播放.svg" alt="play" class="icon">
                  {{item.watch_count}}
                </span>
                <span>{{ format_time( item.create_time)}}</span>
              </div>
            </div>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted ,defineProps,computed} from "vue";

const props = defineProps({
    video_list: Array
})

let video_len=ref(null);

//时间格式化
const format_time = (time) => {
  let date = new Date(time);
  let year = date.getFullYear();
  let month = date.getMonth() + 1;
  let day = date.getDate();
  return `${year}-${month}-${day}`;
}

// 视频时间格式化
const format_video_time = (time) => {
  let days = Math.floor(time / 86400); // 86400秒 = 1天
  let hours = Math.floor((time % 86400) / 3600); // 3600秒 = 1小时
  let minutes = Math.floor((time % 3600) / 60);
  let seconds = Math.floor(time % 60);

  if (days > 0) {
    return `${days}天 ${hours}:${minutes.toString().padStart(2, '0')}`;
  } else if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}`;
  } else {
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }
};
//获取指定元素内视频长度
const get_video_len = (e) => {
  let video = e.target;
  let time = video.duration;
  video_len.value = format_video_time(time);
};

</script>

<style scoped>
.icon{
  width: 25px;
  height: 25px;
  object-fit: cover;
}
.content{
  width:100%;
  height: auto;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin-bottom: 20px;
}
.video_list{
  display: flex;
  flex-wrap: wrap;
  gap:30px;
}
.item{
  display: flex;
  flex-direction: column;
  max-width: 150px;
}
.video_box {
  width: 160px;
  height: 100px;
  display: flex;
  position: relative;
  cursor: pointer;
  border-radius: 5px;
  overflow: hidden;
}
.video_box video{
  width: 100%;
  height: auto;
  max-height: 160px;
  object-fit: cover;
}
.video_tiem{
  position: absolute;
  right: 5px;
  bottom: 5px;
  background-color: rgba(133,133,133,0.5);
  color: white;
  padding: 3px;
  border-radius: 5px;
  display: none;
}
.video_box:hover .video_tiem {
  display: block;
}
.item_content{
  display: flex;
  flex-direction: column;
  gap:10px;
}
.video_play_data{
  display: flex;
  justify-content: space-between;
  gap:10px;
  color: rgba(133,133,133,1);
  align-items: center;
}
</style>