<template>
    <BackButton />
    <var-row class="database-entrance">
        <var-col :span="12">
            <RouterLink to="/classification" class="nav-link">
                <DatabaseIcon />
                <span class="label">按分类浏览</span>
            </RouterLink>
        </var-col>
        <var-col :span="12">
            <RouterLink to="/distribution" class="nav-link">
                <MapIcon />
                <span class="label">按地点浏览</span>
            </RouterLink>
        </var-col>
    </var-row>
    <TextSearchBar class="search-bar" @submit="getQueryResult" />
</template>

<script setup>
import BackButton from '../components/BackButton.vue';
import DatabaseIcon from '../components/icons/IconDatabase.vue';
import MapIcon from '../components/icons/IconMap.vue'
import TextSearchBar from '../components/TextSearchBar.vue';
import router from '@/router'


function getQueryResult(queryValue) {
    router.push({ path: "/query", query: { queryValue: queryValue } })
}
</script>

<style>
.database-entrance {
    margin-top: 200px;
}

.search-bar {
    margin-top: 50px;
}
</style>