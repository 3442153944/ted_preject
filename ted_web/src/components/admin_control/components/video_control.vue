<template>
  <div class="video_control">
    <div class="content">
        <div>视频管理</div>
        <div class="video_list">
          <div class="item" v-for="(item,index) in video_list" :key="index">
            <div class="video_item">
              <div class="video_box">
                <video :src="'http://localhost:8000/static/video/'+item.video_file_path"
                 :poster="'http://localhost:8000/static/img/img/'+item.video_cover_path" 
                 preload="auto" muted="true" controls></video>
              </div>
              <div class="video_info">
                <div class="info_item">
                  <span>视频标题：{{item.video_title}}</span>
                </div>
                <div class="info_item">
                  <span>视频作着：{{item.username}}</span>
                </div>
                <div class="info_item">
                  <span>视频介绍：{{item.video_introduce}}</span>
                </div>
                <div class="info_item">
                  <span>视频投稿时间：{{item.create_time}}</span>
                </div>
                <div class="info_item">
                  <span>视频标签：{{item.video_tags}}</span>
                </div>
                <div class="info_item">
                  <span>播放量：{{item.watch_count}}&nbsp;喜欢：{{item.like_count}}&nbsp;收藏：{{item.collect_count}}</span>
                </div>
                <div class="info_item">
                  <div class="user_info">
                    <div class="avatar">
                      <img :src="'http://localhost:8000/static/img/thumbnail/'+item.avatar_path+'.png'" alt="头像">
                    </div>
                    <div class="username">
                      <span>{{item.username}}</span>
                    </div>
                  </div>
                </div>
                <div class="btn_box">
                  <span class="delete hover" @click="del_video(item.video_id)">删除</span>
                </div>
              </div>
            </div>
          </div>
        </div>
    </div>
    <div class="check_point" ref="check_point"></div>
  </div>
</template>

<script setup>
import {ref,onMounted,onUnmounted} from 'vue'
import get_video_list from '../ts/get_video_list';
import delete_video from '../ts/delete_video';

let video_list=ref([])

let check_point = ref(null)
let limit=ref(10)
let offset=ref(0)
let total=ref(0)

//检查是否需要加载更多
let obs=new IntersectionObserver(async (entries)=>{
  entries.forEach(async (entry)=>{
    if(entry.isIntersecting){
      offset.value+=limit.value
      let res=await get_video_list(limit.value,offset.value)
      if(res.status==200){
        total.value=res.data.total
        video_list.value=video_list.value.concat(res.data)
      }
    }
  })
},{
  root:null,
  rootMargin:'200px',
  threshold:0
})

//删除视频
async function del_video(id){
  alert('确定删除该视频吗？')
  let res=await delete_video(id)
  if(res.status==200){
    video_list.value=video_list.value.filter(item=>item.id!=id)
    console.log('删除成功');
  }
}

onMounted(async ()=>{
  let res=await get_video_list(limit.value,offset.value)
  if(res.status==200){
    total.value=res.data.total
    video_list.value=res.data
  }
  obs.observe(check_point.value)
})

onUnmounted(()=>{
  obs.disconnect()
})

</script>

<style scoped>
.video_control{
  width: 85vw;
  display: flex;
  flex-direction: column;
  margin: auto;
}
.content{
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
}
.video_list{
  width: 100%;
  height: auto;
  display: flex;
  gap:10px;
  flex-direction: column;
}
.check_point{
  width: 1px;
  height: 1px;
  display: block;
  opacity: 0;
}
.item{
  width: 100%;
  height: 350px;
  min-width: 500px;
  display: flex;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(133,133,133,1);
}
.video_item{
  display: flex;
  flex-direction: row;
  gap:10px;
}
.video_box{
  width:100%;
  height: 100%;
  max-width: 500px;
  max-height: 350px;
  display: flex;
  position: relative;
}
.video_box video{
  width: auto;
  height: auto;
  max-width: 500px;
  max-height: 350px;
  object-fit: cover;
}
.video_info{
  width: fit-content;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  gap:5px;
}
.user_info{
  width: 100%;
  height: 50px;
  display: flex;
  gap:10px;
  align-items: center;
}
.avatar{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
}
.avatar img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.delete {
  padding: 10px 17.5px;
  background-color: rgb(247, 23, 23);
  cursor: pointer;
  border-radius: 5px;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.hover:hover {
  transition: all 0.3s;
  opacity: 0.8;
  transform: scale(1.05);
  transform: translateY(-2px);
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.4);
}
</style>