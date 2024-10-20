<template>
    <div class="base_info_box">
        <div class="content">
            <h2>个人信息</h2>
            <div class="item" v-for="(value, key) in fields" :key="key" >
                <span>{{ keyLabels[key] }}：</span>
                <template v-if="key === 'sex'">
                    <section>
                        <input type="radio" name="sex" value="男" v-model="base_info_local.sex">男
                        <input type="radio" name="sex" value="女" v-model="base_info_local.sex">女
                    </section>
                </template>
                <template v-else-if="key === 'birthday'">
                    <input type="date" v-model="base_info_local.birthday">
                </template>
                <template v-else-if="[ 'date_joined'].includes(key)">
                    <span>{{ formatDate(base_info_local[key])}}</span>
                </template>
                <template v-else-if="key=='id'">
                    <span>{{ base_info_local[key] }}</span>
                </template>
                <template v-else>
                    <input_box v-model="base_info_local[key]"></input_box>
                </template>
            </div>
            <div class="btn_box">
                <div class="btn" @click="saveChanges">
                    <span>保存</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, reactive } from 'vue';
import input_box from './input_box.vue';
import edit_base_userinfo from './js/edit_base_userinfo';

//格式化加入时间
const formatDate = (isoString) => {
    const parsedDate = new Date(isoString);
    const year = parsedDate.getFullYear();
    const month = String(parsedDate.getMonth() + 1).padStart(2, '0');
    const day = String(parsedDate.getDate()).padStart(2, '0');
    const hours = String(parsedDate.getHours()).padStart(2, '0');
    const minutes = String(parsedDate.getMinutes()).padStart(2, '0');
    const seconds = String(parsedDate.getSeconds()).padStart(2, '0');
    
    return `${year}年${month}月${day}日 ${hours}:${minutes}:${seconds}`;
};


const props = defineProps({
    base_info: {
        type: Object,
        default: () => ({})
    }
});

const emit = defineEmits(['update:base_info']);

// 本地克隆 base_info 避免直接修改
let base_info_local = ref({ ...props.base_info });

// 字段列表
const fields = {
    username: '',
    id: '',
    email: '',
    date_joined: '',
    sex: '',
    birthday: '',
    introduce: '',
    self_website: '',
    self_website_introduce: '',
    user_tags: ''
};

// 字段的中文标签
const keyLabels = {
    username: '用户名',
    id: 'ID',
    email: '邮箱',
    date_joined: '加入时间',
    sex: '性别',
    birthday: '生日',
    introduce: '个人简介',
    self_website: '个人网站',
    self_website_introduce: '个人网站简介',
    user_tags: '个人标签'
};

// 触发保存并 emit 数据
const saveChanges = async () => {
    console.log(base_info_local.value);
    let res=await edit_base_userinfo(base_info_local.value.username, base_info_local.value.email, 
    base_info_local.value.sex, base_info_local.value.birthday, base_info_local.value.introduce, 
    base_info_local.value.self_website, base_info_local.value.self_website_introduce, 
    base_info_local.value.user_tags);
    console.log(res);
};
</script>

<style scoped>
.base_info_box {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    max-width: 800px;
    margin: 0 auto;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

h2 {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
}

.item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #ddd;
}

.item span {
    width: 150px;
    font-weight: bold;
}

input[type="date"] {
    padding: 5px;
}

section {
    display: flex;
    gap: 10px;
}

.btn_box {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.btn {
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #45a049;
}
</style>