<script setup>
import { reactive, onMounted } from "vue";
import NavbarMenu from "./components/menus/NavbarMenu.vue";
import LoginView from "./views/LoginView.vue"
import { RequestHandler } from "./helpers/reqs.js";
import * as fake_data from "../../fake_data.json";

const state = reactive({
  isAuthenticated: false,
  user: null,
});

function setState(data){
  if (data.isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
    state.user = data.user;
  }
}

function auth_check(username, password){

}

function authenticate() {
  // let req = new RequestHandler("http://192.168.1.108:8000/auth/login", "POST");
  // req.reqConf.body = {
  //   username: "w1ck3d",
  //   password: "13",
  // };
  try {
    // let data = req.sendRequest();
    let data = fake_data;
    console.log("Login successful!");
    setState(data);
  } catch (error) {
    console.error(error);
    state.isAuthenticated = false;
    state.user = null;
  }
}

onMounted(() => {
  authenticate();
});
</script>

<template>
  <header>
    <NavbarMenu />
  </header>
  <main>
    <LoginView v-if="state.isAuthenticated" />
    <router-view v-else />
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
