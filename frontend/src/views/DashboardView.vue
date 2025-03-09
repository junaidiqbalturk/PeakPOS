<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import api from "../services/api";

const router = useRouter();
const user = ref(null);
const errorMessage = ref("");

const fetchUserData = async () => {
  try {
    const response = await api.get("/user/me"); // Fetch user data
    user.value = response.data;
  } catch (error) {
    console.error("Error fetching user data:", error);
    localStorage.removeItem("token");
    localStorage.removeItem("isAuthenticated");
    router.push("/");
  }
};



const logout = () => {
  localStorage.removeItem("token");
  router.push("/");
};

onMounted(fetchUserData);
</script>

<template>
  <v-container>
    <v-card class="pa-6">
      <v-card-title>Welcome, {{ user ? user.username : "Loading..." }}</v-card-title>
      <v-card-subtitle>Your Dashboard</v-card-subtitle>

      <v-alert v-if="errorMessage" type="error" class="mt-4">
        {{ errorMessage }}
      </v-alert>

      <v-btn color="red" class="mt-4" @click="logout">Logout</v-btn>
    </v-card>
  </v-container>
</template>
