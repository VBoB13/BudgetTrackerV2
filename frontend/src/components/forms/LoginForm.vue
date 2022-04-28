<script setup>
import InputField from "./inputs/InputField.vue";

const usernameInput = {
  name: "username",
  type: "text",
  class: "inputField",
  placeholder: "Username here...",
  value: ""
}

const pwdInput = {
  name: "password",
  type: "password",
  class: "inputField",
  placeholder: "Password here...",
  value: ""
}

function login(){
  if(username === "w1ck3d" && password === "13") return true;
  else return false;
}

</script>

<template>
  <form @submit.prevent="login" class="form_std">
    <InputField v-bind="usernameInput" /><br>
    <InputField v-bind="pwdInput" />
    <p><button type="submit">Login</button></p>
  </form>
</template>

<style scoped>
.form_std {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
