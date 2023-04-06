<template>
    <div class="distribution-panel">
        <p class="distribution-item">分布：<span>{{ info.distribution.join('、') }}</span></p>
        <p class="distribution-item" v-if="info.environmantalValue !== undefined">
            环境价值：<span>{{ info.environmantalValue.join("、") }}</span>
        </p>
        <p class="distribution-item" v-if="info.industrialValue !== undefined">
            工业价值：<span>{{ info.industrialValue.join("、") }}</span>
        </p>
        <p class="distribution-item" v-if="info.dietaryValue !== undefined">
            食用价值：<span>{{ info.dietaryValue.join("、") }}</span>
        </p>
        <p class="distribution-item" v-if="info.medicalValue !== undefined">
            药用价值：<span>{{ info.medicalValue.join("、") }}</span>
        </p>
        <p class="distribution-item" v-if="info.cultivatedValue !== undefined">
            栽培价值：<span>{{ info.cultivatedValue.join("、") }}</span>
        </p>
        <p class="distribution-item" v-if="info.disease !== undefined">
            病害：<span>{{ info.disease.join("、") }}</span>
        </p>
        <p class="distribution-item" v-if="info.pest !== undefined">
            虫害：<span>{{ info.pest.join("、") }}</span>
        </p>


    </div>
</template>

<script setup>
defineProps(['info'])
</script>

<style>
.distribution-panel {
    margin: 20px
}

.distribution-item {
    font-weight: bold;
    text-align: start;
}
</style>