<script setup>
const props = defineProps(["transaction", "detail_title"]);
</script>

<template>
  <section
    class="transaction-detail-section"
    v-if="Object.keys(props.transaction).length > 0"
  >
    <h3>{{ props.detail_title }}</h3>
    <dl v-for="[key, value] of Object.entries(props.transaction)" :key="key">
      <dt class="detail-title" :key="key">
        {{ key.slice(0, 1).toUpperCase() + key.slice(1) }}:
      </dt>
      <dd :key="key">{{ value }}</dd>
    </dl>
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
  margin: 2em;
  padding: 1em;
}
.warning {
  color: #fda;
  font-style: italic;
}
</style>