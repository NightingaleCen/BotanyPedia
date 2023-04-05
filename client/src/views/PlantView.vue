<template>
    <BackButton />
    <div class="plant-display">
        <var-image class="plant-image" :src="info.imageLink" fit="cover" height="300px" weight="280px" />
        <p class="canonical-name">{{ canonicalName }}</p>
        <p class="chinese-name">{{ info.chineseName }}</p>
    </div>
    <div class="div-button">
        <var-button block color="#2E8540" text-color="#fff" class="util-button" @click="showPopup(PlantFlora)">
            <p>植物志</p>
        </var-button>
        <var-button block color="#2E8540" text-color="#fff" class="util-button" @click="showPopup(null)">
            <p>性状描述</p>
        </var-button>
        <var-button block color="#2E8540" text-color="#fff" class="util-button" @click="showPopup(null)">
            <p>功用分布</p>
        </var-button>

        <var-popup v-model:show="displayPopup" position="top" @click="displayPopup = false">
            <component :is="currentComponent" :info="info"></component>
        </var-popup>

    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import BackButton from '../components/BackButton.vue';
import PlantFlora from '../components/PlantFlora.vue';
import axios from 'axios';

const props = defineProps(['canonicalName'])

const info = ref({})

const displayPopup = ref(false)
const showComponent = ref("")
const currentComponent = computed(() => { console.log(showComponent); return showComponent.value })

// just for test
onMounted(() => {
    axios.get("http://localhost:8080/queryInfo", { params: { name: props.canonicalName } }).then(
        (response) => {
            let data = response.data
            info.value.imageLink = '../src/assets/logo.jpeg'
            info.value.chineseName = data['中文名']
            info.value.canonicalName = props.canonicalName
            info.value.family = [data.kingdom, data.phylum, data.class, data.order, data.family, data.genus]
            info.value.description = data['描述'].replace(/\r\n/g, "<br>&emsp;&emsp;")

        }
    )
})

function showPopup(component) {
    displayPopup.value = true;
    showComponent.value = component
}

</script>

<style>
.plant-display {
    margin: 25px;
    text-align: center
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

.util-button {
    text-align: center;
    margin: 20px 0;
}

.util-button p {
    font-weight: bold;
}

.div-button {
    text-align: center;
    margin: auto;
}
</style>