<script setup>
const NOW = new Date();
const MONTH = NOW.getMonth()+1 < 10 ? `0${NOW.getMonth()+1}` : `${NOW.getMonth()+1}`
const TODAY = `${NOW.getFullYear()}-${MONTH}-${NOW.getDate()}`;

const props = defineProps({
  id: {
    type: String,
    required: false
  },
  name: {
    type: String,
    required: true
  },
  value: {
    type: String,
    default: `${new Date().getFullYear()}-${new Date().getMonth()+1}-${new Date().getDate()}`
  },
  required: {
    type: Boolean,
    default: true,
    required: false
  },
  min: {
    type: String,
    default: "2022-02-22"
  },
  max: {
    type: String,
    default: `${new Date().getFullYear()}-${new Date().getMonth()+1 < 10 ? '0' + `${new Date().getMonth()+1}` : new Date().getMonth()+1}-${new Date().getDate()}`
  }
});

</script>
<template>
  <section class="inputField">
    <label :for="props.id ?? props.name">
      {{ props.id ? `${props.id[6]}`.toUpperCase() + `${props.id}`.slice(7) : `${props.name[6]}`.toUpperCase() + `${props.name}`.slice(7)}}
    </label>
    <br>
    <input
      :id="props.id ?? ''"
      :name="props.name"
      type="date"
      class="inputField"
      v-model="TODAY"
      :required="props.required ?? false"
      :min="props.min"
      :max="props.max"
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
