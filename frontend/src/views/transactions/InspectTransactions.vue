<script setup>
import { ref, computed, toRaw, isProxy } from "vue";
import TransactionList from "./TransactionList.vue";
import TransactionDetail from "./TransactionDetail.vue";
import { RequestHandler } from "../../helpers/reqs";

const emit = defineEmits(["transactionEdit"]);

const edit_transaction = ref({});
const delete_transactions = ref([]);
const transaction_list_key = ref(true);
let del_transactions_num = 0;

const transaction_exist = computed(() => {
  return Object.keys(edit_transaction.value).length > 0;
});

const send_transaction = computed(() => {
  if (isProxy(send_transaction)) return toRaw(edit_transaction.value);
  return edit_transaction.value;
});

const delete_transaction_num = computed(() => {
  del_transactions_num = delete_transactions.value.length;
  return delete_transactions.value.length;
});

function start_edit(transaction, temp) {
  edit_transaction.value = transaction;
}

function delete_transaction(transaction, event) {
  let exists_in_delete = false;
  if (!delete_transactions.value.includes(transaction))
    delete_transactions.value.push(transaction);
}

function confirm_delete() {
  let confirm_delete = confirm(`Delete ${del_transactions_num} transactions?`);
  if (confirm_delete) {
    let req_obj = new RequestHandler("/transactions/delete", "POST");
    req_obj.reqConf.data = { transactions: delete_transactions.value };
    req_obj
      .sendRequest()
      .then(() => {
        delete_transactions.value = [];
        alert(`Transactions deleted!`);
        transaction_list_key.value = !transaction_list_key.value;
      })
      .catch((error) => {
        console.error(error);
      });
  }
}

function clear_delete_transactions() {
  delete_transactions.value = [];
}
</script>

<template>
  <h1>Inspect Transactions</h1>
  <section v-if="delete_transaction_num > 0" class="delete_transaction">
    <button @click="confirm_delete" class="btn-delete--small">
      {{ `Delete ${delete_transaction_num} transactions.` }}</button
    >&nbsp;&nbsp;
    <button @click="clear_delete_transactions" class="btn-clear--small">
      {{ `Clear ${delete_transaction_num} transactions from delete pool.` }}
    </button>
  </section>
  <section class="inspect">
    <TransactionList
      @transactionEdit="(transaction, temp) => start_edit(transaction, temp)"
      @transactionDelete="
        (transaction, event) => delete_transaction(transaction, event)
      "
      :key="transaction_list_key"
    />
    <Transition>
      <TransactionDetail
        v-if="transaction_exist"
        :transaction="send_transaction"
        detail_title="Marked Transaction"
      />
    </Transition>
  </section>
</template>

<style scoped>
section.inspect {
  display: flex;
  justify-content: center;
}

button.btn-delete--small {
  padding: 0.25em;
  background-color: lightcoral;
  border: 1px solid black;
  border-radius: 0.25em;
}

button.btn-clear--small {
  padding: 0.25em;
  background-color: yellowgreen;
  border: 1px solid black;
  border-radius: 0.25em;
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
