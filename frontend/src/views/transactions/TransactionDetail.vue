<script setup>
const props = defineProps(['transaction']);
</script>

<template>
    <section class="transaction-detail">
        <dl v-if="props.transaction !== {}">
            <dt class="detail-title">{{ props.transaction.date }} : {{ props.transaction.comment }}</dt>
            <dd>{{ props.transaction.amount }} ({{ props.transaction.category }})</dd>
        </dl>
        <h3 v-else class="warning">No transaction have been added yet...</h3>
    </section>
</template>

<style scoped>
section.transaction-detail {
    border: 1px solid #000000;
    border-radius: 1em;
}
.warning {
    color: #fda;
    font-style: italic;
}
</style>