<script setup>
import router from "../../router/";

function goBack() {
  router.go(-1);
}
</script>

<template>
    <nav>
      <button @click="goBack">Back</button>&nbsp;|&nbsp;
      <RouterLink :to="{ name: 'Home' }">Home</RouterLink>&nbsp; |&nbsp;
      <RouterLink :to="{ name: 'About' }">About</RouterLink>
    </nav>
</template>

<style scoped>
nav {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}
button {
  cursor: pointer;
  padding: 0.5em;
  border: 1px solid #000000;
  border-radius: 1em;
  background-color: #666;
  color: #fff;
}
a {
  padding: 0.25em;
}
a:hover {
  color: #f89;
  text-decoration: none;
  background-color: #334499;
}
</style>