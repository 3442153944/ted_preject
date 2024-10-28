<template>
  <div class="collect_works">
    <div class="content">
        <h2>收藏的作品</h2>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore()
const router = useRouter()

</script>

<style scoped>
  
</style>