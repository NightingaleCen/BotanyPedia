<template>
    <BackButton class="back-button" />
    <SearchUploader @submit=submitImage />
    <var-popup v-model:show="showPopup">
        <Loading is-loading="isLoading" />
    </var-popup>
</template>

<script setup>
import { ref } from 'vue';
import BackButton from '../components/BackButton.vue';
import SearchUploader from '../components/SearchUploader.vue'
import Loading from '../components/Loading.vue'

const showPopup = ref(false)
const isLoading = ref(false)
const currentPopupPage = ref(null)


function submitImage(file) {
    showPopup.value = true
    isLoading = true
    console.log(file)
}

</script>

<style>
.back-button {
    position: absolute;
    top: 0;
    left: 0;
    padding: 15px;
}
</style>