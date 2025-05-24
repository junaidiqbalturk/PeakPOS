<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { signupUser } from "../services/api"; // Import the signup function

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const successMessage = ref("");
const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const currentStep = ref(1);
const agreeToTerms = ref(false);

// Form validation
const formValidation = ref({
  username: { valid: true, message: "" },
  email: { valid: true, message: "" },
  password: { valid: true, message: "" },
  confirmPassword: { valid: true, message: "" }
});

// Password strength calculation
const passwordStrength = computed(() => {
  if (!password.value) return 0;

  let strength = 0;

  // Length check
  if (password.value.length >= 6) strength += 1;
  if (password.value.length >= 10) strength += 1;

  // Complexity checks
  if (/[A-Z]/.test(password.value)) strength += 1; // Has uppercase
  if (/[a-z]/.test(password.value)) strength += 1; // Has lowercase
  if (/[0-9]/.test(password.value)) strength += 1; // Has number
  if (/[^A-Za-z0-9]/.test(password.value)) strength += 1; // Has special char

  return Math.min(Math.floor((strength / 6) * 100), 100);
});

const strengthLabel = computed(() => {
  const strength = passwordStrength.value;
  if (strength === 0) return "";
  if (strength < 40) return "Weak";
  if (strength < 70) return "Medium";
  return "Strong";
});

const strengthColor = computed(() => {
  const strength = passwordStrength.value;
  if (strength < 40) return "#ef4444";
  if (strength < 70) return "#f59e0b";
  return "#10b981";
});

// Form validation functions
const validateUsername = () => {
  if (!username.value.trim()) {
    formValidation.value.username = { valid: false, message: "Username is required" };
    return false;
  }
  if (username.value.length < 3) {
    formValidation.value.username = { valid: false, message: "Username must be at least 3 characters" };
    return false;
  }
  formValidation.value.username = { valid: true, message: "" };
  return true;
};

const validateEmail = () => {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.value.trim()) {
    formValidation.value.email = { valid: false, message: "Email is required" };
    return false;
  }
  if (!emailPattern.test(email.value)) {
    formValidation.value.email = { valid: false, message: "Please enter a valid email address" };
    return false;
  }
  formValidation.value.email = { valid: true, message: "" };
  return true;
};

const validatePassword = () => {
  if (!password.value) {
    formValidation.value.password = { valid: false, message: "Password is required" };
    return false;
  }
  if (password.value.length < 6) {
    formValidation.value.password = { valid: false, message: "Password must be at least 6 characters" };
    return false;
  }
  formValidation.value.password = { valid: true, message: "" };
  return true;
};

const validateConfirmPassword = () => {
  if (!confirmPassword.value) {
    formValidation.value.confirmPassword = { valid: false, message: "Please confirm your password" };
    return false;
  }
  if (password.value !== confirmPassword.value) {
    formValidation.value.confirmPassword = { valid: false, message: "Passwords do not match" };
    return false;
  }
  formValidation.value.confirmPassword = { valid: true, message: "" };
  return true;
};

const validateCurrentStep = () => {
  if (currentStep.value === 1) {
    const isUsernameValid = validateUsername();
    const isEmailValid = validateEmail();
    return isUsernameValid && isEmailValid;
  } else if (currentStep.value === 2) {
    const isPasswordValid = validatePassword();
    const isConfirmPasswordValid = validateConfirmPassword();
    return isPasswordValid && isConfirmPasswordValid;
  }
  return true;
};

// Navigation between steps
const nextStep = () => {
  if (validateCurrentStep()) {
    currentStep.value++;
  }
};

const prevStep = () => {
  currentStep.value--;
};

// Toggle password visibility
const togglePasswordVisibility = (field) => {
  if (field === 'password') {
    showPassword.value = !showPassword.value;
  } else {
    showConfirmPassword.value = !showConfirmPassword.value;
  }
};

// Signup function
const signup = async () => {
  // Clear any previous messages
  errorMessage.value = "";
  successMessage.value = "";

  // Validate form
  if (!validateCurrentStep() || !agreeToTerms.value) {
    if (!agreeToTerms.value) {
      errorMessage.value = "Please agree to the Terms of Service and Privacy Policy";
    }
    return;
  }

  loading.value = true;
  try {
    await signupUser(username.value, email.value, password.value);
    successMessage.value = "Account created successfully! Redirecting to login...";

    // Reset form fields
    username.value = "";
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    agreeToTerms.value = false;

    // Redirect after a short delay
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
    <div class="signup-card">
      <!-- Logo and Header -->
      <div class="card-header">
        <img src="../assets/logo-pp.png" alt="PeakPOS Logo" class="header-logo">
        <h1>Create Account</h1>
        <p class="subtitle">Start your journey with PeakPOS</p>
      </div>

      <!-- Progress Steps -->
      <div class="progress-steps">
        <div class="step" :class="{ 'active': currentStep >= 1, 'completed': currentStep > 1 }">
          <div class="step-indicator">
            <span v-if="currentStep > 1"><i class="material-icons">check</i></span>
            <span v-else>1</span>
          </div>
          <span class="step-label">Account Info</span>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'active': currentStep >= 2, 'completed': currentStep > 2 }">
          <div class="step-indicator">
            <span v-if="currentStep > 2"><i class="material-icons">check</i></span>
            <span v-else>2</span>
          </div>
          <span class="step-label">Security</span>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'active': currentStep >= 3 }">
          <div class="step-indicator">
            <span v-if="currentStep > 3"><i class="material-icons">check</i></span>
            <span v-else>3</span>
          </div>
          <span class="step-label">Complete</span>
        </div>
      </div>

      <!-- Alert Messages -->
      <transition name="fade">
        <div v-if="errorMessage" class="alert error">
          <i class="material-icons">error_outline</i>
          <span>{{ errorMessage }}</span>
          <button @click="errorMessage = ''" class="alert-close">
            <i class="material-icons">close</i>
          </button>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="successMessage" class="alert success">
          <i class="material-icons">check_circle_outline</i>
          <span>{{ successMessage }}</span>
        </div>
      </transition>

      <!-- Form Steps -->
      <form @submit.prevent="currentStep === 3 ? signup() : nextStep()" class="signup-form">
        <!-- Step 1: Account Information -->
        <div v-if="currentStep === 1" class="form-step">
          <h2 class="step-title">Account Information</h2>

          <div class="form-group" :class="{ 'has-error': !formValidation.username.valid }">
            <label for="username">Username</label>
            <div class="input-field">
              <i class="material-icons icon-prefix">person</i>
              <input
                id="username"
                v-model="username"
                type="text"
                placeholder="Choose a username"
                @blur="validateUsername"
                @input="formValidation.username.valid = true"
              />
            </div>
            <div v-if="!formValidation.username.valid" class="error-text">
              {{ formValidation.username.message }}
            </div>
          </div>

          <div class="form-group" :class="{ 'has-error': !formValidation.email.valid }">
            <label for="email">Email Address</label>
            <div class="input-field">
              <i class="material-icons icon-prefix">email</i>
              <input
                id="email"
                v-model="email"
                type="email"
                placeholder="Enter your email"
                @blur="validateEmail"
                @input="formValidation.email.valid = true"
              />
            </div>
            <div v-if="!formValidation.email.valid" class="error-text">
              {{ formValidation.email.message }}
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="router.push('/login')" class="btn-text">
              Already have an account?
            </button>
            <button type="submit" class="btn-primary">
              Continue <i class="material-icons">arrow_forward</i>
            </button>
          </div>
        </div>

        <!-- Step 2: Security -->
        <div v-if="currentStep === 2" class="form-step">
          <h2 class="step-title">Set Your Password</h2>

          <div class="form-group" :class="{ 'has-error': !formValidation.password.valid }">
            <label for="password">Password</label>
            <div class="input-field">
              <i class="material-icons icon-prefix">lock</i>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Create a secure password"
                @blur="validatePassword"
                @input="formValidation.password.valid = true"
              />
              <button
                type="button"
                class="icon-suffix"
                @click="togglePasswordVisibility('password')"
                tabindex="-1"
              >
                <i class="material-icons">{{ showPassword ? 'visibility_off' : 'visibility' }}</i>
              </button>
            </div>
            <div v-if="!formValidation.password.valid" class="error-text">
              {{ formValidation.password.message }}
            </div>
            <div v-else-if="password.length > 0" class="password-strength-indicator">
              <div class="strength-bar-container">
                <div class="strength-bar" :style="{ width: passwordStrength + '%', backgroundColor: strengthColor }"></div>
              </div>
              <span class="strength-label" :style="{ color: strengthColor }">{{ strengthLabel }}</span>
            </div>
            <div v-if="password.length > 0" class="password-tips">
              <div class="tip-item" :class="{ 'satisfied': password.length >= 6 }">
                <i class="material-icons">{{ password.length >= 6 ? 'check_circle' : 'radio_button_unchecked' }}</i>
                <span>At least 6 characters</span>
              </div>
              <div class="tip-item" :class="{ 'satisfied': /[A-Z]/.test(password) }">
                <i class="material-icons">{{ /[A-Z]/.test(password) ? 'check_circle' : 'radio_button_unchecked' }}</i>
                <span>At least 1 uppercase letter</span>
              </div>
              <div class="tip-item" :class="{ 'satisfied': /[0-9]/.test(password) }">
                <i class="material-icons">{{ /[0-9]/.test(password) ? 'check_circle' : 'radio_button_unchecked' }}</i>
                <span>At least 1 number</span>
              </div>
            </div>
          </div>

          <div class="form-group" :class="{ 'has-error': !formValidation.confirmPassword.valid }">
            <label for="confirmPassword">Confirm Password</label>
            <div class="input-field">
              <i class="material-icons icon-prefix">lock_outline</i>
              <input
                id="confirmPassword"
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Confirm your password"
                @blur="validateConfirmPassword"
                @input="formValidation.confirmPassword.valid = true"
              />
              <button
                type="button"
                class="icon-suffix"
                @click="togglePasswordVisibility('confirm')"
                tabindex="-1"
              >
                <i class="material-icons">{{ showConfirmPassword ? 'visibility_off' : 'visibility' }}</i>
              </button>
            </div>
            <div v-if="!formValidation.confirmPassword.valid" class="error-text">
              {{ formValidation.confirmPassword.message }}
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="prevStep" class="btn-secondary">
              <i class="material-icons">arrow_back</i> Back
            </button>
            <button type="submit" class="btn-primary">
              Continue <i class="material-icons">arrow_forward</i>
            </button>
          </div>
        </div>

        <!-- Step 3: Final Step -->
        <div v-if="currentStep === 3" class="form-step">
          <h2 class="step-title">Almost Done</h2>

          <div class="account-summary">
            <div class="summary-item">
              <div class="summary-label">Username</div>
              <div class="summary-value">{{ username }}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">Email</div>
              <div class="summary-value">{{ email }}</div>
            </div>
          </div>

          <div class="form-group checkbox-group">
            <label class="checkbox-container">
              <input type="checkbox" v-model="agreeToTerms" />
              <span class="checkbox-mark"></span>
              <span class="checkbox-text">
                I agree to the <a href="#" class="link">Terms of Service</a> and <a href="#" class="link">Privacy Policy</a>
              </span>
            </label>
          </div>

          <div class="form-actions">
            <button type="button" @click="prevStep" class="btn-secondary">
              <i class="material-icons">arrow_back</i> Back
            </button>
            <button type="submit" class="btn-primary" :class="{ 'loading': loading }" :disabled="loading || !agreeToTerms">
              <span v-if="!loading">Create Account</span>
              <div v-else class="spinner"></div>
            </button>
          </div>
        </div>
      </form>

      <!-- Bottom Info -->
      <div class="card-footer">
        <div class="footer-info">
          <p>By signing up, you will get full access to:</p>
          <div class="features-list">
            <div class="feature">
              <i class="material-icons">shopping_cart</i>
              <span>POS Management</span>
            </div>
            <div class="feature">
              <i class="material-icons">inventory</i>
              <span>Inventory Tracking</span>
            </div>
            <div class="feature">
              <i class="material-icons">bar_chart</i>
              <span>Analytics Dashboard</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Illustration Panel (visible on larger screens) -->
    <div class="illustration-panel">
      <div class="illustration">
        <img src="../assets/illustration.svg" alt="Illustration" class="illustration-image" />
      </div>
      <div class="illustration-content">
        <h2>Transform Your Business with PeakPOS</h2>
        <p>Join thousands of businesses already using our platform to streamline operations and boost growth</p>

        <div class="testimonials">
          <div class="testimonial">
            <div class="quote">"PeakPOS revolutionized how we manage our store. Sales are up 30% since we started using it!"</div>
            <div class="author">
              <div class="author-avatar">JD</div>
              <div class="author-info">
                <div class="author-name">John Doe</div>
                <div class="author-title">Owner, Retail Store</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base Styles */
.signup-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(120deg, #f8fafc 0%, #eef2ff 100%);
  color: #1e293b;
}

/* Card Styles */
.signup-card {
  flex: 1;
  max-width: 600px;
  padding: 2.5rem;
  background-color: white;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.header-logo {
  height: 60px;
  margin-bottom: 1.5rem;
}

.card-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #64748b;
  font-size: 1rem;
}

/* Progress Steps */
.progress-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
  padding: 0 1rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 2;
  flex: 1;
}

.step-indicator {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f8fafc;
  border: 2px solid #e2e8f0;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.step-label {
  font-size: 0.875rem;
  color: #64748b;
  transition: color 0.3s ease;
}

.step.active .step-indicator {
  background-color: #4f46e5;
  border-color: #4f46e5;
  color: white;
}

.step.active .step-label {
  color: #4f46e5;
  font-weight: 600;
}

.step.completed .step-indicator {
  background-color: #4f46e5;
  border-color: #4f46e5;
  color: white;
}

.step-connector {
  flex: 1;
  height: 2px;
  background-color: #e2e8f0;
  z-index: 1;
  margin: 0 -10px;
  margin-top: -20px;
  transition: background-color 0.3s ease;
}

.step.completed + .step-connector {
  background-color: #4f46e5;
}

/* Alert Styles */
.alert {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  position: relative;
}

.alert.error {
  background-color: #fef2f2;
  color: #ef4444;
  border-left: 4px solid #ef4444;
}

.alert.success {
  background-color: #f0fdf4;
  color: #10b981;
  border-left: 4px solid #10b981;
}

.alert i {
  margin-right: 10px;
  font-size: 20px;
}

.alert-close {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 0;
  display: flex;
}

/* Form Styles */
.signup-form {
  flex: 1;
}

.form-step {
  animation: slideIn 0.3s ease;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #1e293b;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #334155;
}

.input-field {
  display: flex;
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #f8fafc;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.input-field:focus-within {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.has-error .input-field {
  border-color: #ef4444;
  background-color: #fef2f2;
}

.icon-prefix {
  padding: 0 12px;
  color: #64748b;
  display: flex;
  align-items: center;
}

.input-field input {
  flex: 1;
  padding: 12px 8px;
  border: none;
  background: transparent;
  font-size: 1rem;
  color: #1e293b;
  outline: none;
}

.input-field input::placeholder {
  color: #94a3b8;
}

.icon-suffix {
  padding: 0 12px;
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.icon-suffix:hover {
  color: #4f46e5;
}

.error-text {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
}

/* Password Strength */
.password-strength-indicator {
  margin-top: 0.75rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.strength-bar-container {
  flex: 1;
  height: 4px;
  background-color: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.strength-bar {
  height: 100%;
  width: 0;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.strength-label {
  font-size: 0.75rem;
  font-weight: 600;
}

.password-tips {
  margin-top: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: #64748b;
}

.tip-item i {
  font-size: 16px;
  color: #94a3b8;
}

.tip-item.satisfied {
  color: #10b981;
}

.tip-item.satisfied i {
  color: #10b981;
}

/* Checkbox Styles */
.checkbox-group {
  margin-bottom: 1rem;
}

.checkbox-container {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  user-select: none;
}

.checkbox-mark {
  display: inline-block;
  width: 20px;
  height: 20px;
  background-color: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 4px;
  margin-right: 10px;
  position: relative;
  flex-shrink: 0;
  margin-top: 2px;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkbox-container input:checked ~ .checkbox-mark {
  background-color: #4f46e5;
  border-color: #4f46e5;
}

.checkbox-container input:checked ~ .checkbox-mark:after {
  content: "";
  position: absolute;
  left: 6px;
  top: 2px;
  width: 6px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-text {
  font-size: 0.875rem;
  color: #334155;
  line-height: 1.4;
}

.link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
}

/* Button Styles */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
}

.btn-primary {
  background-color: #4f46e5;
  color: white;
}

.btn-primary:hover {
  background-color: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.btn-primary:disabled {
  background-color: #c7d2fe;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-secondary {
  background-color: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.btn-secondary:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

.btn-text {
  background: transparent;
  border: none;
  color: #4f46e5;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
}

.btn-text:hover {
  text-decoration: underline;
}

.loading {
  position: relative;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Account Summary */
.account-summary {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.summary-item {
  display: flex;
  margin-bottom: 0.75rem;
  align-items: center;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.summary-label {
  width: 100px;
  font-weight: 500;
  color: #64748b;
}

.summary-value {
  flex: 1;
  color: #1e293b;
  font-weight: 500;
}

/* Card Footer */
.card-footer {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.footer-info p {
  text-align: center;
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.features-list {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.feature i {
  font-size: 1.5rem;
  color: #4f46e5;
}

.feature span {
  font-size: 0.75rem;
  color: #334155;
  text-align: center;
}

/* Illustration Panel */
.illustration-panel {
  flex: 1;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
  display: none;
}

.illustration {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}

.illustration-image {
  max-width: 100%;
  max-height: 350px;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-15px);
  }
  100% {
    transform: translateY(0);
  }
}

.illustration-content {
  text-align: center;
}

.illustration-content h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.illustration-content p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

/* Testimonials */
.testimonials {
  margin-top: 2rem;
}

.testimonial {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
}

.quote {
  font-size: 1rem;
  font-style: italic;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.author-name {
  font-weight: 600;
}

.author-title {
  font-size: 0.75rem;
  opacity: 0.8;
}

/* Animations */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive Styles */
@media (min-width: 1024px) {
  .illustration-panel {
    display: flex;
  }
}

@media (max-width: 1200px) {
  .signup-card {
    padding: 2rem;
  }
}

@media (max-width: 768px) {
  .signup-card {
    padding: 1.5rem;
    max-width: 100%;
  }

  .form-actions {
    flex-direction: column-reverse;
    gap: 1rem;
  }

  .btn-primary, .btn-secondary, .btn-text {
    width: 100%;
    justify-content: center;
  }

  .features-list {
    flex-wrap: wrap;
  }

  .feature {
    flex: 0 0 33.333%;
  }
}

@media (max-width: 640px) {
  .signup-card {
    padding: 1.25rem;
  }

  .header-logo {
    height: 50px;
  }

  .step-label {
    font-size: 0.75rem;
  }

  .step-indicator {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 480px) {
  .signup-card {
    padding: 1rem;
  }

  .progress-steps {
    margin-bottom: 1.5rem;
  }

  .step-label {
    display: none;
  }

  .step-indicator {
    width: 28px;
    height: 28px;
    font-size: 0.75rem;
  }

  .step-indicator i {
    font-size: 14px;
  }

  .features-list {
    gap: 0.75rem;
  }
}
</style>