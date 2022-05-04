<script setup>
const props = defineProps(['transaction']);
console.log(props.transaction);
</script>

<template>
    <section class="transaction-detail">
        <dl>
            <dt class="detail-title">{{ props.transaction.date }} : {{ props.transaction.comment }}</dt>
            <dd>{{ props.transaction.currency }} ${{ props.transaction.amount }} ({{ props.transaction.category }})</dd>
        </dl>
    </section>
</template>

<style scoped>
dt.detail-title {
    font-weight: bold;
}
section.transaction-detail {
    border: 1px solid #000000;
    border-radius: 1em;
}
.warning {
    color: #fda;
    font-style: italic;
}
</style>