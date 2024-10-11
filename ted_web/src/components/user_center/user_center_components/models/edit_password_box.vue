<template>
    <div class="edit_password_box">
        <div class="content">
            <h2>修改密码</h2>

            <!-- 旧密码输入框 -->
            <div class="item">
                <span>请输入旧密码：</span>
                <input placeholder="旧密码" type="password" v-model="his_password" />
                <div class="msg" v-if="errorMessages.his_password">
                    <span>{{ errorMessages.his_password }}</span>
                </div>
            </div>

            <!-- 新密码输入框 -->
            <div class="item">
                <span>请输入新密码：</span>
                <input placeholder="新密码" type="password" v-model="new_password" />
                <div class="msg" v-if="errorMessages.new_password">
                    <span>{{ errorMessages.new_password }}</span>
                </div>
            </div>

            <!-- 确认新密码输入框 -->
            <div class="item">
                <span>请确认新密码：</span>
                <input placeholder="确认新密码" type="password" v-model="confirm_password" />
                <div class="msg" v-if="errorMessages.confirm_password">
                    <span>{{ errorMessages.confirm_password }}</span>
                </div>
            </div>

            <!-- 确认按钮 -->
            <div class="btn" @click="validatePasswords">
                <span>确认</span>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import edit_password from './js/edit_password';

// 密码输入
const his_password = ref('')
const new_password = ref('')
const confirm_password = ref('')

// 错误消息对象
const errorMessages = ref({
    his_password: '',
    new_password: '',
    confirm_password: ''
})

// 验证密码长度和复杂性
const validatePassword = (password) => {
    if (password.length < 8) {
        return '密码长度不能少于8位';
    }

    // 至少包含两种字符类型（字母、数字、特殊字符）
    const hasLetter = /[A-Za-z]/.test(password)
    const hasNumber = /[0-9]/.test(password)
    const hasSpecial = /[^A-Za-z0-9]/.test(password)
    const charTypesCount = [hasLetter, hasNumber, hasSpecial].filter(Boolean).length

    if (charTypesCount < 2) {
        return '密码至少需要包含字母、数字或特殊字符中的两种';
    }

    return ''
}

// 验证输入的密码
const validatePasswords = async () => {
    errorMessages.value.his_password = his_password.value ? '' : '请输入旧密码'
    errorMessages.value.new_password = validatePassword(new_password.value)
    errorMessages.value.confirm_password =
        new_password.value !== confirm_password.value ? '两次输入的新密码不一致' : ''

    let res=await edit_password(his_password.value,new_password.value,confirm_password.value)
    if(res.status==200){
        alert('修改成功')
    }else{
        alert(res.msg)
    }
}
</script>

<style scoped>
.edit_password_box {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    max-width: 400px;
    margin: 0 auto;
}

.content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

h2 {
    text-align: center;
    font-size: 24px;
}

.item {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.item span {
    font-weight: bold;
}

input {
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

input:focus {
    outline: none;
    border-color: #4caf50;
}

.msg span {
    color: red;
    font-size: 14px;
}

.btn {
    background-color: #4caf50;
    color: white;
    text-align: center;
    padding: 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #45a049;
}
</style>