<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <section class="menu">
    <RouterLink class="tooltip" :to="{ name: 'Add' }">
      <img
        src="../../assets/icons/Add-Icon.svg"
        alt="Add"
        title="Add transactions to database."
      />
    </RouterLink>
    <RouterLink class="tooltip" :to="{ name: 'Stats' }">
      <img
        src="../../assets/icons/Stats.svg"
        alt="Stats"
        title="Show summary statistics about your budget."
      />
    </RouterLink>
    <RouterLink class="tooltip" :to="{ name: 'Inspect' }">
      <img
        src="../../assets/icons/Inspect.svg"
        alt="Inspect"
        title="Explore and/or manage individual entries."
      />
    </RouterLink>
  </section>
</template>

<style scoped>
section.menu {
  border: 1px solid #020050;
  padding: 5px;
  width: 80vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
section.menu > a:hover > img {
  opacity: 0.5;
}
</style>
