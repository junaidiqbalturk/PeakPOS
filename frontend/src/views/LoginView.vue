<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);
const passwordVisible = ref(false);
const rememberMe = ref(false);
const loginSuccess = ref(false);

// Import your existing API service
import { loginUser } from "../services/api";

// Your existing login function with added success animation
const login = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    const response = await loginUser(email.value, password.value);

    // Show success animation before redirecting
    loginSuccess.value = true;

    localStorage.setItem("token", response.token); // Ensure the token is stored
    localStorage.setItem("isAuthenticated", "true"); // Store authentication state

    // Store email in localStorage if "remember me" is checked
    if (rememberMe.value) {
      localStorage.setItem("rememberedEmail", email.value);
    } else {
      localStorage.removeItem("rememberedEmail");
    }

    // Delay navigation to show success animation
    setTimeout(() => {
      router.push("/dashboard"); // Redirect after login
    }, 1000);
  } catch (error) {
    errorMessage.value = error.message || "Invalid credentials";
  } finally {
    loading.value = false;
  }
};

// Toggle password visibility
const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};

// Check for remembered email on component mount
const checkRememberedEmail = () => {
  const rememberedEmail = localStorage.getItem("rememberedEmail");
  if (rememberedEmail) {
    email.value = rememberedEmail;
    rememberMe.value = true;
  }
};

onMounted(() => {
  checkRememberedEmail();
});
</script>

<template>
  <div class="login-page" :class="{ 'success-background': loginSuccess }">
    <!-- We're using an SVG background with animated stars -->

    <div class="login-container" :class="{ 'zoom-out': loginSuccess }">
      <!-- Logo and branding section -->
      <div class="branding-section">
        <div class="logo-container">
          <v-icon icon="mdi-point-of-sale" size="x-large" color="white" class="logo-icon" />
          <h1 class="brand-name">PeakPOS</h1>
        </div>
        <p class="brand-tagline">Elevate your business operations</p>
      </div>

      <!-- Login card -->
      <v-card class="login-card" elevation="8" rounded="lg">
        <v-card-item>
          <v-card-title class="text-center text-h4 font-weight-bold pb-0 gradient-text">
            Welcome Back
          </v-card-title>
          <v-card-subtitle class="text-center pb-5">
            Sign in to your PeakPOS account
          </v-card-subtitle>
        </v-card-item>

        <!-- Error alert -->
        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          class="mx-4 mb-6 alert-animation"
          closable
          @click:close="errorMessage = ''"
        >
          {{ errorMessage }}
        </v-alert>

        <v-card-text>
          <v-form @submit.prevent="login" class="login-form">
            <!-- Email field -->
            <v-text-field
              v-model="email"
              label="Email"
              variant="outlined"
              prepend-inner-icon="mdi-email-outline"
              autocomplete="email"
              class="input-field"
              hide-details="auto"
              required
            ></v-text-field>

            <!-- Password field with visibility toggle -->
            <v-text-field
              v-model="password"
              :type="passwordVisible ? 'text' : 'password'"
              label="Password"
              variant="outlined"
              prepend-inner-icon="mdi-lock-outline"
              :append-inner-icon="passwordVisible ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="togglePasswordVisibility"
              autocomplete="current-password"
              class="input-field"
              hide-details="auto"
              required
            ></v-text-field>

            <!-- Remember me & Forgot password -->
            <div class="form-options">
              <v-checkbox
                v-model="rememberMe"
                label="Remember me"
                color="primary"
                hide-details
                density="compact"
                class="remember-me-checkbox"
              ></v-checkbox>
              <v-btn
                variant="text"
                color="primary"
                class="forgot-password-btn"
                size="small"
                @click="router.push('/forgot-password')"
              >
                Forgot Password?
              </v-btn>
            </div>

            <!-- Login button -->
            <v-btn
              :loading="loading"
              block
              color="primary"
              size="large"
              type="submit"
              class="login-btn"
              :class="{
                'login-btn-shake': errorMessage,
                'login-btn-success': loginSuccess
              }"
              :disabled="loading || loginSuccess"
            >
              <template v-if="!loginSuccess">
                <v-icon icon="mdi-login" class="me-2"></v-icon>
                Sign In
              </template>
              <template v-else>
                <v-icon icon="mdi-check-circle" class="me-2"></v-icon>
                Success!
              </template>
            </v-btn>
          </v-form>
        </v-card-text>

        <!-- Sign up link -->
        <v-card-text class="text-center pt-0">
          <div class="signup-prompt">
            <span>Don't have an account?</span>
            <router-link to="/signup" class="signup-btn">Create Account</router-link>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<style scoped>
/* Main container with animated background */
.login-page {
  min-height: 100vh;
  width: 100%;
  background-color: #0c1220; /* Fallback color */
  background-image: url('../assets/animated-bg.svg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  position: relative;
  overflow: hidden;
  transition: all 1s ease;
}

/* Success state background transition */
.success-background {
  background-color: #0D3C14;
  background-image: none;
  animation: successPulse 2s infinite alternate;
}

@keyframes successPulse {
  from { background-color: #0D3C14; }
  to { background-color: #1B5E20; }
}

/* Login Container with improved animation */
.login-container {
  width: 100%;
  max-width: 450px;
  animation: fadeIn 0.6s ease-in-out;
  position: relative;
  z-index: 1;
  transition: transform 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.zoom-out {
  transform: scale(0.95) translateY(20px);
}

/* Enhanced branding section */
.branding-section {
  text-align: center;
  margin-bottom: 2rem;
  color: white;
  animation: fadeInDown 0.8s ease-out;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 0.5rem;
}

.logo-icon {
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.5));
  animation: pulse 3s infinite;
}

.brand-name {
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  background: linear-gradient(45deg, #fff, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-tagline {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
  font-weight: 300;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

/* Enhanced login card */
.login-card {
  border-radius: 16px !important;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.97) !important;
  padding: 1rem;
  backdrop-filter: blur(10px);
  animation: slideUp 0.5s ease-out;
}

/* Gradient text for title */
.gradient-text {
  background: linear-gradient(45deg, #1a237e, #5c6bc0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Enhanced form styling */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-field {
  transition: all 0.3s ease;
  border-radius: 8px;
}

.input-field:focus-within {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
}

.remember-me-checkbox {
  opacity: 0.85;
  transition: opacity 0.2s;
}

.remember-me-checkbox:hover {
  opacity: 1;
}

.forgot-password-btn {
  font-size: 0.85rem;
  text-transform: none;
  letter-spacing: 0;
  transition: color 0.2s ease;
}

.forgot-password-btn:hover {
  color: #303F9F !important;
  text-decoration: underline;
}

/* Enhanced login button */
.login-btn {
  margin-top: 1rem;
  height: 52px;
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.5px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(26, 35, 126, 0.3);
  transition: all 0.3s ease;
  background: linear-gradient(45deg, #1a237e, #3949ab) !important;
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.7s ease;
}

.login-btn:hover:not(:disabled)::before {
  left: 100%;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(26, 35, 126, 0.4);
}

.login-btn:active:not(:disabled) {
  transform: translateY(1px);
}

.login-btn-shake {
  animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}

.login-btn-success {
  background: linear-gradient(45deg, #2E7D32, #43A047) !important;
  box-shadow: 0 6px 15px rgba(46, 125, 50, 0.4) !important;
}

/* Enhanced signup prompt */
.signup-prompt {
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.signup-btn {
  color: var(--v-primary-base);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
}

.signup-btn:hover {
  color: #303F9F !important;
  text-decoration: underline;
}

.alert-animation {
  animation: slideDown 0.3s ease-out;
}

/* Enhanced Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0% { filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.5)); }
  50% { filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.8)); }
  100% { filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.5)); }
}

/* Advanced Responsive Design */
@media (max-width: 600px) {
  .login-page {
    padding: 1rem;
    align-items: flex-start;
    padding-top: 5vh;
  }

  .login-card {
    padding: 0.75rem;
  }

  .branding-section {
    margin-bottom: 1.5rem;
  }

  .brand-name {
    font-size: 2rem;
  }

  .brand-tagline {
    font-size: 0.9rem;
  }

  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .forgot-password-btn {
    margin-left: -8px;
  }

  .login-form {
    gap: 16px;
  }
}

/* Handle very small screens */
@media (max-width: 350px) {
  .brand-name {
    font-size: 1.75rem;
  }

  .login-card {
    padding: 0.5rem;
  }

  .login-btn {
    height: 48px;
  }
}

/* Handle landscape mode on small devices */
@media (max-height: 700px) and (orientation: landscape) {
  .login-page {
    padding-top: 1rem;
    align-items: flex-start;
  }

  .branding-section {
    margin-bottom: 0.75rem;
  }

  .brand-name {
    font-size: 1.75rem;
  }

  .brand-tagline {
    font-size: 0.85rem;
  }

  .login-form {
    gap: 12px;
  }
}

/* For non-touch devices */
@media (hover: hover) {
  .login-btn:hover {
    filter: brightness(1.05);
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .login-card {
    background: rgba(30, 30, 30, 0.95) !important;
    border-color: rgba(255, 255, 255, 0.05);
  }
}
</style>