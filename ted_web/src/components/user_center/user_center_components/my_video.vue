<template>
  <div class="my_video">
    <div class="content">
      <h2>我的视频</h2>
      <div class="video_list">
        <div class="item" v-for="(item, index) in video_list" :key="index">
          <div class="item_content">
            <div class="video_box" @mouseleave="video_len = ''" @click="to_content_page(item.id)">
              <video :src="'http://localhost:8000/static/video/' + item.video_file_path"
                :poster="'http://localhost:8000/static/img/img/' + item.video_cover_path"
                @mouseenter="get_video_len($event)"></video>
              <div class="video_tiem" v-if="video_len">
                <span>{{ video_len }}</span>
              </div>
            </div>
            <div class="video_title">
              <span>{{ item.title }}</span>
            </div>
            <div class="video_play_data">
              <span style="display: flex;align-items: center;gap:10px;">
                <img src="http://localhost:8000/static/svg/播放.svg" alt="play" class="icon">
                {{ item.watch_count }}
              </span>
              <span>{{ format_time(item.create_time) }}</span>
            </div>
            <div class="edit_box">
              <span v-if="delete_btn_index == index" @click="delete_video(item.id)" style="background-color: red;cursor: pointer;color:white;padding:0px 10px;
                border-radius:5px;">
                删除该视频</span>
              <div class="more_btn" @click="set_del_btn_index(index)">
                <img class="icon" src="http://localhost:8000/static/svg/展开.svg"
                  :style="delete_btn_index == index ? 'transform:rotate(0deg)' : ''">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, computed } from "vue";
import update_video_status from "../js/update_video_status";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

const props = defineProps({
  video_list: Array
})

let video_len = ref(null);

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


//展开指定位置删除按钮
let delete_btn_index = ref(-1)
function set_del_btn_index(index) {
  delete_btn_index.value = (delete_btn_index.value == index ? -1 : index)
}

//删除指定视频
async function delete_video(id) {
  alert('确认删除该视频吗？')
  let res = await update_video_status(id)
  if (res.status == 200) {
    video_list.value = video_list.value.filter(item => item.id != id)
    store.commit('set_global_msg', "删除视频成功")
  }
  else {
    store.commit('set_global_msg', res.msg)
  }
}

//视频跳转
function to_content_page(id){
    router.push('/content_page')
    store.commit('set_video_id',id)
}

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
  overflow: hidden;
  margin-bottom: 20px;
}

.video_list {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.item {
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

.video_box video {
  width: 100%;
  height: auto;
  max-height: 160px;
  object-fit: cover;
}

.video_tiem {
  position: absolute;
  right: 5px;
  bottom: 5px;
  background-color: rgba(133, 133, 133, 0.5);
  color: white;
  padding: 3px;
  border-radius: 5px;
  display: none;
}

.video_box:hover .video_tiem {
  display: block;
}

.item_content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.video_play_data {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  color: rgba(133, 133, 133, 1);
  align-items: center;
}

.edit_box {
  display: flex;
  position: relative;
  justify-content: flex-end;
  width: 100%;
  align-items: center;
  gap: 10px;
}

.more_btn {
  width: 30px;
  height: 25px;
  display: flex;
  justify-content: center;
  cursor: pointer;
  align-items: center;
  transition: all 0.3s;
}

.more_btn:hover {
  background-color: #525252;
  border-radius: 5px;
}

.more_btn img {
  /*旋转180°*/
  transform: rotate(180deg);
  transition: all 0.3s;
}

.edit_box span {
  transition: all 0.3s;
}
</style>