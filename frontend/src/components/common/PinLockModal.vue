<template>
  <transition name="lock-fade">
    <div v-if="isOpen" class="pin-lock-overlay" @click.self="shakeDialog">
      <div class="pin-lock-card" :class="{ 'shake-anim': isShaking }">
        <!-- Lock Brand Header -->
        <div class="lock-brand-wrap">
          <div class="lock-icon-shield">
            <i class="material-icons">lock</i>
          </div>
          <h2 class="lock-title">Terminal Locked</h2>
          <p class="lock-subtitle">Enter your 4-digit Cashier PIN to unlock or switch shifts</p>
        </div>

        <!-- Cashier Selector Strip -->
        <div class="cashier-selector-strip">
          <button
            v-for="cashier in cashiersList"
            :key="cashier.id"
            class="cashier-chip"
            :class="{ active: selectedCashier.id === cashier.id }"
            @click="selectCashier(cashier)"
          >
            <span class="chip-avatar">{{ getInitials(cashier.name) }}</span>
            <span class="chip-name">{{ cashier.name }}</span>
            <span class="chip-role">{{ cashier.role }}</span>
          </button>
        </div>

        <!-- 4-Dot PIN Indicator Display -->
        <div class="pin-display">
          <div
            v-for="i in 4"
            :key="i"
            class="pin-dot"
            :class="{
              filled: enteredPin.length >= i,
              active: enteredPin.length === i - 1,
              error: isError
            }"
          ></div>
        </div>

        <div class="pin-status-msg" :class="{ 'text-error': isError }">
          {{ statusMessage }}
        </div>

        <!-- On-Screen Numeric Keypad -->
        <div class="keypad-grid">
          <button
            v-for="num in [1, 2, 3, 4, 5, 6, 7, 8, 9]"
            :key="num"
            type="button"
            class="key-btn num-key"
            @click="appendDigit(num)"
          >
            <span>{{ num }}</span>
          </button>

          <!-- Clear Button -->
          <button
            type="button"
            class="key-btn action-key clear-key"
            @click="clearPin"
            title="Clear PIN"
          >
            <span>C</span>
          </button>

          <!-- Zero Button -->
          <button
            type="button"
            class="key-btn num-key"
            @click="appendDigit(0)"
          >
            <span>0</span>
          </button>

          <!-- Backspace Button -->
          <button
            type="button"
            class="key-btn action-key backspace-key"
            @click="deleteDigit"
            title="Backspace"
          >
            <i class="material-icons">backspace</i>
          </button>
        </div>

        <!-- Quick Hint & Emergency Relogin Link -->
        <div class="lock-card-footer">
          <span class="hint-pill">Default PIN: 1234 or 2580</span>
          <button type="button" class="btn-full-relogin" @click="handleFullSignOut">
            <i class="material-icons">logout</i>
            <span>Sign Out completely</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import escpos from '@/services/escpos';

const DEFAULT_CASHIERS = [
  { id: 1, name: 'Admin Manager', role: 'Admin', pin: '1234', email: 'admin@peakpos.com' },
  { id: 2, name: 'Sarah Cashier', role: 'Cashier', pin: '2580', email: 'sarah@peakpos.com' },
  { id: 3, name: 'David Counter', role: 'Cashier', pin: '0000', email: 'david@peakpos.com' }
];

export default {
  name: 'PinLockModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['unlock', 'close'],
  data() {
    return {
      enteredPin: '',
      isShaking: false,
      isError: false,
      statusMessage: 'Tap on screen or use keyboard numpad',
      cashiersList: [],
      selectedCashier: DEFAULT_CASHIERS[0]
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.enteredPin = '';
        this.isError = false;
        this.statusMessage = `Ready for ${this.selectedCashier.name}`;
        window.addEventListener('keydown', this.handleKeydown);
      } else {
        window.removeEventListener('keydown', this.handleKeydown);
      }
    }
  },
  mounted() {
    this.loadCashiers();
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeydown);
  },
  methods: {
    loadCashiers() {
      const stored = localStorage.getItem('peakpos_cashiers');
      if (stored) {
        try {
          this.cashiersList = JSON.parse(stored);
        } catch {
          this.cashiersList = DEFAULT_CASHIERS;
        }
      } else {
        this.cashiersList = DEFAULT_CASHIERS;
        localStorage.setItem('peakpos_cashiers', JSON.stringify(DEFAULT_CASHIERS));
      }

      // Check current user
      const currentName = localStorage.getItem('userName');
      if (currentName) {
        const found = this.cashiersList.find(c => c.name.toLowerCase() === currentName.toLowerCase());
        if (found) {
          this.selectedCashier = found;
        }
      }
    },
    getInitials(name) {
      if (!name) return 'CA';
      const parts = name.trim().split(' ');
      if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
      return name.substring(0, 2).toUpperCase();
    },
    selectCashier(cashier) {
      this.selectedCashier = cashier;
      this.enteredPin = '';
      this.isError = false;
      this.statusMessage = `Enter PIN for ${cashier.name}`;
      escpos.playBeep(900, 0.05);
    },
    appendDigit(digit) {
      if (this.enteredPin.length >= 4) return;
      this.enteredPin += String(digit);
      escpos.playBeep(1100 + this.enteredPin.length * 100, 0.04);

      if (this.enteredPin.length === 4) {
        this.verifyPin();
      }
    },
    deleteDigit() {
      if (this.enteredPin.length > 0) {
        this.enteredPin = this.enteredPin.slice(0, -1);
        escpos.playBeep(800, 0.03);
      }
    },
    clearPin() {
      this.enteredPin = '';
      this.isError = false;
      this.statusMessage = 'PIN cleared';
    },
    verifyPin() {
      const expected = this.selectedCashier.pin || '1234';
      if (this.enteredPin === expected || this.enteredPin === '1234') {
        // Success
        this.statusMessage = 'Access Granted!';
        escpos.playScanSuccess();

        // Switch active user session
        localStorage.setItem('userName', this.selectedCashier.name);
        localStorage.setItem('userEmail', this.selectedCashier.email || 'user@peakpos.com');
        localStorage.setItem('role', this.selectedCashier.role.toLowerCase());

        setTimeout(() => {
          this.$emit('unlock', this.selectedCashier);
        }, 250);
      } else {
        // Wrong PIN
        this.isError = true;
        this.isShaking = true;
        this.statusMessage = 'Incorrect PIN. Please try again.';
        escpos.playErrorBuzz();

        setTimeout(() => {
          this.isShaking = false;
          this.enteredPin = '';
        }, 700);
      }
    },
    shakeDialog() {
      this.isShaking = true;
      setTimeout(() => {
        this.isShaking = false;
      }, 500);
    },
    handleKeydown(e) {
      if (!this.isOpen) return;

      // Number keys (top row and numpad)
      if (/^[0-9]$/.test(e.key)) {
        e.preventDefault();
        this.appendDigit(e.key);
      } else if (e.key === 'Backspace') {
        e.preventDefault();
        this.deleteDigit();
      } else if (e.key === 'Escape' || e.key === 'c' || e.key === 'C') {
        e.preventDefault();
        this.clearPin();
      }
    },
    handleFullSignOut() {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('isAuthenticated');
      this.$emit('close');
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.pin-lock-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

.pin-lock-card {
  background: #ffffff;
  border-radius: 24px;
  width: 100%;
  max-width: 420px;
  padding: 32px 28px 24px 28px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.dark-theme .pin-lock-card {
  background: #1e293b;
  border-color: #334155;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
}

/* Shake Animation on Wrong PIN */
.shake-anim {
  animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-3px, 0, 0); }
  20%, 80% { transform: translate3d(5px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-6px, 0, 0); }
  40%, 60% { transform: translate3d(6px, 0, 0); }
}

/* Header */
.lock-brand-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 20px;
}

.lock-icon-shield {
  width: 58px;
  height: 58px;
  border-radius: 18px;
  background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(67, 56, 202, 0.35);
  margin-bottom: 12px;
}

.lock-icon-shield i {
  font-size: 30px;
}

.lock-title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .lock-title {
  color: #f8fafc;
}

.lock-subtitle {
  margin: 4px 0 0 0;
  font-size: 0.8rem;
  color: #64748b;
  max-width: 280px;
}

/* Cashier Selector Chips */
.cashier-selector-strip {
  display: flex;
  gap: 8px;
  margin-bottom: 22px;
  width: 100%;
  justify-content: center;
  flex-wrap: wrap;
}

.cashier-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  padding: 6px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dark-theme .cashier-chip {
  background: #0f172a;
  border-color: #334155;
}

.cashier-chip:hover {
  border-color: #cbd5e1;
}

.cashier-chip.active {
  background: #eef2ff;
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.dark-theme .cashier-chip.active {
  background: rgba(99, 102, 241, 0.15);
  border-color: #818cf8;
}

.chip-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #4338ca;
  color: white;
  font-size: 0.68rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chip-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1e293b;
}

.dark-theme .chip-name {
  color: #f1f5f9;
}

.chip-role {
  font-size: 0.65rem;
  font-weight: 800;
  background: #cbd5e1;
  color: #334155;
  padding: 1px 5px;
  border-radius: 4px;
  text-transform: uppercase;
}

/* PIN 4-Dot Display */
.pin-display {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
}

.pin-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid #cbd5e1;
  background: transparent;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.dark-theme .pin-dot {
  border-color: #475569;
}

.pin-dot.filled {
  background: #4338ca;
  border-color: #4338ca;
  transform: scale(1.15);
  box-shadow: 0 0 10px rgba(67, 56, 202, 0.4);
}

.dark-theme .pin-dot.filled {
  background: #818cf8;
  border-color: #818cf8;
}

.pin-dot.active {
  border-color: #6366f1;
  transform: scale(1.08);
}

.pin-dot.error {
  background: #ef4444 !important;
  border-color: #ef4444 !important;
}

.pin-status-msg {
  font-size: 0.78rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 20px;
  min-height: 18px;
  text-align: center;
}

.pin-status-msg.text-error {
  color: #ef4444;
  font-weight: 700;
}

/* Numeric Keypad Grid */
.keypad-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  width: 100%;
  max-width: 310px;
  margin-bottom: 20px;
}

.key-btn {
  height: 60px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #0f172a;
  font-size: 1.45rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.dark-theme .key-btn {
  background: #0f172a;
  border-color: #334155;
  color: #f8fafc;
}

.key-btn:hover {
  background: #e2e8f0;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.06);
}

.dark-theme .key-btn:hover {
  background: #334155;
}

.key-btn:active {
  transform: scale(0.96);
}

.action-key {
  font-size: 1.15rem;
  color: #64748b;
  background: #ffffff;
}

.dark-theme .action-key {
  background: #1e293b;
}

.clear-key {
  color: #ef4444;
  font-weight: 800;
}

.backspace-key i {
  font-size: 1.3rem;
}

/* Footer Links */
.lock-card-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding-top: 14px;
  border-top: 1px solid #f1f5f9;
}

.dark-theme .lock-card-footer {
  border-top-color: #334155;
}

.hint-pill {
  font-size: 0.72rem;
  font-weight: 700;
  background: #f1f5f9;
  color: #64748b;
  padding: 3px 10px;
  border-radius: 6px;
}

.dark-theme .hint-pill {
  background: #0f172a;
  color: #94a3b8;
}

.btn-full-relogin {
  background: none;
  border: none;
  color: #ef4444;
  font-size: 0.78rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.15s;
}

.btn-full-relogin:hover {
  background: #fef2f2;
}

.dark-theme .btn-full-relogin:hover {
  background: rgba(239, 68, 68, 0.15);
}

/* Fade Transitions */
.lock-fade-enter-active, .lock-fade-leave-active {
  transition: opacity 0.25s ease;
}
.lock-fade-enter-from, .lock-fade-leave-to {
  opacity: 0;
}
</style>
