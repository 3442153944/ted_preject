<template>
  <div class="collect_works">
    <div class="content">
        <h2>收藏的作品</h2>
        <div class="choose_short">
          <div class="short_fun">
              <span style="background-color: rgba(133,133,133,1);color:white;padding:5px 10px;border-radius:5px;">排序方式</span>
              <span style="cursor: pointer;" @click="sortBy('time')" >按时间排序</span>
              <span @click="sortBy('views')" style="cursor: pointer;">按播放量排序</span>
          </div>
          <div class="short_upload">
              <span style="background-color: rgba(133,133,133,1);color:white;padding:5px 10px;border-radius:5px;">排序顺序</span>
              <span @click="changeOrder('asc')" style="cursor: pointer;">升序排序</span>
              <span @click="changeOrder('desc')" style="cursor: pointer;">降序排序</span>
          </div>
      </div>
      <div class="submit_works_list">
          <div class="item" v-for="(item, index) in sortedVideos" :key="index">
              <video :src="'http://localhost:8000/static/video/' + item.video_file_path"
                  :poster="'http://localhost:8000/static/img/img/' + (item.video_cover_path ? item.video_cover_path : '102718099_p0.png')" 
                  @click="to_video_content(item.id)">
              </video>
              <div class="video_info">
                  <div class="video_title">
                      <span>{{ item.title }}</span>
                  </div>
                  <div class="play_info">
                      <div class="play_count">
                          <img src="http://localhost:8000/static/svg/播放.svg" alt="播放" class="icon">
                          <span>{{ item.watch_count }}</span>
                      </div>
                      <div class="time">
                          <img src="http://localhost:8000/static/svg/时间.svg" alt="时间" class="icon">
                          <span>{{ format_time(item.create_time) }}</span>
                      </div>
                  </div>
              </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()

const props = defineProps({
    user_info: {
        type: Object,
        default: () => { }
    }
})

// 排序状态
const sortKey = ref('time'); // 当前排序依据
const sortOrder = ref('asc'); // 当前排序顺序（升序或降序）

// 格式化时间
function format_time(time) {
    if (!time) return ''; // 处理空时间

    const date = new Date(time.replace(/-/g, '/'));
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const minute = String(date.getMinutes()).padStart(2, '0');

    return `${month}月${day}日 ${hour}时${minute}分`;
}

// 排序函数
const sortedVideos = computed(() => {
    const videos = [...props.user_info.data.collected_videos]; // 创建视频列表的副本
    if (sortKey.value === 'time') {
        videos.sort((a, b) => new Date(a.create_time) - new Date(b.create_time));
    } else if (sortKey.value === 'views') {
        videos.sort((a, b) => a.watch_count - b.watch_count);
    }
    
    if (sortOrder.value === 'desc') {
        videos.reverse(); // 如果是降序，反转数组
    }
    
    return videos;
});

// 改变排序依据
function sortBy(key) {
    if (sortKey.value === key) {
        // 如果点击的是同一排序依据，切换排序顺序
        sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
    } else {
        sortKey.value = key; // 更新排序依据
        sortOrder.value = 'asc'; // 默认升序
    }
}

// 改变排序顺序
function changeOrder(order) {
    sortOrder.value = order;
}

//视频内容页跳转
const to_video_content = (id) => {
    router.push('content_page')
    store.commit('set_video_id', id)
}

</script>

<style scoped>
.submit_works_list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 20px;
}
.choose_short{
    display: flex;
    gap:10px;
}
.choose_short span{
    padding: 5px 10px;
    background-color: rgba(0,150,250,1);
    color: white;
    border-radius: 5px;
    font-size: 16px;
    font-weight: bold;
}
.choose_short span:hover{
    opacity: 0.8;
    transition: all 0.2s ease-in-out;
    transform: scale(1.03);
    transform: translateY(-2px);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}
.short_fun{
    display: flex;
    gap:10px;
    align-items: center;
}
.short_upload{
    display: flex;
    gap:10px;
    align-items: center;
}
.item {
    width: calc(100% / 4 - 20px);
    display: flex;
    flex-direction: column;
    height: 200px;
    margin:10px 0px;
}

video {
    width: 100%;
    height: 100%;
    border-radius: 5px;
    background-color: black;
    cursor: pointer;
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.video_info {
    display: flex;
    flex-direction: column;
    gap:10px;
}
.play_info{
    display: flex;
    gap:10px;
    justify-content: space-between;
}
.play_count{
    display: flex;
    gap:5px;
}
.time{
    display: flex;
    align-items: center;
    gap:5px;
}
</style>
