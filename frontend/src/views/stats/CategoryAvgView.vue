<script setup>
import { reactive, computed, onMounted, toRaw, isProxy } from "vue";
import { RequestHandler } from "../../helpers/reqs";
import CheckBox from "../../components/forms/inputs/CheckBox.vue";
import Chart from "../../components/charts/Chart.vue";

const state = reactive({
  received_data: {},
  data_loaded: false,
});

function get_category_sum_graph() {
  const req_obj = new RequestHandler("/stats/get_category_sum_ratio", "POST");
  req_obj
    .sendRequest()
    .then((data) => {
      state.received_data = data;
      state.data_loaded = true;
      console.log(toRaw(state.received_data));
    })
    .catch((error) => {
      console.error(error);
      state.received_data = {};
      state.data_loaded = false;
    });
}

onMounted(() => {
  get_category_sum_graph();
});
</script>

<template>
  <section class="stats">
    <Chart v-if="state.data_loaded" :data="toRaw(state.received_data)" />
  </section>
</template>

<style scoped>
section.stats {
  border: 1px solid black;
  border-radius: 1em;
  padding: 0.5em;
}
</style>
