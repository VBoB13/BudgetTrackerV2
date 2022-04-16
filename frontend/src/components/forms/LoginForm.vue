<script setup>
import { ref } from "vue";

const username = ref("");
const password = ref("");

console.log(`${username.value}`);
console.log(`${password.value}`);
</script>

<template>
  <form @submit="login">
    <h3>Login</h3>
  </form>
</template>
