<script setup>
import { RouterLink } from "vue-router";
import MainMenu from "../components/menus/MainMenu.vue";
console.log("Hi mom!");
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink>&nbsp; |&nbsp;
      <RouterLink to="/about">About</RouterLink>
    </nav>
  </header>
  <main>
    <h1>Budget Tracker</h1>
  </main>
  <MainMenu />
</template>

<style scoped>
h1 {
  text-align: center;
}
main {
  display: flex;
  justify-content: center;
}
header {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
</style>
