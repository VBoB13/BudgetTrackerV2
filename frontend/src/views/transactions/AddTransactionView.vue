<script setup>
import { onMounted, reactive, computed } from "vue";
import { RequestHandler } from "../../helpers/reqs";

import InputField from "../../components/forms/inputs/InputField.vue";
import DateField from "../../components/forms/inputs/DateField.vue";
import SubmitButton from "../../components/forms/buttons/SubmitButton.vue";
import CheckBox from "../../components/forms/inputs/CheckBox.vue";
import SelectField from "../../components/forms/inputs/SelectField.vue";
import TransactionDetail from "./TransactionDetail.vue";

const state = reactive({
  transaction: {},
  show_transaction: false,
  transaction_queue: 0,
  category_choices: [],
});

// const category_choices = ref();

async function update_transaction(data) {
  data = await Promise.resolve(data);
  state.transaction = data;
}

async function get_all_categories() {
  const reqObj = new RequestHandler("http://0.0.0.0:8000/categories/get_all");
  await reqObj.sendRequest().then((data) => {
    console.log(data.categories);
    state.category_choices = data.categories;
  });
}

async function check_transaction_queue() {
  let req_obj2 = new RequestHandler(
    "http://0.0.0.0:8000/transactions/check_temp_to_db"
  );
  state.transaction_queue = await req_obj2
    .sendRequest()
    .then((data) => data.transactions);
}

function add_transaction() {
  const transForm = document.getElementById("add-trans-form");
  const formData = new FormData(transForm);
  let finalFormData = [];
  for (var pair of formData.entries()) {
    finalFormData.push([`${pair[0]}`.slice(6), pair[1]]);
  }
  const data = Object.fromEntries(finalFormData);
  let req_obj = new RequestHandler(
    "http://0.0.0.0:8000/transactions/add",
    "POST"
  );
  req_obj.reqConf.data = data;
  req_obj
    .sendRequest()
    .then((response_data) => update_transaction(response_data.transaction))
    .catch((err) => {
      console.log("Save data to DB: FAILED!");
      console.log(`Reason: ${err}`);
      console.log("Saving to temp. file...");
      let req_obj = new RequestHandler(
        "http://0.0.0.0:8000/transactions/add_temp",
        "POST"
      );
      req_obj.reqConf.data = data;
      req_obj
        .sendRequest()
        .then((response_data) => {
          update_transaction(response_data.transaction);
          check_transaction_queue();
        })
        .catch((err) => {
          state.transaction = {};
          console.log(`Unable to save to temp .json file!`);
          console.error(err);
        });
    });
}

const checkbox_props = {
  id: "show_transaction",
  name: "show_transaction",
  text: "Show last added transaction?",
};

const checkbox_status = () => {
  state.show_transaction = document.getElementById("show_transaction").checked;
};

let category_select_props = computed(() => {
  return {
    id: "trans_category",
    name: "trans_category",
    choices: state.category_choices,
    label: "Category",
  };
});

onMounted(() => {
  get_all_categories();
  const first_el = document.getElementById("trans_category");
  first_el.focus();
  check_transaction_queue();
});
</script>

<template>
  <section class="transactions">
    <div class="form-add">
      <h2>Add Transaction</h2>
      <form id="add-trans-form" @submit.prevent="add_transaction">
        <!-- DateField -->
        <DateField id="trans_date" name="trans_date" />
        <!-- Category -->
        <SelectField v-bind="category_select_props" />
        <!-- Amount -->
        <InputField
          id="trans_amount"
          name="trans_amount"
          type="number"
          placeholder="Amount"
        />
        <!-- Currency -->
        <InputField
          id="trans_currency"
          name="trans_currency"
          value="NTD"
          maxlength="3"
          placeholder="Currency (3 characters)"
        />
        <!-- Store -->
        <InputField id="trans_store" name="trans_store" placeholder="Store" />
        <!-- User -->
        <InputField
          id="trans_user_id"
          name="trans_user_id"
          type="number"
          placeholder="User ID"
        />
        <!-- Comment -->
        <InputField
          id="trans_comment"
          name="trans_comment"
          placeholder="Comment"
        />
        <!-- Submit -->
        <SubmitButton />
      </form>
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
