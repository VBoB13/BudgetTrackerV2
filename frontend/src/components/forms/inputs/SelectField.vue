<script setup>
const props = defineProps({
    id: {
        type: String,
        required: true
    },
    name: {
        type: String,
        required: true
    },
    choices: {
        type: Array,
        required: true
    },
    label: {
        type: String,
        required: true
    },
    class: {
        type: String,
        default: "inputField"
    }
});
</script>

<template>
    <section class="inputField">
        <label :for="props.id">{{ props.label }}</label><br>
        <select :name="props.name" :id="props.id" :class="props.class">
            <option value="" selected>-- Please choose a {{ props.label.toLowerCase() }} --</option>
            <option v-for="(choice, index) of props.choices" :value="choice.name" :key="index">
                {{ choice.name[0].toUpperCase() + choice.name.slice(1) }}
            </option>
        </select>
    </section>
</template>

<style scoped>
select.inputField {
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
