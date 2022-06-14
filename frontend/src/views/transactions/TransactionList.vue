<script setup>
import { onMounted, ref, computed } from "vue";
import { RequestHandler } from "../../helpers/reqs";

const emit = defineEmits(["transactionEdit"]);

const transactions = ref([]);
const trans_sum = ref(0);
const temp_data = ref(false);

function get_transactions() {
  const req_obj = new RequestHandler(
    "http://0.0.0.0:8000/transactions/get_all"
  );
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
        @mousedown="$emit('transactionEdit', transaction, temp_data)"
      >
        {{ transaction.date }}: {{ transaction.amount }}
        {{ transaction.currency }}
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
</style>