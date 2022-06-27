<script setup>
import { onMounted, reactive, computed } from "vue";
import { RequestHandler } from "../../helpers/reqs";
import { TODAY } from "../../helpers/constants";
import InputField from "../../components/forms/inputs/InputField.vue";
import DateField from "../../components/forms/inputs/DateField.vue";
import SubmitButton from "../../components/forms/buttons/SubmitButton.vue";
import SelectField from "../../components/forms/inputs/SelectField.vue";

const emit = defineEmits(["update_trans"]);

const props = defineProps({
  transaction: {
    type: Object,
    required: false,
  },
  mode: {
    type: String,
    required: false,
    default: "add",
  },
});

function add_transaction() {
  const transForm = document.getElementById("add-trans-form");

  const formData = new FormData(transForm);
  let finalFormData = [];
  for (var pair of formData.entries()) {
    finalFormData.push([`${pair[0]}`.slice(6), pair[1]]);
  }
  const data = Object.fromEntries(finalFormData);
  // URL
  let url = "/transactions/add";
  if (props.mode === "edit") {
    url = `/transactions/edit`;
    data.id = props.transaction?.id;
    data.old_transaction = props.transaction ?? null;
  }
  let req_obj = new RequestHandler(url, "POST");
  req_obj.reqConf.data = data;
  req_obj
    .sendRequest()
    .then((response_data) => emit("update_trans", response_data.transaction))
    .catch((err) => {
      console.log("Save data to DB: FAILED!");
      console.log(`Reason: ${err}`);
      console.log("Saving to temp. file...");
      if (props.mode !== "edit") url = "/transactions/add_temp";
      let req_obj = new RequestHandler(url, "POST");
      req_obj.reqConf.data = data;
      req_obj
        .sendRequest()
        .then((response_data) => {
          emit("update_trans", response_data.transaction);
        })
        .catch((err) => {
          console.log(`Unable to save to temp .json file!`);
          console.error(err);
        });
    });
}

const state = reactive({
  category_choices: [],
});

async function get_categories() {
  const reqObj = new RequestHandler("/categories/get_all");
  await reqObj
    .sendRequest()
    .then((data) => {
      state.category_choices = data.categories;
    })
    .catch((error) => {
      console.error(error);
    });
}

let category_select_props = computed(() => {
  return {
    id: "trans_category",
    name: "trans_category",
    choices: state.category_choices,
    label: "Category",
  };
});

onMounted(() => {
  get_categories();
  const first_el = document.getElementById("trans_category");
  first_el.focus();
});
</script>

<template>
  <form id="add-trans-form" @submit.prevent="add_transaction">
    <!-- DateField -->
    <DateField
      id="trans_date"
      name="trans_date"
      :value="props.transaction?.date ?? TODAY"
    />
    <!-- Category -->
    <SelectField
      v-bind="category_select_props"
      :value="props.transaction?.category"
    />
    <!-- Amount -->
    <InputField
      id="trans_amount"
      name="trans_amount"
      type="number"
      placeholder="Amount"
      :value="props.transaction?.amount"
    />
    <!-- Currency -->
    <InputField
      id="trans_currency"
      name="trans_currency"
      maxlength="3"
      placeholder="Currency (3 characters)"
      :value="props.transaction?.currency ?? 'NTD'"
    />
    <!-- Store -->
    <InputField
      id="trans_store"
      name="trans_store"
      placeholder="Store"
      :value="props.transaction?.store ?? ''"
    />
    <!-- User -->
    <InputField
      id="trans_user_id"
      name="trans_user_id"
      type="number"
      placeholder="User ID"
      :value="props.transaction?.user ?? ''"
    />
    <!-- Comment -->
    <InputField
      id="trans_comment"
      name="trans_comment"
      placeholder="Comment"
      :value="props.transaction?.comment ?? ''"
    />
    <!-- Submit -->
    <SubmitButton />
  </form>
</template>

<style scoped>
form {
  padding: 0.5em;
  border: 1px solid #000000;
  border-radius: 1em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  align-items: center;
}
</style>