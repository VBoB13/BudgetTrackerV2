<script setup>
function goBack(){
  this.$router.go(-1);
}
</script>

<template>
    <nav>
      <button class="normal" @click="goBack">Back</button>&nbsp;|&nbsp;
      <RouterLink :to="{ name: 'Home' }">Home</RouterLink>&nbsp; |&nbsp;
      <RouterLink :to="{ name: 'About' }">About</RouterLink>
    </nav>
</template>

<style scoped>
nav {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
}
</style>