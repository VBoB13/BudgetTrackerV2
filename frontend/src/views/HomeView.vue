<script setup>
import MainMenu from "../components/menus/MainMenu.vue";
</script>

<template>
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
button.normal {
  padding: 0.3em;
  background-color: #efefef;
  border-radius: 0.25em;
  border: 1px solid black;
}
</style>
