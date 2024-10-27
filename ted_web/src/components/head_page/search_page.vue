<template>
    <div class="search_page">
        <div class="content">
            <h2>搜索</h2>
            <div class="title">
                <div class="title_item" :class="{ active: isActive('video') }" @click="toggleResult('video')">
                    <span>视频</span>
                </div>
                <div class="title_item" :class="{ active: isActive('user') }" @click="toggleResult('user')">
                    <span>用户</span>
                </div>
            </div>
            <div class="search_result">
                <div v-if="showVideoResults" class="result video_result">
                    <div class="video_item" v-for="(item, index) in video_data" :key="index">
                        <div class="video_card" @click="to_content(item.video_id)">
                            <div style="position: relative;">
                                <img :src="'http://localhost:8000/static/img/img/' +
                                    (item.video_cover_path ? item.video_cover_path : '102718099_p0.png')" alt="视频封面" />
                                <span class="watch_count">
                                    <img src="http://localhost:8000/static/svg/播放.svg" class="icon">
                                    {{ item.watch_count }}</span>
                            </div>
                            <div class="video_info">
                                <span>{{ item.video_title }}</span>

                            </div>
                            <div class="video_author">
                                <div class="author_avatar">
                                    <img :src="'http://localhost:8000/static/img/thumbnail/' +
                                        (item.avatar_path ? item.avatar_path : '227708771630839632276') + '.png'"
                                        alt="作者头像" />
                                </div>
                                <div class="author_info">
                                    <span>{{ item.author }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="showUserResults" class="result user_result">
                    <div class="user_item" v-for="(item, index) in user_data" :key="index">
                        <div class="user_card">
                            <div class="user_info">
                                <div class="user_avatar">
                                    <img :src="'http://localhost:8000/static/img/thumbnail/' +
                                    (item.avatar_path ? item.avatar_path : '227708771630839632276') + '.png'" alt="用户头像" />
                                </div>
                                <div class="user_name">
                                    <span style="cursor: pointer;">{{ item.username }}</span>
                                    <span>&nbsp;{{ item.introduce }}</span>
                                    <div class="user_follow" :class="item.is_follow?'is_follow':'not_follow'" 
                                    @click="follow_user(index,item.user_id)">
                                        <span>{{item.is_follow?'已关注':'关注'}}</span>
                                    </div>
                                </div>
                                
                            </div>
                            <div class="user_video_list" v-if="item.video_data.length">
                                <div class="video_list_item"  v-for="(item,index) in item.video_data" :key="index">
                                    <div class="v_list_item" v-if="index<3">
                                        <div class="video_cover" @click="to_content(item.id)">
                                            <img :src="'http://localhost:8000/static/img/img/'+
                                            (item.video_cover_path?item.video_cover_path:'102718099_p0.png')" alt="封面">
                                        </div>
                                        <span>{{item.title}}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="user_video_list" v-else>
                                <span>该用户暂无视频</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="search_tips" v-if="!video_data.length && !user_data.length">
                    <span>这里空空如也，尝试换个内容吧</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, watch, defineEmits } from 'vue';
import search from './search';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import update_follow_status from './update_follow_status';

let result = ref();
let video_data = ref([]);
let user_data = ref([]);
let showVideoResults = ref(true);
let showUserResults = ref(false);

const props = defineProps({
    search_key: {
        type: [String, Number],
        default: ''
    }
});

const emit = defineEmits(['close_page', 'clear'])

watch(() => props.search_key, async (newVal) => {
    if (newVal) {
        result.value = await search(newVal);
        video_data.value = result.value.video_data;
        user_data.value = result.value.user_data;
        console.log(user_data.value);
    }
});

const toggleResult = (type) => {
    if (type === 'video') {
        showVideoResults.value = true;
        showUserResults.value = false;
    } else {
        showVideoResults.value = false;
        showUserResults.value = true;
    }
};

const isActive = (type) => {
    return (type === 'video' && showVideoResults.value) || (type === 'user' && showUserResults.value);
};

// 内容页跳转
const router = useRouter();
const store = useStore();
const to_content = (id) => {
    router.push('/content_page');
    store.commit('set_video_id', id);
    emit('close_page');
    emit('clear');
};

const follow_user=async (index,id)=>{
    if(user_data.value[index].is_follow==0 || user_data.value[index].is_follow==null){
        user_data.value[index].is_follow=1;
        const result=await update_follow_status(id,'add');
        console.log(result)
    }
    else{
        user_data.value[index].is_follow=0;
        const result=await update_follow_status(id,'cancel');
        console.log(result)
    }
    console.log(id);
}
</script>

<style scoped>
.search_page {
    width: 100%;
    position: absolute;
    top: calc(100% + 5px);
    min-height: 100vh;
    display: flex;
    background-color: rgba(255, 255, 255, 1);
    z-index: 10;
    padding: 10px;
}

.title {
    display: flex;
    cursor: pointer;
    margin-bottom: 1em;
}

.title_item {
    margin-right: 20px;
    padding: 10px 15px;
    border: 1px solid transparent;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
}

.title_item.active {
    background-color: #007bff;
    color: white;
    border-color: #007bff;
}

.search_result {
    display: flex;
    flex-direction: column;
}

.video_item {
    margin: 10px;
    width: 400px;
    height: 400px;
    display: flex;
    flex-direction: column;
}

.user_item {
    width: calc(100% / 3 - 20px);
    height: 250px;
    display: flex;
    min-width: 350px;
    min-height: 250px;
}

.video_card {
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    transition: box-shadow 0.3s;
    flex-direction: column;
    cursor: pointer;
    width: 100%;
    height: 100%;
    position: relative;
}

.user_card {
    display: flex;
    align-items: flex-start;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    transition: box-shadow 0.3s;
    flex-direction: column;
    width: 100%;
    height: 100%;
    gap: 10px;
}
.user_info{
    display: flex;
    gap:10px;
    width: 100%;
    align-items: center;
    height: 100px;
    border-bottom: 1px solid rgba(0,0,0,0.3);
}
.user_avatar{
    width: 60px;
    height: 60px;
    display: flex;
    overflow: hidden;
    border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.3);
}
.user_avatar img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
.user_name{
    display: flex;
    flex-direction: column;
    gap:5px;
    text-wrap: nowrap;
    overflow: hidden;
}
.user_follow{
    width: 80px;
    height: auto;
    padding: 7.5px 15px;
    display: flex;
    border: 1px solid rgba(0,0,0,0.3);
    border-radius: 5px;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease-in-out;
}
.user_follow:hover{
    opacity: 0.8;
    cursor: pointer;
}
.is_follow{
    background-color: rgba(133,133,133,1);
    color: white;
}
.not_follow{
    background-color: rgba(0,150,250,1);
    color: white;
}

.video_card:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.user_card:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.video_card img {
    width: 400px;
    height: auto;
    max-height: 300px;
    min-height: 250px;
}

.video_info {
    display: flex;
    width: 100%;
    margin-top: 10px;
}



.video_result {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.video_author {
    height: 60px;
    display: flex;
    width: 100%;
    align-items: center;
    margin-top: 20px;
}

.video_author img {
    width: 55px;
    height: 55px;
    object-fit: cover;
    border-radius: 50%;
    min-height: 0;
}

.watch_count {
    position: absolute;
    bottom: 10px;
    left: 5px;
    background-color: rgba(141, 141, 141, 0.5);
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    display: flex;
    gap: 10px;
    align-items: center;
}

.watch_count img {
    width: 15px;
    height: 15px;
    object-fit: cover;
    min-height: 0;
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
}

.user_result {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.user_video_list{
    display: flex;
    gap:10px;
    height: calc(100% - 100px);
}
.video_list_item{
    width: calc(100% / 3 - 10px);
    display: flex;
}
.v_list_item{
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.video_cover{
    width: 100%;
    height: 100%;
    object-fit: cover;
    cursor: pointer;
    border-radius: 15px;
}
.video_cover img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 15px;
}
</style>