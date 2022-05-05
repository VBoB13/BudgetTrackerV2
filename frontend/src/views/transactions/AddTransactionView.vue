<script setup>
import { onMounted, onUpdated, reactive, computed } from "vue";
import { RequestHandler } from "../../helpers/reqs";

import InputField from "../../components/forms/inputs/InputField.vue";
import DateField from "../../components/forms/inputs/DateField.vue";
import SubmitButton from "../../components/forms/buttons/SubmitButton.vue";
import CheckBox from "../../components/forms/inputs/CheckBox.vue";
import SelectField from "../../components/forms/inputs/SelectField.vue";
import TransactionDetail from "./TransactionDetail.vue";

const state = reactive({
    transaction: {},
    show_transaction: false
});

async function update_transaction(data) {
    data = await Promise.resolve(data);
    state.transaction = data;
}

function add_transaction(){
    const transForm = document.getElementById("add-trans-form");
    const formData = new FormData(transForm);
    let finalFormData = [];
    for(var pair of formData.entries()){
        finalFormData.push([`${pair[0]}`.slice(6), pair[1]]);
    };
    const data = Object.fromEntries(finalFormData);
    try{
        let req_obj = new RequestHandler("http://0.0.0.0:8000/transactions/add_temp", "POST");
        req_obj.reqConf.data = data;
        const data2 = req_obj.sendRequest().then(response_data => {
            return response_data.transaction;
        });
        update_transaction(data2)
    } catch(err){
        console.log("Save data to temp file: FAILED!");
        console.error(err);
        state.transaction = {};
    }
};

const category_choices = ["Food", "Rent & Utilities", "Leisure", "Travel", "Others"];

const category_select_props = {
    id: "trans_category",
    name: "trans_category",
    choices: category_choices,
    label: "Category"
};

const checkbox_props = {
    id: "show_transaction",
    name: "show_transaction",
    text: "Show last added transaction?"
};

const checkbox_status = () => {
    state.show_transaction = document.getElementById("show_transaction").checked;
};

onMounted(() => {
    const first_el = document.getElementById("trans_category");
    first_el.focus();
});
</script>

<template>
    <main class="transactions">
        <div class="form-add">
            <h2>Add Transaction</h2>
            <form id="add-trans-form" @submit.prevent="add_transaction">
                <!-- DateField -->
                <DateField id="trans_date" name="trans_date" />
                <!-- Category -->
                <SelectField v-bind="category_select_props" />
                <!-- Amount -->
                <InputField id="trans_amount" name="trans_amount" type="number" placeholder="Amount" />
                <!-- Currency -->
                <InputField id="trans_currency" name="trans_currency" value="NTD" maxlength="3" placeholder="Currency (3 characters)" />
                <!-- Store -->
                <InputField id="trans_store" name="trans_store" placeholder="Store" />
                <!-- User -->
                <InputField id="trans_user_id" name="trans_user_id" type="number" placeholder="User ID" />
                <!-- Comment -->
                <InputField id="trans_comment" name="trans_comment" placeholder="Comment" />
                <!-- Submit -->
                <SubmitButton />
            </form>
        </div>
        <section class="last-transaction">
            <CheckBox @prevTransChecked="checkbox_status" v-bind="checkbox_props" />
            <TransactionDetail v-if="state.show_transaction" :transaction="state.transaction" />
        </section>
    </main>
</template>

<style scoped>
main.transactions {
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
    padding: 1em;
    border: 1px solid #000000;
    border-radius: 1em;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-content: center;
    align-items: center;
}
section.last-transaction {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-content: center;
    align-items: center;
    height: 99vh;
}
</style>
