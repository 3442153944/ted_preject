<template>
  <div class="index_video_list">
    <div class="content">
        <h2>我的视频</h2>
        <div class="video_list">
            <div class="video_item" v-for="(item,index) in video_list" :key="index">
                <div class="item">
                    <div class="video_cover" @click="to_content_page(item.id)">
                        <video 
                        :src="'http://localhost:8000/static/video/'+item.video_file_path"
                        :poster="'http://localhost:8000/static/img/img/'+item.video_cover_path"></video>
                    </div>
                    <div class="video_info">
                        <div class="title">
                            <span>{{item.title}}</span>
                        </div>
                        <div class="play_info">
                            <span>
                                <img class="icon" src="http://localhost:8000/static/svg/播放.svg">
                                {{item.watch_count}}
                            </span>
                            <span style="font-size: 14px;">{{format_time(item.create_time)}}</span>
                        </div>
                        <div class="edit_box">
                            <span v-if="delete_btn_index==index" @click="delete_video(item.id)"
                            style="background-color: red;cursor: pointer;color:white;padding:0px 10px;
                            border-radius:5px;">
                                删除该视频</span>
                            <div class="more_btn" @click="set_del_btn_index(index)">
                                <img class="icon" src="http://localhost:8000/static/svg/展开.svg" 
                                :style="delete_btn_index==index?'transform:rotate(0deg)':''">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref ,defineProps,computed} from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import update_video_status from "../js/update_video_status";

const store = useStore();
const router = useRouter();

const props = defineProps({
    video_list: Array
})

let video_list = ref([]);

//时间格式化去掉时分秒
let format_time=(tiem)=>{
    let time = new Date(tiem);
    return time.toLocaleDateString();
}

//视频跳转
function to_content_page(id){
    router.push('/content_page')
    store.commit('set_video_id',id)
}

//展开指定位置删除按钮
let delete_btn_index=ref(-1)
function set_del_btn_index(index){
    delete_btn_index.value=(delete_btn_index.value==index?-1:index)
}

//删除指定视频
async function delete_video(id){
    alert('确认删除该视频吗？')
    let res=await update_video_status(id)
    if(res.status==200){
        video_list.value=video_list.value.filter(item=>item.id!=id)
        store.commit('set_global_msg',"删除视频成功")
    }
    else{
        store.commit('set_global_msg',res.msg)
    }
}

onMounted(()=>{
    video_list.value=props.video_list
})

</script>

<style scoped>
.icon{
    width:15px;
    height: 15px;
    object-fit: cover;
}
.video_list{
    display: flex;
    flex-wrap: wrap;
    gap:20px;
}
.video_item{
    width:calc(100% / 5 - 20px) ;
    display: flex;
    flex-direction: column;
}
.item{
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.video_cover{
    max-width:calc(100vw / 5 - 20px);
    max-height: 200px;
    width: auto;
    height: auto;
    display: flex;
    overflow: hidden;
}
.item video{
    width: 100%;
    height: auto;
    object-fit: cover;
    cursor: pointer;
    /**/
    max-height: 100px;
}
.video_info{
    display: flex;
    gap: 10px;
    flex-direction: column;
}
.play_info{
    display: flex;
    gap:10px;
    font-size: 14px;
    align-items: center;
    justify-content: space-between;
}
.play_info span{
    display: flex;
    align-items: center;
    gap:5px;
}
.edit_box{
    display: flex;
    position: relative;
    justify-content: flex-end;
    width: 100%;
    align-items: center;
    gap: 10px;
}
.more_btn{
    width: 30px;
    height: 25px;
    display: flex;
    justify-content: center;
    cursor: pointer;
    align-items: center;
    transition: all 0.3s;
}
.more_btn:hover{
    background-color: #525252;
    border-radius: 5px;
}
.more_btn img{
    /*旋转180°*/
    transform: rotate(180deg);
    transition: all 0.3s;
}
.edit_box span{
    transition: all 0.3s;
}
</style>