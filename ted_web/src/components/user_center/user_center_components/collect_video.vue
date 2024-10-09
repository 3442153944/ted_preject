<template>
  <div class="collect_video">
    <div class="content">
        <h2>我的收藏</h2>
        <div class="video_list">
            <div class="video_item"></div>
        </div>
    </div>
  </div>
</template>

<script setup>
import {ref,defineProps} from 'vue'

const props = defineProps({
    video_list:Array
})

</script>

<style scoped>
  
</style>