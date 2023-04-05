<template>
    <BackButton />
    <div class="classification-folder">
        <Folder current-attribute="classification" :opened-folder="openedFolder" />
    </div>
</template>

<script setup>
import { computed } from 'vue';
import BackButton from '../components/BackButton.vue';
import Folder from '../components/Folder.vue';

const props = defineProps(["openFolder"])

const openedFolder = computed(() => {
    if (props.openFolder === undefined) {
        return []
    }
    else {
        return props.openFolder
    }
})

</script>

<style>
.classification-folder {
    margin: 55px 0;
}
</style>