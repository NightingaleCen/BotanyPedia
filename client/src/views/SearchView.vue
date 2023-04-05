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
    console.log(file)
    setTimeout(() => {
        isLoading.value = false
        isDisplayingResult.value = true
    }, 1000);


}

</script>
