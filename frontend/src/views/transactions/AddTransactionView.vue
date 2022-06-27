<script setup>
import { onMounted, onUpdated, reactive, computed } from "vue";
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
  let req_obj2 = new RequestHandler("/transactions/check_temp_to_db");
  state.transaction_queue = await req_obj2
    .sendRequest()
    .then((data) => data.transactions);
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
      <CheckBox @prevTransChecked="checkbox_status" v-bind="checkbox_props" />
      <span class="small"
        >There are <strong>{{ state.transaction_queue }}</strong> transactions
        waiting to be submitted.</span
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

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
