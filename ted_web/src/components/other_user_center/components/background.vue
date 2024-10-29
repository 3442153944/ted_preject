<template>
    <div class="background">
        <div class="content">
            <div class="background_img">
                <img src="http://localhost:8000/static/img/img/102718099_p0.png" alt="默认背景图">
            </div>
            <div class="user_info" v-if="user_info.data">
                <div class="user_box">
                    <div class="user_avatar">
                        <img :src="'http://localhost:8000/static/img/thumbnail/' +
                            (user_info.data.user_info.avatar_path ?
                                user_info.data.user_info.avatar_path : '227708771630839632276') + '.png'" alt="用户头像">
                    </div>
                    <div class="info_box">
                        <div class="user_name">
                            <span>{{ user_info.data.user_info.username }}</span>
                        </div>
                        <div class="user_introduce">
                            <span>{{ user_info.data.user_info.introduce }}</span>
                        </div>
                    </div>
                </div>
                <div class="follow_box" :class="is_follow==1?'is_follow':'no_follow'" @click="change_follow_status()">
                    <div class="follow_btn">
                        <span >{{ is_follow == 0 ? '关注' : '已关注' }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, onMounted } from 'vue'
import update_follow_status from '../js/update_follow_status';
import { useStore } from 'vuex'

const store = useStore()

const props = defineProps({
    user_info: {
        type: Object,
        default: () => ({ data: { user_info: {}, is_followed: 0 } })
    }
})

let user_info_back = ref({})
let is_follow = ref(0)
onMounted(() => {
    console.log(props.user_info)
    if (props.data) {
        user_info_back.value = props.data.user_info
        console.log(user_info_back.value)
        is_follow.value = props.user_info.data.is_followed
    }
})

//切换关注状态
const change_follow_status = async () => {
    let result
    if (is_follow.value == 0) {
        result=await update_follow_status(props.user_info.data.user_info.id, 'add')
        if(result.status==200)
    {
        is_follow.value=1
    }
        store.commit('set_global_msg',result.msg)
    }
    else{
        result=await update_follow_status(props.user_info.data.user_info.id, 'cancel')
        if(result.status==200)
    {
        is_follow.value=0
    }
        store.commit('set_global_msg',result.msg)
    }
    console.log(result)
}

</script>

<style scoped>
.background {
    width: 100vw;
    height: 50vh;
    display: flex;
}

.content {
    width: 100%;
    height: 100%;
    display: flex;
    position: relative;
    flex-direction: column;
}

.background_img {
    width: 100%;
    height: 100%;
}

.background_img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.user_info {
    display: flex;
    position: absolute;
    bottom: 0px;
    left: 0px;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.7);
    justify-content: space-between;
    padding: 5px;
}
.user_box{
    display: flex;
    gap: 10px;
    margin-left: 10px;
}
.user_avatar{
    width: 100px;
    height: 100px;
    display: flex;
    border-radius: 50%;
    overflow: hidden;
}
.user_avatar img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}
.info_box{
    display: flex;
    flex-direction: column;
    gap:10px;
}
.follow_box{
    display: flex;
    margin-right: 20px;
    padding: 8px 16px;
    border: 1px solid rgba(255, 255, 255, 0.7);
    width: 100px;
    height: 25px;
    align-items: center;
    justify-content: center;
    margin-top: auto;
    margin-bottom: auto;
    border-radius: 10px;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
    font-weight: bold;
}
.follow_box:hover{
    opacity: 0.8;
    box-shadow: 0px 0px 3px rgba(0,0,0,0.5);
    transform: scale(1.03);
}
.is_follow{
    color: white;
    background-color: rgba(133,133,133,1);
}
.no_follow{
    color: white;
    background-color: rgba(0,150,250,1);
}
</style>