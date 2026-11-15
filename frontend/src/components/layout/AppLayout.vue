<template>
  <div class="peak-shell" :class="{ 'dark-mode': isDarkMode, 'sidebar-collapsed': isSidebarCollapsed }">
    <!-- Mobile Backdrop -->
    <div
      v-if="isMobileOpen"
      class="mobile-backdrop"
      @click="isMobileOpen = false"
    ></div>

    <!-- Unified Enterprise Sidebar -->
    <aside class="peak-sidebar" :class="{ 'collapsed': isSidebarCollapsed, 'mobile-open': isMobileOpen }">
      <!-- Sidebar Header / Branding -->
      <div class="sidebar-header">
        <router-link to="/dashboard" class="brand-link">
          <div class="brand-logo-wrap">
            <img src="../../assets/logo-pp.png" alt="PeakPOS" class="brand-logo-img" />
          </div>
          <div class="brand-text" v-if="!isSidebarCollapsed">
            <h1 class="brand-title">Peak<span>POS</span></h1>
            <span class="brand-badge">SaaS Enterprise</span>
          </div>
        </router-link>
        <button
          class="sidebar-toggle-btn"
          @click="toggleSidebar"
          :title="isSidebarCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'"
          aria-label="Toggle sidebar"
        >
          <i class="material-icons">{{ isSidebarCollapsed ? 'menu_open' : 'menu' }}</i>
        </button>
      </div>

      <!-- Quick Action: Open Sales Register -->
      <div class="register-quick-action" v-if="!isSidebarCollapsed">
        <router-link to="/sales" class="btn-open-register">
          <i class="material-icons">point_of_sale</i>
          <div class="register-cta-text">
            <strong>Open Register</strong>
            <small>High-Speed POS [F9]</small>
          </div>
          <span class="pulse-indicator"></span>
        </router-link>
      </div>
      <div class="register-quick-action-collapsed" v-else>
        <router-link to="/sales" class="btn-register-icon" title="Open Register [F9]">
          <i class="material-icons">point_of_sale</i>
        </router-link>
      </div>

      <!-- Navigation Menu -->
      <nav class="sidebar-nav">
        <div class="nav-section-label" v-if="!isSidebarCollapsed">OPERATIONS</div>

        <router-link to="/dashboard" class="nav-link" active-class="active" v-if="hasRole(['super_admin', 'admin', 'manager'])">
          <i class="material-icons">dashboard</i>
          <span class="nav-text">Dashboard</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Dashboard</span>
        </router-link>

        <router-link to="/sales" class="nav-link" active-class="active">
          <i class="material-icons">shopping_cart_checkout</i>
          <span class="nav-text">Sales Counter</span>
          <span class="nav-pill-badge">POS</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Sales Counter [F9]</span>
        </router-link>

        <router-link to="/reports" class="nav-link" active-class="active" v-if="hasRole(['super_admin', 'admin', 'manager'])">
          <i class="material-icons">insights</i>
          <span class="nav-text">Reports & Analytics</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Reports & Analytics</span>
        </router-link>

        <router-link to="/customers" class="nav-link" active-class="active">
          <i class="material-icons">people_alt</i>
          <span class="nav-text">Customer Ledger</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Customer Ledger</span>
        </router-link>

        <div class="nav-section-label" v-if="!isSidebarCollapsed && hasRole(['super_admin', 'admin', 'manager'])">CATALOG & INVENTORY</div>

        <router-link to="/admin/products" class="nav-link" active-class="active" v-if="hasRole(['super_admin', 'admin', 'manager'])">
          <i class="material-icons">inventory_2</i>
          <span class="nav-text">Products Catalog</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Products Catalog</span>
        </router-link>

        <router-link to="/admin/categories" class="nav-link" active-class="active" v-if="hasRole(['super_admin', 'admin', 'manager'])">
          <i class="material-icons">category</i>
          <span class="nav-text">Categories</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Categories</span>
        </router-link>

        <router-link to="/admin/settings/discounts" class="nav-link" active-class="active" v-if="hasRole(['super_admin', 'admin', 'manager'])">
          <i class="material-icons">loyalty</i>
          <span class="nav-text">Discounts & Offers</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Discounts & Offers</span>
        </router-link>

        <div class="nav-section-label" v-if="!isSidebarCollapsed && hasRole(['super_admin', 'admin'])">CONFIGURATION</div>

        <router-link to="/admin/settings" class="nav-link" active-class="active" v-if="hasRole(['super_admin', 'admin'])">
          <i class="material-icons">tune</i>
          <span class="nav-text">Settings & Receipts</span>
          <span class="nav-tooltip" v-if="isSidebarCollapsed">Settings & Receipts</span>
        </router-link>
      </nav>

      <!-- Sidebar Footer / User Profile -->
      <div class="sidebar-footer">
        <div class="user-profile-strip" @click="isUserMenuOpen = !isUserMenuOpen">
          <div class="user-avatar-wrap">
            <div class="user-avatar">{{ userInitials }}</div>
            <span class="user-online-dot"></span>
          </div>
          <div class="user-details" v-if="!isSidebarCollapsed">
            <span class="user-name">{{ userName }}</span>
            <span class="user-role-badge">{{ userRole }}</span>
          </div>
          <i class="material-icons user-caret" v-if="!isSidebarCollapsed">
            {{ isUserMenuOpen ? 'expand_more' : 'unfold_more' }}
          </i>
        </div>

        <!-- User Popup Menu -->
        <transition name="pop-menu">
          <div class="user-popup-menu" v-if="isUserMenuOpen" @click.stop>
            <div class="popup-header">
              <strong>{{ userName }}</strong>
              <small>{{ userEmail }}</small>
            </div>
            <div class="popup-divider"></div>
            <button class="popup-item lock-item" @click="isLocked = true; isUserMenuOpen = false">
              <i class="material-icons">lock</i>
              <span>Lock Terminal [Ctrl+L]</span>
            </button>
            <router-link to="/admin/settings" class="popup-item" @click="isUserMenuOpen = false">
              <i class="material-icons">settings</i>
              <span>System Settings</span>
            </router-link>
            <div class="popup-divider"></div>
            <button class="popup-item logout-item" @click="handleLogout">
              <i class="material-icons">logout</i>
              <span>Sign Out</span>
            </button>
          </div>
        </transition>
      </div>
    </aside>

    <!-- Main Content Shell -->
    <div class="peak-main-area">
      <!-- Universal Enterprise Header -->
      <header class="peak-header">
        <div class="header-left">
          <!-- Universal Header Sidebar Toggle Button (desktop and mobile) -->
          <button
            class="header-toggle-sidebar-btn"
            @click="toggleSidebar"
            :title="isSidebarCollapsed ? 'Expand Sidebar [Ctrl+B]' : 'Collapse Sidebar [Ctrl+B]'"
            aria-label="Toggle sidebar"
          >
            <i class="material-icons">{{ isSidebarCollapsed ? 'menu' : 'menu_open' }}</i>
          </button>

          <!-- Mini Brand Logo when sidebar is collapsed completely -->
          <router-link to="/dashboard" class="header-brand-mini" v-if="isSidebarCollapsed">
            <img src="../../assets/logo-pp.png" alt="PeakPOS" class="header-brand-logo" />
            <span class="header-brand-name">Peak<span>POS</span></span>
          </router-link>

          <div class="breadcrumb-trail">
            <span class="crumb-root">PeakPOS</span>
            <i class="material-icons crumb-sep">chevron_right</i>
            <span class="crumb-current">{{ pageTitle || $route.name || 'Terminal' }}</span>
          </div>
        </div>

        <div class="header-center">
          <div class="global-search-box">
            <i class="material-icons search-icon">search</i>
            <input
              type="text"
              class="search-input"
              placeholder="Search products, orders, customers... [Ctrl+K]"
            />
            <span class="search-kbd">⌘K</span>
          </div>
        </div>

        <div class="header-right">
          <!-- Real-Time Clock -->
          <div class="header-clock">
            <i class="material-icons">schedule</i>
            <span>{{ liveClock }}</span>
          </div>

          <!-- Quick Sales POS Launch Button -->
          <router-link to="/sales" class="header-pos-pill" title="Launch POS Counter [F9]">
            <i class="material-icons">flash_on</i>
            <span>POS Register</span>
          </router-link>

          <!-- Quick Lock Terminal Button -->
          <button
            class="header-icon-btn lock-btn"
            @click="isLocked = true"
            title="Lock Terminal & Switch Cashier [Ctrl+L]"
          >
            <i class="material-icons">lock_outline</i>
          </button>

          <!-- Theme Dark/Light Mode Switcher -->
          <button
            class="header-icon-btn theme-toggle"
            @click="toggleTheme"
            :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
          >
            <i class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</i>
          </button>

          <!-- Notification Trigger -->
          <div class="header-notification-wrap">
            <button
              class="header-icon-btn"
              @click="showNotifications = !showNotifications"
              title="Notifications"
            >
              <i class="material-icons">notifications</i>
              <span class="badge-dot"></span>
            </button>

            <!-- Notifications Dropdown -->
            <transition name="pop-menu">
              <div class="notifications-panel" v-if="showNotifications" @click.stop>
                <div class="panel-header">
                  <strong>System Notifications</strong>
                  <span class="unread-pill">Real-time</span>
                </div>
                <div class="panel-list">
                  <div class="panel-item">
                    <i class="material-icons text-success">check_circle</i>
                    <div>
                      <p>Database connected & synced successfully</p>
                      <small>Just now</small>
                    </div>
                  </div>
                  <div class="panel-item">
                    <i class="material-icons text-info">point_of_sale</i>
                    <div>
                      <p>POS High-Speed terminal ready for billing</p>
                      <small>Today</small>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </header>

      <!-- Scrollable Main View Container -->
      <main class="peak-content-viewport" ref="viewport">
        <slot />
      </main>
    </div>

    <!-- Fast Cashier PIN Switch / Terminal Lock Overlay -->
    <PinLockModal
      :is-open="isLocked"
      @unlock="onTerminalUnlocked"
      @close="isLocked = false"
    />
  </div>
</template>

<script>
import PinLockModal from '@/components/common/PinLockModal.vue';

export default {
  name: 'AppLayout',
  components: {
    PinLockModal
  },
  props: {
    pageTitle: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isLocked: false,
      isDarkMode: localStorage.getItem('peakpos_dark_mode') === 'true',
      isSidebarCollapsed: localStorage.getItem('peakpos_sidebar_collapsed') === 'true',
      isMobileOpen: false,
      isUserMenuOpen: false,
      showNotifications: false,
      liveClock: '',
      clockInterval: null,
      userName: localStorage.getItem('userName') || 'Administrator',
      userEmail: localStorage.getItem('userEmail') || 'admin@peakpos.com',
      userRole: (localStorage.getItem('role') || 'Admin').toUpperCase()
    };
  },
  computed: {
    userInitials() {
      const parts = this.userName.trim().split(' ');
      if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
      }
      return this.userName.substring(0, 2).toUpperCase() || 'AD';
    }
  },
  mounted() {
    this.updateClock();
    this.clockInterval = setInterval(this.updateClock, 1000);

    // Apply dark mode class to html/body if active
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark-theme');
    } else {
      document.documentElement.classList.remove('dark-theme');
    }

    // Global click listener to close popups
    document.addEventListener('click', this.handleDocumentClick);

    // Keyboard shortcut engine (F9 -> POS, Ctrl+B -> Sidebar)
    window.addEventListener('keydown', this.handleGlobalKeydown);

    // Initialize 3D Card Hover & Glow effects for all metric-cards in slot
    this.$nextTick(() => {
      this.initMetricCardEffects();
    });
  },
  beforeUnmount() {
    if (this.clockInterval) clearInterval(this.clockInterval);
    document.removeEventListener('click', this.handleDocumentClick);
    window.removeEventListener('keydown', this.handleGlobalKeydown);
  },
  methods: {
    hasRole(allowedRoles) {
      const currentRole = (localStorage.getItem('role') || 'cashier').toLowerCase();
      return currentRole === 'super_admin' || allowedRoles.includes(currentRole);
    },
    updateClock() {
      const now = new Date();
      this.liveClock = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    },
    toggleSidebar() {
      if (window.innerWidth <= 900) {
        this.isMobileOpen = !this.isMobileOpen;
      } else {
        this.isSidebarCollapsed = !this.isSidebarCollapsed;
        localStorage.setItem('peakpos_sidebar_collapsed', this.isSidebarCollapsed ? 'true' : 'false');
      }
    },
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('peakpos_dark_mode', this.isDarkMode ? 'true' : 'false');
      if (this.isDarkMode) {
        document.documentElement.classList.add('dark-theme');
      } else {
        document.documentElement.classList.remove('dark-theme');
      }
    },
    handleDocumentClick(e) {
      if (!e.target.closest('.user-profile-strip') && !e.target.closest('.user-popup-menu')) {
        this.isUserMenuOpen = false;
      }
      if (!e.target.closest('.header-notification-wrap')) {
        this.showNotifications = false;
      }
    },
    handleGlobalKeydown(e) {
      // F9 opens POS sales register
      if (e.key === 'F9') {
        e.preventDefault();
        this.$router.push('/sales');
      }
      // Ctrl+B toggles sidebar
      if ((e.ctrlKey || e.metaKey) && (e.key === 'b' || e.key === 'B')) {
        e.preventDefault();
        this.toggleSidebar();
      }
      // Ctrl+L locks terminal
      if ((e.ctrlKey || e.metaKey) && (e.key === 'l' || e.key === 'L')) {
        e.preventDefault();
        this.isLocked = true;
      }
    },
    onTerminalUnlocked(cashier) {
      this.userName = cashier.name;
      this.userEmail = cashier.email || this.userEmail;
      this.userRole = cashier.role.toUpperCase();
      this.isLocked = false;
    },
    handleLogout() {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      localStorage.removeItem('isAuthenticated');
      this.$router.push('/');
    },
    /**
     * Preserves and enhances the user's favorite 3D card tilt, backdrop glow,
     * and mousemove light tracking across all views inside this layout!
     */
    initMetricCardEffects() {
      const cards = this.$el.querySelectorAll('.metric-card-inner');
      cards.forEach(card => {
        const backdrop = card.querySelector('.metric-card-backdrop');
        const glow = card.querySelector('.metric-card-glow');

        card.addEventListener('mouseenter', () => {
          if (backdrop) backdrop.style.opacity = '1';
          if (glow) glow.style.opacity = '0.85';
        });

        card.addEventListener('mouseleave', () => {
          if (backdrop) backdrop.style.opacity = '0';
          if (glow) glow.style.opacity = '0';
          card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
        });

        card.addEventListener('mousemove', (e) => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;

          const centerX = rect.width / 2;
          const centerY = rect.height / 2;
          const rotateX = ((y - centerY) / centerY) * -6;
          const rotateY = ((x - centerX) / centerX) * 6;

          card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

          if (glow) {
            glow.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.85) 0%, rgba(255,255,255,0) 65%)`;
          }
        });
      });
    }
  }
};
</script>

<style scoped>
/* ==========================================================================
   ENTERPRISE APPLAYOUT THEME & CSS VARIABLES
   ========================================================================== */
.peak-shell {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #f1f5f9;
  color: #1e293b;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  overflow: hidden;
  --sidebar-w: 260px;
  --sidebar-collapsed-w: 74px;
  --header-h: 64px;
  --brand-primary: #4338ca;
  --brand-primary-light: #e0e7ff;
  --brand-accent: #06b6d4;
  --surface-card: #ffffff;
  --border-subtle: #e2e8f0;
  --text-main: #0f172a;
  --text-muted: #64748b;
  transition: background-color 0.25s ease, color 0.25s ease;
}

.peak-shell.dark-mode {
  background-color: #0f172a;
  color: #f8fafc;
  --surface-card: #1e293b;
  --border-subtle: #334155;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
}

/* ==========================================================================
   ENTERPRISE SIDEBAR
   ========================================================================== */
.peak-sidebar {
  width: var(--sidebar-w);
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 100;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.02);
  flex-shrink: 0;
}

.peak-shell.dark-mode .peak-sidebar {
  background: #1e293b;
  border-right-color: #334155;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
}

.peak-sidebar.collapsed {
  width: 0 !important;
  min-width: 0 !important;
  max-width: 0 !important;
  border-right: none !important;
  padding: 0 !important;
  margin: 0 !important;
  opacity: 0 !important;
  pointer-events: none !important;
  overflow: hidden !important;
  box-shadow: none !important;
}

/* Sidebar Header */
.sidebar-header {
  height: var(--header-h);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid var(--border-subtle);
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  overflow: hidden;
}

.brand-logo-wrap {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(67, 56, 202, 0.25);
}

.brand-logo-img {
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.5px;
  line-height: 1.1;
}

.peak-shell.dark-mode .brand-title {
  color: #f8fafc;
}

.brand-title span {
  color: #4338ca;
}

.peak-shell.dark-mode .brand-title span {
  color: #818cf8;
}

.brand-badge {
  font-size: 0.65rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sidebar-toggle-btn {
  background: transparent;
  border: none;
  color: #64748b;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-toggle-btn:hover {
  background: #f1f5f9;
  color: #4338ca;
}

.peak-shell.dark-mode .sidebar-toggle-btn:hover {
  background: #334155;
  color: #818cf8;
}

/* Quick Action Register Button */
.register-quick-action {
  padding: 14px 16px;
}

.btn-open-register {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #4338ca 0%, #3730a3 100%);
  color: #ffffff;
  padding: 10px 14px;
  border-radius: 12px;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(67, 56, 202, 0.35);
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-open-register:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(67, 56, 202, 0.45);
}

.register-cta-text {
  display: flex;
  flex-direction: column;
}

.register-cta-text strong {
  font-size: 0.88rem;
  font-weight: 800;
}

.register-cta-text small {
  font-size: 0.72rem;
  opacity: 0.85;
}

.pulse-indicator {
  position: absolute;
  right: 12px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.3);
  animation: pulseGreen 2s infinite;
}

@keyframes pulseGreen {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(52, 211, 153, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); }
}

.register-quick-action-collapsed {
  display: flex;
  justify-content: center;
  padding: 12px 0;
}

.btn-register-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: #4338ca;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  box-shadow: 0 4px 10px rgba(67, 56, 202, 0.3);
  transition: transform 0.2s;
}

.btn-register-icon:hover {
  transform: scale(1.05);
}

/* Navigation Links */
.sidebar-nav {
  flex: 1;
  padding: 8px 12px;
  overflow-y: auto;
}

.nav-section-label {
  font-size: 0.65rem;
  font-weight: 800;
  color: #94a3b8;
  letter-spacing: 0.8px;
  margin: 16px 12px 6px 12px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  color: #64748b;
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 600;
  margin-bottom: 4px;
  transition: all 0.2s ease;
  position: relative;
}

.nav-link i {
  font-size: 1.3rem;
  color: #64748b;
  transition: color 0.2s;
}

.nav-link:hover {
  background: #f8fafc;
  color: #1e293b;
}

.peak-shell.dark-mode .nav-link:hover {
  background: #334155;
  color: #f8fafc;
}

.nav-link:hover i {
  color: #4338ca;
}

.peak-shell.dark-mode .nav-link:hover i {
  color: #818cf8;
}

.nav-link.active {
  background: #eef2ff;
  color: #4338ca;
  font-weight: 700;
}

.peak-shell.dark-mode .nav-link.active {
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
}

.nav-link.active i {
  color: #4338ca;
}

.peak-shell.dark-mode .nav-link.active i {
  color: #818cf8;
}

.nav-pill-badge {
  margin-left: auto;
  font-size: 0.65rem;
  font-weight: 800;
  background: #4338ca;
  color: white;
  padding: 2px 6px;
  border-radius: 6px;
}

.nav-tooltip {
  display: none;
  position: absolute;
  left: calc(var(--sidebar-collapsed-w) - 6px);
  background: #1e293b;
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 0.75rem;
  white-space: nowrap;
  z-index: 200;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  pointer-events: none;
}

.peak-sidebar.collapsed .nav-link:hover .nav-tooltip {
  display: block;
}

/* Sidebar User Footer */
.sidebar-footer {
  padding: 12px 14px;
  border-top: 1px solid var(--border-subtle);
  position: relative;
}

.user-profile-strip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-profile-strip:hover {
  background: #f1f5f9;
}

.peak-shell.dark-mode .user-profile-strip:hover {
  background: #334155;
}

.user-avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.user-online-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10b981;
  border: 2px solid #ffffff;
}

.user-details {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex: 1;
}

.user-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role-badge {
  font-size: 0.68rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
}

.user-caret {
  color: #94a3b8;
  font-size: 1.2rem;
}

/* Popup Menu */
.user-popup-menu {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 12px;
  right: 12px;
  background: #ffffff;
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
  padding: 8px;
  z-index: 250;
}

.peak-shell.dark-mode .user-popup-menu {
  background: #1e293b;
  border-color: #334155;
}

.popup-header {
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
}

.popup-header strong {
  font-size: 0.85rem;
  color: var(--text-main);
}

.popup-header small {
  font-size: 0.72rem;
  color: var(--text-muted);
}

.popup-divider {
  height: 1px;
  background: var(--border-subtle);
  margin: 6px 0;
}

.popup-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 10px;
  border-radius: 8px;
  background: none;
  border: none;
  text-decoration: none;
  color: var(--text-main);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.popup-item:hover {
  background: #f1f5f9;
}

.peak-shell.dark-mode .popup-item:hover {
  background: #334155;
}

.popup-item.logout-item {
  color: #ef4444;
}

.popup-item.logout-item:hover {
  background: #fef2f2;
}

.peak-shell.dark-mode .popup-item.logout-item:hover {
  background: rgba(239, 68, 68, 0.15);
}

/* ==========================================================================
   MAIN VIEWPORT & ENTERPRISE HEADER
   ========================================================================== */
.peak-main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.peak-header {
  height: var(--header-h);
  background: #ffffff;
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 50;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.peak-shell.dark-mode .peak-header {
  background: #1e293b;
  border-bottom-color: #334155;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-toggle-sidebar-btn {
  background: #f8fafc;
  border: 1px solid var(--border-subtle);
  color: #64748b;
  width: 38px;
  height: 38px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.header-toggle-sidebar-btn:hover {
  background: #f1f5f9;
  color: #4338ca;
  border-color: #cbd5e1;
}

.peak-shell.dark-mode .header-toggle-sidebar-btn {
  background: #0f172a;
  border-color: #334155;
  color: #94a3b8;
}

.peak-shell.dark-mode .header-toggle-sidebar-btn:hover {
  background: #334155;
  color: #818cf8;
}

.header-brand-mini {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  padding-right: 12px;
  border-right: 1px solid var(--border-subtle);
  margin-right: 4px;
}

.header-brand-logo {
  width: 26px;
  height: 26px;
  object-fit: contain;
}

.header-brand-name {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.5px;
}

.header-brand-name span {
  color: #4338ca;
}

.peak-shell.dark-mode .header-brand-name span {
  color: #818cf8;
}

.breadcrumb-trail {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.88rem;
  font-weight: 600;
}

.crumb-root {
  color: #64748b;
}

.crumb-sep {
  font-size: 1.1rem;
  color: #94a3b8;
}

.crumb-current {
  color: var(--text-main);
  font-weight: 800;
}

/* Header Center Search */
.header-center {
  flex: 1;
  max-width: 480px;
  margin: 0 24px;
}

.global-search-box {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  padding: 6px 12px;
  gap: 8px;
  transition: all 0.2s;
}

.peak-shell.dark-mode .global-search-box {
  background: #0f172a;
}

.global-search-box:focus-within {
  border-color: #6366f1;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.peak-shell.dark-mode .global-search-box:focus-within {
  background: #1e293b;
}

.search-icon {
  font-size: 1.2rem;
  color: #94a3b8;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.85rem;
  color: var(--text-main);
}

.search-kbd {
  font-size: 0.65rem;
  font-weight: 800;
  background: #e2e8f0;
  color: #64748b;
  padding: 2px 6px;
  border-radius: 4px;
  letter-spacing: 0.5px;
}

.peak-shell.dark-mode .search-kbd {
  background: #334155;
  color: #94a3b8;
}

/* Header Right */
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-clock {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
  font-weight: 700;
  color: #64748b;
  padding: 6px 10px;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid var(--border-subtle);
}

.peak-shell.dark-mode .header-clock {
  background: #0f172a;
}

.header-pos-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  text-decoration: none;
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 800;
  box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
  transition: transform 0.15s;
}

.header-pos-pill:hover {
  transform: translateY(-1px);
}

.header-icon-btn {
  width: 38px;
  height: 38px;
  border-radius: 9px;
  background: #f8fafc;
  border: 1px solid var(--border-subtle);
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.peak-shell.dark-mode .header-icon-btn {
  background: #0f172a;
  color: #94a3b8;
}

.header-icon-btn:hover {
  background: #f1f5f9;
  color: #4338ca;
  border-color: #cbd5e1;
}

.peak-shell.dark-mode .header-icon-btn:hover {
  background: #334155;
  color: #818cf8;
}

.badge-dot {
  position: absolute;
  top: 7px;
  right: 7px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  border: 2px solid white;
}

/* Notifications Dropdown */
.header-notification-wrap {
  position: relative;
}

.notifications-panel {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 320px;
  background: #ffffff;
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
  padding: 12px;
  z-index: 250;
}

.peak-shell.dark-mode .notifications-panel {
  background: #1e293b;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-subtle);
}

.unread-pill {
  font-size: 0.65rem;
  font-weight: 800;
  background: #ecfdf5;
  color: #059669;
  padding: 2px 6px;
  border-radius: 4px;
}

.panel-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

.panel-item {
  display: flex;
  gap: 10px;
  padding: 8px;
  border-radius: 8px;
  background: #f8fafc;
}

.peak-shell.dark-mode .panel-item {
  background: #0f172a;
}

.panel-item p {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-main);
}

.panel-item small {
  font-size: 0.68rem;
  color: var(--text-muted);
}

.text-success { color: #10b981; }
.text-info { color: #0284c7; }

/* Content Viewport */
.peak-content-viewport {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 24px;
}

/* Transitions */
.pop-menu-enter-active, .pop-menu-leave-active {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.pop-menu-enter-from, .pop-menu-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

/* Responsive Media Queries */
@media (max-width: 900px) {
  .header-center { display: none; }
  .header-clock { display: none; }
  .mobile-toggle-btn { display: block; }
  .peak-sidebar {
    position: fixed;
    top: 0;
    left: -280px;
    height: 100vh;
    transition: left 0.3s ease;
  }
  .peak-sidebar.mobile-open {
    left: 0;
  }
  .mobile-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(15, 23, 42, 0.5);
    z-index: 90;
  }
  .peak-content-viewport {
    padding: 16px;
  }
}
</style>
