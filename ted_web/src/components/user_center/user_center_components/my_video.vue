<template>
  <div class="my_video">
    <div class="content">
        <h2>我的视频</h2>
        <div class="video_list"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted ,defineProps} from "vue";

const props = defineProps({
    video_list: Array
})

</script>

<style scoped>
  
</style>