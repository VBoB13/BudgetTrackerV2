<script setup>
import StatsMenu from "../components/menus/stats/StatsMenu.vue";
const menuChoices = ["Daily Avg.", "Category Avg."];
</script>

<template>
    <main>
        <h1>Stats</h1>
        <StatsMenu :choices="menuChoices" />
    </main>    
</template>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
</style>
