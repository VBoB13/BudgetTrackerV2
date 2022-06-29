<script setup>
import { reactive, ref, onMounted, toRaw, isProxy } from "vue";
import { RequestHandler } from "../../helpers/reqs";
import CheckBox from "../../components/forms/inputs/CheckBox.vue";
import Chart from "chart.js/auto";

const img_yes = ref(true);
const img = ref(false);
const received_data = ref([]);

const state = reactive({
  img_yes: false,
  img: false,
  received_data: [],
});

function isImage(data) {
  return !Array.isArray(data);
}

const checkbox_props = {
  id: "image_check",
  name: "image_check",
  text: "Download image from backend? (lower quality but faster)",
};

function toggle_img() {
  state.img_yes = document.getElementById("image_check").checked;
}

function get_category_sum_graph() {
  const req_obj = new RequestHandler("/stats/get_category_sum_ratio", "POST");
  const yes_data = [["yes", state.img_yes]];
  req_obj.reqConf.data = Object.fromEntries(yes_data);
  req_obj
    .sendRequest()
    .then((data) => {
      if (state.img_yes) state.img = `data:image/png;base64,` + data;
      else {
        state.received_data = data;
        console.log(toRaw(state.received_data));
      }
    })
    .catch((error) => {
      console.error(error);
      state.img = false;
      state.img_yes = false;
      state.received_data = [];
    });
}

onMounted(() => {
  get_category_sum_graph();
});
</script>

<template>
  <section class="stats">
    <h3>Category Avg.</h3>
    <img
      v-if="state.img !== false"
      :src="state.img"
      alt="Category avg. graph"
    />
    <h5 v-else>No graph yet.</h5>
    <CheckBox v-bind="checkbox_props" @box-checked="toggle_img" />
  </section>
</template>
