<template>
    <div>
        <var-cell :title="chineseName" :description="canonicalName" @click="jump">
            <template #extra>
                <var-icon :name="imageLink" :size="50" />
            </template>
        </var-cell>
    </div>
</template>

<script setup>
import router from '@/router'
import { onMounted, ref } from 'vue';
import axios from 'axios';

const props = defineProps(['canonicalName'])
const chineseName = ref('')
const imageLink = ref('')

onMounted(() => {
    axios.get("http://localhost:8080/queryInfo", { params: { name: props.canonicalName } }).then(
        (response) => {
            let data = response.data
            imageLink.value = "http://localhost:8080" + data['image']
            chineseName.value = data['中文名'][0]
        }
    )
})

function jump() {
    router.push({ name: "plant", params: { canonicalName: props.canonicalName } })
}

</script>