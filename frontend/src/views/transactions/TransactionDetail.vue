<script setup>
const props = defineProps(['transaction']);
console.log(props.transaction);
</script>

<template>
    <section class="transaction-detail">
        <h3>Previous transaction:</h3>
        <dl v-for="[key, value] of Object.entries(props.transaction)">
            <dt class="detail-title" :key="key">{{ key.substr(0, 1).toUpperCase() + key.substr(1) }}:</dt>
            <dd :key="key">{{ value }}</dd>
        </dl>
    </section>
</template>

<style scoped>
dt.detail-title {
    font-weight: bold;
}
dd {
    font-style: italic;
}
h3 {
    text-decoration: underline;
}
section.transaction-detail {
    border: 1px solid #000000;
    border-radius: 1em;
    align-self: center;
    margin: 2em;
    padding: 1em;
}
.warning {
    color: #fda;
    font-style: italic;
}
</style>