<script setup>
import { onMounted, onUpdated, reactive, computed, ref } from "vue";
import { RequestHandler } from "../../helpers/reqs";
import { get_all_categories } from "../../helpers/getters";

import InputField from "../../components/forms/inputs/InputField.vue";
import DateField from "../../components/forms/inputs/DateField.vue";
import SubmitButton from "../../components/forms/buttons/SubmitButton.vue";
import CheckBox from "../../components/forms/inputs/CheckBox.vue";
import SelectField from "../../components/forms/inputs/SelectField.vue";
import TransactionDetail from "./TransactionDetail.vue";

const state = reactive({
    transaction: {},
    show_transaction: false,
    transaction_queue: 0
});

const category_choices = ref([
        {
            "id": 1,
            "name": "Food",
            "color": "Green"
        },
        {
            "id": 2,
            "name": "Rent & Utilities",
            "color": "Gray"
        },
        {
            "id": 3,
            "name": "Medical",
            "color": "Pink"
        },
        {
            "id": 4,
            "name": "Leisure",
            "color": "Blue"
        },
        {
            "id": 5,
            "name": "Travel",
            "color": "LightBlue"
        },
        {
            "id": 6,
            "name": "Kitties",
            "color": "LightBlue"
        },
        {
            "id": 7,
            "name": "Others",
            "color": "LightGray"
        }
    ]);

async function update_transaction(data) {
    data = await Promise.resolve(data);
    state.transaction = data;
};

async function check_transaction_queue(){
    let req_obj2 = new RequestHandler("http://0.0.0.0:8000/transactions/check_temp_to_db");
    state.transaction_queue = await req_obj2.sendRequest().then(data => data.transactions);
};

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
        req_obj.sendRequest().then(response_data => update_transaction(response_data.transaction));
        
    } catch(err){
        console.log("Save data to temp file: FAILED!");
        console.error(err);
        state.transaction = {};
    }
};

const checkbox_props = {
    id: "show_transaction",
    name: "show_transaction",
    text: "Show last added transaction?"
};

const checkbox_status = () => {
    state.show_transaction = document.getElementById("show_transaction").checked;
};

const category_select_props = {
    id: "trans_category",
    name: "trans_category",
    choices: category_choices.value,
    label: "Category"
};

onMounted(() => {
    category_choices.value = get_all_categories().then(data => data);
    const first_el = document.getElementById("trans_category");
    first_el.focus();
    check_transaction_queue();
});
onUpdated(() => {
    console.log(category_choices.value);
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
            <span class="small">There are <strong>{{ state.transaction_queue }}</strong> transactions waiting to be submitted.</span>
        </div>
        <div class="last-transaction">
            <CheckBox @prevTransChecked="checkbox_status" v-bind="checkbox_props" />
            <TransactionDetail v-if="state.show_transaction" :transaction="state.transaction" />
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
    padding: 1em;
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
</style>
