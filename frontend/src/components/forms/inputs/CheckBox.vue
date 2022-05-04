<script setup>
const props = defineProps({
    id: {
        type: String,
        required: true
    },
    name: {
        type: String,
        required: false,
        default: ""
    },
    text: {
        type: String,
        required: true
    }
});
</script>

<template>
    <div class="input-field">
        <input type="checkbox" v-bind="props">
        <label :for="props.name ? props.name : props.id">{{ props.text }}</label>
    </div>
</template>

<style scoped>
div.input-field {
    margin: 1em;
}
</style>