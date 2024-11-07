<template>
  <div class="dynamic_control">
    <div class="content">
      <div>动态管理</div>
      <div class="search_box">
        <input
          type="text"
          placeholder="动态ID/标题/发送者ID"
          v-model="search_type"
        />
      </div>
      <div class="dynamic_list" v-if="dynamic_list.length > 0">
        <div class="dynamic_item" v-for="(item, index) in dynamic_list" :key="index">
          <div class="dynamic_info">
            <div class="info_item">
              <span>动态ID：{{ item.id }}</span>
            </div>
            <div class="info_item">
              <span>标题：{{ item.title }}</span>
            </div>
            <div class="info_item">
              <span>内容：<div class="text_content" v-html="format_content_to_html(item.content)"></div></span>
            </div>
            <div class="info_item">
              <span>发送者ID：{{ item.send_user_id }}</span>
            </div>
            <div class="info_item">
              <span>发送时间：{{ item.send_time }}</span>
            </div>
            <div class="info_item">
              <span>状态：{{ item.dynamic_status }}</span>
            </div>
            <div class="info_item" v-if=" item.img_list">
              <div class="img_list">
                <div class="img_item" v-for="(img,img_index) in item.img_list.split(',')" :key="img_index">
                  <img :src="`${ip}img/img/${img}`" alt="图片">
                </div>
              </div>
            </div>
          </div>
          <div class="delete hover">
            <span @click="del_dynamic(item.id)">删除该动态</span>
          </div>
        </div>
      </div>
    </div>
    <div class="check_point" ref="check_point"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue';
import get_dynamic_list from '../ts/get_dynamic_list';
import search_dynamic from '../ts/search_dynamic';
import delete_dynamic from '../ts/delete_dynamic';

let ip = "http://localhost:8000/static/"

// 格式化 content 的内容为 HTML 内容
function format_content_to_html(content) {
    // 使用正则表达式替换 $包裹的内容为 <img> 标签
    return content.replace(/\$([^$]+)\$/g, (match, emoji) => {
        const emojiSrc = `${ip}emoji/${emoji}`;
        return `<img src="${emojiSrc}" alt="${emoji}" 
        style="width: 16px; height: 16px; object-fit: cover; display: inline-block;">`;
    });
}

// 搜索参数和分页控制
const search_type = ref('');
const search_limit = ref(10);
const search_offset = ref(0);
const search_total = ref(0);
const isSearching = ref(false);

// 动态列表和分页参数
const limit = ref(10);
const offset = ref(0);
const total = ref(0);
const dynamic_list = ref([]);

// 滚动加载观察点
const check_point = ref(null);

// 获取普通动态列表
async function get_dyn_list() {
  const res = await get_dynamic_list(limit.value, offset.value);
  if (res?.status === 200) {
    total.value = res.total;
    dynamic_list.value = dynamic_list.value.concat(res.data);
  }
}

// 获取搜索结果
async function search_dyn() {
  const res = await search_dynamic(search_type.value, search_limit.value, search_offset.value);
  if (res?.status === 200) {
    search_total.value = res.total;
    dynamic_list.value = dynamic_list.value.concat(res.data);
  }
}

// 加载更多动态（区分搜索和普通模式）
async function load_more_dynamics() {
  if (isSearching.value) {
    search_offset.value += search_limit.value;
    await search_dyn();
  } else {
    offset.value += limit.value;
    await get_dyn_list();
  }
}

// 删除动态
async function del_dynamic(id) {
  if (confirm('确定删除该动态吗？')) {
    const res = await delete_dynamic(id);
    if (res?.status === 200) {
      dynamic_list.value = dynamic_list.value.filter(item => item.id !== id);
    } else {
      console.error(res?.msg);
    }
  }
}

// 监听输入框变化，触发搜索
watch(search_type, async (newValue) => {
  isSearching.value = !!newValue;
  search_offset.value = 0;
  offset.value = 0;
  dynamic_list.value = [];
  if (isSearching.value) {
    await search_dyn();
  } else {
    await get_dyn_list();
  }
});

// 滚动观察器，用于加载更多数据
const observer = new IntersectionObserver(async (entries) => {
  if (entries[0].isIntersecting) {
    await load_more_dynamics();
  }
}, {
  root: null,
  rootMargin: '200px',
  threshold: 0,
});

onMounted(async () => {
  await get_dyn_list();
  if (check_point.value) {
    observer.observe(check_point.value);
  }
});

onUnmounted(() => {
  observer.disconnect();
});
</script>

<style scoped>
.dynamic_control {
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
  width: 90%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.dynamic_list {
  margin-top: 10px;
}

.dynamic_item {
  background: #fff;
  padding: 15px;
  border: 1px solid #e1e1e1;
  border-radius: 6px;
  margin-bottom: 10px;
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
}

.dynamic_info {
  margin-bottom: 10px;
}

.info_item {
  font-size: 14px;
  color: #333;
  margin: 5px 0;
}
.img_list{
  width: 100%;
  height: auto;
  display: flex;
  flex-wrap: wrap;
  gap:10px;
}
.img_item{
  width: 100px;
  height: 100px;
  border-radius: 5px;
  display: flex;
}
.img_item img{
  width: auto;
  height: auto;
  max-width: 100px;
  max-height: 100px;
  object-fit: cover;
  border-radius: 5px;
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
.text_content{
  display: flex;
  gap:5px;
  align-items: center;
  flex-wrap: wrap;
}
</style>
