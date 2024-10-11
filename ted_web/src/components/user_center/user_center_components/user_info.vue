<template>
  <div class="user_info">
    <div class="content">
        <h2>个人信息</h2>
        <div class="user_info_item">
          <div class="switch_menu">
            <div class="switch_menu_item" @click="change_page(0)" 
            :class="{'switch_menu_item_choose':page_index == 0}">基本信息</div>
            <div class="switch_menu_item" @click="change_page(1)" 
            :class="{'switch_menu_item_choose':page_index == 1}">修改密码</div>
            <div class="switch_menu_item" @click="change_page(2)"
            :class="{'switch_menu_item_choose':page_index == 2}">修改头像</div>
          </div>
          <div class="base_info_box" v-if="page_index == 0">
            <base_info_box :base_info="user_info"></base_info_box>
          </div>
          <div class="edit_password_box" v-if="page_index == 1">
            <edit_password_box></edit_password_box>
          </div>
          <div class="edit_avatar_box" v-if="page_index == 2">
            <edit_avatar_box :base_info="user_info"></edit_avatar_box>
          </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import {ref,watch,onMounted,defineEmits,defineProps} from 'vue'
import input_box from './models/input_box.vue';
import base_info_box from './models/base_info_box.vue';
import edit_password_box from './models/edit_password_box.vue';
import edit_avatar_box from './models/edit_avatar_box.vue';

const props = defineProps({
  user_info:{
    type:Object,
    default:()=>{}
  }
})

let page_index = ref(0)

//修改页面
const change_page = (index)=>{
  page_index.value = index
}


</script>

<style scoped>
.content{
  display: flex;
  flex-direction: column;
  gap:20px;
  margin-bottom: 20px;
}
.user_info_item{
  display: flex;
  gap:20px;
}
.switch_menu{
  display: flex;
  flex-direction: column;
  min-width: 150px;
  gap:10px;
  align-items: center;
  justify-content: center;
  border:1px solid #ccc;
  border-radius: 15px;
  padding: 20px 0px;
  max-height: 250px;
}
.switch_menu_item{
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  border-bottom: 1px solid #ccc;
  transition: all 0.2s ease-in-out;
  border-radius: 15px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 2px 3px 10px rgba(0, 150, 210, 0.3);
}
.switch_menu_item:hover{
  background-color: rgba(0,150,220,1);
  color: white;
  transform: scale(1.02);
  transform: translateY(-1px);
}
.switch_menu_item_choose{
  background-color: rgba(0,150,220,1);
  color: white;
  transform: scale(1.02);
  transform: translateY(-1px);
}
.base_info_box{
  flex:1;
}
.edit_password_box{
  flex:1;
}
.edit_avatar_box{
  flex:1;
}
</style>