<template>
  <div class="video_control">
    <div class="content">
        <div>视频管理</div>
        <div class="video_list">
          <div class="item" v-for="(item,index) in video_list" :key="index">
            {{ item }}
          </div>
        </div>
    </div>
    <div class="check_point" ref="check_point"></div>
  </div>
</template>

<script setup>
import {ref,onMounted,onUnmounted} from 'vue'
import get_video_list from '../ts/get_video_list';

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
  
</style>