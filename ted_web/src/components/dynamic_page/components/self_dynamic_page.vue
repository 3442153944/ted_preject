<template>
    <div class="self_dynamic_page">
        <div class="content" ref="content">
            <h3>我的动态</h3>
            <div class="item_list">
                <div class="item" v-for="(item, index) in self_dynamic_list.slice(0, max_len)" :key="index">
                    <div class="title">
                        <span>{{ item.title }}</span>
                    </div>
                    <div class="item_content" v-html="format_content_to_html(item.content)"></div>
                    <div class="item_imgs" v-if="item.img_list">
                        <div class="item_img" v-for="(item, index) in item.img_list.split(/[,]/)" 
                         :key="index">
                            <img :src="'http://localhost:8000/static/img/img/' + item" alt="图像" @click="preview_img(item)">
                        </div>
                    </div>
                </div>
                <div class="show_more" @click="show_more">
                    <span>查看更多</span>
                </div>
            </div>
        </div>
        <preview_box :img_path="img_src" v-if="preview_box_show" @close_page="preview_box_show = false"></preview_box>
    </div>
</template>

<script setup>
import { ref, defineProps,watch,defineEmits } from 'vue'
import preview_box from './preview_box.vue';

let ip = "http://localhost:8000/static/"
const props = defineProps({
    self_dynamic_list: {
        type: [Array, Object],
        default: () => { }
    }
})

const emit = defineEmits(['show_more'])

function show_more() {
    max_len.value += 2
    emit('show_more')
}

let img_src = ref('')
let preview_box_show = ref(false)
let content= ref(null)
let max_len=ref(2)

function preview_img(path) {
    preview_box_show.value = true
    img_src.value = path
}

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
.self_dynamic_page {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, 1);
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    padding: 5px;
    margin-bottom: 20px;
}

.content {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    max-width: calc(100% - 10px);
}

.item_list {
    width: 100%;
    height: auto;
    display: flex;
    gap: 10px;
    flex-direction: column;
}

.item {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
    /*字间距*/
    letter-spacing: 1.3px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(133, 133, 133, 0.8);
}

.title {
    font-size: 18px;
    font-weight: bold;
}

.item_content {
    font-size: 16px;
    font-weight: 500;
    color: #333;
    line-height: 1.5;
    letter-spacing: 1.3px;
    word-break: break-all;
    word-wrap: break-word;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 3px;
}

.item_imgs {
    width: 100%;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}
.item_img{
    display: flex;
    flex-wrap: wrap;
}

.item_imgs img {
    max-width: 400px;
    max-height: 400px;
    width: auto;
    height: auto;
    object-fit: cover;
    border-radius: 10px;
    background-color: rgba(0,150,250,0.2);
    cursor: zoom-in;
}
.show_more{
    font-size: 18px;
    color: rgba(133, 133, 133, 1);
    cursor: pointer;
    display: inline-block;
    width: 75px;
    text-align: center;
    height: 20px;
}
.show_more:hover{
    /*下划线*/
    text-decoration: underline;
}
</style>