<template>
    <div class="edit_avatar_box">
        <div class="content">
            <h2>修改头像</h2>
            <div class="item">
                <div class="background">
                    <!-- 背景图片，覆盖毛玻璃效果 -->
                    <div class="background_image" ref="background"></div>
                    <!-- 头像部分，放置在背景的正中间 -->
                    <div class="avatar" @mouseenter="showButton" @mouseleave="hideButton">
                        <img :src="avatarSrc" alt="头像" ref="avatar" />
                        <div class="edit_box" v-show="showEditButton">
                            <span @click="click_avatar">选择头像</span>
                        </div>
                    </div>
                    <!-- 文件选择器 -->
                    <input type="file" name="avatar" id="avatar" accept="image/png, image/jpeg, image/jpg"
                        ref="choose_avatar" style="display: none;" @change="reload_avatar($event)" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps,onMounted } from 'vue';
import edit_user_avatar from './js/edit_avatar';

const props = defineProps({
    base_info: {
        type: Object,
        default: () => {
            return {}
        }
    }
});

// 默认头像路径
let avatarSrc = ref(`http://localhost:8000/static/img/img/${props.base_info.avatar_path}.png`);
let background = ref(null);
let avatar = ref(null);
let choose_avatar = ref(null);
let showEditButton = ref(false); // 控制选择头像按钮的显示

// 显示头像选择按钮
const showButton = () => {
    showEditButton.value = true;
};

// 隐藏头像选择按钮
const hideButton = () => {
    showEditButton.value = false;
};

// 点击选择头像
const click_avatar = () => {
    choose_avatar.value.click();
};

// 预览并上传头像
const reload_avatar = async (event) => {
    let file = event.target.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        background.value.style.backgroundImage = `url(${this.result})`;
        avatarSrc.value = this.result;
    };

    // 上传头像到后端
    let res = await edit_user_avatar(file);
    if (res.status == 200) {
        alert('修改成功');
    } else {
        alert(res.msg);
    }
};

//加载时设置背景图像
onMounted(() => {
    background.value.style.backgroundImage = `url(${avatarSrc.value})`;
});
</script>

<style scoped>
.edit_avatar_box {
display: flex;
flex-direction: column;
}

.content {
    
}

.item {
    position: relative;
    display: inline-block;
}

.background {
    min-width: 360px;
    min-height: 180px;
    width: 800px;
    height: 400px;
    position: relative;
    border-radius: 10px;
    overflow: hidden;
}

.background_image {
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position: center;
    filter: blur(3px);
    opacity: 0.98;
}

.avatar {
    position: absolute;
    bottom: 0px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 4px solid rgba(0,150,250,0.5);
    background-color: white;
    overflow: hidden;
    transition: all 0.3s ease;
}

.avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.edit_box {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.avatar:hover .edit_box {
    opacity: 1;
}

.edit_box span {
    cursor: pointer;
    font-size: 14px;
}

.icon {
    width: 25px;
    height: 25px;
    object-fit: cover;
}
</style>