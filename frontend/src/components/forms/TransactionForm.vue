<script setup>
import { onMounted } from "vue";

const state = reactive({
  transaction: {},
  category_choices: [],
});

async function get_categories() {
  const reqObj = new RequestHandler("/categories/get_all");
  await reqObj.sendRequest().then((data) => {
    console.log(data.categories);
    state.category_choices = data.categories;
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
});
</script>

<template>
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
    <InputField id="trans_comment" name="trans_comment" placeholder="Comment" />
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