<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);

const login = async () => {
  loading.value = true;
  try {
    const response = await axios.post("http://127.0.0.1:5000/api/auth/login", {
      email: email.value,
      password: password.value,
    });

    localStorage.setItem("token", response.data.token);
    router.push("/dashboard");  // Redirect to dashboard after login
  } catch (error) {
    errorMessage.value = "Invalid credentials, please try again!";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-600 to-purple-600 p-4">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <h2 class="text-3xl font-semibold text-center text-gray-800 mb-6">Welcome to PeakPOS</h2>

      <div v-if="errorMessage" class="bg-red-100 text-red-600 p-3 rounded-md mb-4 text-center">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="login" class="space-y-5">
        <div>
          <label class="block text-gray-600 font-medium">Email</label>
          <input
              v-model="email"
              type="email"
              placeholder="Enter your email"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              required
          />
        </div>

        <div>
          <label class="block text-gray-600 font-medium">Password</label>
          <input
              v-model="password"
              type="password"
              placeholder="Enter your password"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
              required
          />
        </div>

        <button
            type="submit"
            class="w-full py-3 text-white bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition duration-300"
            :disabled="loading"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="text-center text-gray-500 mt-4">
        Don't have an account?
        <router-link to="/signup" class="text-blue-500 font-medium hover:underline">Sign Up</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Extra custom styling if needed */
</style>
