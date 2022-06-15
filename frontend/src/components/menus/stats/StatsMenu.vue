<script setup>
import { RouterLink } from "vue-router";
const props = defineProps({
  choices: {
    type: Array[Object],
    required: true,
  },
});
</script>

<template>
  <section class="tab-menu">
    <RouterLink
      :to="choice.route"
      v-for="(choice, index) of props.choices"
      :key="index"
    >
      <div class="tab-choice">
        {{ choice.name }}
      </div>
    </RouterLink>
  </section>
</template>

<style scoped>
section.tab-menu {
  display: flex;
  justify-content: center;
  align-items: center;
}
div.tab-choice {
  box-sizing: border-box;
  background-color: #aaf;
  border: 1px solid #000;
  border-radius: 1em 1em 0 0;
  margin-left: 0.25em;
  margin-right: 0.25em;
  padding: 0.25em;
}
</style>
