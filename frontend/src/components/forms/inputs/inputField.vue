<script setup>
import { ref, defineProps, onMounted } from "vue";

const props = defineProps({
  name: String(""),
  type: String("text"),
  class: String("text_input"),
  placeholder: String("")
});

const fieldVal = ref("")

onMounted(() => {
  if (props.name === "" || props.name === null || props.name === undefined) throw Error("Input field MUST have a name...");
});
</script>

<template>
  <input
    v-bind="props"
    v-model="fieldVal"
  />
</template>
