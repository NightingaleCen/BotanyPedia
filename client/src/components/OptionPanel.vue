<template>
    <div class="option-panel">
        <p class="hint-text">以下哪个选项，更能准确描述您所看到的植物的<br>{{ attributeName }}</p>
        <var-button class="option-button" block color="#2E8540" text-color="#fff"
            v-for="(attribute, name) in attributeValue" @click="makeChoice(name)">
            {{ attribute.join('、') }}
        </var-button>
        <var-button class="option-button" block color="#2E8540" text-color="#fff" @click="makeChoice(null)">
            都不符合
        </var-button>
    </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';

const props = defineProps(["attributes"])
const emit = defineEmits(["choiceMade"])
const choiceCount = ref(0)

onMounted(() => {

})

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
</script>

<style>
.option-panel {
    text-align: center;
    margin: 20px 10px;
}

.hint-text {
    font-weight: bold;
    margin-bottom: 10px;
}

.option-button {
    font-weight: bold;
    margin: 10px 0;
}
</style>