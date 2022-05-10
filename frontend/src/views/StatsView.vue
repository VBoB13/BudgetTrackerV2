<script setup>
import { ref } from "vue";
import StatsMenu from "../components/menus/stats/StatsMenu.vue";
import router from "../router/index"; 

const menuChoices = [{name: "Daily Avg.", route: "/daily"}, {name: "Category Avg.", route: "/category"}];

function click_menu(route){
    router.push(route);
}
</script>

<template>
    <main>
        <h1>Stats</h1>
        <StatsMenu @menu-item="(route) => click_menu(route)" :choices="menuChoices" />
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
