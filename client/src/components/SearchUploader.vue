<template>
    <div class="uploader-area">
        <p class="uploader-text">请上传不超过10M的植物图片</p>
        <var-uploader class="uploader" v-model="files" @after-read="handleAfterRead" :maxlength="1" />
        <button @click="$emit('submit', files[0])" v-show="submitActive">
            <UpIcon class="btn" />
        </button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import UpIcon from './icons/IconUp.vue';

const files = ref([])
const submitActive = ref(false)

defineEmits(['submit'])

function handleAfterRead(file) {
    if (file.file.size <= 10 * 1024 * 1024) {
        submitActive.value = true
    } else {
        Snackbar.warning({ content: '文件大于10M', position: 'top' })
        submitActive.value = false
    }
}

</script>
<style>
.uploader-area {
    margin-top: 100px;
    text-align: center;
}

.uploader-text {
    margin-bottom: 20px;
    font-weight: bold;
}

.uploader {
    --uploader-file-size: 230px;
}

.uploader-area div div {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.btn {
    margin-top: 45px;
    width: 75px;
    height: auto;
}
</style>