<script setup>
import { ref, onMounted } from "vue";
import { RequestHandler } from '../../helpers/reqs';

const img_yes = ref(true);
const img = ref(false);

function isImage(data){
  return data && data['type'].split('/')[0] === 'image';
}

function get_daily_avg_graph(){
  const req_obj = new RequestHandler("http://0.0.0.0:8000/stats/get_daily_category_sum", "POST");
  const yes_data = [["yes", img_yes.value]];
  req_obj.data = Object.fromEntries(yes_data);
  req_obj.sendRequest()
    .then((data) => {
      if (!isImage(data)) throw new Error(`Could not update image!`);
      img.value = data;
    })
    .catch((error) => {
      console.error(error);
      if (img.value !== false) img.value = false;
    })
}

onMounted(() => {
  get_daily_avg_graph();
});
</script>

<template>
  <section class="stats">
    <h3>Daily Avg.</h3>
    <img v-if="img !== false" :src="img" alt="Daily avg. graph" />
    <h5 v-else>No graph yet.</h5>
  </section>
</template>
