<template>
  <div class="dynamic_index">
    <div class="content">
        <input_index></input_index>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useStore} from 'vuex'
import input_index from '../input_box/input_index.vue';

const router = useRouter()
const store = useStore()

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