<script setup>
import InputField from "./inputs/InputField.vue";

const emit = defineEmits(['formloginevent']);

const usernameInput = {
  id: "username",
  name: "username",
  type: "text",
  class: "inputField",
  placeholder: "Username here...",
  value: ""
}

const pwdInput = {
  id: "password",
  name: "password",
  type: "password",
  class: "inputField",
  placeholder: "Password here...",
  value: ""
}

</script>

<template>
  <div class="form">
    <form @submit.prevent="emit('formloginevent')" class="form_std">
    <InputField v-bind="usernameInput" /><br>
    <InputField v-bind="pwdInput" />
    <p><button type="submit">Login</button></p>
  </form>
  </div>
</template>

<style scoped>
.form_std {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
button[type='submit'] {
  border: 1px solid #000000;
  border-radius: 0.5em;
  padding: 0.66em;
  background-color: #5DF;
}
</style>
