<script setup>
import { ref } from "vue";

const username = ref("");
const password = ref("");

console.log(`${username.value}`);
console.log(`${password.value}`);
</script>
