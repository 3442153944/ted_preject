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
    width:160px;
    height: 100px;
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
</style>