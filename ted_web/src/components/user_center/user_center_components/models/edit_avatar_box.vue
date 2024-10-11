<template>
  <div class="edit_avatar_box">
    <div class="content">
        <h2>修改头像</h2>
        <div class="item">
            <div class="avatar">
                <img :src="'http://localhost:8000/static/img/img/'+base_info.avatar_path+'.png'" alt="头像">
            </div>
            <div class="edit_box">
                <span>选择头像</span>
                <input type="file" name="avatar" id="avatar" accept="image/png, image/jpeg, image/jpg" style="display: none;">
                <img src="http://localhost:8000/static/svg/图像.svg" class="icon" alt="图像">
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted,defineProps } from 'vue'
import edit_user_avatar from './js/edit_avatar';

const props = defineProps({
    base_info: {
        type: Object,
        default: () => {
            return {}
        }
    }
})

</script>

<style scoped>
.icon{
    width: 25px;
    height: 25px;
    object-fit: cover;
}
</style>