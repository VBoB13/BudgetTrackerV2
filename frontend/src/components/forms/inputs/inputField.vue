<script setup>
import { ref, defineProps, onMounted } from "vue";

const field = defineProps({
  name: String(""),
  type: String("text"),
  value: String(""),
  class: String("text_input"),
});

const fieldVal = ref("");

function onInput(e) {
  fieldVal.value = e.target.value;
}

onMounted(() => {
  // Something...
});
</script>

<template>
  <input
    v-bind="field"
    @input="onInput"
    placeholder="{{ field.name }} here..."
  />
</template>
