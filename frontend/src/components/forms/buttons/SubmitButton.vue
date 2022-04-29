<script setup>
const props = defineProps({
    value: {
        type: String,
        default: "Submit"
    },
    type: {
        type: String,
        default: "submit"
    }
})
</script>

<template>
    <p class="submit_p">
        <input v-bind="props">
    </p>
</template>

<style scoped>
p.submit_p {
    display: flex;
    justify-content: center;
}

input {
    padding: 0.66em;
    border-radius: 1em;
    border: 1px solid #000000;
    cursor: pointer;
}
</style>