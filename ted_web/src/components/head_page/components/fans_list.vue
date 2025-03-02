<template>
    <div class="follow_list">
        <div class="content" v-if="follow_list.length > 0">
            <h1>粉丝列表</h1>
            <div class="follow_list_item" v-for="(item, index) in follow_list" :key="index">
                <div class="avatar">
                    <img
                        :src="'http://localhost:8000/static/img/thumbnail/' + (item.avatar_path ? item.avatar_path + '.png' : 'default_avatar.png')">
                </div>
                <div class="username" @click="to_other_user_center(item.operation_user_id)">
                    <span>{{ item.username }}</span>
                </div>
            </div>
        </div>
        <div class="check_point" ref="check_point"
            style="display:block;width:1px;height:1px;opacity:0;pointer-events:none;"></div>
    </div>
</template>


<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore()
const router = useRouter()

// 其他用户的用户中心跳转
const to_other_user_center = (id) => {
    router.push('/other_user_center');
    store.commit('set_other_user_id', id);
}

const user = computed(() => store.getters.user)
const limit = ref(10)
const offset = ref(0)
console.log(user.value)
const follow_list = ref([])
const check_point = ref(null)
async function get_follow_list() {
    try {
        const res = await fetch('http://localhost:8000/api/user/GetFansList/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
            },
            body: JSON.stringify({
                user_id: user.value.id,
                limit: limit.value,
                offset: offset.value
            })
        })
        const data = await res.json()
        return data;
    }
    catch (err) {
        console.log(err)
    }
}

const observer = new IntersectionObserver(async function (entries) {
    if (entries[0].isIntersecting) {
        offset.value += limit.value
        let result = await get_follow_list()
        follow_list.value.append(result.data)
        //以ID去重
        follow_list.value = follow_list.value.filter(
            (item, index, arr) =>
                arr.findIndex((item2) => item2.id === item.id) === index
        )
    }
}, {
    rootMargin: '0px',
    threshold: 0
})

onMounted(async function () {
    let result = await get_follow_list()
    follow_list.value = result.data
    if (check_point) {
        observer.observe(check_point.value)
    }
})
onUnmounted(function () {
    observer.disconnect()
})

</script>

<style scoped>
.content {
    width: 90%;
    display: flex;
    margin: 10px auto;
    flex-direction: column;
    gap: 5px;
}

.follow_list_item {
    display: flex;
    flex-direction: row;
    gap: 10px;
    border-bottom: 1px solid rgba(133, 133, 133, 1);
    align-items: center;
}

.avatar {
    width: 30px;
    height: 30px;
    display: flex;
    min-width: 30px;
    min-height: 30px;
}

.avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

.username {
    display: flex;
    align-items: center;
    cursor: pointer;
    transition: all 0.2s;
}

.username:hover {
    opacity: 0.8;
    /*下划线*/
    text-decoration: underline;
    text-underline-offset: 2px;
    text-decoration-thickness: 1px;
}
</style>