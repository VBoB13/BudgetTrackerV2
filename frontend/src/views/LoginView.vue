<script setup>
import LoginForm from "../components/forms/LoginForm.vue";

const emit = defineEmits(['loginevent']);

</script>

<template>
    <h1>Login</h1>
    <LoginForm @formloginevent="emit('loginevent', { prev_url: this.$route.redirectedFrom })" />
</template>

<style scoped>
h1 {
    text-align: center;
}
</style>