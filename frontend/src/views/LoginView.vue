<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { loginUser } from "../services/api";

const router = useRouter();
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);
const passwordVisible = ref(false);
const rememberMe = ref(false);
const loginSuccess = ref(false);
const showForgotModal = ref(false);

const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};

// Quick demo login credential filler
const fillCredentials = (type) => {
  if (type === 'admin') {
    email.value = 'admin@peakpos.com';
    password.value = 'admin123';
  } else if (type === 'cashier') {
    email.value = 'cashier@peakpos.com';
    password.value = 'cashier123';
  }
  errorMessage.value = '';
};

// Primary Login Handler
const handleLogin = async () => {
  if (!email.value.trim() || !password.value) {
    errorMessage.value = "Please enter both email and password.";
    return;
  }

  loading.value = true;
  errorMessage.value = "";

  try {
    const response = await loginUser(email.value.trim(), password.value);
    loginSuccess.value = true;

    // Secure local storage persistence
    localStorage.setItem("token", response.token);
    localStorage.setItem("isAuthenticated", "true");
    localStorage.setItem("role", response.role || "cashier");
    localStorage.setItem("username", response.username || "");

    if (response.tenant) {
      localStorage.setItem("tenant", JSON.stringify(response.tenant));
      if (response.tenant.currency_symbol) {
        localStorage.setItem("currency_symbol", response.tenant.currency_symbol);
      }
      if (response.tenant.currency) {
        localStorage.setItem("store_currency", response.tenant.currency);
      }
    }

    if (rememberMe.value) {
      localStorage.setItem("rememberedEmail", email.value.trim());
    } else {
      localStorage.removeItem("rememberedEmail");
    }

    // Broadcast auth changes to components
    window.dispatchEvent(new Event('auth-changed'));
    window.dispatchEvent(new Event('currency-changed'));

    // Role-based redirect
    setTimeout(() => {
      const userRole = (response.role || "cashier").toLowerCase();
      if (userRole === "cashier") {
        router.push("/sales");
      } else {
        router.push("/dashboard");
      }
    }, 700);
  } catch (error) {
    errorMessage.value = error.message || error.error || "Invalid email or password. Please try again.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  const remembered = localStorage.getItem("rememberedEmail");
  if (remembered) {
    email.value = remembered;
    rememberMe.value = true;
  }
});
</script>

<template>
  <div class="auth-wrapper">
    <!-- Left Column: Authentication Form Card -->
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
          <h1 class="welcome-heading">Welcome Back</h1>
          <p class="welcome-subtext">Sign in to manage your store, inventory, and point-of-sale terminal</p>
        </div>

        <!-- Quick Demo Credentials Bar -->
        <div class="quick-demo-strip">
          <span class="demo-strip-label">Fast Demo Fill:</span>
          <div class="demo-pills">
            <button
              type="button"
              class="demo-pill admin-pill"
              @click="fillCredentials('admin')"
              title="Fill Admin credentials"
            >
              <i class="material-icons">admin_panel_settings</i>
              <span>Admin</span>
            </button>
            <button
              type="button"
              class="demo-pill cashier-pill"
              @click="fillCredentials('cashier')"
              title="Fill Cashier credentials"
            >
              <i class="material-icons">point_of_sale</i>
              <span>Cashier</span>
            </button>
          </div>
        </div>

        <!-- Error Feedback Banner -->
        <transition name="shake-fade">
          <div v-if="errorMessage" class="auth-alert error-alert">
            <i class="material-icons">error_outline</i>
            <span class="alert-text">{{ errorMessage }}</span>
            <button type="button" class="btn-dismiss-alert" @click="errorMessage = ''">
              <i class="material-icons">close</i>
            </button>
          </div>
        </transition>

        <!-- Main Login Form -->
        <form @submit.prevent="handleLogin" class="auth-form" novalidate>
          <!-- Email Input Group -->
          <div class="form-group">
            <label for="login-email">Email Address</label>
            <div class="input-wrapper" :class="{ 'has-content': email }">
              <i class="material-icons field-prefix-icon">mail_outline</i>
              <input
                id="login-email"
                type="email"
                v-model="email"
                placeholder="name@company.com"
                autocomplete="email"
                required
                class="form-input"
              />
            </div>
          </div>

          <!-- Password Input Group -->
          <div class="form-group">
            <div class="label-row">
              <label for="login-password">Password</label>
              <button
                type="button"
                class="btn-inline-link"
                @click="showForgotModal = true"
              >
                Forgot Password?
              </button>
            </div>
            <div class="input-wrapper" :class="{ 'has-content': password }">
              <i class="material-icons field-prefix-icon">lock_outline</i>
              <input
                id="login-password"
                :type="passwordVisible ? 'text' : 'password'"
                v-model="password"
                placeholder="Enter your password"
                autocomplete="current-password"
                required
                class="form-input"
              />
              <button
                type="button"
                class="btn-password-toggle"
                @click="togglePasswordVisibility"
                :title="passwordVisible ? 'Hide password' : 'Show password'"
                tabindex="-1"
              >
                <i class="material-icons">{{ passwordVisible ? 'visibility_off' : 'visibility' }}</i>
              </button>
            </div>
          </div>

          <!-- Options Row: Remember Me -->
          <div class="form-options-row">
            <label class="custom-checkbox-container">
              <input type="checkbox" v-model="rememberMe" />
              <span class="custom-checkbox-box"></span>
              <span class="checkbox-text-label">Remember my login</span>
            </label>
          </div>

          <!-- Submit CTA Button -->
          <button
            type="submit"
            class="btn-primary-auth"
            :class="{ 'btn-loading': loading, 'btn-success': loginSuccess }"
            :disabled="loading || loginSuccess"
          >
            <div v-if="loading" class="spinner-auth"></div>
            <template v-else-if="loginSuccess">
              <i class="material-icons">check_circle</i>
              <span>Access Granted &bull; Redirecting...</span>
            </template>
            <template v-else>
              <span>Sign In to Terminal</span>
              <i class="material-icons">arrow_forward</i>
            </template>
          </button>
        </form>

        <!-- Switch to Signup User Journey Link -->
        <div class="auth-switch-prompt">
          <span>Don't have a PeakPOS store yet?</span>
          <router-link to="/signup" class="switch-link">
            Create an Account
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

    <!-- Right Column: Brand Hero Showcase Panel -->
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
            <span>Next-Generation Retail & Pharmacy POS</span>
          </div>
          <h2 class="hero-headline">
            Transform Your Store Operations with <span>PeakPOS</span>
          </h2>
          <p class="hero-paragraph">
            The ultra-fast, multi-tenant cloud point-of-sale engineered for seamless retail, grocery, and pharmacy checkout.
          </p>
        </div>

        <!-- 3D Glass Showcase Card (Interactive Terminal Preview) -->
        <div class="terminal-showcase-card">
          <div class="showcase-card-header">
            <div class="showcase-header-left">
              <div class="pos-pulse-ring">
                <i class="material-icons">point_of_sale</i>
              </div>
              <div>
                <h4 class="showcase-card-title">PeakPOS High-Speed Terminal</h4>
                <span class="showcase-card-status">Online &bull; Ready for Checkout</span>
              </div>
            </div>
            <span class="showcase-tag">Kiosk Mode</span>
          </div>

          <!-- Mini Metrics Strip -->
          <div class="showcase-metrics-grid">
            <div class="metric-mini-tile">
              <span class="metric-mini-label">Scan Speed</span>
              <span class="metric-mini-val">0.3s</span>
            </div>
            <div class="metric-mini-tile">
              <span class="metric-mini-label">Currency</span>
              <span class="metric-mini-val">PKR / USD / AED</span>
            </div>
            <div class="metric-mini-tile">
              <span class="metric-mini-label">Security</span>
              <span class="metric-mini-val">4-Digit PIN Lock</span>
            </div>
          </div>

          <!-- Feature Bullets inside Glass Card -->
          <div class="showcase-feature-list">
            <div class="showcase-feat-item">
              <div class="feat-icon-bullet"><i class="material-icons">bolt</i></div>
              <div class="feat-text">
                <strong>Lightning Fast Checkout:</strong> Keyboard shortcuts [F1-F12], barcode scanning, and instant thermal receipts.
              </div>
            </div>
            <div class="showcase-feat-item">
              <div class="feat-icon-bullet"><i class="material-icons">inventory_2</i></div>
              <div class="feat-text">
                <strong>Real-Time Stock & Pricing:</strong> Automatic inventory deductions, low stock warnings, and multi-currency adaptation.
              </div>
            </div>
            <div class="showcase-feat-item">
              <div class="feat-icon-bullet"><i class="material-icons">shield</i></div>
              <div class="feat-text">
                <strong>Multi-Tenant Staff Isolation:</strong> Dedicated cashier roles, lock terminal screen, and owner executive dashboards.
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
            "PeakPOS revolutionized our daily retail checkout. Our queues are cut in half and cashiers learned the interface in less than 10 minutes!"
          </p>
          <div class="testimonial-author">
            <div class="author-avatar-chip">RA</div>
            <div class="author-details">
              <span class="author-name">Retail Store Director</span>
              <span class="author-org">Verified Enterprise Customer</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Password Reset Guidance Modal -->
    <transition name="fade-modal">
      <div v-if="showForgotModal" class="modal-overlay" @click.self="showForgotModal = false">
        <div class="modal-card-dialog">
          <div class="modal-icon-circle">
            <i class="material-icons">lock_reset</i>
          </div>
          <h3 class="modal-dialog-title">Forgot Your Password?</h3>
          <p class="modal-dialog-desc">
            To maintain multi-tenant data isolation and cashier terminal security, password resets and 4-digit PIN updates are managed directly by your Store Administrator.
          </p>
          <div class="modal-dialog-box">
            <i class="material-icons">info</i>
            <span>Store owners can update credentials anytime in <strong>Settings &rarr; Staff & Cashiers</strong>.</span>
          </div>
          <button type="button" class="btn-primary-auth modal-btn" @click="showForgotModal = false">
            Understood
          </button>
        </div>
      </div>
    </transition>
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
  margin-bottom: 1.75rem;
}

.logo-aura-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border-radius: 18px;
  background: #ffffff;
  margin-bottom: 1rem;
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
  margin: 0 0 0.45rem 0;
}

.welcome-subtext {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
  line-height: 1.45;
}

/* ==================== QUICK DEMO CREDENTIALS BAR ==================== */
.quick-demo-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 0.45rem 0.75rem;
  margin-bottom: 1.5rem;
}

.demo-strip-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
}

.demo-pills {
  display: flex;
  gap: 0.5rem;
}

.demo-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 0.3rem 0.65rem;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.demo-pill i {
  font-size: 14px;
}

.admin-pill {
  background: #ede9fe;
  color: #6d28d9;
  border-color: #ddd6fe;
}

.admin-pill:hover {
  background: #ddd6fe;
  transform: translateY(-1px);
}

.cashier-pill {
  background: #e0f2fe;
  color: #0284c7;
  border-color: #bae6fd;
}

.cashier-pill:hover {
  background: #bae6fd;
  transform: translateY(-1px);
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
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-group label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #334155;
}

.btn-inline-link {
  background: transparent;
  border: none;
  font-size: 0.82rem;
  font-weight: 600;
  color: #4f46e5;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s ease;
}

.btn-inline-link:hover {
  color: #3730a3;
  text-decoration: underline;
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

/* ==================== CUSTOM CHECKBOX ==================== */
.form-options-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: -0.2rem;
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
}

/* ==================== CTA BUTTON ==================== */
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

.btn-primary-auth.btn-success {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
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
  margin-top: 2.5rem;
  padding-top: 1.5rem;
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

/* Ambient Glow Orbs */
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

/* ==================== FORGOT PASSWORD MODAL ==================== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 1.5rem;
}

.modal-card-dialog {
  background: #ffffff;
  border-radius: 20px;
  padding: 2.25rem;
  max-width: 440px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
  animation: zoomModal 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.modal-icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #ede9fe;
  color: #6d28d9;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.modal-icon-circle i {
  font-size: 32px;
}

.modal-dialog-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 0.5rem 0;
}

.modal-dialog-desc {
  font-size: 0.92rem;
  color: #64748b;
  line-height: 1.5;
  margin: 0 0 1.25rem 0;
}

.modal-dialog-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.85rem 1rem;
  font-size: 0.84rem;
  color: #334155;
  text-align: left;
  line-height: 1.45;
  margin-bottom: 1.5rem;
  width: 100%;
}

.modal-dialog-box i {
  font-size: 18px;
  color: #4f46e5;
  flex-shrink: 0;
  margin-top: 1px;
}

.modal-btn {
  margin-top: 0;
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

@keyframes zoomModal {
  from { opacity: 0; transform: scale(0.92); }
  to { opacity: 1; transform: scale(1); }
}

.fade-modal-enter-active, .fade-modal-leave-active {
  transition: opacity 0.25s ease;
}

.fade-modal-enter-from, .fade-modal-leave-to {
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

  .quick-demo-strip {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .demo-pills {
    width: 100%;
  }

  .demo-pill {
    flex: 1;
    justify-content: center;
  }

  .trust-footer {
    gap: 0.75rem;
  }
}
</style>
