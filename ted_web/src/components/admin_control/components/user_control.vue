<template>
    <div class="user_control">
        <div class="content">
            <div>用户管理</div>
            <div class="search_box">
                <input type="text" placeholder="请输入用户名/id" v-model="search">
                <span class="edit hover" @click="performSearch">搜索</span>
            </div>
            <div class="item_list" v-if="user_list.length > 0">
                <div class="item" v-for="(item, index) in user_list" :key="index">
                    <div class="user_box">
                        <div class="avatar">
                            <img :src="'http://localhost:8000/static/img/thumbnail/' +
                                (item.avatar_path ? item.avatar_path : 'default_avatar') + '.png'" alt="头像">
                        </div>
                        <div class="info_box">
                            <div class="username">用户名：{{ item.username }}</div>
                            <div class="introduce">个人简介： {{ item.introduce || '这个人很懒，什么都没写' }}</div>
                            <div class="user_tags">用户标签：{{ item.user_tags || '无个人标签' }}</div>
                            <div class="sex">性别：{{ item.sex || '未知' }}</div>
                            <div class="self_website">个人网站：{{ item.self_website || '无个人网站' }}</div>
                            <div class="self_website_introduce">个人网站简介：{{ item.self_website_introduce || '无个人网站简介' }}
                            </div>
                            <div class="date_joined">注册时间：{{ item.date_joined || '未知' }}</div>
                            <div class="email">邮箱：{{ item.email || '无邮箱' }}</div>
                            <div class="btn_box">
                                <span class="edit hover" @click="set_edit_user_info_show(item)">编辑</span>
                                <span class="delete hover">删除用户</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <edit_user_info v-if="edit_user_info_show" @close_page="close_edit_user_info_show"
            :user_info="choose_user_info"></edit_user_info>
        <div class="check_point" ref="check_point"></div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import get_user_list from '../ts/get_user_list';
import edit_user_info from './edit_user_info.vue';
import searchUser from '../ts/search_user';

// 搜索框
let search = ref('');

// 用户信息列表
let user_list = ref([]);
let edit_user_info_show = ref(false);
let choose_user_info = ref(null);

// 分页控制
let limit = ref(10);
let offset = ref(0);
let total = ref(0);
let isSearching = ref(false); // 用于区分是否正在搜索
let check_point = ref(null);

// 设置观察者
const observe = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting && !isSearching.value) {
        if (offset.value < total.value) {
            offset.value += limit.value;
            let res = await get_user_list(limit.value, offset.value);
            if (res.status === 200) {
                user_list.value = user_list.value.concat(res.data);
            }
        }
    }
});

// 执行搜索
async function performSearch() {
    if (search.value.trim() !== '') {
        offset.value = 0; // 重置偏移量
        isSearching.value = true; // 设置为搜索状态
        let res = await searchUser(search.value, limit.value, offset.value);
        if (res && res.status === 200) {
            total.value = res.total;
            user_list.value = res.data;
        }
    } else {
        resetUserList(); // 搜索为空时重置列表
    }
}

// 重置用户列表
async function resetUserList() {
    offset.value = 0;
    isSearching.value = false;
    let res = await get_user_list(limit.value, offset.value);
    if (res && res.status === 200) {
        total.value = res.total;
        user_list.value = res.data;
    }
}

// 监听搜索框输入
watch(search, async (newSearch) => {
    if (newSearch.trim() === '') {
        await resetUserList();
    }
});

function set_edit_user_info_show(item) {
    edit_user_info_show.value = true;
    choose_user_info.value = item;
}

function close_edit_user_info_show() {
    edit_user_info_show.value = false;
}

// 组件挂载和卸载时的操作
onMounted(async () => {
    await resetUserList();
    observe.observe(check_point.value);
});

onUnmounted(() => {
    //observe.unobserve(check_point.value);
    observe.disconnect();
});
</script>

<style scoped>
.user_control {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
}

.content {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}
.search_box{
    display: flex;
    gap:10px;
}
.item_list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    border-top: 1px solid rgba(133, 133, 133, 1);
    padding-top: 5px;
}

.item {
    width: 100%;
    display: flex;
    gap: 10px;
    border-bottom: 1px solid rgba(133, 133, 133, 1);
    padding: 5px 0;
}

.user_box {
    display: flex;
    gap: 10px;
}

.avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: flex;
}

.avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

.info_box {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.btn_box {
    display: flex;
    gap: 10px;
}

.edit {
    padding: 10px 17.5px;
    background-color: rgba(0, 150, 250, 1);
    cursor: pointer;
    border-radius: 5px;
    color: white;
    font-size: 18px;
    font-weight: 600;
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