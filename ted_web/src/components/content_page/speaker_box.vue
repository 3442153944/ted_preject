<template>
    <div class="speaker_box">
        <div class="content" v-if="user_info_1">
            <div class="title">
                <span>关于演讲者</span>
            </div>
            <div class="speaker_info">
                <div class="info_box">
                    <div class="avatar">
                        <img :src="'http://localhost:8000/static/img/thumbnail/' + user_info_1.avatar_path + '.png'">
                    </div>
                    <div class="speaker_name" >
                        <span style="font-size: 18px;font-weight:bold;cursor: pointer;"
                            @click="to_other_user_center(user_info_1.author_id)">{{ user_info_1.username }}</span>
                        <span style="font-size: 12px;color:rgb(133,133,133)">{{ user_info_1.user_tags }}</span>
                    </div>
                    <div class="follow_btn" :class="user_info_1.is_follow ? 'is_follow' : 'not_follow'" 
                    @click="update_follow()">
                        <span>{{ user_info_1.is_follow ? '已关注' : '关注' }}</span>
                    </div>
                </div>
                <div class="speaker_intruduction">
                    <span>{{ user_info_1.introduce }}</span>
                </div>
            </div>
            <div class="speaker_self_website_list">
                <div class="website_box">
                    <div class="website_intruduction">
                        <span>{{ user_info_1.self_website_introduce }}</span>
                    </div>
                    <div class="go_website">
                        <a :href="user_info_1.self_website" target="_blank">
                            <span>学习/了解&nbsp;→</span>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import update_follow_status from './js/update_follow_status';

const store = useStore();
const router = useRouter();

let props = defineProps({
    user_info: Object
});
let user_info_1 = ref({}); // 初始化为一个空对象

// 监听 props.user_info 的变化
watch(() => props.user_info, (newVal) => {
    user_info_1.value = newVal; // 更新 user_info_1
}, { immediate: true }); // immediate 确保在组件挂载时也会执行一次

// 其他用户的用户中心跳转
const to_other_user_center = (id) => {
    router.push('/other_user_center');
    store.commit('set_other_user_id', id);
}

// 更新关注状态
async function update_follow() {
    const action = user_info_1.value.is_follow ? 'cancel' : 'add';
    const res = await update_follow_status(user_info_1.value.author_id, action);
    console.log(res);

    if (res.status === 200) {
        user_info_1.value.is_follow = !user_info_1.value.is_follow; // 切换关注状态
    }

    store.commit('set_global_msg', res.msg);
}

onMounted(() => {
    console.log(user_info_1.value);
});
</script>


<style scoped>
.speaker_box {
    display: flex;
    flex-direction: column;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.title {
    font-size: 24px;
    font-weight: 700;
    border-bottom: 1px solid rgb(133, 133, 133);
}

.speaker_info {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.info_box {
    gap: 10px;
    display: flex;
    align-items: center;
    position: relative;
}

.follow_btn {
    position: absolute;
    right: 10px;
    margin-top: auto;
    margin-left: auto;
    padding: 5px 20px;
    border-radius: 10px;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}

.follow_btn:hover {
    opacity: 0.8;
    transform: scale(1.05);
    transform: translateY(-2px);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.4);
}

.is_follow {
    background-color: rgb(133, 133, 133);
}

.not_follow {
    background-color: rgba(0, 150, 250, 1);
}

.avatar {
    width: 50px;
    height: 50px;
    display: flex;
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

.speaker_name {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.speaker_intruduction {
    border-top: 1px solid rgb(133, 133, 133);
    display: flex;
    align-items: center;
}

.speaker_self_website_list {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    border-top: 1px solid rgb(133, 133, 133);
}

.website_box {
    margin-top: 10px;
    width: 90%;
    padding: 20px;
    display: flex;
    position: relative;
    background-color: rgba(133, 133, 133, 0.5);
    border-radius: 10px;
    justify-content: space-between;
}

.website_intruduction {
    width: 80%;
    display: flex;
    align-items: center;
}

.go_website {
    width: calc(100% - 80% - 10px);
    display: flex;
    padding: 5px 15px;
    background-color: red;
    color: white;
    border-radius: 10px;
    justify-content: center;
    align-items: center;
    align-self: flex-end;
    font-size: 18px;
    font-weight: 700;
}

.go_website a {
    text-decoration: none;
    color: white;
}
</style>