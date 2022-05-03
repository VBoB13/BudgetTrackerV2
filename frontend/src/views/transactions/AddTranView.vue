<script setup>
import { onMounted, ref, computed } from "vue";
import { RequestHandler } from "../../helpers/reqs";

import InputField from "../../components/forms/inputs/InputField.vue";
import DateField from "../../components/forms/inputs/DateField.vue";
import SubmitButton from "../../components/forms/buttons/SubmitButton.vue";
import TransactionDetail from "./TransactionDetail.vue";

const transaction_detail = ref({});
const loaded_detail = ref(false);

function add_transaction(){
    const transForm = document.getElementById("add-trans-form");
    const formData = new FormData(transForm);
    let finalFormData = [];
    for(var pair of formData.entries()){
        finalFormData.push([`${pair[0]}`.slice(6), pair[1]]);
    };
    const data = Object.fromEntries(finalFormData);
    console.log({data});
    try{
        let req_obj = new RequestHandler("http://0.0.0.0:8000/transactions/add_temp", "POST");
        req_obj.reqConf["data"] = data;
        const data2 = req_obj.sendRequest().then(response_data => {
            return response_data;
        });
        transaction_detail.value = data2;
        loaded_detail.value = true;
    } catch(err){
        console.log("Save data to temp file: FAILED!");
        console.error(err);
        transaction_detail.value = {};
        loaded_detail.value = false;
    }
};

const check_added_transaction = () => {
    computed(() => {
        if (transaction_detail !== {}) {
            return false;
        }
        else {
            return true;
        }
    });
}

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
                <InputField id="trans_category" name="trans_category" placeholder="Category" />
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
        <TransactionDetail v-if="check_added_transaction()" :transaction="transaction_detail" />
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
</style>
