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

const props = defineProps(['canonicalName', 'chineseName', 'imageLink'])

function jump() {
    router.push({ name: "plant", params: { canonicalName: props.canonicalName } })
}

</script>