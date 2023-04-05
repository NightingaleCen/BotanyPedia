<template>
    <BackButton />
    <div class="distribution-folder">
        <Folder current-attribute="area" :opened-folder="[]" />
    </div>
</template>

<script setup>
import BackButton from '../components/BackButton.vue';
import Folder from '../components/Folder.vue';
</script>

<style>
.distribution-folder {
    margin: 55px 0;
}
</style>