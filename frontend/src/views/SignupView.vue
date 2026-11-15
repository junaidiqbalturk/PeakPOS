<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { signupUser } from "../services/api";

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

// Form validation state
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
  if (password.value.length >= 6) strength += 1;
  if (password.value.length >= 10) strength += 1;
  if (/[A-Z]/.test(password.value)) strength += 1;
  if (/[a-z]/.test(password.value)) strength += 1;
  if (/[0-9]/.test(password.value)) strength += 1;
  if (/[^A-Za-z0-9]/.test(password.value)) strength += 1;
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

// Validation functions
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

const nextStep = () => {
  if (validateCurrentStep()) {
    currentStep.value++;
  }
};

const prevStep = () => {
  currentStep.value--;
};

const togglePasswordVisibility = (field) => {
  if (field === 'password') {
    showPassword.value = !showPassword.value;
  } else {
    showConfirmPassword.value = !showConfirmPassword.value;
  }
};

const signup = async () => {
  errorMessage.value = "";
  successMessage.value = "";

  if (!validateCurrentStep() || !agreeToTerms.value) {
    if (!agreeToTerms.value) {
      errorMessage.value = "Please agree to the Terms of Service and Privacy Policy";
    }
    return;
  }

  loading.value = true;
  try {
    await signupUser(username.value.trim(), email.value.trim(), password.value);
    successMessage.value = "Account created successfully! Redirecting to login...";

    username.value = "";
    email.value = "";
    password.value = "";
    confirmPassword.value = "";
    agreeToTerms.value = false;

    setTimeout(() => router.push("/"), 1500);
  } catch (error) {
    errorMessage.value = error.message || error.error || "Signup failed. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="auth-wrapper">
    <!-- Left Column: Registration Form Card -->
    <div class="auth-form-panel">
      <div class="auth-content-box">
        <!-- Brand Header with Responsive Animated Logo -->
        <div class="brand-header">
          <div class="logo-aura-container">
            <img
              src="../assets/peakpos-logo.png"
              alt="PeakPOS Official Logo"
              class="official-peakpos-logo"
            />
          </div>
          <h1 class="welcome-heading">Create Account</h1>
          <p class="welcome-subtext">Start your high-speed cloud POS journey with PeakPOS</p>
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
          <div class="step-connector" :class="{ 'completed': currentStep > 1 }"></div>
          <div class="step" :class="{ 'active': currentStep >= 2, 'completed': currentStep > 2 }">
            <div class="step-indicator">
              <span v-if="currentStep > 2"><i class="material-icons">check</i></span>
              <span v-else>2</span>
            </div>
            <span class="step-label">Security</span>
          </div>
          <div class="step-connector" :class="{ 'completed': currentStep > 2 }"></div>
          <div class="step" :class="{ 'active': currentStep >= 3 }">
            <div class="step-indicator">
              <span v-if="currentStep > 3"><i class="material-icons">check</i></span>
              <span v-else>3</span>
            </div>
            <span class="step-label">Complete</span>
          </div>
        </div>

        <!-- Alert Messages -->
        <transition name="shake-fade">
          <div v-if="errorMessage" class="auth-alert error-alert">
            <i class="material-icons">error_outline</i>
            <span class="alert-text">{{ errorMessage }}</span>
            <button type="button" class="btn-dismiss-alert" @click="errorMessage = ''">
              <i class="material-icons">close</i>
            </button>
          </div>
        </transition>

        <transition name="fade">
          <div v-if="successMessage" class="auth-alert success-alert">
            <i class="material-icons">check_circle_outline</i>
            <span class="alert-text">{{ successMessage }}</span>
          </div>
        </transition>

        <!-- Form Steps -->
        <form @submit.prevent="currentStep === 3 ? signup() : nextStep()" class="auth-form" novalidate>
          <!-- Step 1: Account Information -->
          <div v-if="currentStep === 1" class="step-container">
            <h2 class="step-subheading">Store Account Information</h2>

            <div class="form-group" :class="{ 'has-error': !formValidation.username.valid }">
              <label for="reg-username">Username</label>
              <div class="input-wrapper" :class="{ 'has-content': username }">
                <i class="material-icons field-prefix-icon">person_outline</i>
                <input
                  id="reg-username"
                  v-model="username"
                  type="text"
                  placeholder="Choose your username"
                  autocomplete="username"
                  required
                  class="form-input"
                  @blur="validateUsername"
                  @input="formValidation.username.valid = true"
                />
              </div>
              <span v-if="!formValidation.username.valid" class="validation-error">
                {{ formValidation.username.message }}
              </span>
            </div>

            <div class="form-group" :class="{ 'has-error': !formValidation.email.valid }">
              <label for="reg-email">Email Address</label>
              <div class="input-wrapper" :class="{ 'has-content': email }">
                <i class="material-icons field-prefix-icon">mail_outline</i>
                <input
                  id="reg-email"
                  v-model="email"
                  type="email"
                  placeholder="owner@store.com"
                  autocomplete="email"
                  required
                  class="form-input"
                  @blur="validateEmail"
                  @input="formValidation.email.valid = true"
                />
              </div>
              <span v-if="!formValidation.email.valid" class="validation-error">
                {{ formValidation.email.message }}
              </span>
            </div>

            <button type="submit" class="btn-primary-auth">
              <span>Continue to Security</span>
              <i class="material-icons">arrow_forward</i>
            </button>
          </div>

          <!-- Step 2: Password & Security -->
          <div v-if="currentStep === 2" class="step-container">
            <h2 class="step-subheading">Set Your Security Password</h2>

            <div class="form-group" :class="{ 'has-error': !formValidation.password.valid }">
              <label for="reg-password">Password</label>
              <div class="input-wrapper" :class="{ 'has-content': password }">
                <i class="material-icons field-prefix-icon">lock_outline</i>
                <input
                  id="reg-password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Create strong password"
                  autocomplete="new-password"
                  required
                  class="form-input"
                  @blur="validatePassword"
                  @input="formValidation.password.valid = true"
                />
                <button
                  type="button"
                  class="btn-password-toggle"
                  @click="togglePasswordVisibility('password')"
                  tabindex="-1"
                >
                  <i class="material-icons">{{ showPassword ? 'visibility_off' : 'visibility' }}</i>
                </button>
              </div>
              <span v-if="!formValidation.password.valid" class="validation-error">
                {{ formValidation.password.message }}
              </span>

              <!-- Password Strength Meter -->
              <div v-if="password.length > 0" class="strength-box">
                <div class="strength-track">
                  <div
                    class="strength-fill"
                    :style="{ width: passwordStrength + '%', backgroundColor: strengthColor }"
                  ></div>
                </div>
                <span class="strength-caption" :style="{ color: strengthColor }">{{ strengthLabel }}</span>
              </div>
            </div>

            <div class="form-group" :class="{ 'has-error': !formValidation.confirmPassword.valid }">
              <label for="reg-confirm-password">Confirm Password</label>
              <div class="input-wrapper" :class="{ 'has-content': confirmPassword }">
                <i class="material-icons field-prefix-icon">verified_user</i>
                <input
                  id="reg-confirm-password"
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="Re-enter your password"
                  autocomplete="new-password"
                  required
                  class="form-input"
                  @blur="validateConfirmPassword"
                  @input="formValidation.confirmPassword.valid = true"
                />
                <button
                  type="button"
                  class="btn-password-toggle"
                  @click="togglePasswordVisibility('confirm')"
                  tabindex="-1"
                >
                  <i class="material-icons">{{ showConfirmPassword ? 'visibility_off' : 'visibility' }}</i>
                </button>
              </div>
              <span v-if="!formValidation.confirmPassword.valid" class="validation-error">
                {{ formValidation.confirmPassword.message }}
              </span>
            </div>

            <div class="form-step-actions">
              <button type="button" @click="prevStep" class="btn-step-back">
                <i class="material-icons">arrow_back</i>
                <span>Back</span>
              </button>
              <button type="submit" class="btn-primary-auth flex-1">
                <span>Review & Finish</span>
                <i class="material-icons">arrow_forward</i>
              </button>
            </div>
          </div>

          <!-- Step 3: Complete & Review -->
          <div v-if="currentStep === 3" class="step-container">
            <h2 class="step-subheading">Almost Done! Review Details</h2>

            <div class="review-details-card">
              <div class="review-row">
                <span class="review-label">Store Username:</span>
                <span class="review-val">{{ username }}</span>
              </div>
              <div class="review-row">
                <span class="review-label">Owner Email:</span>
                <span class="review-val">{{ email }}</span>
              </div>
              <div class="review-row">
                <span class="review-label">Initial Tenant:</span>
                <span class="review-val">Default Cloud Tenant</span>
              </div>
            </div>

            <!-- Terms Checkbox -->
            <div class="form-options-row">
              <label class="custom-checkbox-container">
                <input type="checkbox" v-model="agreeToTerms" />
                <span class="custom-checkbox-box"></span>
                <span class="checkbox-text-label">
                  I agree to the <a href="#" class="inline-legal-link">Terms of Service</a> &amp;
                  <a href="#" class="inline-legal-link">Privacy Policy</a>
                </span>
              </label>
            </div>

            <div class="form-step-actions">
              <button type="button" @click="prevStep" class="btn-step-back">
                <i class="material-icons">arrow_back</i>
                <span>Back</span>
              </button>
              <button
                type="submit"
                class="btn-primary-auth flex-1"
                :class="{ 'btn-loading': loading }"
                :disabled="loading || !agreeToTerms"
              >
                <div v-if="loading" class="spinner-auth"></div>
                <template v-else>
                  <span>Launch PeakPOS Store</span>
                  <i class="material-icons">rocket_launch</i>
                </template>
              </button>
            </div>
          </div>
        </form>

        <!-- Switch to Login User Journey Link -->
        <div class="auth-switch-prompt">
          <span>Already have an account?</span>
          <router-link to="/" class="switch-link">
            Sign In to Terminal
            <i class="material-icons">chevron_right</i>
          </router-link>
        </div>

        <!-- Trust Badges Footer -->
        <div class="trust-footer">
          <div class="trust-badge">
            <i class="material-icons">verified_user</i>
            <span>Role-Based Access</span>
          </div>
          <div class="trust-badge">
            <i class="material-icons">speed</i>
            <span>Sub-second POS</span>
          </div>
          <div class="trust-badge">
            <i class="material-icons">cloud_done</i>
            <span>Cloud Sync</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Brand Hero Showcase Panel (Identical Match to Login) -->
    <div class="auth-hero-panel">
      <!-- Ambient Gradient Backdrops & Orbs -->
      <div class="ambient-orb orb-1"></div>
      <div class="ambient-orb orb-2"></div>
      <div class="ambient-mesh-pattern"></div>

      <div class="hero-showcase-content">
        <!-- Main Pitch Heading -->
        <div class="hero-brand-pitch">
          <div class="pitch-badge">
            <span class="live-dot"></span>
            <span>Join 1,000+ Growing Businesses</span>
          </div>
          <h2 class="hero-headline">
            Build, Scale &amp; Automate with <span>PeakPOS</span>
          </h2>
          <p class="hero-paragraph">
            From single boutique stores to high-volume pharmacy chains, streamline inventory, multi-currency pricing, and cashier shifts with ease.
          </p>
        </div>

        <!-- 3D Glass Showcase Card -->
        <div class="terminal-showcase-card">
          <div class="showcase-card-header">
            <div class="showcase-header-left">
              <div class="pos-pulse-ring">
                <i class="material-icons">storefront</i>
              </div>
              <div>
                <h4 class="showcase-card-title">Instant Store Onboarding</h4>
                <span class="showcase-card-status">3-Minute Setup &bull; Zero Hardware Lock</span>
              </div>
            </div>
            <span class="showcase-tag">SaaS Ready</span>
          </div>

          <!-- Mini Metrics Strip -->
          <div class="showcase-metrics-grid">
            <div class="metric-mini-tile">
              <span class="metric-mini-label">Hardware</span>
              <span class="metric-mini-val">PC / Tablet / POS</span>
            </div>
            <div class="metric-mini-tile">
              <span class="metric-mini-label">Printers</span>
              <span class="metric-mini-val">ESC/POS 80mm</span>
            </div>
            <div class="metric-mini-tile">
              <span class="metric-mini-label">Isolation</span>
              <span class="metric-mini-val">100% Multi-Tenant</span>
            </div>
          </div>

          <!-- Feature Bullets inside Glass Card -->
          <div class="showcase-feature-list">
            <div class="showcase-feat-item">
              <div class="feat-icon-bullet"><i class="material-icons">category</i></div>
              <div class="feat-text">
                <strong>Categorized Visual Catalog:</strong> High-definition touch product grid with responsive search, barcodes &amp; formulas.
              </div>
            </div>
            <div class="showcase-feat-item">
              <div class="feat-icon-bullet"><i class="material-icons">currency_exchange</i></div>
              <div class="feat-text">
                <strong>Localized Store Currency:</strong> Built-in support for Pakistan Rupee (PKR Rs.), USD, AED, GBP, and custom symbols.
              </div>
            </div>
            <div class="showcase-feat-item">
              <div class="feat-icon-bullet"><i class="material-icons">manage_accounts</i></div>
              <div class="feat-text">
                <strong>Staff Management Studio:</strong> Add cashiers, managers, and admins with 4-digit terminal quick-unlock PINs.
              </div>
            </div>
          </div>
        </div>

        <!-- Verified Testimonial Quote -->
        <div class="hero-testimonial-bubble">
          <div class="star-rating">
            <i class="material-icons">star</i>
            <i class="material-icons">star</i>
            <i class="material-icons">star</i>
            <i class="material-icons">star</i>
            <i class="material-icons">star</i>
          </div>
          <p class="testimonial-quote">
            "Setting up our store on PeakPOS was completely frictionless. Within 15 minutes our inventory was uploaded and our cashiers were running sales!"
          </p>
          <div class="testimonial-author">
            <div class="author-avatar-chip">TM</div>
            <div class="author-details">
              <span class="author-name">Tariq Mahmood</span>
              <span class="author-org">Founder &amp; General Manager, PeakMart</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ==================== GLOBAL AUTH WRAPPER ==================== */
.auth-wrapper {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #0f172a;
  overflow-x: hidden;
}

/* ==================== LEFT FORM PANEL ==================== */
.auth-form-panel {
  flex: 1;
  max-width: 580px;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 3rem 2.5rem;
  box-shadow: 10px 0 30px rgba(15, 23, 42, 0.03);
  position: relative;
  z-index: 10;
  overflow-y: auto;
}

.auth-content-box {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
}

/* ==================== LOGO & ANIMATIONS ==================== */
.brand-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.logo-aura-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border-radius: 18px;
  background: #ffffff;
  margin-bottom: 0.75rem;
  position: relative;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.official-peakpos-logo {
  height: 64px;
  width: auto;
  max-width: 190px;
  object-fit: contain;
  filter: drop-shadow(0 6px 16px rgba(99, 102, 241, 0.22));
  animation: peakLogoFloat 5s ease-in-out infinite, peakLogoGlow 4s ease-in-out infinite alternate;
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.35s ease;
}

.official-peakpos-logo:hover {
  transform: translateY(-4px) scale(1.06);
  filter: drop-shadow(0 10px 24px rgba(124, 58, 237, 0.45));
}

@keyframes peakLogoFloat {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-4px) rotate(0.6deg);
  }
}

@keyframes peakLogoGlow {
  0% {
    filter: drop-shadow(0 4px 12px rgba(99, 102, 241, 0.18));
  }
  100% {
    filter: drop-shadow(0 8px 22px rgba(124, 58, 237, 0.38));
  }
}

.welcome-heading {
  font-size: 1.85rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.03em;
  margin: 0 0 0.35rem 0;
}

.welcome-subtext {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
  line-height: 1.45;
}

/* ==================== PROGRESS STEPS ==================== */
.progress-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 1.25rem 0 1.75rem 0;
  position: relative;
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
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #f8fafc;
  border: 2px solid #e2e8f0;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
  margin-bottom: 0.35rem;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.step.active .step-indicator {
  background-color: #4f46e5;
  border-color: #4f46e5;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.step.completed .step-indicator {
  background-color: #10b981;
  border-color: #10b981;
  color: #ffffff;
}

.step-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #64748b;
  transition: color 0.3s ease;
}

.step.active .step-label {
  color: #4f46e5;
  font-weight: 700;
}

.step.completed .step-label {
  color: #10b981;
}

.step-connector {
  flex: 1;
  height: 2px;
  background-color: #e2e8f0;
  margin: 0 -8px 18px -8px;
  z-index: 1;
  transition: background-color 0.3s ease;
}

.step-connector.completed {
  background-color: #10b981;
}

/* ==================== ALERT FEEDBACK ==================== */
.auth-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  font-size: 0.88rem;
  margin-bottom: 1.25rem;
  animation: slideDown 0.3s ease;
}

.error-alert {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.success-alert {
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.alert-text {
  flex: 1;
  font-weight: 500;
  line-height: 1.35;
}

.btn-dismiss-alert {
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 2px;
  display: flex;
}

.btn-dismiss-alert i {
  font-size: 16px;
}

/* ==================== FORM ELEMENTS ==================== */
.auth-form {
  display: flex;
  flex-direction: column;
}

.step-container {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  animation: stepFade 0.3s ease;
}

@keyframes stepFade {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.step-subheading {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #334155;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  transition: all 0.25s ease;
}

.input-wrapper:focus-within {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3.5px rgba(99, 102, 241, 0.12);
}

.form-group.has-error .input-wrapper {
  border-color: #ef4444;
  background: #fff5f5;
}

.field-prefix-icon {
  position: absolute;
  left: 12px;
  color: #94a3b8;
  font-size: 20px;
  pointer-events: none;
  transition: color 0.25s ease;
}

.input-wrapper:focus-within .field-prefix-icon {
  color: #4f46e5;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 42px 0 42px;
  border: none;
  background: transparent;
  font-size: 0.95rem;
  color: #0f172a;
  outline: none;
  font-family: inherit;
}

.form-input::placeholder {
  color: #94a3b8;
}

.btn-password-toggle {
  position: absolute;
  right: 12px;
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  padding: 4px;
  border-radius: 6px;
  transition: color 0.2s ease;
}

.btn-password-toggle:hover {
  color: #4f46e5;
}

.btn-password-toggle i {
  font-size: 20px;
}

.validation-error {
  font-size: 0.8rem;
  color: #ef4444;
  font-weight: 500;
  margin-top: 2px;
}

/* ==================== PASSWORD STRENGTH ==================== */
.strength-box {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 6px;
}

.strength-track {
  flex: 1;
  height: 5px;
  background: #e2e8f0;
  border-radius: 9999px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: width 0.3s ease, background-color 0.3s ease;
}

.strength-caption {
  font-size: 0.78rem;
  font-weight: 700;
  min-width: 50px;
}

/* ==================== STEP 3: REVIEW CARD ==================== */
.review-details-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.review-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.review-label {
  color: #64748b;
  font-weight: 500;
}

.review-val {
  font-weight: 700;
  color: #0f172a;
}

/* ==================== CUSTOM CHECKBOX ==================== */
.form-options-row {
  display: flex;
  align-items: center;
  margin-top: 0.25rem;
}

.custom-checkbox-container {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.custom-checkbox-container input {
  display: none;
}

.custom-checkbox-box {
  width: 18px;
  height: 18px;
  border-radius: 5px;
  border: 1.5px solid #cbd5e1;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.custom-checkbox-container input:checked + .custom-checkbox-box {
  background: #4f46e5;
  border-color: #4f46e5;
}

.custom-checkbox-container input:checked + .custom-checkbox-box::after {
  content: "";
  width: 4.5px;
  height: 9px;
  border: solid #ffffff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
  margin-bottom: 2px;
}

.checkbox-text-label {
  font-size: 0.86rem;
  font-weight: 500;
  color: #475569;
  line-height: 1.4;
}

.inline-legal-link {
  color: #4f46e5;
  text-decoration: none;
  font-weight: 600;
}

.inline-legal-link:hover {
  text-decoration: underline;
}

/* ==================== BUTTONS ==================== */
.form-step-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.flex-1 {
  flex: 1;
}

.btn-step-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 50px;
  padding: 0 1.25rem;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  background: #f8fafc;
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-step-back:hover {
  background: #f1f5f9;
  color: #1e293b;
  border-color: #cbd5e1;
}

.btn-primary-auth {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 50px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  color: #ffffff;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-top: 0.5rem;
}

.btn-primary-auth:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 22px rgba(124, 58, 237, 0.45);
  background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
}

.btn-primary-auth:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary-auth:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner-auth {
  width: 22px;
  height: 22px;
  border: 2.5px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #ffffff;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ==================== SWITCH PROMPT ==================== */
.auth-switch-prompt {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #64748b;
  flex-wrap: wrap;
}

.switch-link {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-weight: 700;
  color: #4f46e5;
  text-decoration: none;
  transition: all 0.2s ease;
}

.switch-link:hover {
  color: #3730a3;
  text-decoration: underline;
  transform: translateX(2px);
}

.switch-link i {
  font-size: 16px;
}

/* ==================== TRUST FOOTER ==================== */
.trust-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.25rem;
  margin-top: 2rem;
  padding-top: 1.25rem;
  border-top: 1px solid #f1f5f9;
  flex-wrap: wrap;
}

.trust-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
}

.trust-badge i {
  font-size: 16px;
  color: #4f46e5;
}

/* ==================== RIGHT HERO SHOWCASE PANEL ==================== */
.auth-hero-panel {
  flex: 1.2;
  background: linear-gradient(145deg, #2e1065 0%, #4338ca 40%, #6366f1 85%, #7c3aed 100%);
  color: #ffffff;
  padding: 4rem 3.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.ambient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}

.orb-1 {
  width: 400px;
  height: 400px;
  top: -80px;
  right: -80px;
  background: rgba(124, 58, 237, 0.4);
}

.orb-2 {
  width: 350px;
  height: 350px;
  bottom: -60px;
  left: -60px;
  background: rgba(99, 102, 241, 0.45);
}

.ambient-mesh-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 24px 24px;
  opacity: 0.5;
  pointer-events: none;
}

.hero-showcase-content {
  width: 100%;
  max-width: 540px;
  position: relative;
  z-index: 5;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Brand Pitch */
.pitch-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 0.4rem 0.9rem;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  margin-bottom: 1rem;
  backdrop-filter: blur(10px);
}

.live-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 10px #34d399;
  animation: pulseDot 2s infinite;
}

@keyframes pulseDot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.hero-headline {
  font-size: 2.25rem;
  font-weight: 800;
  line-height: 1.25;
  margin: 0 0 1rem 0;
  letter-spacing: -0.02em;
}

.hero-headline span {
  background: linear-gradient(120deg, #ffffff 0%, #ddd6fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-paragraph {
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
}

/* 3D Glass Showcase Card */
.terminal-showcase-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 20px;
  padding: 1.75rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.terminal-showcase-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 26px 55px rgba(0, 0, 0, 0.35);
}

.showcase-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.showcase-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pos-pulse-ring {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.pos-pulse-ring i {
  font-size: 24px;
}

.showcase-card-title {
  font-size: 1.05rem;
  font-weight: 700;
  margin: 0;
  color: #ffffff;
}

.showcase-card-status {
  font-size: 0.78rem;
  color: #a7f3d0;
  font-weight: 600;
}

.showcase-tag {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  background: rgba(99, 102, 241, 0.35);
  border: 1px solid rgba(167, 139, 250, 0.4);
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  letter-spacing: 0.05em;
}

.showcase-metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.metric-mini-tile {
  background: rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 0.6rem 0.75rem;
  display: flex;
  flex-direction: column;
}

.metric-mini-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: rgba(255, 255, 255, 0.65);
}

.metric-mini-val {
  font-size: 0.95rem;
  font-weight: 700;
  color: #ffffff;
  margin-top: 2px;
}

.showcase-feature-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.showcase-feat-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.feat-icon-bullet {
  width: 26px;
  height: 26px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #c4b5fd;
  margin-top: 2px;
}

.feat-icon-bullet i {
  font-size: 16px;
}

.feat-text {
  font-size: 0.85rem;
  line-height: 1.45;
  color: rgba(255, 255, 255, 0.9);
}

.feat-text strong {
  color: #ffffff;
}

/* Testimonial Bubble */
.hero-testimonial-bubble {
  background: rgba(0, 0, 0, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 1.25rem 1.5rem;
  backdrop-filter: blur(12px);
}

.star-rating {
  display: flex;
  gap: 2px;
  color: #facc15;
  margin-bottom: 0.5rem;
}

.star-rating i {
  font-size: 16px;
}

.testimonial-quote {
  font-size: 0.9rem;
  font-style: italic;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.92);
  margin: 0 0 0.85rem 0;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 10px;
}

.author-avatar-chip {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #ffffff;
}

.author-details {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #ffffff;
}

.author-org {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.65);
}

/* ==================== TRANSITIONS ==================== */
.shake-fade-enter-active {
  animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97);
}

.shake-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.shake-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* ==================== RESPONSIVENESS ==================== */
@media (max-width: 1024px) {
  .auth-hero-panel {
    display: none;
  }

  .auth-form-panel {
    max-width: 100%;
    padding: 3rem 1.5rem;
  }

  .auth-content-box {
    max-width: 480px;
  }
}

@media (max-width: 640px) {
  .auth-form-panel {
    padding: 2rem 1.25rem;
  }

  .official-peakpos-logo {
    height: 52px;
  }

  .welcome-heading {
    font-size: 1.6rem;
  }

  .trust-footer {
    gap: 0.75rem;
  }
}
</style>
