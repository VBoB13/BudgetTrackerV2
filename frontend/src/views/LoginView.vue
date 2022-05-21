<script setup>
import LoginForm from "../components/forms/LoginForm.vue";

const emit = defineEmits(["loginevent"]);
</script>

<template>
  <section class="login">
    <h1>Login</h1>
    <LoginForm
      @formloginevent="
        emit('loginevent', { prev_url: this.$route.redirectedFrom })
      "
    />
  </section>
</template>

<style scoped>
h1 {
  text-align: center;
}
section.login {
  border: 1px solid #000000;
  border-radius: 1em;
  margin-top: 2em;
}
</style>
