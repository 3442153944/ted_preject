<template>
  <div class="edit_user_info">
    <div class="content">
        <div class="item">
            <div class="title">
                <span></span>
                <span>修改用户信息</span>
                <span class="close_btn" @click="close()">
                    <img src="http://localhost:8000/static/svg/退出.svg" alt="退出">
                </span>
            </div>
            <div class="form" v-if="user_info">
                <div class="avatar">
                    <img :src="'http://localhost:8000/static/img/thumbnail/'+user_info.avatar_path+'.png'" alt="头像">
                </div>
                <span class="sure_btn" @click="re_avatar(user_info.id)">重置头像</span>
                <div class="form_item">
                    <span>用户ID：</span>
                    <input type="text" :value="user_info.id" disabled>
                </div>
                <div class="form_item">
                    <span>用户名：</span>
                    <input type="text" v-model="user_info.username">
                </div>
                <div class="form_item">
                    <span>密码：</span>
                    <input type="text" v-model="user_info.password" disabled>
                </div>
                <div class="form_item">
                    <span>新密码：</span>
                    <input type="text" v-model="new_password">
                </div>
                <div class="form_item">
                    <span>邮箱：</span>
                    <input type="text" v-model="user_info.email" >
                </div>
                <div class="form_item">
                    <span>个人简介：</span>
                    <input type="text" v-model="user_info.introduce">
                </div>
                <div class="form_item">
                    <span>用户标签：</span>
                    <input type="text" v-model="user_info.user_tags">
                </div>
                <div class="form_item">
                    <span>用户级别/权限：</span>
                    <input type="text" v-model="user_info.is_superuser">
                </div>
                <div class="form_item">
                    <span>性别：</span>
                    <input type="text" v-model="user_info.sex">
                </div>
                <div class="form_item">
                    <span>个人网站：</span>
                    <input type="text" v-model="user_info.self_website">
                </div>
                <div class="form_item">
                    <span>个人网站简介：</span>
                    <input type="text" v-model="user_info.self_website_introduce">
                </div>
                <div class="form_item">
                    <span>注册时间：</span>
                    <input type="text" v-model="user_info.date_joined">
                </div>
            </div>
            <div class="btn_box">
                <span class="sure_btn" @click="edit_user()">
                    确定
                </span>
                <span class="cancel_btn" @click="close()">
                    取消
                </span>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import {ref,defineProps,defineEmits} from 'vue'
import edit_user_info from '../ts/edit_user_info'
import reset_avatar from '../ts/reset_avatar';

const props = defineProps({
    user_info:Object
})
let user_info=ref(props.user_info)
let new_password=ref()

const emit=defineEmits(['close_page'])

function close(){
    emit('close_page')
}

//修改用户信息
async function edit_user(){
    let res=await edit_user_info(user_info.value,new_password.value)
    if(res.status==200){
        alert('修改成功')
    }
    else{
        alert(res.msg)
    }
}

//重置头像
async function re_avatar(id){
    let res=await reset_avatar(id)
    if(res.status==200){
        alert('重置成功')
    }
    else{
        alert(res.msg)
    }
}

</script>

<style scoped>
.edit_user_info{
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    position: fixed;
    left: 0;
    top:0;
    background-color: rgba(0,0,0,0.5);
}
.content{
    width: 80vw;
    height: 80vh;
    display: flex;
    flex-direction: column;
    background-color: rgb(255,255,255);
    padding: 5px;
    border-radius: 5px;
    margin: auto;
    box-sizing: border-box;
    overflow-y: auto;
}
.item{
    display: flex;
    flex-direction: column;
    gap:10px;
}
.title{
    width: calc(100% - 20px);
    margin-left: auto;
    margin-right: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.close_btn{
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}
.close_btn:hover{
    border-radius: 50%;
    background-color: rgba(0,0,0,0.3);
    transform: scale(1.05);
    transform: translateY(-2px);
    transition: all 0.3s;
}
.close_btn img{
    width: 25px;
    height: 25px;
    object-fit: cover;
    border-radius: 50%;
}
.form{
    width: calc(100% - 20px);
    margin-left: auto;
    margin-right: auto;
    display: flex;
    flex-direction: column;
    gap:10px;
}
.avatar{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    display: flex;
}
.avatar img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
.btn_box{
    width: calc(100% - 20px);
    margin-left: auto;
    margin-right: auto;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}
.sure_btn{
    width: 80px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    background-color: rgb(0, 174, 255);
    color: white;
    cursor: pointer;
}
.sure_btn:hover{
    background-color: rgb(0, 174, 255);
    transform: scale(1.05);
    transition: all 0.3s;
    opacity: 0.8;
}
.cancel_btn{
    width: 60px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    background-color: rgb(255, 0, 0);
    color: white;
    cursor: pointer;
}
.cancel_btn:hover{
    background-color: rgb(255, 0, 0);
    transform: scale(1.05);
    transition: all 0.3s;
    opacity: 0.8;
}
</style>