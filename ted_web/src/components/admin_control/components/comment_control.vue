<template>
  <div class="comment_control">
    <div class="content">
        <div>评论管理</div>
        <div class="search_box">
          <input type="text" placeholder="评论ID/视频ID/用户ID" v-model="search_type">
        </div>
        <div class="comment_list" v-if="comment_list.length>0">
          <div class="comment_item" v-for="(item,index) in comment_list" :key="index">
            {{ item }}
          </div>
        </div>
    </div>
    <div class="check_point" ref="check_point"></div>
  </div>
</template>

<script setup>
import {ref,onMounted,watch} from 'vue'
import get_comment_list from '../ts/get_comment_list';
import search_comment from '../ts/search_comment';
import delete_comment from '../ts/delete_comment';

//评论搜索
let search_type=ref()

//获取评论列表
let limit=ref(10)
let offset=ref(0)
let total=ref(0)
let comment_list=ref([])

//滚动加载
let check_point=ref(null)

//获取评论列表
async function get_com_list(){
  let res=await get_comment_list(limit.value,offset.value)
  if(res.status==200){
    comment_list.value=res.data
    total.value=res.total
  }
}
onMounted(async ()=>{
  await get_com_list()
})

</script>

<style scoped>
.check_point{
  width: 1px;
  height: 1px;
  display: block;
  opacity: 0;
}
</style>