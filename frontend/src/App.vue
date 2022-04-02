<script setup>
import { reactive, onMounted } from "vue";
import HomeView from "./views/HomeView.vue";
import AboutView from "./views/AboutView.vue";
import { RequestHandler } from "./helpers/reqs";

const state = reactive({
  isAuthenticated: false,
  user: null,
});

function authenticate() {
  let req = new RequestHandler("http://192.168.1.108:8000/auth/login", "POST");
  req.reqConf.body = {
    username: "w1ck3d",
    password: "13",
  };
  try {
    state.user = req.sendRequest();
  } catch (error) {
    console.error(error);
  }
  console.log("Login successful!");
  state.isAuthenticated = true;
}

onMounted(() => {
  authenticate();
});
</script>

<template>
  <main>
    <HomeView v-if="state.isAuthenticated" />
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
