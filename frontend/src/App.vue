<script setup>
import { reactive, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import NavbarMenu from "./components/menus/NavbarMenu.vue";
import LoginView from "./views/LoginView.vue";
import { RequestHandler } from "./helpers/reqs.js";
import * as user_data from "../../user_data.json";

const router = useRouter();
const route = useRoute();

const state = reactive({
  isAuthenticated: false,
  user: "",
});

function login(prev_url = "") {
  let username = document.getElementById("login_username").value;
  let password = document.getElementById("login_password").value;
  user_data.users.forEach((user) => {
    if (username === user.username) {
      if (password === user.password) {
        state.isAuthenticated = true;
        state.user = user.username;
        if (prev_url) router.push({ name: prev_url });
      } else {
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
  req
    .sendRequest()
    .then((data) => {
      state.isAuthenticated = data.isAuthenticated;
      state.user = data.user;
    })
    .catch((rej_response) => {
      console.error(rej_response);
      state.isAuthenticated = false;
      state.user = "";
      router.push({ name: "Login", query: { prev_url: route.name } });
    });
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
    <LoginView
      v-if="!state.isAuthenticated"
      @loginevent="({ prev_url }) => login(prev_url)"
    />
    <router-view v-else />
  </main>
</template>

<style>
header {
  display: flex;
  justify-content: center;
  align-items: center;
}
span.text-code {
  padding: 0.1em;
  background-color: lightgray;
  font-family: "Courier New", Courier, monospace;
  font-size: 0.9em;
}
div#app {
  display: grid;
  margin: 0px;
  grid-template-rows: 40px 100%;
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  background: linear-gradient(
    180deg,
    #afe2ff -8.06%,
    rgba(175, 226, 255, 0) 100%
  );
  min-height: 100vh;
}

body {
  margin: 0px;
}

main {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}
</style>
