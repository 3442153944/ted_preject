<template>
  <div class="admin_index">
    <div class="content">
        <div>管理面板</div>
        <div class="user_box" v-if="user_info">
            <span style="color: white;margin-left:10px;">欢迎来{{user_info.username}}到管理页</span>
            <div class="user_info">
                <span>{{user_info.username}}</span>
                <div class="avatar">
                    <img :src="'http://localhost:8000/static/img/thumbnail/'+user_info.avatar_path+'.png'" alt="头像">
                </div>
            </div>
        </div>
        <div class="switch_menu">
            <div class="menu_item " style="margin-left: 20px;"
             @click="set_page_index(0)" :class="page_index==0?'is_choose':''">用户管理</div>
            <div class="menu_item" @click="set_page_index(1)" :class="page_index==1?'is_choose':''">视频管理</div>
            <div class="menu_item" @click="set_page_index(2)" :class="page_index==2?'is_choose':''">评论管理</div>
            <div class="menu_item" @click="set_page_index(3)" :class="page_index==3?'is_choose':''">动态管理</div>
        </div>
        <user_control v-if="page_index==0"></user_control>
        <video_control v-if="page_index==1"></video_control>
        <comment_control v-if="page_index==2"></comment_control>
        <dynamic_control v-if="page_index==3"></dynamic_control>
    </div>
  </div>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import check_admin from './ts/check_admin';
import get_user_info from './ts/get_user_info';
import user_control from './components/user_control.vue';
import video_control from './components/video_control.vue';
import comment_control from './components/comment_control.vue';
import dynamic_control from './components/dynamic_control.vue';

let user_info=ref()
let page_index=ref(0)

//设置页面索引
function set_page_index(index){
    page_index.value=index;
}

onMounted(async function (){
    let res=await check_admin();
    if(!res){
        alert("您没有权限访问该页面");
        location.href="/";
    }
    let result=await get_user_info();
    console.log(result);
    user_info.value=result.data;
})

</script>

<style scoped>
.admin_index{
    width: 85vw;
    height: auto;
    display: flex;
    flex-direction: column;
    margin: auto;
}
.content{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.user_box{
    width: 100vw;
    height: 60px;
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    background: linear-gradient(to right, rgba(0,150,200,1),rgba(0,150,250,1));
    align-items: center;
    color: white;
    margin-left: -7.5vw;
}
.user_info{
    display: flex;
    align-items: center;
    gap:10px;
    width: fit-content;
}
.avatar{
    width: 50px;
    height: 50px;
    align-items: center;
    display: flex;
    border-radius: 50%;
    margin-right: 10px;
}
.avatar img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
.switch_menu{
    width: 100%;
    display: flex;
    gap:15px;
    margin-top: 10px;
    margin-bottom: 10px;
    background:linear-gradient(to right,rgb(90, 90, 90),rgba(133,133,133,1));
    color: white;
    margin-left: auto;
    margin-right: auto;
    padding: 10px 0px;
    border-radius: 5px;
}
.menu_item{
    width: 100px;
    height: 100%;
    display: flex;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s;
    align-items: center;
}
.is_choose{
    background-color: rgba(233,233,233,1);
    color: black;
    transform: scale(1.05);
    font-size: 18px;
    font-weight: 500;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(255,255,255,0.5);
}
</style>