<script setup>
import { ref, computed } from "vue";
import TransactionList from "./TransactionList.vue";
import TransactionDetail from "./TransactionDetail.vue";

const emit = defineEmits(["transactionEdit"]);

const edit_transaction = ref({});

const transaction_exist = computed(() => {
  return Object.keys(edit_transaction.value).length > 0;
});

function start_edit(transaction, temp) {
  edit_transaction.value = transaction;
}
</script>

<template>
  <h1>Inspect Transactions</h1>
  <section class="inspect">
    <TransactionList
      @transactionEdit="(transaction, temp) => start_edit(transaction, temp)"
    />
    <Transition>
      <TransactionDetail
        v-if="transaction_exist"
        :transaction="edit_transaction"
        :detail_title="`Marked Transaction`"
      />
    </Transition>
  </section>
</template>

<style scoped>
section.inspect {
  display: flex;
  justify-content: center;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
