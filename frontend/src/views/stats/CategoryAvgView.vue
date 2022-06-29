<script setup>
import { ref, onMounted } from "vue";
import { RequestHandler } from "../../helpers/reqs";
import CheckBox from "../../components/forms/inputs/CheckBox.vue";

const img_yes = ref(true);
const img = ref(false);

function isImage(data) {
  return data.length > 0;
}

const checkbox_props = {
  id: "image_check",
  name: "image_check",
  text: "Download image from backend? (lower quality but faster)",
};

function toggle_img() {
  img_yes.value = document.getElementById("image_check").checked;
}

function get_category_sum_graph() {
  const req_obj = new RequestHandler("/stats/get_category_sum_ratio", "POST");
  const yes_data = [["yes", img_yes.value]];
  req_obj.reqConf.data = Object.fromEntries(yes_data);
  req_obj
    .sendRequest()
    .then((data) => {
      if (!isImage(data)) throw new Error(`Could not update image!`);
      img.value = `data:image/png;base64,` + data;
    })
    .catch((error) => {
      console.error(error);
      if (img.value !== false) img.value = false;
    });
}

onMounted(() => {
  get_category_sum_graph();
});
</script>

<template>
  <section class="stats">
    <h3>Category Avg.</h3>
    <img v-if="img !== false" :src="img" alt="Category avg. graph" />
    <h5 v-else>No graph yet.</h5>
    <CheckBox v-bind="checkbox_props" />
  </section>
</template>
