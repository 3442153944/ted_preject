<template>
    <div class="upload_box">
        <div class="content">
            <!-- 上传按钮 -->
            <div class="upload_btn" v-if="!video_file">
                <span @click="upload_btn">上传视频</span>
                <input type="file" name="file" ref="upload_file" @change="change_file" style="display: none;"
                    accept="video/*">
            </div>
            <!-- 上传进度条 -->
            <div v-if="video_file" class="progress_box">
                <div class="progress_bar">
                    <div class="video_file_name">
                        <span>{{ video_filename }}</span>
                    </div>
                    <div class="bar">
                        <div class="load_info" style="display: flex;gap:5px;">
                            <span>已经上传: {{ uploaded_percentage }}%</span>
                            <span>当前速度: {{ current_speed }} MB/s</span>
                            <span>剩余时间: {{ remaining_time }} s</span>
                            <span>&nbsp;</span>
                            <button @click="pause_upload">暂停</button>
                            <span>&nbsp;</span>
                            <button @click="retry_upload">重新上传</button>
                        </div>
                    </div>
                    <progress_bar :progress="uploaded_percentage" style="margin-top: 10px;"></progress_bar>
                </div>
            </div>
            <div class="video_box" v-if="video_file" style="width: 500px;height:300px;object-fit: cover;">
                <video :src="video_url" controls ref="video" style="width: 100%;height: 100%;object-fit: cover;">

                </video>
            </div>
            <!-- 视频封面选择 -->
            <div class="upload_info" >
                <div class="video_cover" v-if="video_file">
                    <span>封面</span>
                    <div class="cover_box">
                        <div class="cover_default">
                            <img :src="choose_video_cover" alt="默认封面" v-if="choose_video_cover" ref="choose_video_cover_file">
                            <div class="upload_cover" @click="choose_default_cover">
                                <span >上传自定义封面</span>
                                <input type="file" name="file" ref="upload_cover_file" style="display: none;"
                                    @change="upload_custom_cover">
                            </div>
                        </div>
                        <div class="cover_item" v-for="(item, index) in video_cover_list" :key="index"
                            @click="select_cover(item,index)">
                            <div class="cover_mask" >
                                <img :src="item" alt="封面预览">
                                <div class="choose_cover" v-if="choose_video_cover_index == index">
                                    <img src="http://localhost:8000/static/svg/正确.svg" alt="选择" class="icon">
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>

                <!-- 视频标题输入 -->
                <div class="video_title">
                    <span>视频标题</span>
                    <input type="text" placeholder="请输入视频标题" v-model="video_title">
                </div>

                <!-- 视频标签输入 -->
                <div class="video_tags">
                    <span>视频标签</span>
                    <div style="display: flex;flex-direction:column;width:100%;gap:10px;">
                        <div class="tag_box">
                            <span v-for="(tag, index) in video_tags" :key="index" class="tag_item">{{ tag }} <button
                                    @click="remove_tag(index)">x</button></span>
                        </div>
                        <div class="tag_input">
                            <input type="text" placeholder="请输入视频标签" v-model="new_tag" @keydown.enter.prevent="add_tag">
                            <span @click="add_tag">添加</span>
                        </div>
                    </div>
                </div>
                <!-- 视频简介输入 -->
                <div class="video_introduce">
                    <span>视频简介</span>
                    <textarea placeholder="请输入视频简介" v-model="video_description"></textarea>
                </div>

                <!-- 提交按钮 -->
                <div class="submit_btn">
                    <span @click="submit_video" :disabled="!video_file">投稿</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref,computed } from 'vue';
import get_video_cover from './js/get_video_cover';
import progress_bar from './progress_bar.vue';
import  upload_video  from './js/upload_video';
import {back_upload_progress} from './js/upload_video'

let upload_file = ref(null);
let upload_cover_file = ref();
let video_cover_list = ref([]);
let choose_video_cover = ref(null);
let choose_video_cover_index = ref(0);
let video_file = ref();
let video_filename = ref('');
let video_title = ref('');
let video_tags = ref([]);
let new_tag = ref('');
let video_description = ref('');
let uploaded_percentage = ref(0);
let current_speed = ref(0);
let remaining_time = ref(0);
//根据函数返回的值设置进度条
const handleUploadProgress = (count, speed, time) => {
    uploaded_percentage.value = count;
    current_speed.value = speed;
    remaining_time.value = time;
};

//封面图像引用
let choose_video_cover_file = ref(null);
let video_url = ref(null);
let video= ref(null);

const upload_btn = () => {
    upload_file.value.click();
};

const choose_default_cover = () => {
    upload_cover_file.value.click();
};

// 获取封面
const change_file = async (e) => {
    video_file.value = e.target.files[0];
    video_filename.value = video_file.value.name;
    set_video(e);
    // 获取封面图
    video_cover_list.value = await get_video_cover(video_file.value);
    choose_video_cover.value = video_cover_list.value[0]; // 选择默认第一个封面
};

//设置视频
const set_video = (e) => {
    video.value = e.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(video.value);
    reader.onload = function () {
        video_url.value = reader.result;
    };
}

// 选择封面
const select_cover = (cover,index) => {
    choose_video_cover.value = cover;
    choose_video_cover_index.value = index;
};

// 上传自定义封面
const upload_custom_cover = (e) => {
    let file = e.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        choose_video_cover.value = reader.result;
    };
};

// 添加标签
const add_tag = () => {
    if (new_tag.value.trim() !== '' && !video_tags.value.includes(new_tag.value)) {
        video_tags.value.push(new_tag.value.trim());
        new_tag.value = '';
    }
};

// 删除标签
const remove_tag = (index) => {
    video_tags.value.splice(index, 1);
};

// 获取图像字节流
const getImgByte = async (imgUrl) => {
    const response = await fetch(imgUrl);
    const blob = await response.blob();
    
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = img.width; // 保持原始宽度
            canvas.height = img.height; // 保持原始高度

            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, img.width, img.height);
            
            // 导出为高质量 Blob
            canvas.toBlob((blob) => {
                resolve(blob);
            }, 'image/jpeg', 1.0); // 1.0 为最高质量
        };
        img.onerror = reject;
        img.src = URL.createObjectURL(blob);
    });
};
//获取视频字节流
const get_video_bytes=async (url)=>{
    const response = await fetch(url);
    const blob = await response.blob();
    return blob;
}

// 提交视频
const submit_video = async () => {
    const video_data = {
        title: video_title.value,
        tags: video_tags.value,
        description: video_description.value,
        cover: choose_video_cover.value,
        video_file: video_file.value,
    };
    //获取封面
    let cover_file = await getImgByte(choose_video_cover.value); // 获取封面图像字节流
    if(!cover_file &&video_file.value!=null){
        alert('请选择封面图像')
    }
    //转换为blod类型
    cover_file = new Blob([cover_file], { type: 'image/jpeg' });

    //获取视频
    let video_bytes = await get_video_bytes(video_url.value); // 获取视频字节流
    if (!video_bytes && video_file.value!=null){
        alert('请选择视频文件')
    }

    video_bytes = new Blob([video_bytes], { type: 'video/mp4' });

    video_file.value = video_bytes;
    if (cover_file){
        console.log('封面图像字节流：', cover_file);
        let res=await upload_video(video_file.value,cover_file,video_data,handleUploadProgress);
        console.log('上传视频结果：', res);
    }else{
        console.warn('获取封面图像字节流失败');
    }
  
    // 模拟提交
    console.log('提交视频数据：', video_data);
};

// 暂停上传
const pause_upload = () => {
    // 暂停上传逻辑
};

// 重新上传
const retry_upload = () => {
    // 重新上传逻辑
};
</script>

<style scoped>
.icon{
    width: 25px;
    height: 25px;
    object-fit: cover;
}
.upload_box{
    display: flex;
    flex-direction: column;
    gap:20px;
}
.content{
    display: flex;
    flex-direction: column;
    gap:20px;
}
.upload_btn{
    width:200px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60px;
    border-radius: 10px;
}
.upload_btn span{
    font-size: 18px;
    font-weight: bold;
    background-color: rgba(0,150,250,1);
    color: white;
    transition: all 0.2s ease-in-out;
    padding: 10px;
    border-radius: 10px;
}
.upload_btn span:hover{
    cursor: pointer;
    transform: scale(1.05);
    transform: translateY(-1px);
    opacity: 0.8;
}
.progress_box{
    display: flex;
    align-items: center;
    
}
.upload_info{
    width: 100%;
    display: flex;
    gap:20px;
    flex-direction: column;
}
.video_cover{
    display: flex;
    gap:20px;
    align-items: center;
    justify-content:flex-start;
}
.cover_box{
    flex: 1;
    display: flex;
    gap:20px;
    align-items: center;
}
.upload_cover{
    display: flex;
    position: absolute;
    left: 0;
    top: 0;
    opacity: 0;
    justify-content: center;
    align-items: center;
    z-index: 2;
    width: 100%;
    height: 100%;
}
.upload_cover:hover{
    cursor: pointer;
    opacity: 1;
    background-color: rgba(0,0,0,0.3);
    color: white;
}
.cover_default{
    width: calc(100% * 0.35);
    height: 150px;
    display: flex;
    position: relative;
    align-items: center;
    justify-content: center;
    padding: 5px 0px;
    border-radius: 15px;
    overflow: hidden;
}
.cover_default img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: flex;
    max-height: 150px;
    max-width: 300px;
}
.cover_item{
    flex: 1;
    display: flex;
    width: calc( ( 100% - (100% * 0.35) ) / 4);
    max-height: 125px;
}
.cover_mask{
    display: flex;
   cursor: pointer;
   position: relative;
}
.cover_mask:hover{
    background-color: rgba(0,0,0,0.3);
}
.cover_mask img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    max-width: 250px;
    max-height: 125px;
}
.choose_cover{
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top:0;
    display: flex;
    opacity: 1;
    transition: all 0.2s ease-in-out;
}
.choose_cover img{
    position: absolute;
    bottom: 5px ;
    right: 5px;
    width: 25px;
    height: 25px;
    object-fit: cover;
    background-color: rgba(255,255,255,0.5);
    border-radius: 50%;
}
.video_title{
    display: flex;
    gap:20px;
}
.video_title input{
    flex: 1;
    padding: 3px;
    background-color: wihte;
    border-radius: 5px;
    border: 1px solid rgba(133,133,133,1);
    font-size: 18px;
}
.video_tags{
    display: flex;
    gap:20px;
}
.tag_box{
    display: flex;
    gap:10px;
    flex-wrap: wrap;
    background-color: rgba(255,255,255,1);
    border-radius: 10px;
    padding: 5px;
    width: 90%;
    height: auto;
    min-height: 20px;
}
.tag_box span{
    padding: 3px 8px;
    background-color: rgba(26, 145, 243, 0.5);
    border-radius: 5px;
    display: flex;
    gap:5px;
    align-items: center;
}
.tag_box button{
    padding: 2px;
    font-size: 14px;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background-color: rgba(255,255,255,1);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}
.tag_box button:hover{
    background-color: rgba(233,233,233,1);
}
.tag_input{
    display: flex;
    gap:10px;
    align-items: center;
}
.tag_input input{
    padding: 3px;
    background-color: wihte;
    border-radius: 5px;
    border: 1px solid rgba(133,133,133,1);
    font-size: 18px;
}
.tag_input span{
    padding: 5px 10px;
    background-color: rgba(0,150,250,1);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    color: white;
}
.tag_input span:hover{
    background-color: rgba(0,150,250,0.8);
}
.video_introduce{
    display: flex;
    gap:10px;
    width: 100%;
}
.video_introduce textarea{
    flex:1;
    min-height: 30px;
    padding: 5px;
    width: 100%;
    border-radius: 5px;
    /*允许竖向高度调整*/
    resize: vertical;
}
.submit_btn{
    display: flex;
    margin: auto;
    margin-top: 20px;
}
.submit_btn span{
    padding: 10px 20px;
    background-color: rgba(0,150,250,1);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    color: white;
}
.submit_btn span:hover{
    background-color: rgba(0,150,250,0.8);
    transform: scale(1.05);
    transform: translateY(-2px);
}
</style>