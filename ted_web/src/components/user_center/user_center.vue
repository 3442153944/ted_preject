<template>
  <div class="user_center" v-if="user_info">
    <div class="content">
        <background :user_info="user_info" v-if="background_ready"></background>
        <switch_page :user_info="user_info" v-if="background_ready" @switch_page="set_switch_page"></switch_page>
        <div class="index" v-if="page_item=='主页'">
          <index_item :user_info="user_info" v-if="background_ready"></index_item>
          <index_video_list :video_list="user_info.data.user_videos" v-if="background_ready"></index_video_list>
        </div>
        <div class="my_video" v-if="page_item=='投稿'">
          <my_video :video_list="user_info.data.user_videos" v-if="background_ready"></my_video>
        </div>
        <div class="collect" v-if="page_item=='收藏'">
          <collect_video  v-if="background_ready" :video_list="user_info.data.collected_videos"></collect_video>
        </div>
        <div class="user_info" v-if="page_item=='个人信息'">
          <user_info_1 v-if="background_ready" :user_info="user_info.data.user_info"></user_info_1>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref,onMounted ,watch} from 'vue'
import get_all_user_info from './js/get_user_info';
import background from './user_center_components/background.vue';
import switch_page from './user_center_components/switch_page.vue';
import index_item from './user_center_components/index_item.vue';
import index_video_list from './user_center_components/index_video_list.vue';
import my_video from './user_center_components/my_video.vue';
import collect_video from './user_center_components/collect_video.vue';
import user_info_1 from './user_center_components/user_info.vue';

const user_info = ref(null);
const background_ready = ref(false);

let page_item=ref('主页')

function set_switch_page(item){
  page_item.value=item
  console.log(page_item.value)
}

onMounted(async function(){
  user_info.value = await get_all_user_info();
  console.log(user_info.value);
  background_ready.value = true;
})

</script>

<style scoped>
.content{
  width:90%;
  display: flex;
  margin: auto;
  flex-direction: column;
  gap:10px;
}
  
</style>