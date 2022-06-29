<script setup>
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  name: {
    type: String,
    required: false,
    default: "",
  },
  text: {
    type: String,
    required: true,
  },
});
const emits = defineEmits(["boxChecked"]);
</script>

<template>
  <div class="input-field">
    <input type="checkbox" v-bind="props" @click="emits('boxChecked')" />
    <label :for="props.name ? props.name : props.id">{{ props.text }}</label>
  </div>
</template>

<style scoped>
div.input-field {
  margin: 1em;
}
</style>