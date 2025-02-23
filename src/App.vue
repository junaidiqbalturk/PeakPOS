<script setup>
import { ref, onMounted } from "vue";
import { getWelcomeMessage } from "./services/api";

const message = ref("Loading...");

onMounted(async () => {
  const data = await getWelcomeMessage();
  message.value = data.message;
});
</script>

<template>
  <div class="container">
    <h1>PeakPOS</h1>
    <p>{{ message }}</p>
  </div>
</template>

<style>
.container {
  text-align: center;
  margin-top: 50px;
}
</style>
