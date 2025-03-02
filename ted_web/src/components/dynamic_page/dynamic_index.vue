<template>
    <div class="dynamic_index">
        <div class="content">
            <input_index></input_index>
            <self_dynamic_page :self_dynamic_list="dynamic.data.self_dynamic_list" v-if="dynamic" 
            @show_more="show_more()"></self_dynamic_page>
            <other_dynamic_page :other_dynamic_list="dynamic.data.follow_user_dynamic_list" v-if="dynamic">
            </other_dynamic_page>
            <div class="check_point" style="display: block;opacity: 0;width:1px;height:1px;" ref="check_point"></div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import input_index from '../input_box/input_index.vue';
import get_dynamic from './js/get_dynamic';
import self_dynamic_page from './components/self_dynamic_page.vue';
import other_dynamic_page from './components/other_dynamic_page.vue';

const router = useRouter()
const store = useStore()
let check_point = ref(null)

let observer = new IntersectionObserver(async (entries) => {
    if (entries[0].isIntersecting) {
        other_offset.value += other_limit.value
        let result = await get_dynamic(null, 'self', limit.value, offset.value, other_limit.value, other_offset.value)
        dynamic.value.data.follow_user_dynamic_list.push(...result.data.follow_user_dynamic_list)
    }
},
    {
        root: null,
        rootMargin: '200px',
        threshold: 1.0
    })

let dynamic = ref()
let limit = ref(2)
let offset = ref(0)
let other_limit = ref(2)
let other_offset = ref(0)

async function show_more() {
    offset.value += limit.value
    let result = await get_dynamic(null, 'self', limit.value, offset.value, other_limit.value, other_offset.value)
    dynamic.value.data.self_dynamic_list.push(...result.data.self_dynamic_list)
}

onMounted(async () => {
    dynamic.value = await get_dynamic(null, 'self', limit.value, offset.value, other_limit.value, other_offset.value)
    console.log(dynamic.value)
    if (check_point.value) {
        observer.observe(check_point.value)
    }
})

onUnmounted(() => {
    observer.disconnect()
})

</script>

<style scoped>
.dynamic_index {
    width: 100vw;
    height: auto;
    min-height: calc(100vh - 100px);
    display: flex;
    flex-direction: column;
    gap: 10px;
    background-image: url('http://localhost:8000/static/img/img/104107025_p2.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
}

.content {
    width: 85%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 0px auto;
    margin-top: 20px;
}
</style>