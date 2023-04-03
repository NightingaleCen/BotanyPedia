<template>
    <button @click="goBack">
        <LeftIcon />
    </button>
</template>
  
<script setup>
import LeftIcon from './icons/IconLeft.vue';
import router from '@/router'

function goBack() {
    router.go(-1)
}

</script>

<style>
button {
    background: none;
    border: none;
    margin: 0;
}

svg {
    width: 50px;
    height: auto;
}
</style>
  