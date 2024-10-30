<template>
  <div class="dynamic_index">
    <div class="content">
        <input_index></input_index>
        <self_dynamic_page :self_dynamic_list="dynamic.data.self_dynamic_list" v-if="dynamic"></self_dynamic_page>
        <other_dynamic_page :other_dynamic_list="dynamic.data.follow_user_dynamic_list" v-if="dynamic"></other_dynamic_page>
        <div class="check_point" style="display: none;opacity: 0;width:1px;height:1px;" ref="check_point"></div>
    </div>
  </div>
</template>

<script setup>
import {ref,onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {useStore} from 'vuex'
import input_index from '../input_box/input_index.vue';
import get_dynamic from './js/get_dynamic';
import self_dynamic_page from './components/self_dynamic_page.vue';
import other_dynamic_page from './components/other_dynamic_page.vue';

const router = useRouter()
const store = useStore()
let check_point=ref(null)

let observer=new IntersectionObserver((entries)=>{
    if(entries[0].isIntersecting){
        offset.value+=limit.value

    }
})

let dynamic=ref()
let limit=ref(10)
let offset=ref(0)

onMounted(async ()=>{
    dynamic.value=await get_dynamic(null,'self',limit.value,offset.value)
    console.log(dynamic.value)
})

</script>

<style scoped>
.dynamic_index{
    width: 100vw;
    height: auto;
    min-height: calc(100vh - 100px);
    display: flex;
    flex-direction: column;
    gap:10px;
    background-image: url('http://localhost:8000/static/img/img/104107025_p2.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
}
.content{
    width: 85%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap:10px;
    margin:0px auto;
    margin-top: 20px;
}
</style>