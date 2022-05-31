<script setup>
import { ref, computed } from "vue";
import TransactionList from "./TransactionList.vue";
import TransactionDetail from "./TransactionDetail.vue";

const emit = defineEmits(["transactionEdit"]);

const edit_transaction = ref({});

const transaction_exist = computed(() => {
  return Object.keys(edit_transaction).length > 0;
});

function start_edit(transaction, temp) {
  edit_transaction.value = transaction;
}
</script>

<template>
  <h1>Inspect & Edit Transactions</h1>
  <section class="inspect">
    <TransactionList
      @transactionEdit="(transaction, temp) => start_edit(transaction, temp)"
    />
    <TransactionDetail
      v-if="transaction_exist"
      :transaction="edit_transaction"
      v-bind:detail_title="`Marked Transaction`"
    />
  </section>
</template>

<style scoped>
section.inspect {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>