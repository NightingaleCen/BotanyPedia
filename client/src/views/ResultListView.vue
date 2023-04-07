<template>
    <BackButton />
    <div class="item-list">
        <template v-for="item in resultItems" :key="item">
            <ResultItem :canonical-name="item" />
            <var-divider class="devider" hairline v-if="resultItems.length > 1" />
        </template>
        <var-divider class="no-result" hairline description="没有结果" v-if="resultItems.length === 0" />
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import BackButton from '../components/BackButton.vue';
import ResultItem from '../components/ResultItem.vue';

const props = defineProps(["queryValue"])

const resultItems = ref([])

onMounted(() => {
    axios.get("/api/searchName", { params: { name: props.queryValue } }).then(
        (response) => {
            let data = response.data
            resultItems.value = data
        }
    )

})
</script>

<style>
.item-list {
    margin-top: 50px;
}

.devider {
    --divider-text-margin: 12px 0;
}

.no-result {
    text-align: center;
}
</style>
