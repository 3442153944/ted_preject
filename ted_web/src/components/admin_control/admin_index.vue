<template>
  <div class="admin_index">
    <div class="content">
        <div>管理面板</div>
    </div>
  </div>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import check_admin from './ts/check_admin';

onMounted(async function (){
    let res=await check_admin();
    if(!res){
        alert("您没有权限访问该页面");
        location.href="/";
    }
})

</script>

<style scoped>
  
</style>