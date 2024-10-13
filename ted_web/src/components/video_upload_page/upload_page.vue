<template>
  <div class="upload_page">
    <div class="content">
        <div class="title">
            <span>投稿视频</span>
        </div>
        <upload_box></upload_box>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import upload_box from './upload_box.vue'

</script>

<style scoped>
.upload_page{
    width: 90%;
    height: 100%;
    display: flex;
    margin: auto;
    gap:20px;
    margin-top: 20px;
    background-color: rgba(233,233,233,0.5);
    padding: 10px;
    border-radius: 10px;
}
.content{
    display: flex;
    flex-direction: column;
    gap:10px;

}
.title{
    font-size: 20px;
    font-weight: bold;
    color: #333;
}
</style>