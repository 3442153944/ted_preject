<template>
    <div class="input_index">
        <div class="content">
            <div ref="input_box" class="input_box" contenteditable="true"></div>
            <div class="interaction_box">
                <div class="item_list">
                    <div class="item">
                        <div class="img" :class="{ choose_status: status_index == 0 }">
                            <img class="icon" :src="ip + 'emoji/张嘴闭眼笑.svg'" @click="set_status_index(0)">
                        </div>
                        <emoji_box v-if="status_index == 0" class="item_sub_box" @emoji="add_content_emoji($event)">
                        </emoji_box>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import emoji_box from './emoji_box/emoji_box.vue';

let ip = 'http://localhost:8000/static/';
let input_box = ref(null);
let status_index = ref(0);

// 切换状态索引
function set_status_index(index) {
    status_index.value = (status_index.value === index) ? -1 : index;
}

// 新增动态HTML内容中的标签
function add_content_emoji(emoji) {
  if (input_box.value) {
    // 创建 img 元素并设置属性
    const img = document.createElement('img');
    img.src = `${ip}emoji/${emoji}`;
    img.className = 'emoji'; // 应用 class
    img.style.width = '20px';
    img.style.height = '20px';
    img.style.objectFit = 'cover';

    // 插入 img 元素
    input_box.value.appendChild(img);

    // 光标移动到文本框末尾
    placeCaretAtEnd(input_box.value);
  }
}

// 将光标放到内容的末尾
function placeCaretAtEnd(el) {
    el.focus();
    const range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
}
</script>

<style scoped>
.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}

.emoji {
    width: 20px;
    height: 20px;
    object-fit: cover;
}
.input_box {
    font-size: 16px;
    width: calc(100% - 10px);
    height: auto;
    align-items: center;
    /*字间距*/
    letter-spacing: 1.5px;
    display: flex;
    gap:2px;
    /*行间距*/
    line-height: 1.3;
    padding: 5px;
    border:1px solid rgba(133,133,133,1);
    border-radius: 5px;
}
.choose_status {
    background-color: rgba(0, 150, 250, 1);
    transition: all 0.3s;
    transform: scale(1.05);
}

.input_index {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, 1);
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.5);
    max-width: calc(100vw - 40px);
    transition: all 0.3s;
}

.content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.interaction_box {
    width: 100%;
    height: 80px;
    display: flex;
    gap: 10px;
    position: relative;
}

.item {
    width: 60px;
    height: 60px;
    display: flex;
    position: relative;
}

.img {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 50%;
}

.img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.item_sub_box {
    position: absolute;
    top: 80px;
}
</style>