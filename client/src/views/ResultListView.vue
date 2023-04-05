<template>
    <BackButton />
    <div class="item-list">
        <ResultItem v-for="(item, key) in testItems" :key="key" :canonical-name="key" :chinese-name="item.chineseName"
            :image-link="item.imageLink" />
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import BackButton from '../components/BackButton.vue';
import ResultItem from '../components/ResultItem.vue';

defineProps(["queryValue"])

const testItems = ref({})

onMounted(() => {
    testItems.value = {
        "canonical name1": {
            chineseName: "Chinese name1",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name2": {
            chineseName: "Chinese name2",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name3": {
            chineseName: "Chinese name3",
            imageLink: "../src/assets/logo.jpeg"
        }, "canonical name4": {
            chineseName: "Chinese name1",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name5": {
            chineseName: "Chinese name2",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name6": {
            chineseName: "Chinese name3",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name7": {
            chineseName: "Chinese name2",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name8": {
            chineseName: "Chinese name3",
            imageLink: "../src/assets/logo.jpeg"
        }, "canonical name9": {
            chineseName: "Chinese name1",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name10": {
            chineseName: "Chinese name2",
            imageLink: "../src/assets/logo.jpeg"
        },
        "canonical name11": {
            chineseName: "Chinese name3",
            imageLink: "../src/assets/logo.jpeg"
        }, "canonical name12": {
            chineseName: "Chinese name1",
            imageLink: "../src/assets/logo.jpeg"
        },
    }
})
</script>

<style>
.item-list {
    margin-top: 50px;
}
</style>
