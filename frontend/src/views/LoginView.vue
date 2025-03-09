<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);

import { loginUser } from "../services/api";

const login = async () => {
  loading.value = true;
  try {
    const response = await loginUser(email.value, password.value);

    localStorage.setItem("token", response.token); // Ensure the token is stored
    localStorage.setItem("isAuthenticated", "true"); // Store authentication state
    router.push("/dashboard"); // Redirect after login
  } catch (error) {
    errorMessage.value = error.message || "Invalid credentials";
  } finally {
    loading.value = false;
  }
};


</script>

<template>
  <div class="full-screen-container">
    <v-card class="pa-6 rounded-lg shadow-lg login-card">
      <v-card-title class="text-center text-h4 font-weight-bold">
        Welcome to PeakPOS
      </v-card-title>

      <v-card-subtitle class="text-center text-grey-darken-1">
        Please sign in to continue
      </v-card-subtitle>

      <v-alert v-if="errorMessage" type="error" class="mb-4">
        {{ errorMessage }}
      </v-alert>

      <v-form @submit.prevent="login">
        <v-text-field
          v-model="email"
          label="Email"
          variant="outlined"
          prepend-inner-icon="mdi-email"
          class="custom-field"
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          variant="outlined"
          prepend-inner-icon="mdi-lock"
          class="custom-field"
          required
        ></v-text-field>

        <v-btn
          :loading="loading"
          block
          color="blue-darken-3"
          variant="elevated"
          type="submit"
          class="mt-4 rounded-lg animate-btn"
        >
          Sign In
        </v-btn>
      </v-form>

      <v-card-text class="text-center mt-3">
        <span class="text-grey-darken-1">Don't have an account?</span>
        <router-link to="/signup" class="text-primary font-weight-bold">Sign Up</router-link>
      </v-card-text>
    </v-card>
  </div>
</template>


<style scoped>
/* Ensure Full-Screen Background */
.full-screen-container {
  position: absolute;
  width: 100%;
  height: 100vh;
  top: 0;
  left: 0;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Modern Login Card */
.login-card {
  max-width: 420px;
  width: 90%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  padding: 24px;
}

/* Custom Input Fields */
.custom-field {
  border-radius: 8px;
}

/* Button Animation */
.animate-btn {
  transition: all 0.3s ease;
}
.animate-btn:hover {
  transform: scale(1.05);
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-card {
    padding: 20px;
  }
}
</style>
