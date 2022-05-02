<script setup>
const props = defineProps({
  id: {
    type: String,
    required: false,
  },
  name: String,
  type: {
    type: String,
    default: "text",
    required: false,
  },
  class: {
    type: String,
    default: "inputField",
  },
  placeholder: {
    type: String,
    default: "Text goes here...",
  },
  value: {
    type: String,
    default: "",
  },
  required: {
    type: Boolean,
    default: true,
    required: false,
  },
});
</script>

<template>
  <section class="inputField">
    <label :for="props.id ?? props.name">
      {{
        props.id
          ? `${props.id[6]}`.toUpperCase() + `${props.id}`.slice(7)
          : `${props.name[6]}`.toUpperCase() + `${props.name}`.slice(7)
      }}
    </label>
    <br />
    <input
      :id="props.id ?? ''"
      :name="props.name"
      :type="props.type"
      :class="props.class"
      :placeholder="props.placeholder"
      :value="props.value"
      :required="props.required ?? false"
    />
  </section>
</template>

<style scoped>
input.inputField {
  border-radius: 1.5em;
  border: 1px solid #000000;
  padding: 0.66em;
  margin: 0.25em;
}

section.inputField {
  padding-bottom: 0.66em;
  align-self: flex-start;
}
</style>
