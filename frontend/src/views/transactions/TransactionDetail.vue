<script setup>
import { ref, computed } from "vue";
import TransactionForm from "../../components/forms/TransactionForm.vue";

const emit = defineEmits(["update_transaction"]);

const edit_val = ref(false);

const edit_title = computed(() => {
  if (edit_val.value) return "Cancel edit";
  return "Edit";
});

const toggle_class = computed(() => {
  if (edit_val.value) return "btn-cancel-edit--small";
  return "btn-edit--small";
});

function toggle_edit() {
  edit_val.value = !edit_val.value;
}

const props = defineProps(["transaction", "detail_title"]);
</script>

<template>
  <section
    class="transaction-detail-section"
    v-if="Object.keys(props.transaction).length > 0"
  >
    <button :class="toggle_class" @click="toggle_edit">
      {{ edit_title }}
    </button>
    <h3>{{ props.detail_title }}</h3>
    <div v-if="!edit_val">
      <dl v-for="[key, value] of Object.entries(props.transaction)" :key="key">
        <dt class="detail-title" :key="key">
          {{ key.slice(0, 1).toUpperCase() + key.slice(1) }}:
        </dt>
        <dd :key="key">{{ value }}</dd>
      </dl>
    </div>
    <div v-else>
      <TransactionForm
        @update_trans="(transaction) => emit('update_transaction', transaction)"
        :transaction="props.transaction"
        mode="edit"
      />
    </div>
  </section>
</template>

<style scoped>
dl {
  margin-top: 0.25em;
  margin-bottom: 0.25em;
}
dt.detail-title {
  font-weight: bold;
}
dd {
  font-style: italic;
}
h3 {
  text-decoration: underline;
}
section.transaction-detail-section {
  border: 1px solid #000000;
  border-radius: 1em;
  align-self: center;
  margin: 1em;
  padding: 1em;
  align-self: flex-start;
}
.warning {
  color: #fda;
  font-style: italic;
}

button.btn-edit--small {
  padding: 0.25em;
  background-color: lightyellow;
  border: 1px solid black;
  border-radius: 0.25em;
}

button.btn-cancel-edit--small {
  padding: 0.25em;
  background-color: lightgray;
  border: 1px solid black;
  border-radius: 0.25em;
}
</style>