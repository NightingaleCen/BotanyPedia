<template>
    <div class="result-display">
        <RouterLink :to="'/plant/' + canonicalName">
            <var-image class="result-image" :src="imageLink" fit="cover" height="300px" weight="280px" />
        </RouterLink>
        <p class="canonical-name">{{ canonicalName }}</p>
        <p class="chinese-name">{{ chineseName }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const props = defineProps(['canonicalName'])

const imageLink = ref("")
const chineseName = ref("")

onMounted(() => {
    axios.get("/api/queryInfo", { params: { name: props.canonicalName } }).then(
        (response) => {
            let data = response.data
            imageLink.value = data['image']
            chineseName.value = data['中文名'][0]
        }
    )
})
</script>

<style>
.result-display {
    padding: 20px;
}

.canonical-name {
    text-align: center;
    font-size: large;
    font-weight: bold;
    font-style: italic;
}

.chinese-name {
    text-align: center;
    font-weight: bold;
}
</style>