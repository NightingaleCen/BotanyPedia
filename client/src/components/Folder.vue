<template>
    <var-collapse class="top-folder" v-model="folderToOpen">
        <var-collapse-item v-for="item in Items" :title="getItemName(item)" :name="getItemName(item)">
            <component v-if="showComponent(item)" :is="subcomponent"
                v-bind="currentAttribute === 'spieces' ? item : nextProps">
            </component>
        </var-collapse-item>
    </var-collapse>
</template>

<script setup>
import { computed, onMounted, ref, defineAsyncComponent } from 'vue';

const ResultItem = defineAsyncComponent(() =>
    import('./ResultItem.vue')
)
const Folder = defineAsyncComponent(() =>
    import('./Folder.vue')
)

const props = defineProps(["currentAttribute", "openedFolder"])
const folderToOpen = ref([])
const Items = ref({})
const nextProps = ref({})

function showComponent(item) {
    if (folderToOpen.value.includes(getItemName(item))) {
        return true
    }
    else if (props.openedFolder.includes(getItemName(item))) {
        return true
    }
    else {
        return false
    }
}

onMounted(() => {
    folderToOpen.value = props.openedFolder
    nextProps.value = { currentAttribute: getNextAttribute(), openedFolder: getNextOpenFolder() }

    if (props.currentAttribute == "spieces") {
        Items.value = {
            "canonical name1": {
                canonicalName: "canonical name1",
                chineseName: "Chinese name1",
                imageLink: "../src/assets/logo.jpeg"
            },
            "canonical name2": {
                canonicalName: "canonical name2",
                chineseName: "Chinese name2",
                imageLink: "../src/assets/logo.jpeg"
            },
            "canonical name3": {
                canonicalName: "canonical name3",
                chineseName: "Chinese name3",
                imageLink: "../src/assets/logo.jpeg"
            },
        }
    } else if (props.currentAttribute == "genus") {
        Items.value = ["属", "属1"]
    } else if (props.currentAttribute == "family") {
        Items.value = ["科", "科1"]
    } else if (props.currentAttribute == "area") {
        Items.value = ["地区", "地区1"]
    } else if (props.currentAttribute == "province") {
        Items.value = ["省", "省1"]
    }

})

function getItemName(item) {
    if (typeof item == "object") {
        return item.chineseName
    }
    else {
        return item
    }
}

function getNextAttribute() {
    switch (props.currentAttribute) {
        case "family":
            return "genus"
        case "genus":
            return "spieces"
        case "area":
            return "province"
        case "province":
            return "spieces"
        default:
            break
    }
}

function getNextOpenFolder() {
    return props.openedFolder
}

const subcomponent = computed(() => {
    if (props.currentAttribute == "spieces") {
        return ResultItem
    }
    else {
        return Folder
    }
})

</script>

<style>
.top-folder {
    --collapse-content-padding: 0 3px 5px;
}
</style>