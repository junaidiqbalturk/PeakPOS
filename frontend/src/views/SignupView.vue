<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { signupUser } from "../services/api"; // ✅ Import the function

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const loading = ref(false);

const signup = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match!";
    return;
  }

  loading.value = true;
  try {
    await signupUser(username.value, email.value, password.value);
    successMessage.value = "Account created successfully! Redirecting...";
    setTimeout(() => router.push("/"), 2000);
  } catch (error) {
    errorMessage.value = error.message || "Signup failed. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>


<template>
  <div class="full-screen-container">
    <v-card class="pa-6 rounded-lg shadow-lg signup-card">
      <v-card-title class="text-center text-h4 font-weight-bold">
        Create an Account
      </v-card-title>

      <v-card-subtitle class="text-center text-grey-darken-1">
        Join PeakPOS today
      </v-card-subtitle>

      <v-alert v-if="errorMessage" type="error" class="mb-4">
        {{ errorMessage }}
      </v-alert>

      <v-alert v-if="successMessage" type="success" class="mb-4">
        {{ successMessage }}
      </v-alert>

      <v-form @submit.prevent="signup">
        <v-text-field
          v-model="username"
          label="Username"
          variant="outlined"
          prepend-inner-icon="mdi-account"
          class="custom-field"
          required
        ></v-text-field>

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

        <v-text-field
          v-model="confirmPassword"
          label="Confirm Password"
          type="password"
          variant="outlined"
          prepend-inner-icon="mdi-lock-check"
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
          Sign Up
        </v-btn>
      </v-form>

      <v-card-text class="text-center mt-3">
        <span class="text-grey-darken-1">Already have an account?</span>
        <router-link to="/" class="text-primary font-weight-bold">Login</router-link>
      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
/* Full-Screen Background */
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

/* Modern Signup Card */
.signup-card {
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
  .signup-card {
    padding: 20px;
  }
}
</style>
