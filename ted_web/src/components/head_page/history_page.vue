<template>
  <div class="history_page">
    <div class="content">
      <div>历史记录</div>
      <div class="item_list">
        <div class="item" v-for="(item,index) in watch_his" :key="index">
          <div class="video_box">
            <video :src="'http://localhost:8000/static/video/'+item.video_file_path" 
            preload="auto" :poster="'http://localhost:8000/static/img/img/'+item.video_cover_path"></video>
          </div>
          <div class="video_info">
            <span>{{item.title}}</span>
            <span>{{item.introduce}}</span>
            <span>{{format_time(item.watch_his_time)}}</span>
          </div>
          <div class="user_info">
            <div class="avatar">
              <img :src="'http://localhost:8000/static/img/thumbnail/'+item.author_info.avatar_path+'.png'">
            </div>
            <span>{{item.author_info.username}}</span>
          </div>
          {{ item }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue'
import get_watch_his from './get_watch_his';

let watch_his = ref([])
onMounted(async function () {
  let res = await get_watch_his()
  if (res.status == 200) {
    watch_his.value = res.data
  }
  else {
    console.warn(res.msg)
  }
  //清除author_id为空以及author_info为空的记录
  watch_his.value = watch_his.value.filter(item => (item.author_id==null || item.author_id=='' 
  || item.author_info==null || item.author_info=={})?false:true)
})

//格式化时间
function format_time(time){
  let date = new Date(time)
  let year = date.getFullYear()
  let month = date.getMonth()+1
  let day = date.getDate()
  return `${year}年${month}月${day}日`
}

</script>

<style scoped></style>