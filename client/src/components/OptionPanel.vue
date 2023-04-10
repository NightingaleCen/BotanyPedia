<template>
    <div class="option-panel">
        <div class="non-province-panel" v-if="attributeName !== 'province'">
            <p class="hint-text">以下哪个选项，更能准确描述您所看到的植物的<br>{{ attributeName }}</p>
            <template v-for="(attribute, name) in attributeValue">
                <var-button v-if="attribute.length !== 0" class="option-button" block color="#2E8540" text-color="#fff"
                    size="large" @click="makeChoice(name)">
                    {{ attribute.join('、') }}
                </var-button>
            </template>
            <var-button class="option-button" block color="#2E8540" text-color="#fff" size="large"
                @click="makeChoice(null)">
                都不符合
            </var-button>
        </div>

        <div class="province-panel" v-if="attributeName === 'province'">
            <p class="hint-text">为了提供更精确的识别结果，我们需要您提供这张照片的位置信息</p>
            <var-select class="location-selector" placeholder="选择一个位置" v-model="province" @change="chooseProvince">
                <var-option v-for="item in provinceList" :label="item" />
            </var-select>
            <var-button class="option-button" block color="#2E8540" text-color="#fff" size="large" @click="getIPProvince">
                获取当前位置
            </var-button>
            <var-button class="option-button" block color="#2E8540" text-color="#fff" size="large"
                @click="makeChoice(null)">
                我不想提供位置信息
            </var-button>
        </div>

    </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import axios from 'axios';

const props = defineProps(["attributes"])
const emit = defineEmits(["choiceMade"])
const choiceCount = ref(0)
const province = ref("")

const provinceList = [
    '河北',
    '山西',
    '辽宁',
    '吉林',
    '黑龙江',
    '江苏',
    '浙江',
    '安徽',
    '福建',
    '江西',
    '山东',
    '河南',
    '湖北',
    '湖南',
    '广东',
    '海南',
    '四川',
    '贵州',
    '云南',
    '陕西',
    '甘肃',
    '青海',
    '台湾',
    '内蒙古',
    '广西',
    '西藏',
    '宁夏',
    '新疆',
    '北京',
    '天津',
    '上海',
    '重庆',
    '香港',
    '澳门',]

const attributeValue = computed(() => {
    let attributeName = Object.keys(props.attributes)[choiceCount.value]
    return props.attributes[attributeName]
})

const attributeName = computed(() => {
    return Object.keys(props.attributes)[choiceCount.value]
})


function makeChoice(name) {
    emit('choiceMade', name)
    choiceCount.value++
}

function chooseProvince(location) {
    for (let canonicalName in props.attributes["province"]) {
        for (let index in props.attributes["province"][canonicalName]) {
            if (location.includes(props.attributes["province"][canonicalName][index])) {
                makeChoice(canonicalName)
                return
            }
        }
    }
    makeChoice(null)
}

function getIPProvince() {
    axios.get("/getLocation"
    ).then(
        (response) => {
            let location = response.data.data
            chooseProvince(location)
        }).catch(
            (error) => {
                console.log("error")
            }
        )
}
</script>

<style>
.option-panel {
    text-align: center;
    margin: 20px 10px;
}

.location-selector {
    margin-top: -20px;
    margin-bottom: 20px;
}

.hint-text {
    font-weight: bold;
    margin-bottom: 10px;
}

.option-button {
    font-weight: bold;
    margin: 15px 0;
}
</style>