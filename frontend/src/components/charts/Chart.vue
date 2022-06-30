<script setup>
import { onMounted } from "vue";
import Chart from "chart.js/auto";
import { CATEGORY_COLORS } from "../../helpers/constants";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

function myChart_config() {
  console.log(props.data);
  const no_of_labels = Object.values(props.data.Category).length;
  let labels = [],
    sums = [],
    colors = [];
  for (let i = 0; i < no_of_labels; i++) {
    labels.push(props.data.Category[i]);
    sums.push(props.data.Sum[i]);
    colors.push(CATEGORY_COLORS[props.data.Category[i]]);
  }
  // return OPTIONS instead and send as props to chart's own component
  return {
    type: "doughnut",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Sums per category",
          data: sums,
          backgroundColor: colors,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "Category Sums (NTD)",
        },
      },
    },
  };
}

onMounted(() => {
  const chart_el = document.getElementById("myChart");
  const chart_config = myChart_config();
  console.log(chart_config);
  const myChart = new Chart(chart_el, chart_config);
});
</script>

<template>
  <canvas id="myChart" width="400" height="400"></canvas>
</template>