<template>
  <div class="other_user_center">
    <div class="content">
        <background :user_info="user_info"></background>
    </div>
  </div>
</template>

<script setup>
import {ref,defineProps,computed,watch,onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {useStore} from 'vuex'
import background from './components/background.vue';
import get_all_user_info from './js/get_all_userinfo';

const router = useRouter()
const store = useStore()

const props=defineProps({
    user_id:{
        type:[Number,String],
        default:''
    }
})

let user_id=computed(()=>store.getters.other_user_id)

watch(user_id,async (newVal)=>{
    console.log('newVal',newVal)
    await get_user_info()
})

let user_info = ref({})

async function get_user_info(){
    let result=await get_all_user_info(user_id.value)
    user_info.value=result
    console.log('user_info',user_info.value)
}

onMounted(async function (){
    await get_user_info()
})

</script>

<style scoped>
  
</style>