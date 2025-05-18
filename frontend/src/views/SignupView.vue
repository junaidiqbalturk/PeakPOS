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
  <div class="signup-container">
    <!-- Left Panel with Illustration -->
    <div class="illustration-panel">
      <div class="logo-container">
        <img src="../assets/logo-pp.png" alt="PeakPOS Logo" class="logo">
      </div>
      <div class="illustration">
        <img src="../assets/illustration.svg" alt="Illustration" class="illustration-image">
      </div>
      <div class="tagline">
        <h2>Welcome to PeakPOS</h2>
        <p>The smarter way to manage your business</p>
      </div>
      <div class="features">
        <div class="feature-item">
          <i class="material-icons">shopping_cart</i>
          <span>Streamline your sales</span>
        </div>
        <div class="feature-item">
          <i class="material-icons">inventory</i>
          <span>Manage inventory easily</span>
        </div>
        <div class="feature-item">
          <i class="material-icons">bar_chart</i>
          <span>Real-time analytics</span>
        </div>
      </div>
    </div>

    <!-- Right Panel with Form -->
    <div class="form-panel">
      <div class="form-container">
        <div class="form-header">
          <h1>Create Your Account</h1>
          <p>Join thousands of businesses using PeakPOS</p>
        </div>

        <div v-if="errorMessage" class="alert error">
          <i class="material-icons">error</i>
          <span>{{ errorMessage }}</span>
        </div>

        <div v-if="successMessage" class="alert success">
          <i class="material-icons">check_circle</i>
          <span>{{ successMessage }}</span>
        </div>

        <form @submit.prevent="signup" class="signup-form">
          <div class="form-group">
            <label for="username">Username</label>
            <div class="input-container">
              <i class="material-icons">person</i>
              <input
                id="username"
                v-model="username"
                type="text"
                placeholder="Enter your username"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <div class="input-container">
              <i class="material-icons">email</i>
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="Enter your email"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-container">
              <i class="material-icons">lock</i>
              <input
                id="password"
                v-model="password"
                type="password"
                placeholder="Create a password"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <div class="input-container">
              <i class="material-icons">lock_outline</i>
              <input
                id="confirmPassword"
                v-model="confirmPassword"
                type="password"
                placeholder="Confirm your password"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            class="signup-button"
            :class="{ 'loading': loading }"
            :disabled="loading"
          >
            <span v-if="!loading">Create Account</span>
            <div v-else class="spinner"></div>
          </button>
        </form>

        <div class="form-footer">
          <p>Already have an account? <router-link to="/">Sign In</router-link></p>
        </div>

        <div class="terms">
          <p>By signing up, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.signup-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: #f5f7fa;
}

/* Left Panel - Illustration */
.illustration-panel {
  flex: 1;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  display: flex;
  flex-direction: column;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

.logo-container {
  margin-bottom: 2rem;
}

.logo {
  height: 60px;
}

.illustration {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 2rem 0;
}

.illustration-image {
  max-width: 80%;
  height: auto;
}

.tagline {
  text-align: center;
  margin-bottom: 2rem;
}

.tagline h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.tagline p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1rem;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 10px;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.feature-item:hover {
  transform: translateX(5px);
  background-color: rgba(255, 255, 255, 0.2);
}

.feature-item i {
  font-size: 1.5rem;
}

/* Right Panel - Form */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.form-container {
  width: 100%;
  max-width: 450px;
  padding: 2rem;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-header h1 {
  font-size: 1.8rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: #64748b;
  font-size: 1rem;
}

.alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.alert.error {
  background-color: #fee2e2;
  color: #ef4444;
}

.alert.success {
  background-color: #dcfce7;
  color: #10b981;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #334155;
}

.input-container {
  display: flex;
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  background-color: #f8fafc;
}

.input-container:focus-within {
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
}

.input-container i {
  color: #64748b;
  margin-right: 0.5rem;
}

.input-container input {
  width: 100%;
  padding: 1rem 0;
  border: none;
  background-color: transparent;
  font-size: 1rem;
  color: #1e293b;
}

.input-container input:focus {
  outline: none;
}

.signup-button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(to right, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.signup-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.signup-button:active {
  transform: translateY(0);
}

.signup-button.loading {
  opacity: 0.8;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.form-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #64748b;
}

.form-footer a, .terms a {
  color: #7c3aed;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.3s ease;
}

.form-footer a:hover, .terms a:hover {
  color: #4f46e5;
  text-decoration: underline;
}

.terms {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  color: #94a3b8;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .signup-container {
    flex-direction: column;
  }

  .illustration-panel {
    padding: 2rem;
  }

  .features {
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
  }

  .feature-item {
    flex: 1;
    min-width: 0;
    flex-direction: column;
    text-align: center;
    padding: 1rem 0.5rem;
  }

  .feature-item:hover {
    transform: translateY(-5px);
  }
}

@media (max-width: 768px) {
  .illustration-panel {
    padding: 1.5rem;
  }

  .tagline h2 {
    font-size: 1.5rem;
  }

  .tagline p {
    font-size: 1rem;
  }

  .features {
    gap: 0.5rem;
  }

  .feature-item i {
    font-size: 1.25rem;
  }

  .feature-item span {
    font-size: 0.875rem;
  }

  .form-panel {
    padding: 1.5rem;
  }

  .form-container {
    padding: 1.5rem;
  }
}

@media (max-width: 640px) {
  .illustration-panel {
    padding: 1rem;
  }

  .features {
    flex-direction: column;
  }

  .feature-item {
    flex-direction: row;
    text-align: left;
    padding: 0.75rem;
  }

  .feature-item:hover {
    transform: translateX(5px);
  }

  .form-panel {
    padding: 1rem;
  }

  .form-container {
    padding: 1rem;
  }

  .form-header h1 {
    font-size: 1.5rem;
  }
}
</style>