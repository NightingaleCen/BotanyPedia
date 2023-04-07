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
        <var-button block color="#2E8540" text-color="#fff" class="util-button" @click="showPopup(AttributePanel)">
            <p>性状描述</p>
        </var-button>
        <var-button block color="#2E8540" text-color="#fff" class="util-button" @click="showPopup(DistributionPanel)">
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
import AttributePanel from '../components/AttributePanel.vue';
import DistributionPanel from '../components/DistributionPanel.vue'
import axios from 'axios';

const props = defineProps(['canonicalName'])

const info = ref({})

const displayPopup = ref(false)
const showComponent = ref("")
const currentComponent = computed(() => { return showComponent.value })

// just for test
onMounted(() => {
    axios.get("/api/queryInfo", { params: { name: props.canonicalName } }).then(
        (response) => {
            let data = response.data
            info.value.imageLink = data['image']
            info.value.chineseName = data['中文名'][0]
            info.value.nickname = data['别名']
            info.value.canonicalName = props.canonicalName
            info.value.family = [data.kingdom, data.phylum, data.class, data.order, data.family, data.genus]
            info.value.description = data['描述'][0].replace(/\r\n/g, "<br>&emsp;&emsp;")
            info.value.lifeForm = data['生活型'][0]
            info.value.leafShape = data['叶片形状']
            info.value.leafColor = data['叶片颜色']
            info.value.flowerShape = data['花朵形状']
            info.value.flowerColor = data['花朵颜色']
            info.value.fruitShape = data['果实形状']
            info.value.fruitColor = data['果实颜色']
            info.value.light = data['光照']
            info.value.temperature = data['温度']
            info.value.resistance = data['抗逆性']
            info.value.distribution = data['province']
            info.value.environmantalValue = data['保护和改造环境价值']
            info.value.industrialValue = data['工业价值']
            info.value.cultivatedValue = data['栽培价值']
            info.value.medicalValue = data['药用价值']
            info.value.dietaryValue = data['食用价值']
            info.value.disease = data['病害名称']
            info.value.pest = data['虫害名称']
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
    margin-top: 50px;
    text-align: center
}

.canonical-name {
    text-align: center;
    font-size: large;
    font-weight: bold;
    font-style: italic;
    margin-top: 10px;
}

.chinese-name {
    text-align: center;
    font-weight: bold;
    margin-bottom: -10px;
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