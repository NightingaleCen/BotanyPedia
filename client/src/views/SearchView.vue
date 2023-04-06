<template>
    <BackButton />
    <SearchUploader @submit=submitImage />
    <var-popup v-model:show="showPopup">
        <Loading v-if="isLoading" />
        <SearchResult v-if="isDisplayingResult" v-bind="test" />
    </var-popup>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import BackButton from '../components/BackButton.vue';
import SearchUploader from '../components/SearchUploader.vue'
import Loading from '../components/Loading.vue'
import SearchResult from '../components/SearchResult.vue';

const showPopup = ref(false)
const isLoading = ref(false)
const isDisplayingResult = ref(false)

const test = {
    imageLink: '../src/assets/logo.jpeg',
    canonicalName: 'CanonicalName',
    chineseName: '中文名'
}



function submitImage(file) {
    showPopup.value = true
    isDisplayingResult.value = false
    isLoading.value = true

    const formData = new FormData()
    formData.append('file', file.file);
    axios.post("http://localhost:8080/uploadImage", formData, {
        headers: { "Content-Type": "multipart/form-data" }
    }).then((response) => {
        isLoading.value = false
        isDisplayingResult.value = true
    })
}

</script>
