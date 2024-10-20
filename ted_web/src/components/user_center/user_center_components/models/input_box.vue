<template>
    <div class="input_box">
        <div class="content" @mouseenter="showIcon = true" @mouseleave="showIcon = false">
            <div class="item" 
                 ref="item" 
                 :contenteditable="isEditable" 
                 @focus="isEditable = true" 
                 @blur="isEditable = false" 
                 @input="updateValue"
                 :class="{'item_use_status':isEditable}"
                 >
                 {{ modelValue }}
            </div>
            <img :src="'http://localhost:8000/static/svg/编辑.svg'" 
                 class="icon" 
                 v-if="showIcon" 
                 @click="enableEditing">
        </div>
    </div>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps, nextTick } from 'vue'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
    modelValue: {
        type: [String, Number],
        default: ''
    }
})

const item = ref(null)
const isEditable = ref(false)
const showIcon = ref(false)

// 点击编辑图标，激活编辑功能并将光标移动到最后
const enableEditing = () => {
    isEditable.value = true;
    if(item.value.innerText=='空'){
        item.value.innerText = '';
    }

    // 在 DOM 更新后聚焦到元素并移动光标到最后
    nextTick(() => {
        item.value.focus();
        moveCursorToEnd();
    });
}

// 将光标移动到内容的末尾
const moveCursorToEnd = () => {
    let element = item.value;
    let range = document.createRange();
    let selection = window.getSelection();
    range.selectNodeContents(element);
    range.collapse(false);  // 移动光标到内容的末尾
    selection.removeAllRanges();
    selection.addRange(range);
}

// 实时更新 modelValue
const updateValue = () => {
    const content = item.value.innerText.trim();

    // 如果是占位符 "空"，先删除
    if (content == '空') {
        item.value.innerText = '';
    }

    // 更新 modelValue
    emit('update:modelValue', item.value.innerText.trim());
}

watch(() => props.modelValue, (newValue) => {
    // 如果内容为空且 DOM 中的内容也为空，才设置默认值
    if (!newValue && !item.value.innerText.trim()) {
        nextTick(() => {
            isEditable.value = true;
            item.value.innerText = '空';  // 设置默认值
            isEditable.value = false;
        });
    } else if (newValue !== item.value.innerText) {
        // 避免不必要的重置
        item.value.innerText = newValue;
    }
});
</script>

<style scoped>
.icon {
    width: 20px;
    height: 20px;
    object-fit: cover;
    align-self: flex-end;
    bottom: 5px;
    right: 5px;
    cursor: pointer;
}

.input_box {
    display: flex;
    position: relative;
}

.content {
    width: 100%;
    height: 100%;
    display: flex;
    gap: 5px;
    position: relative;
}

.item {
    min-height: 10px;
    min-width: 10px;
    padding: 5px;
    border-radius: 5px;
}
.item_use_status{
    background-color: rgba(255,255,255,1);
}
</style>
