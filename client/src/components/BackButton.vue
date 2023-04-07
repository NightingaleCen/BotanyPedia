<template>
    <div class="back-header">
        <h1 class="page-title">
            <button @click="goBack" class="back-button">
                <LeftIcon />
            </button>LeafyLingo
        </h1>
    </div>
</template>
  
<script setup>
import LeftIcon from './icons/IconLeft.vue';
import router from '@/router'

function goBack() {
    router.go(-1)
}

</script>

<style>
.back-header {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    margin: 15px;

}

.back-button {
    position: absolute;
    left: 0;
}

.page-title {
    text-align: center;
    font-weight: bold;
    color: #2E8540;

}

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
  