<template>
  <div class="video_control">
    <div class="content">
      <div>视频管理</div>
      <div class="search_box">
        <span>搜索视频</span>
        <input
          type="text"
          placeholder="请输入视频标题/id/用户名/用户ID"
          v-model="search_type"
        />
      </div>
      <div class="video_list" v-if="video_list.length > 0">
        <div class="item" v-for="(item, index) in video_list" :key="index">
          <div class="video_item">
            <div class="video_box">
              <video
                :src="'http://localhost:8000/static/video/' + item.video_file_path"
                :poster="'http://localhost:8000/static/img/img/' + item.video_cover_path"
                preload="auto"
                muted="true"
                controls
              ></video>
            </div>
            <div class="video_info">
              <div class="info_item">
                <span>视频标题：{{ item.video_title }}</span>
              </div>
              <div class="info_item">
                <span>视频作者：{{ item.username }}</span>
              </div>
              <div class="info_item">
                <span>视频介绍：{{ item.video_introduce }}</span>
              </div>
              <div class="info_item">
                <span>视频投稿时间：{{ item.create_time }}</span>
              </div>
              <div class="info_item">
                <span>视频标签：{{ item.video_tags }}</span>
              </div>
              <div class="info_item">
                <span>播放量：{{ item.watch_count }} 喜欢：{{ item.like_count }} 收藏：{{ item.collect_count }}</span>
              </div>
              <div class="btn_box">
                <span class="delete hover" @click="del_video(item.video_id)">删除</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="check_point" ref="check_point"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import get_video_list from '../ts/get_video_list'
import delete_video from '../ts/delete_video'
import search_video from '../ts/search_video'

// 搜索参数
const search_type = ref('')
const search_limit = ref(10)
const search_offset = ref(0)
const search_total = ref(0)

// 视频列表
const video_list = ref([])

// 滚动加载分页参数
const limit = ref(10)
const offset = ref(0)
const total = ref(0)

// 搜索模式标识
let isSearching = ref(false)

// 获取搜索结果
async function get_search_result() {
  const res = await search_video(search_type.value, search_limit.value, search_offset.value)
  if (res.status === 200) {
    search_total.value = res.total
    video_list.value = res.data
  }
}

// 获取普通视频列表
async function get_initial_videos() {
  const res = await get_video_list(limit.value, offset.value)
  if (res.status === 200) {
    total.value = res.total
    video_list.value = res.data
  }
}

// 加载更多视频（普通或搜索模式）
async function load_more_videos() {
  if (isSearching.value) {
    search_offset.value += search_limit.value
    const res = await search_video(search_type.value, search_limit.value, search_offset.value)
    if (res.status === 200) {
      video_list.value = video_list.value.concat(res.data)
    }
  } else {
    offset.value += limit.value
    const res = await get_video_list(limit.value, offset.value)
    if (res.status === 200) {
      video_list.value = video_list.value.concat(res.data)
    }
  }
}

// 删除视频
async function del_video(id) {
  if (confirm('确定删除该视频吗？')) {
    const res = await delete_video(id)
    if (res.status === 200) {
      video_list.value = video_list.value.filter(item => item.video_id !== id)
      console.log('删除成功')
    }
  }
}

// 监听输入变化并触发搜索
watch(search_type, async (newValue) => {
  isSearching.value = !!newValue
  search_offset.value = 0
  offset.value = 0
  if (isSearching.value) {
    await get_search_result()
  } else {
    await get_initial_videos()
  }
})

// 滚动观察器
const check_point = ref(null)
const observer = new IntersectionObserver(async (entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      await load_more_videos()
    }
  }
}, {
  root: null,
  rootMargin: '200px',
  threshold: 0
})

onMounted(async () => {
  await get_initial_videos()
  observer.observe(check_point.value)
})

onUnmounted(() => {
  observer.disconnect()
})
</script>


<style scoped>
.video_control{
  width: 85vw;
  display: flex;
  flex-direction: column;
  margin: auto;
}
.content{
  width: 100%;
  height: auto;
  display: flex;
  flex-direction: column;
}
.search_box{
  width: fit-content;
  display: flex;
  align-items: center;
  gap:10px;
  margin-top: 10px;
  margin-bottom: 10px;
}
.video_list{
  width: 100%;
  height: auto;
  display: flex;
  gap:10px;
  flex-direction: column;
}
.check_point{
  width: 1px;
  height: 1px;
  display: block;
  opacity: 0;
}
.item{
  width: 100%;
  height: 350px;
  min-width: 500px;
  display: flex;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(133,133,133,1);
}
.video_item{
  display: flex;
  flex-direction: row;
  gap:10px;
}
.video_box{
  width:100%;
  height: 100%;
  max-width: 500px;
  max-height: 350px;
  display: flex;
  position: relative;
}
.video_box video{
  width: auto;
  height: auto;
  max-width: 500px;
  max-height: 350px;
  object-fit: cover;
}
.video_info{
  width: fit-content;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  gap:5px;
}
.user_info{
  width: 100%;
  height: 50px;
  display: flex;
  gap:10px;
  align-items: center;
}
.avatar{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
}
.avatar img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.delete {
  padding: 10px 17.5px;
  background-color: rgb(247, 23, 23);
  cursor: pointer;
  border-radius: 5px;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.hover:hover {
  transition: all 0.3s;
  opacity: 0.8;
  transform: scale(1.05);
  transform: translateY(-2px);
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.4);
}
</style>