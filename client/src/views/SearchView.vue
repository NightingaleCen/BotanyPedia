<template>
    <BackButton />
    <SearchUploader @submit=submitImage />
    <var-popup v-model:show="showPopup">
        <Loading v-if="isLoading" />
        <SearchResult v-if="isDisplayingResult" :canonical-name="canonicalName" />
    </var-popup>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import qs from 'qs';
import BackButton from '../components/BackButton.vue';
import SearchUploader from '../components/SearchUploader.vue'
import Loading from '../components/Loading.vue'
import SearchResult from '../components/SearchResult.vue';

const showPopup = ref(false)
const isLoading = ref(false)
const isDisplayingResult = ref(false)

const canonicalName = ref("")



function submitImage(file) {
    showPopup.value = true
    isDisplayingResult.value = false
    isLoading.value = true

    const formData = new FormData()
    formData.append('file', file.file);
    axios.post("http://localhost:8080/uploadImage", formData, {
        headers: { "Content-Type": "multipart/form-data" }
    }).then((response) => {
        let candidates = response.data
        if (Object.keys(candidates).length === 1) {
            canonicalName.value = Object.keys(candidates)[0]
            isLoading.value = false
            isDisplayingResult.value = true
        } else {
            console.log(Object.keys(candidates))
            axios.get("http://localhost:8080//integrateInformation", {
                params: {
                    candidates: Object.keys(candidates),
                }, paramsSerializer: {
                    serialize: function (params) {
                        return qs.stringify(params, { arrayFormat: 'repeat' })
                    }
                },
            }).then(
                (response) => {
                    let candidates_attributes = response.data
                    console.log(candidates_attributes)
                }
            )
        }
    })
}

</script>
