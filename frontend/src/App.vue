<script setup>
import { reactive, onMounted } from "vue";
import NavbarMenu from "./components/menus/NavbarMenu.vue";
import LoginView from "./views/LoginView.vue"
import { RequestHandler } from "./helpers/reqs.js";
import * as user_data from "../../user_data.json";

const state = reactive({
  isAuthenticated: false,
  user: "",
});

function login(prev_url=""){
  let username = document.getElementById('login_username').value;
  let password = document.getElementById('login_password').value;
  user_data.users.forEach(user => {
    if(username === user.username){
      if (password === user.password){
        state.isAuthenticated = true;
        state.user = user.username;
        if (prev_url) router.push(`${prev_url}`);
      }
      else {
        state.isAuthenticated = false;
        state.user = "";
      }
    }
  });
}

function authenticate() {
  let req = new RequestHandler("http://0.0.0.0:8000/auth/login", "POST");
  req.reqConf["data"] = {
    username: "w1ck3d",
    password: "13",
  };
  try {
    let data = req.sendRequest();
  } catch (error) {
    console.error(error);
    state.isAuthenticated = false;
    state.user = "";
    this.$router.push({ name: 'Login'});
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
    <LoginView v-if="!state.isAuthenticated" @loginevent="({prev_url}) => login(prev_url)" />
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
