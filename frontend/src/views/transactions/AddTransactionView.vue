<script setup>
import { onMounted, onUpdated, reactive } from "vue";
import { RequestHandler } from "../../helpers/reqs";
import CheckBox from "../../components/forms/inputs/CheckBox.vue";
import TransactionDetail from "./TransactionDetail.vue";
import TransactionForm from "../../components/forms/TransactionForm.vue";

const state = reactive({
  transaction: {},
  show_transaction: false,
  transaction_queue: 0,
});

// const category_choices = ref();

async function update_transaction(data) {
  data = await Promise.resolve(data);
  state.transaction = data;
  check_transaction_queue();
}

async function check_transaction_queue() {
  let req_obj = new RequestHandler("/transactions/check_temp_to_db");
  state.transaction_queue = await req_obj
    .sendRequest()
    .then((data) => data.transactions);
}

async function temp_to_db() {
  let req_obj = new RequestHandler("/transactions/temp_to_db", "POST");
  let save_success = await req_obj.sendRequest().then((data) => data.success);
  if (save_success) {
    alert("Transactions saved successfully!");
    await check_transaction_queue();
  } else {
    alert("Transactions save FAILED!");
  }
}

const checkbox_props = {
  id: "show_transaction",
  name: "show_transaction",
  text: "Show last added transaction?",
};

const checkbox_status = () => {
  state.show_transaction = document.getElementById("show_transaction").checked;
};

onMounted(() => {
  check_transaction_queue();
});
</script>

<template>
  <section class="transactions">
    <div class="form-add">
      <h2>Add Transaction</h2>
      <TransactionForm
        @update_trans="(transaction) => update_transaction(transaction)"
      />
      <CheckBox @boxChecked="checkbox_status" v-bind="checkbox_props" />
      <span class="small"
        >There are <strong>{{ state.transaction_queue }}</strong> transactions
        waiting
        <i class="temp_to_db" v-on:click="temp_to_db">to be submitted.</i></span
      >
    </div>
    <div class="last-transaction">
      <Transition>
        <TransactionDetail
          v-if="state.show_transaction"
          :transaction="state.transaction"
          :detail_title="`Last Transaction`"
        />
      </Transition>
    </div>
  </section>
</template>

<style scoped>
section.transactions {
  display: flex;
  justify-content: center;
  align-content: center;
  align-items: flex-start;
}
div.form-add {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
}
div.form-add > form {
  padding: 0.5em;
  border: 1px solid #000000;
  border-radius: 1em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
}
div.last-transaction {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
  height: 99vh;
}

i.temp_to_db {
  cursor: pointer;
  color: blue;
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
