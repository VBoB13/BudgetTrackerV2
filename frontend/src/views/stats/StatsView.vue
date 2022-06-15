<script setup>
import { ref } from "vue";
import StatsMenu from "../../components/menus/stats/StatsMenu.vue";
import router from "../../router/index";

const menuChoices = [
  { name: "Daily Avg.", route: "/stats/daily" },
  { name: "Category Avg.", route: "/stats/category" },
];
</script>

<template>
  <main>
    <h1>Stats</h1>
    <StatsMenu :choices="menuChoices" />
    <router-view></router-view>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

section.stats :is(h3, h5) {
  text-align: center;
}
</style>
