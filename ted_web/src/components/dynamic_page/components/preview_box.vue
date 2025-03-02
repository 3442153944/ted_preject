<template>
  <div class="preview_box">
    <div class="content" @click="close_page">
        <img :src="'http://localhost:8000/static/img/img/'+img_path">
    </div>
  </div>
</template>

<script setup>
import { ref ,defineProps,defineEmits} from 'vue'

const props = defineProps({
    img_path: String
})

const emit=defineEmits(['close_page'])

function close_page(){
    emit('close_page')
}

</script>

<style scoped>
.preview_box {
    width: 100vw;
    height: 100vh;
    position: fixed;
    top:0;
    left:0;
    background-color: rgba(0,0,0,0.6);
    display: flex;
    z-index: 100;
    max-width: 100vw;
    max-height: 100vh;
}
.content{
    width: 100%;
    height: 100%;
    cursor: zoom-out;
    display: flex;
    align-items: center;
    justify-content: center;
}
.content img{
    width: auto;
    height: auto;
    object-fit: cover;
    max-width: 100%;
    max-height: 100%;
}
</style>