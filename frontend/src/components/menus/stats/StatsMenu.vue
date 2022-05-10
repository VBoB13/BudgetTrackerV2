<script setup>
const props = defineProps({
    choices: {
        type: Array[Object],
        required: true
    }
});

const emits = defineEmits(['menu-item']);
</script>

<template>
    <section class="tab-menu">
        <div class="tab-choice" @click="emits('menu-item', choice.route)" v-for="(choice, index) of props.choices" :key="index">
            {{ choice.name }}
        </div>
    </section>    
</template>

<style scoped>
section.tab-menu {
    background-color: #aaf;
    display: flex;
    justify-content: center;
    align-items: center;
}
div.tab-choice {
    border: 1px solid #000;
    border-radius: 1em 1em 0 0;
    margin-left: 0.25em;
    margin-right: 0.25em;
    padding: 0.25em;
}
</style>
