<template>
    <div class="dynamic_page">
        <div class="content">
            <h1>动态</h1>
            <div class="dynamic_list" v-if="dynamic_list.length > 0">
                <div class="dynamic_item" v-for="(item, index) in dynamic_list" :key="index">
                    <div class="dynamic_title">
                        <span>{{ item.title }}</span>
                    </div>
                    <div class="dynamic_content" v-html="format_content_to_html(item.content)"></div>
                    <div class="dynamic_imgs" v-if="item.img_list">
                        <div class="dynamic_img" v-for="(item, index) in item.img_list.split(/[,]/)" :key="index">
                            <img :src="'http://localhost:8000/static/img/img/' + item" alt="图像">
                        </div>
                    </div>
                    <div class="send_time">
                        <span>{{item.send_time}}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref ,defineProps,onMounted} from 'vue'
let ip = "http://localhost:8000/static/"
const props = defineProps({
    dynamic_list: {
        type: Array,
        default: () => []
    }
})

// 视频时间格式化
const format_video_time = (time) => {
  let days = Math.floor(time / 86400); // 86400秒 = 1天
  let hours = Math.floor((time % 86400) / 3600); // 3600秒 = 1小时
  let minutes = Math.floor((time % 3600) / 60);
  let seconds = Math.floor(time % 60);

  if (days > 0) {
    return `${days}天 ${hours}:${minutes.toString().padStart(2, '0')}`;
  } else if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}`;
  } else {
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }
};

// 格式化 content 的内容为 HTML 内容
function format_content_to_html(content) {
  // 使用正则表达式替换 $包裹的内容为 <img> 标签
  return content.replace(/\$([^$]+)\$/g, (match, emoji) => {
    const emojiSrc = `${ip}emoji/${emoji}`;
    return `<img src="${emojiSrc}" alt="${emoji}" 
        style="width: 16px; height: 16px; object-fit: cover; display: inline-block;">`;
  });
}

</script>

<style scoped>
.dynamic_list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.dynamic_item {
    display: flex;
    flex-direction: column;
    border-bottom: 1px solid rgba(133, 133, 133, 1);
}

.dynamic_title {
    font-size: 20px;
    font-weight: bold;
}

.dynamic_content {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: center;
}

.dynamic_imgs {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: baseline;
}

.dynamic_img img {
    max-width: 100px;
    max-height: 100px;
    object-fit: cover;
    width: auto;
    height: auto;
}

.dynamic_btns {
    display: flex;
    align-items: center;
    padding: 10px 15px;
    width: fit-content;
    cursor: pointer;
    transition: all 0.2s;
    background-color: rgb(235, 116, 118);
    margin-bottom: 10px;
    border-radius: 8px;
    color: white;
    margin-top: 10px;
}

.dynamic_btns:hover {
    opacity: 0.8;
}
</style>