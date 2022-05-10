<script setup>
import { ref } from "vue";
import StatsMenu from "../components/menus/stats/StatsMenu.vue";
const menuChoices = ["Daily Avg.", "Category Avg."];

const menu_choice = ref(0);

function click_menu(item_no){
    menu_choice.value = item_no;
}
</script>

<template>
    <main>
        <h1>Stats</h1>
        <StatsMenu @menu-item="(item_no) => click_menu(item_no)" :choices="menuChoices" />
        <h3>{{ menuChoices[menu_choice] }}</h3>
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
