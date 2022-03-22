<script setup>
import { ref } from "vue";
import HomeView from "./views/HomeView.vue";
import AboutView from "./views/AboutView.vue";
import { RequestHandler } from "./helpers/reqs";

const login = ref(false);
let user = null;

try {
  let req = new RequestHandler("192.168.1.108:8000/auth/login", "POST");
  user = req.sendRequest();
} catch (error) {
  console.error(error);
}
if (user.id !== null) {
  login.value = true;
}
</script>

<template>
  <main>
    <HomeView v-if="login" />
    <AboutView v-else />
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
</style>
