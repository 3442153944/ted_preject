<template>
  <div class="dynamic_index">
    <div class="content">
        <h2>动态</h2>
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
  
</style>