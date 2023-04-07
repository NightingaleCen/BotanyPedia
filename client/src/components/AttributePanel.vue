<template>
    <div class="attribute-panel">
        <p class="attribute-item">学名：<span class="attribute-canonical-name">{{ info.canonicalName }}</span></p>
        <p class="attribute-item">中文名：<span>{{ info.chineseName[0] }}</span></p>
        <p class="attribute-item" v-if="info.nickname !== undefined">别名：<span>{{ info.nickname.join('、') }}</span></p>
        <p class="attribute-item">
            植物学分类：
            <var-breadcrumbs class="classification-breadcrumbs">
                <template v-for="item in info.family">
                    <var-breadcrumb>
                        {{ item }}
                        <template #separator>
                            <var-icon name="menu-right" style="margin: 1px 4px 0" />
                        </template></var-breadcrumb>
                </template>
            </var-breadcrumbs>
        </p>
        <p class="attribute-item" v-if="info.lifeForm !== undefined">
            生活型：<span>{{ info.lifeForm[0] }}</span>
        </p>
        <p class="attribute-item" v-if="info.leafColor !== undefined">
            叶片颜色：<span>{{ info.leafColor.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.leafShape !== undefined">
            叶片形状：<span>{{ info.leafShape.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.flowerColor !== undefined">
            花朵颜色：<span>{{ info.flowerColor.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.flowerShape !== undefined">
            花朵形状：<span>{{ info.flowerShape.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.fruitColor !== undefined">
            果实颜色：<span>{{ info.fruitColor.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.fruitShape !== undefined">
            果实形状：<span>{{ info.fruitShape.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.light !== undefined">
            适宜光照：<span>{{ info.light.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.temperature !== undefined">
            适宜温度：<span>{{ info.temperature.join("、") }}</span>
        </p>
        <p class="attribute-item" v-if="info.resistance !== undefined">
            抗逆性：<span>{{ info.resistance.join("、") }}</span>
        </p>

    </div>
</template>

<script setup>
defineProps(['info'])
</script>

<style>
.attribute-panel {
    margin: 20px
}

.attribute-item {
    font-weight: bold;
    text-align: start;
}

.attribute-canonical-name {
    font-style: italic;
}

.classification-breadcrumbs {
    --breadcrumb-inactive-color: #000000;
    --breadcrumb-active-color: #000000;

}
</style>