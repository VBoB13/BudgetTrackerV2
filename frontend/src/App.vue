<script setup>
import { RouterLink } from "vue-router";
import HomeView from "./views/HomeView.vue";
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink>&nbsp; |&nbsp;
      <RouterLink to="/about">About</RouterLink>
    </nav>
  </header>
  <main>
    <HomeView />
  </main>
</template>

<style>
body {
  position: relative;
  width: 390px;
  height: 98.4vh;
  left: 40%;
  background: linear-gradient(
    180deg,
    #afe2ff -8.06%,
    rgba(175, 226, 255, 0) 100%
  );
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
