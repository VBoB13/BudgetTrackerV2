<script setup>
const props = defineProps({
  name: String,
  type: {
    type: String,
    default: "text",
    required: true
  },
  class: {
    type: String,
    default: "inputField"
  },
  placeholder: {
    type: String,
    default: "Text goes here..."
  },
  value: {
    type: String,
    default: ""
  },
  required: {
    type: Boolean,
    default: true
  }
});
// ['name', 'type', 'class', 'placeholder', 'value', 'required']
</script>

<template>
  <input
    :name="props.name"
    :type="props.type"
    :class="props.class"
    :placeholder="props.placeholder"
    :value="props.value"
    :required="props.required"
  />
</template>
