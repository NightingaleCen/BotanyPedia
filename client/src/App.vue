<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Footer from './components/Footer.vue';
</script>

<template>
  <RouterView />
  <Footer />
</template>

<style>
html,
body {
  height: 100%;
}

#app {
  min-height: 100%;
}
</style>
