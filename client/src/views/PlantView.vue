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

        <var-popup v-model:show="displayPopup">
            <component :is="currentComponent" :info="info"></component>
        </var-popup>

    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import BackButton from '../components/BackButton.vue';
import PlantFlora from '../components/PlantFlora.vue';

const props = defineProps(['canonicalName'])

const info = ref({})

const displayPopup = ref(false)
const showComponent = ref("")
const currentComponent = computed(() => { console.log(showComponent); return showComponent.value })

// just for test
onMounted(() => {
    info.value.imageLink = '../src/assets/logo.jpeg'
    info.value.chineseName = '中文名'
    info.value.canonicalName = props.canonicalName
    info.value.family = ["科", "属"]
    info.value.description = "2013年大西洋飓风季是继1994年以来第一个没有大型飓风形成的大西洋飓风季。热带风暴安德烈亚是全季首场风暴，于6月5日形成，最后一个气旋则是场没有命名的亚热带风暴，于12月7日消散。全年只有飓风英格丽德和温贝托达到飓风强度。热带风暴安德烈亚是唯一登陆美国的风暴，从佛罗里达州登上美国东岸，导致4人遇难。7月上旬，热带风暴尚塔尔从背风群岛经过，造成1人丧生。热带风暴多利安、埃琳以及飓风温贝托只给佛得角群岛带去了狂风天气。墨西哥是本季受灾最严重的国家，飓风英格丽德、第八号热带低气压、热带风暴巴里和热带风暴费尔南德均在该国登陆，其中单英格丽德就造成至少23人死亡，经济损失达15亿美元。"
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