<template>
    <var-collapse v-if="currentAttribute !== 'genus' && currentAttribute !== 'province'" class="top-folder"
        v-model="folderToOpen">
        <var-collapse-item v-for="item in Items" :title="item" :name="item" :id="item">
            <Folder v-if="showComponent(item)" v-bind="nextProps" :current-folder-name="item" />
        </var-collapse-item>
    </var-collapse>
    <template v-if="currentAttribute === 'genus' || currentAttribute === 'province'" v-for="item in Items">
        <ResultItem class="result-items" :canonical-name="item" />
        <var-divider hairline v-if="Items.length > 1" />
    </template>
</template>

<script setup>
import { computed, onMounted, ref, defineAsyncComponent } from 'vue';
import axios from 'axios';

const ResultItem = defineAsyncComponent(() =>
    import('./ResultItem.vue')
)
const Folder = defineAsyncComponent(() =>
    import('./Folder.vue')
)

const props = defineProps(["currentAttribute", "openedFolder", "currentFolderName"])
const folderToOpen = ref([])
const Items = ref({})
const nextProps = ref({})

function showComponent(item) {
    if (folderToOpen.value.includes(item)) {
        return true
    }
    else if (props.openedFolder.includes(item)) {
        return true
    }
    else {
        return false
    }
}

onMounted(() => {
    folderToOpen.value = props.openedFolder
    nextProps.value = { currentAttribute: getNextAttribute(), openedFolder: getNextOpenFolder() }

    if (props.currentAttribute == "genus") {
        axios.get("http://localhost:8080/genus", { params: { genus: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "family") {
        axios.get("http://localhost:8080/family", { params: { family: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "order") {
        axios.get("http://localhost:8080/order", { params: { order: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "class") {
        axios.get("http://localhost:8080/class", { params: { class: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "phylum") {
        axios.get("http://localhost:8080/phylum", { params: { phylum: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "kingdom") {
        axios.get("http://localhost:8080/kingdom", { params: { kingdom: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "classification") {
        axios.get("http://localhost:8080/classification").then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "distribution") {
        axios.get("http://localhost:8080/distribution").then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "country") {
        axios.get("http://localhost:8080/country", { params: { country: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "area") {
        axios.get("http://localhost:8080/area", { params: { area: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    } else if (props.currentAttribute == "province") {
        axios.get("http://localhost:8080/province", { params: { province: props.currentFolderName } }).then(
            (response) => {
                let data = response.data
                Items.value = data
            }
        )
    }
})

function getNextAttribute() {
    switch (props.currentAttribute) {
        case "classification":
            return "kingdom"
        case "kingdom":
            return "phylum"
        case "phylum":
            return "class"
        case "class":
            return "order"
        case "order":
            return "family"
        case "family":
            return "genus"

        case "distribution":
            return "country"
        case "country":
            return "area"
        case "area":
            return "province"
        default:
            break
    }
}

function getNextOpenFolder() {
    return props.openedFolder
}
</script>

<style>
.top-folder {
    --collapse-content-padding: 0 3px 5px;
}
</style>
