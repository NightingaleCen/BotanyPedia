<template>
    <div class="search-and-submit">
        <var-input class="search-bar" placeholder="查询植物" clearable v-model="queryValue" @change="changeText"
            @clear="() => { textIsAvailabel = false }"></var-input>
        <div class="submit-button">
            <button @click="$emit('submit', queryValue)" v-show="textIsAvailabel">
                <UpIcon class="btn" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import UpIcon from './icons/IconUp.vue';

const queryValue = ref('')
const textIsAvailabel = ref(false)

defineEmits(["submit"])

function changeText(value) {
    if (queryValue.value != '' && queryValue.value != null) {
        textIsAvailabel.value = true
    }
    else {
        textIsAvailabel.value = false
    }
}

</script>

<style>
.search-bar {
    margin-top: 15px;
}

.submit-button {
    text-align: center;
    margin: auto;
}

.btn {
    width: 75px;
    height: auto;
}
</style>