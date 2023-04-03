<script setup>
import SearchIcon from '../components/icons/IconSearch.vue'
import BookIcon from '../components/icons/IconBook.vue'

</script>

<template>
  <header>
    <img src="../assets/logo.jpeg" class="logo" alt="Logo">
    <h1 class="title">BotanyPedia</h1>
  </header>
  <main>
    <nav>
      <router-link to="/search" class="nav-link">
        <SearchIcon />
        <span class="label">识别</span>
      </router-link>
      <router-link to="/database" class="nav-link">
        <BookIcon />
        <span class="label">百科</span>
      </router-link>
    </nav>
  </main>
</template>

<style>
header {
  padding-bottom: 20px;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

.logo {
  vertical-align: middle;
  height: 80px;
  width: auto;
}

.title {
  text-align: center;
  margin: 0;
  font-size: 40px;
  color: #2E8540;
}

nav {
  padding-top: 150px;
  text-align: center;
}

.nav-link {
  display: inline-block;
  vertical-align: top;
  text-decoration: none;
  color: #333;
  font-size: 16px;
  margin: 0 50px;
  text-align: center;
}

.label {
  display: block;
  text-align: center;
  margin-top: 5px;
  font-size: large;
  font-weight: bold;
}

svg {
  width: 50px;
  height: auto;
}
</style>