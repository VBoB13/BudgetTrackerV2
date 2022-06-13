<script setup>
import { onMounted } from "vue";
import LoginForm from "../components/forms/LoginForm.vue";
import { useRoute } from "vue-router";

const route = useRoute();
const emit = defineEmits(["loginevent"]);

onMounted(() => {
  console.log(route.params.prev_url);
});
</script>

<template>
  <section class="login">
    <h1>Login</h1>
    <LoginForm
      @formloginevent="emit('loginevent', { prev_url: route.query.prev_url })"
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
  width: 50vw;
}
</style>
