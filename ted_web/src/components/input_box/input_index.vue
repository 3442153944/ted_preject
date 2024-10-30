<template>
    <div class="input_index">
        <div class="content">
            <div class="title_box">
                <textarea placeholder="请输入标题" v-model="title"></textarea>
            </div>
            <div ref="input_box" class="input_box" contenteditable="true"></div>
            <div class="input_img_box" ref="input_img_box" v-if="img_file_list.length > 0 || status_index == 1">
                <div class="img_list">
                    <div class="img_item" v-for="(item, index) in img_file_list" :key="index">
                        <img :src="item.url" alt="图像">
                        <div class="delete_img" @click="pop_img_file(index)">
                            <img class="icon" src="http://localhost:8000/static/svg/退出.svg" alt="删除">
                        </div>
                    </div>
                </div>
                <div class="add_img" @click="add_img_input_click()">
                    <img src="http://localhost:8000/static/svg/新增.svg" class="icon">
                    <input type="file" ref="add_img_input" accept="image/*" @change="push_img_file($event)"
                        style="display: none;pointer-events:none;">
                </div>
            </div>
            <div class="interaction_box">
                <div class="item_list">
                    <div class="item">
                        <div class="img" :class="{ choose_status: status_index == 0 }">
                            <img class="icon" :src="ip + 'emoji/张嘴闭眼笑.svg'" @click="set_status_index(0)">
                        </div>
                        <emoji_box v-if="status_index == 0" class="item_sub_box" @emoji="add_content_emoji($event)">
                        </emoji_box>
                    </div>
                    <div class="item">
                        <div class="img" :class="{ choose_status: status_index == 1|| img_file_list.length > 0 }">
                            <img class="icon" :src="ip + 'svg/图像.svg'" @click="set_status_index(1)">
                        </div>
                    </div>
                </div>
                <div class="send_btn" @click="add_dynamic_1() ">
                    <span>发布</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import emoji_box from './emoji_box/emoji_box.vue';
import add_dynamic from './js/add_dynamic';
import { useStore } from 'vuex';

const store = useStore();

let ip = 'http://localhost:8000/static/';
let input_box = ref(null);
let status_index = ref(-1);
let input_img_box = ref(null);
let title = ref('');

//图像文件列表
let img_file_list = ref([]);
let back_img_file_list=[]

// 切换状态索引
function set_status_index(index) {
    status_index.value = (status_index.value === index) ? -1 : index;
}

//模拟点击
function add_img_input_click() {
    input_img_box.value.querySelector('input').click();
}

// 向栈中压入解析为Base64的图像文件
function push_img_file(event) {
    const file = event.target.files[0];
    back_img_file_list.push(file)
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            img_file_list.value.push({ url: e.target.result });
        };
        reader.readAsDataURL(file); // 将文件转换为Data URL
    }
}
//从栈中弹出指定索引图像文件
function pop_img_file(index) {
    img_file_list.value.splice(index, 1);
}

// 新增动态HTML内容中的标签
function add_content_emoji(emoji) {
    if (input_box.value) {
        // 创建 img 元素并设置属性
        const img = document.createElement('img');
        img.src = `${ip}emoji/${emoji}`;
        img.className = 'emoji'; // 应用 class
        img.style.width = '16px';
        img.style.height = '16px';
        img.style.objectFit = 'cover';
        img.style.display = 'inline-block';
        img.alt= emoji;

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

//新增动态
async function add_dynamic_1() {
    console.log('新增动态');
    //获取input_box中的完整原始HTML
    let html = input_box.value.innerHTML;
    console.log(html);
    let result=await add_dynamic(back_img_file_list,title.value,html)
    console.log(result);
    if(result.status==200){
        store.commit('set_global_msg','新增动态消息成功')
    }
    else{
        store.commit('set_global_msg','新增动态消息失败，请稍后重试',data.msg)
    }
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
    gap: 2px;
    /*行间距*/
    line-height: 1.3;
    padding: 5px;
    border: 1px solid rgba(133, 133, 133, 1);
    border-radius: 5px;
    flex-wrap: wrap;
    text-wrap: wrap;
    max-width: calc(100% - 10px);
}

.input_img_box {
    display: flex;
    width: 100%;
    gap: 10px;
    flex-wrap: wrap;
    max-width: calc(100% - 10px);
    align-items: center;
}

.img_list {
    width: auto;
    height: auto;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.img_item {
    width: 100px;
    height: 100px;
    display: flex;
    background-color: rgba(133, 133, 133, 0.5);
    position: relative;
    border-radius: 10px;
}

.img_item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.delete_img {
    position: absolute;
    display: flex;
    width: 20px;
    height: 20px;
    align-items: center;
    justify-content: center;
    background-color: rgba(133, 133, 133, 0.5);
    top: -2px;
    right: -2px;
    border-radius: 50%;
    cursor: pointer;
}

.delete_img:hover {
    opacity: 0.8;
    background-color: rgba(0, 150, 250, 0.5);
    transition: all 0.3s ease-in-out;
}

.delete_img img {
    width: 15px;
    height: 15px;
    object-fit: cover;
}

.add_img {
    width: 60px;
    height: 60px;
    display: flex;
    background-color: rgb(207, 207, 207);
    border-radius: 10px;
    cursor: pointer;
}

.add_img:hover {
    opacity: 0.8;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
    transform: scale(1.05);
}

.add_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.choose_status {
    background-color: rgba(0, 150, 250, 0.5);
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
    max-width: calc(100% - 20px);
    transition: all 0.3s;
}

.content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.title_box{
    width: 100%;
    display: flex;
    max-width: calc(100% - 10px);
    margin-bottom: 10px;
}
.title_box textarea{
    width: 100%;
    height: auto;
    border:1px solid rgba(233,233,233,1);
    border-radius: 10px;
    padding: 5px;
    resize: vertical;
    min-height: 28px;
    font-size: 18px;
    font-weight: bold;
}
.interaction_box {
    width: 100%;
    height: 60px;
    display: flex;
    gap: 10px;
    position: relative;
    justify-content: space-between;
}

.item_list {
    display: flex;
    gap: 10px;
}

.item {
    width: 60px;
    height: 60px;
    display: flex;
    position: relative;
}

.img {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 50%;
}

.img img {
    width: 27.5px;
    height: 27.5px;
    object-fit: cover;
    margin: auto;
}

.item_sub_box {
    position: absolute;
    top: 80px;
}
.send_btn{
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 10px;
    color: white;
    background-color: rgba(0, 150, 250, 1);
    display: flex;
    justify-content: center;
    align-items: center;
    max-height: 26px;
    max-width: 46px;
    font-size: 18px;
    font-weight: 500;
    transition: all 0.3s ease-in-out;
}
.send_btn:hover{
    opacity: 0.8;
    transform: scale(1.02);
    transform: translateY(-2px);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
}
</style>