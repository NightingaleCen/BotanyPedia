<template>
    <div class="flora-area">
        <var-breadcrumbs class="classification">
            <RouterLink :to="{ path: '/classification', query: { openFolder: info.family.slice(0, -1) } }">
                <var-breadcrumb>{{
                    info.family[info.family.length - 2]
                }}</var-breadcrumb>
            </RouterLink>
            <RouterLink :to="{ path: '/classification', query: { openFolder: info.family } }">
                <var-breadcrumb>{{
                    info.family[info.family.length - 1]
                }}</var-breadcrumb>
            </RouterLink>
            <var-breadcrumb>{{ info.chineseName[0] }}</var-breadcrumb>
        </var-breadcrumbs>
        <var-card class="flora-card" :title="info.chineseName[0]" :subtitle="info.canonicalName">
            <template #description>
                <div class="flora-text" v-html="info.description[0].replace(/\r\n/g, '<br>&emsp;&emsp;')"></div>
            </template>
        </var-card>
        <!--添加引用出处-->
    </div>
</template>

<script setup>

const props = defineProps(['info'])

// just for test 
// need to become computed
</script>

<style>
.flora-area {
    margin: auto;
}

.classification {
    margin: 5px 0 0 10px;
}

[class$="subtitle"] {
    font-style: italic;
}

.flora-text {
    text-align: start;
}
</style>