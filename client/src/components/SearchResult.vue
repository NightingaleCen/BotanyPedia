<template>
    <div class="result-display">
        <RouterLink :to="'/plant/' + canonicalName">
            <var-image class="result-image" :src="imageLink" fit="cover" height="300px" weight="280px" />
        </RouterLink>
        <p class="canonical-name">{{ canonicalName }}</p>
        <p class="chinese-name">{{ chineseName }}</p>
    </div>
</template>

<script setup>
defineProps(['imageLink', 'canonicalName', 'chineseName'])
</script>

<style>
.result-display {
    padding: 20px;
}

.canonical-name {
    text-align: center;
    font-size: large;
    font-weight: bold;
    font-style: italic;
}

.chinese-name {
    text-align: center;
    font-weight: bold;
}
</style>