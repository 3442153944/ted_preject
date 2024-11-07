<template>
  <div class="comment_control">
    <div class="content">
      <div>评论管理</div>
      <div class="search_box">
        <input
          type="text"
          placeholder="评论ID/视频ID/用户ID"
          v-model="search_type"
        />
      </div>
      <div class="comment_list" v-if="comment_list.length > 0">
        <div class="comment_item" v-for="(item, index) in comment_list" :key="index">
          <div class="comment_info">
            <div class="info_item">
              <span>评论ID：{{item.comm_id}}</span>
            </div>
            <div class="info_item">
              <span>视频ID：{{item.comm_to_video_id}}</span>
            </div>
            <div class="info_item">
              <span>发送者ID：{{item.user_id}}</span>
            </div>
            <div class="info_item">
              <span>发送者用户名：{{item.username}}</span>
            </div>
            <div class="info_item">
              <span>发送时间：{{item.comm_send_time}}</span>
            </div>
            <div class="info_item">
              <span>评论内容：{{item.comment_content}}</span>
            </div>
          </div>
          <div class="delete hover">
            <span @click="del_comment(item.comm_id)">删除该评论</span>
          </div>
        </div>
      </div>
    </div>
    <div class="check_point" ref="check_point"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import get_comment_list from '../ts/get_comment_list'
import search_comment from '../ts/search_comment'
import delete_comment from '../ts/delete_comment'

// 搜索参数和分页控制
const search_type = ref('')
const search_limit = ref(10)
const search_offset = ref(0)
const search_total = ref(0)
const isSearching = ref(false)

// 评论列表和分页参数
const limit = ref(10)
const offset = ref(0)
const total = ref(0)
const comment_list = ref([])

// 滚动加载观察点
const check_point = ref(null)

// 获取普通评论列表
async function get_com_list() {
  const res = await get_comment_list(limit.value, offset.value)
  if (res.status === 200) {
    total.value = res.total
    comment_list.value = comment_list.value.concat(res.data)
  }
}

// 获取搜索结果
async function search_com() {
  const res = await search_comment(search_type.value, search_limit.value, search_offset.value)
  if (res.status === 200) {
    search_total.value = res.total
    comment_list.value = comment_list.value.concat(res.data)
  }
}

// 加载更多评论（区分搜索和普通模式）
async function load_more_comments() {
  if (isSearching.value) {
    search_offset.value += search_limit.value
    await search_com()
  } else {
    offset.value += limit.value
    await get_com_list()
  }
}

// 删除评论
async function del_comment(id) {
  alert('确定删除该评论吗？')
  const res = await delete_comment(id)
  if (res.status === 200) {
    comment_list.value = comment_list.value.filter(item => item.comm_id !== id)
  } else {
    console.log(res.msg)
  }
}

// 监听输入框变化，触发搜索
watch(search_type, async (newValue) => {
  isSearching.value = !!newValue
  search_offset.value = 0
  offset.value = 0
  comment_list.value = []
  if (isSearching.value) {
    await search_com()
  } else {
    await get_com_list()
  }
})

// 滚动观察器，用于加载更多数据
const observer = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting) {
    await load_more_comments()
  }
}, {
  root: null,
  rootMargin: '200px',
  threshold: 0
})

onMounted(async () => {
  await get_com_list()
  if (check_point.value) {
    observer.observe(check_point.value)
  }
})

onUnmounted(() => {
  observer.disconnect()
})
</script>


<style scoped>
.comment_control {
  font-family: Arial, sans-serif;
  padding: 20px;
  width: 85vw;
  margin: 0 auto;
}

.content {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background-color: #f9f9f9;
}

.search_box input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.comment_list {
  margin-top: 10px;
}

.comment_item {
  background: #fff;
  padding: 15px;
  border: 1px solid #e1e1e1;
  border-radius: 6px;
  margin-bottom: 10px;
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
}

.comment_info {
  margin-bottom: 10px;
}

.info_item {
  font-size: 14px;
  color: #333;
  margin: 5px 0;
}

.delete_btn {
  text-align: right;
}

.delete_btn span {
  cursor: pointer;
  color: #d9534f;
  font-weight: bold;
  transition: color 0.3s ease;
}

.delete_btn span:hover {
  color: #c9302c;
}

.check_point {
  width: 1px;
  height: 1px;
  display: block;
  opacity: 0;
  margin-top: 20px;
}
.delete {
  padding: 10px 17.5px;
  background-color: rgb(247, 23, 23);
  cursor: pointer;
  border-radius: 5px;
  color: white;
  font-size: 18px;
  font-weight: 600;
  width: 100px;
  align-items: center;
  display: flex;
  justify-content: center;
}

.hover:hover {
  transition: all 0.3s;
  opacity: 0.8;
  transform: scale(1.05);
  transform: translateY(-2px);
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.4);
}
</style>