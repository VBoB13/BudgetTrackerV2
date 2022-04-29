<script setup>
import { onMounted } from "vue";
import InputField from "../../components/forms/inputs/InputField.vue";
import DateField from "../../components/forms/inputs/DateField.vue";
import SubmitButton from "../../components/forms/buttons/SubmitButton.vue";
import * as fake_data from "../../../../fake_data.json";

const NOW = new Date();
const TODAY = `${NOW.getFullYear()}-${NOW.getMonth()+1}-${NOW.getDate()}`;


function add_transaction(){
    const transForm = document.getElementById("add-trans-form");
    const formData = new FormData(transForm);
    let finalFormData = [];
    for(var pair of formData.entries()){
        finalFormData.push([`${pair[0]}`.slice(6), pair[1]]);
    };
    const data = Object.fromEntries(finalFormData);
    console.log({data});
    fake_data["transactions"].push(data);
};

onMounted(() => {
    const first_el = document.getElementById("trans_category");
    first_el.focus();
});
</script>

<template>
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
            <InputField id="trans_currency" name="trans_currency" maxlength="3" placeholder="Currency (3 characters)" />
            <!-- User -->
            <InputField id="trans_user" name="trans_user" type="number" placeholder="User ID" />
            <!-- Comment -->
            <InputField id="trans_comment" name="trans_comment" placeholder="Comment" />
            <!-- Submit -->
            <SubmitButton />
        </form>
    </div>
</template>

<style scoped>
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
