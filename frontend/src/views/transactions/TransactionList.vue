<script setup>
import { onMounted, ref, computed } from "vue";
import { RequestHandler } from "../../helpers/reqs";

const emit = defineEmits(["transactionEdit", "transactionDelete"]);

const transactions = ref([]);
const trans_sum = ref(0);
const temp_data = ref(false);
const current_inspection = ref(null);

function get_transactions() {
  const req_obj = new RequestHandler("/transactions/get_all");
  req_obj
    .sendRequest()
    .then((data) => {
      temp_data.value = data.temp;
      transactions.value = data.transactions;
      trans_sum.value = data.sum;
    })
    .catch((rej_response) => {
      transactions.value = [];
      trans_sum.value = 0;
      temp_data.value = false;
    });
}

function make_bold(transaction, temp_data, event) {
  if (current_inspection.value)
    current_inspection.value.style.fontWeight = "normal";
  if (event.target !== current_inspection.value) {
    current_inspection.value = event.target;
    current_inspection.value.style.fontWeight = "bold";
  }
  emit("transactionEdit", transaction, temp_data);
}

function delete_transaction(transaction, event) {
  emit("transactionDelete", transaction, event);
}

const loaded = computed(() => {
  return transactions.value.length > 0;
});

onMounted(() => {
  get_transactions();
});
</script>

<template>
  <div class="item-list">
    <ul v-if="loaded">
      <li
        v-for="(transaction, index) of transactions"
        :key="index"
        @mousedown="(event) => make_bold(transaction, temp_data, event)"
      >
        {{ transaction.date }}: {{ transaction.amount }}
        {{ transaction.currency }}
        <button
          @mousedown="(event) => delete_transaction(transaction, event)"
          class="btn-delete--small"
        >
          X
        </button>
      </li>
    </ul>
    <span class="transaction_sum"
      >Sum: <strong>{{ trans_sum }}</strong></span
    >
  </div>
</template>

<style scoped>
div.item-list {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

span.transaction_sum {
  background-color: #955;
  padding: 0.5em;
  border-radius: 1em;
}

button.btn-delete--small {
  padding: 0.25em;
  background-color: lightcoral;
  border: 1px solid black;
  border-radius: 0.25em;
}
</style>