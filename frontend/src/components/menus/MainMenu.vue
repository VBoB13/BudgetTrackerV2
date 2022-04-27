<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <section class="menu">
    <RouterLink :to="{ name: 'Add' }">
      <img src="../../assets/icons/Add-Icon.svg" alt="Add" />
    </RouterLink>
    <RouterLink :to="{ name: 'Stats' }">
      <img src="../../assets/icons/Stats.svg" alt="Stats" />
    </RouterLink>
    <RouterLink :to="{ name: 'Inspect' }">
      <img src="../../assets/icons/Inspect.svg" alt="Inspect" />
    </RouterLink>
  </section>
</template>

<style scoped>
section.menu {
  border: 1px solid #020050;
  padding: 5px;
  display: flex;
  justify-content: space-between;
  align-content: flex-start;
}
</style>
