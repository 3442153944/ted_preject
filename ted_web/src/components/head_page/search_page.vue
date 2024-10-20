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
                            <img :src="'http://localhost:8000/static/img/img/'+item.video_cover_path" alt="视频封面" />
                            <div class="video_info">
                                <h3>{{ item.video_title }}</h3>
                                <p>作者: {{ item.author }}</p>
                                <p>观看次数: {{ item.watch_count }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="showUserResults" class="result user_result">
                    <div class="user_item" v-for="(item, index) in user_data" :key="index">
                        <div class="user_card">
                            <img :src="'http://localhost:8000/static/img/thumbnail/'+
                            (item.avatar_path?item.avatar_path:'227708771630839632276')+'.png'" alt="用户头像" />
                            <div class="user_info">
                                <h3>{{ item.username }}</h3>
                                <p>{{ item.introduce }}</p>
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
import { ref, defineProps, watch } from 'vue';
import search from './search';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

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

watch(() => props.search_key, async (newVal) => {
    if (newVal) {
        result.value = await search(newVal);
        video_data.value = result.value.video_data;
        user_data.value = result.value.user_data;
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
};
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

.video_item,
.user_item {
    margin: 10px 0;
}

.video_card,
.user_card {
    display: flex;
    align-items: center;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    transition: box-shadow 0.3s;
}

.video_card:hover,
.user_card:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

.video_info,
.user_info {
    margin-left: 10px;
}

.video_info h3,
.user_info h3 {
    margin: 0;
}
</style>