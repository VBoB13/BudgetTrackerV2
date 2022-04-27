<script setup>
import { reactive, onMounted } from "vue";
import { RouterLink } from "vue-router";
import MainMenu from "../components/menus/MainMenu.vue";
import { RequestHandler } from "../helpers/reqs";

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
    state.isAuthenticated = true;
    console.log("Login successful!");
  } catch (error) {
    console.error(error);
    state.isAuthenticated = false;
  }
}

onMounted(() => {
  authenticate();
});
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink>&nbsp; |&nbsp;
      <RouterLink to="/about">About</RouterLink>
    </nav>
  </header>
  <main>
    <h1 v-if="state.isAuthenticated">Budget Tracker</h1>
    <h1 v-else>Login First!</h1>
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
</style>
