<template v-if="isLoading">
    <div class="loading">
        <var-loading type="circle" size="large" />
        <p>Loading...</p>
    </div>
</template>

<script setup>
defineProps(['isLoading'])
</script>

<style>
.loading {
    margin: 20px;
}

.loading * {
    text-align: center;
}

.loading p {
    font-weight: bold;
}
</style>