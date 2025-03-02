<template>
  <div class="collect_video">
    <div class="content">
      <h2>我的收藏</h2>
      <div class="btn_box">
        <div class="edit_btn" @click="edit_status_change()">
          <span>{{edit_status?'关闭':'编辑收藏'}}</span>
        </div>
        <div class="sure_btn edit_btn" v-if="edit_status" @click="submit_video()">
          <span>确定</span>
        </div>
        <div class="choose_all edit_btn" @click="choose_all_video()" v-if="edit_status">
          <span>全选</span>
        </div>
      </div>
      <div class="video_list">
        <div class="item" v-for="(item,index) in video_list" :key="index">
          <div class="item_content">
            <div class="video_box"  @mouseleave="video_len = ''">
              <video :src="'http://localhost:8000/static/video/'+item.video_file_path"
              :poster="'http://localhost:8000/static/img/img/'+item.video_cover_path"
               @mouseenter="get_video_len($event)" @click="to_content_page(item.id)"></video>
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
          <div class="choose_box" v-if="edit_status" @click="choose_video_change(item.id)">
            <div class="choose_img" v-if="choose_video.includes(item.id)">
              <img class="icon" src="http://localhost:8000/static/svg/正确.svg" alt="选择">
            </div>
          </div>
        </div>
      </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted ,defineProps,computed} from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import update_collect from "../js/update_collect";

const store = useStore();
const router = useRouter();

const props = defineProps({
    video_list: Array
})
let video_list = ref(props.video_list)

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

//多选编辑状态开启
let edit_status = ref(false);
function edit_status_change(){
  edit_status.value = !edit_status.value;
}

//多选视频
let choose_video = ref([]);
function choose_video_change(item){
  if(choose_video.value.includes(item)){
    choose_video.value.splice(choose_video.value.indexOf(item),1);
  }else{
    choose_video.value.push(item);
  }
}

//全选视频
function choose_all_video(){
  if(choose_video.value.length == props.video_list.length){
    choose_video.value = [];
  }else{
    choose_video.value = [];
    props.video_list.forEach(item => {
      choose_video.value.push(item.id);
    });
  }
}

//提交视频ID，前端删除对应的视频
async function submit_video(){
  let res= await update_collect(choose_video.value);
  if(res.status == 200){
    video_list.value = video_list.value.filter(item => !choose_video.value.includes(item.id));
    choose_video.value = [];
    store.commit('set_global_msg','删除选定收藏视频成功')
  }
  else{
    store.commit('set_global_msg',res.msg)
  }
  edit_status.value = !edit_status.value;
}

//视频跳转
function to_content_page(id){
    router.push('/content_page')
    store.commit('set_video_id',id)
}

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
.btn_box{
  display: flex;
  gap:10px;
}
.edit_btn{
  display: flex;
  margin-bottom: 20px;
  padding: 10px 25px;
  background-color: rgba(0,150,250,1);
  border-radius: 10px;
  color: white;
  width: fit-content;
  cursor: pointer;
  font-size: 18px;
  font-weight: 500;
}
.edit_btn:hover{
  background-color: rgba(0,150,250,0.8);
  transition: all 0.3s ease-in-out;
  transform: scale(1.05);
  transform: translateY(-2px);
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.4);
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
  position: relative;
}
.choose_box{
  width: 100%;
  height: 100%;
  display: flex;
  position: absolute;
  z-index: 3;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 5px;
  cursor: pointer;
}
.choose_img{
  position: absolute;
  left:5px;
  top:5px;
}
.video_box {
  width: 160px;
  height: 100px;
  display: flex;
  position: relative;
  cursor: pointer;
  border-radius: 5px;
  overflow: hidden;
  max-width: 100%;
  max-height: 100%;
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