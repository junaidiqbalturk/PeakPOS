<template>
  <div class="dashboard-app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Left Navigation Sidebar with better responsive behavior -->
    <aside class="sidebar" :class="{
        'collapsed': isSidebarCollapsed,
        'mobile-open': !isSidebarCollapsed && isMobileView
      }">
      <div class="sidebar-header">
        <div class="brand">
          <div class="logo-container">
            <span class="logo-icon">
              <i class="material-icons">point_of_sale</i>
            </span>
            <img style="height: 66px;" src="../assets/logo-pp.png">
          </div>
        </div>
        <button class="toggle-btn" @click="toggleSidebar" aria-label="Toggle sidebar">
          <i class="material-icons">{{ isSidebarCollapsed ? 'menu_open' : 'menu' }}</i>
        </button>
      </div>

      <div class="sidebar-content">
        <nav class="nav-menu">
          <router-link to="/dashboard" class="nav-item">
            <i class="material-icons">dashboard</i>
            <span class="nav-label">Dashboard</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Dashboard</div>
          </router-link>
          <router-link to="/sales" class="nav-item">
            <i class="material-icons">shopping_cart</i>
            <span class="nav-label">Sales</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Sales</div>
          </router-link>
          <router-link to="/admin/products" class="nav-item">
            <i class="material-icons">inventory_2</i>
            <span class="nav-label">Products Management</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Products</div>
          </router-link>
          <router-link to="/categories" class="nav-item">
            <i class="material-icons">category</i>
            <span class="nav-label">Categories</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Categories</div>
          </router-link>
          <router-link to="/customers" class="nav-item">
            <i class="material-icons">people</i>
            <span class="nav-label">Customers</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Customers</div>
          </router-link>
          <router-link to="/reports" class="nav-item">
            <i class="material-icons">bar_chart</i>
            <span class="nav-label">Reports</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Reports</div>
          </router-link>
          <router-link to="/settings" class="nav-item active">
            <i class="material-icons">settings</i>
            <span class="nav-label">Settings</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Settings</div>
          </router-link>
        </nav>
      </div>

      <div class="sidebar-footer">
        <div class="user-profile" @click="toggleUserMenu">
          <div class="avatar-wrapper">
            <div class="avatar">
              <span>JS</span>
              <span class="status-indicator online"></span>
            </div>
          </div>
          <div class="user-info">
            <span class="user-name">John Smith</span>
            <span class="user-role">Admin</span>
          </div>
          <div class="user-menu-toggle">
            <i class="material-icons">expand_more</i>
          </div>
          <div class="tooltip" v-if="isSidebarCollapsed">John Smith</div>
        </div>

        <div class="user-dropdown" v-if="isUserMenuOpen">
          <div class="dropdown-item">
            <i class="material-icons">person</i>
            <span>My Profile</span>
          </div>
          <div class="dropdown-item">
            <i class="material-icons">settings</i>
            <span>Account Settings</span>
          </div>
          <div class="dropdown-item" @click="toggleDarkMode">
            <i class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</i>
            <span>{{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}</span>
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item logout">
            <i class="material-icons">logout</i>
            <span>Sign Out</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Overlay for mobile sidebar -->
    <div class="sidebar-overlay" v-if="!isSidebarCollapsed && isMobileView" @click="toggleSidebar"></div>

    <!-- Main Content Area with improved responsive design -->
    <main class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <header class="top-header">
        <div class="header-left">
          <button class="mobile-toggle" @click="toggleSidebar">
            <i class="material-icons">menu</i>
          </button>

          <div class="page-info">
            <h1 class="page-title">Settings & Configuration</h1>
            <div class="breadcrumb">
              <span>PeakPOS</span>
              <i class="material-icons">chevron_right</i>
              <span class="current">Settings</span>
            </div>
          </div>
        </div>

        <div class="header-middle">
          <div class="search-container">
            <i class="material-icons">search</i>
            <input type="text" v-model="searchQuery" placeholder="Search settings..." class="search-input" />
          </div>
        </div>

        <div class="header-right">
          <div class="date-display">
            <i class="material-icons">calendar_today</i>
            <span>{{ currentDate }}</span>
          </div>

          <div class="action-buttons">
            <button class="action-btn theme-btn" @click="toggleDarkMode">
              <i class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</i>
            </button>

            <button class="action-btn">
              <i class="material-icons">notifications</i>
            </button>

            <button class="action-btn">
              <i class="material-icons">help_outline</i>
            </button>
          </div>
        </div>
      </header>

      <div class="settings-management">
        <!-- Dashboard Summary -->
        <div class="dashboard-summary">
          <div class="welcome-message">
            <h2>Point of Sales Configurations & Settings</h2>
            <p>Configure your store settings from a single dashboard with ease.</p>
          </div>
        </div>

        <!-- Modern Metrics Grid with Animated 3D Cards - Settings Summary -->
        <div class="metrics-grid">
          <!-- Store Profile Card -->
          <div class="metric-card store" :style="{ '--delay': '0.1s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">store</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">settings</i>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Store Profile</div>
                <div class="metric-value">
                  <span class="value-text">{{ storeSettings.name || 'Your Store' }}</span>
                </div>
                <div class="metric-action">
                  <button @click="activeSection = 'store'" class="btn-configure">
                    Configure <i class="material-icons">arrow_forward</i>
                  </button>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>

          <!-- Discount Management Card -->
          <div class="metric-card discount" :style="{ '--delay': '0.2s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">local_offer</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">percent</i>
                  <span class="trend-value">{{ discountStats.total }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Discount Management</div>
                <div class="metric-value">
                  <span class="value-number">{{ discountStats.active }}</span>
                  <span class="value-label">Active Discounts</span>
                </div>
                <div class="metric-action">
                  <button @click="activeSection = 'discounts'" class="btn-configure">
                    Configure <i class="material-icons">arrow_forward</i>
                  </button>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>

          <!-- Currency Settings Card -->
          <div class="metric-card currency" :style="{ '--delay': '0.3s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon success">
                  <i class="material-icons">payments</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">currency_exchange</i>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Currency Settings</div>
                <div class="metric-value">
                  <span class="value-text">{{ getCurrencySymbol(currencySettings.currency) }} {{ currencySettings.currency }}</span>
                </div>
                <div class="metric-action">
                  <button @click="activeSection = 'currency'" class="btn-configure">
                    Configure <i class="material-icons">arrow_forward</i>
                  </button>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>
        </div>

        <!-- Settings Navigation -->
        <div class="filter-section">
          <div class="filter-header">
            <h3>Settings</h3>
          </div>
          <div class="filters-row settings-nav">
            <button
              v-for="(section, index) in settingsSections"
              :key="index"
              @click="activeSection = section.id"
              :class="['settings-nav-btn', { active: activeSection === section.id }]"
            >
              <i class="material-icons">{{ section.icon }}</i>
              <span>{{ section.name }}</span>
            </button>
          </div>
        </div>

        <!-- Settings Content Sections -->
        <div class="settings-content">
          <!-- Store Profile Section -->
          <div v-if="activeSection === 'store'" class="settings-section">
            <div class="section-header">
              <div class="section-icon">
                <i class="material-icons">store</i>
              </div>
              <h3>Store Profile</h3>
            </div>

            <div class="settings-panel">
              <div class="store-preview">
                <div class="store-logo">
                  <img v-if="storeSettings.logoUrl" :src="storeSettings.logoUrl" alt="Store Logo" />
                  <div v-else class="logo-placeholder">
                    <i class="material-icons">store</i>
                  </div>
                </div>
                <div class="store-info">
                  <h4>{{ storeSettings.name || 'Your Store Name' }}</h4>
                  <p>{{ storeSettings.address || 'Store Address' }}</p>
                </div>
              </div>

              <div class="form-group">
                <label>Store Name</label>
                <input type="text" v-model="storeSettings.name" placeholder="Enter store name" />
              </div>

              <div class="form-group">
                <label>Store Address</label>
                <textarea v-model="storeSettings.address" placeholder="Enter store address" rows="2"></textarea>
              </div>

              <div class="form-group">
                <label>Contact Phone</label>
                <input type="tel" v-model="storeSettings.phone" placeholder="Enter contact phone" />
              </div>

              <div class="form-group">
                <label>Contact Email</label>
                <input type="email" v-model="storeSettings.email" placeholder="Enter contact email" />
              </div>

              <div class="form-group">
                <label>Logo</label>
                <div class="file-upload">
                  <input type="file" id="logo-upload" @change="handleLogoUpload" accept="image/*" />
                  <label for="logo-upload" class="upload-btn">
                    <i class="material-icons">cloud_upload</i> Upload Logo
                  </label>
                </div>
              </div>

              <div class="form-actions">
                <button class="btn-save" @click="saveStoreSettings">
                  <i class="material-icons">save</i> Save Changes
                </button>
              </div>
            </div>
          </div>

          <!-- Discount Management Section -->
          <div v-if="activeSection === 'discounts'" class="settings-section">
            <div class="section-header">
              <div class="section-icon">
                <i class="material-icons">local_offer</i>
              </div>
              <h3>Discount Management</h3>
            </div>

            <div class="settings-panel">
              <div class="discount-stats">
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="material-icons">local_offer</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ discountStats.total }}</h4>
                    <p>Total Discounts</p>
                  </div>
                </div>

                <div class="stat-card">
                  <div class="stat-icon active">
                    <i class="material-icons">check_circle</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ discountStats.active }}</h4>
                    <p>Active Discounts</p>
                  </div>
                </div>

                <div class="stat-card">
                  <div class="stat-icon inactive">
                    <i class="material-icons">cancel</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ discountStats.inactive }}</h4>
                    <p>Inactive Discounts</p>
                  </div>
                </div>
              </div>

              <div class="discount-list">
                <h4 class="sub-heading">Recent Discounts</h4>
                <table v-if="discounts.length > 0">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Type</th>
                      <th>Value</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="discount in discounts" :key="discount.id">
                      <td>{{ discount.name }}</td>
                      <td>{{ discount.discount_type === 'percentage' ? 'Percentage' : 'Fixed' }}</td>
                      <td>{{ discount.discount_type === 'percentage' ? discount.value + '%' : '$' + discount.value.toFixed(2) }}</td>
                      <td>
                        <span :class="['status-badge', discount.active ? 'active' : 'inactive']">
                          {{ discount.active ? 'Active' : 'Inactive' }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div v-else class="no-data-message">
                  <i class="material-icons">local_offer</i>
                  <p>No discounts created yet</p>
                </div>
              </div>

              <div class="form-actions">
                <router-link to="/discounts" class="btn-primary">
                  <i class="material-icons">settings</i> Manage Discounts
                </router-link>
              </div>
            </div>
          </div>

          <!-- Currency Settings Section -->
          <div v-if="activeSection === 'currency'" class="settings-section">
            <div class="section-header">
              <div class="section-icon">
                <i class="material-icons">payments</i>
              </div>
              <h3>Currency Settings</h3>
            </div>

            <div class="settings-panel">
              <div class="form-group">
                <label>Currency</label>
                <select v-model="currencySettings.currency">
                  <option value="USD">US Dollar ($)</option>
                  <option value="EUR">Euro (€)</option>
                  <option value="GBP">British Pound (£)</option>
                  <option value="JPY">Japanese Yen (¥)</option>
                  <option value="CAD">Canadian Dollar (C$)</option>
                  <option value="AUD">Australian Dollar (A$)</option>
                  <option value="CNY">Chinese Yuan (¥)</option>
                  <option value="INR">Indian Rupee (₹)</option>
                </select>
              </div>

              <div class="form-group">
                <label>Symbol Position</label>
                <div class="radio-group">
                  <label class="radio-option">
                    <input type="radio" v-model="currencySettings.symbolPosition" value="before" />
                    <span class="radio-label">Before amount ($100.00)</span>
                  </label>
                  <label class="radio-option">
                    <input type="radio" v-model="currencySettings.symbolPosition" value="after" />
                    <span class="radio-label">After amount (100.00$)</span>
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label>Thousand Separator</label>
                <select v-model="currencySettings.thousandSeparator">
                  <option value=",">Comma (,)</option>
                  <option value=".">Period (.)</option>
                  <option value=" ">Space</option>
                  <option value="">None</option>
                </select>
              </div>

              <div class="form-group">
                <label>Decimal Separator</label>
                <select v-model="currencySettings.decimalSeparator">
                  <option value=".">Period (.)</option>
                  <option value=",">Comma (,)</option>
                </select>
              </div>

              <div class="form-group">
                <label>Decimal Places</label>
                <select v-model="currencySettings.decimalPlaces">
                  <option value="0">0</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                </select>
              </div>

              <div class="form-preview">
                <label>Preview</label>
                <div class="preview-box">
                  {{ formatCurrencyPreview(1234.56) }}
                </div>
              </div>

              <div class="form-actions">
                <button class="btn-save" @click="saveCurrencySettings">
                  <i class="material-icons">save</i> Save Changes
                </button>
              </div>
            </div>
          </div>

          <!-- Tax Settings Section -->
          <div v-if="activeSection === 'taxes'" class="settings-section">
            <div class="section-header">
              <div class="section-icon">
                <i class="material-icons">account_balance</i>
              </div>
              <h3>Tax Settings</h3>
            </div>

            <div class="settings-panel">
              <div class="form-group">
                <label class="checkbox-container">
                  <input type="checkbox" v-model="taxSettings.enableTax" />
                  <span class="checkmark"></span>
                  Enable Tax
                </label>
              </div>

              <div class="form-group" v-if="taxSettings.enableTax">
                <label>Tax Calculation</label>
                <div class="radio-group">
                  <label class="radio-option">
                    <input type="radio" v-model="taxSettings.taxMode" value="inclusive" />
                    <span class="radio-label">Tax Inclusive (prices include tax)</span>
                  </label>
                  <label class="radio-option">
                    <input type="radio" v-model="taxSettings.taxMode" value="exclusive" />
                    <span class="radio-label">Tax Exclusive (add tax to prices)</span>
                  </label>
                </div>
              </div>

              <div class="form-group" v-if="taxSettings.enableTax">
                <label>Default Tax Rate (%)</label>
                <input type="number" v-model="taxSettings.defaultRate" min="0" max="100" step="0.01" />
              </div>

              <div class="form-group" v-if="taxSettings.enableTax">
                <label>Tax Number (Optional)</label>
                <input type="text" v-model="taxSettings.taxNumber" placeholder="VAT/GST number" />
              </div>

              <div class="form-group" v-if="taxSettings.enableTax">
                <label>Display on Receipts</label>
                <div class="checkbox-group">
                  <label class="checkbox-container">
                    <input type="checkbox" v-model="taxSettings.showTaxOnReceipt" />
                    <span class="checkmark"></span>
                    Show tax information on receipts
                  </label>
                </div>
              </div>

              <div class="form-actions">
                <button class="btn-save" @click="saveTaxSettings">
                  <i class="material-icons">save</i> Save Changes
                </button>
              </div>
            </div>
          </div>

          <!-- Receipt Settings Section -->
          <div v-if="activeSection === 'receipt'" class="settings-section" @click="switchToReceipt()">
            <div class="section-header">
              <div class="section-icon">
                <i class="material-icons">receipt</i>
              </div>
              <h3>Receipt Settings</h3>
            </div>

            <div class="settings-panel">
              <div class="form-group">
                <label>Receipt Header</label>
                <textarea v-model="receiptSettings.header" placeholder="Enter text to display at the top of receipts" rows="2"></textarea>
              </div>

              <div class="form-group">
                <label>Receipt Footer</label>
                <textarea v-model="receiptSettings.footer" placeholder="Enter text to display at the bottom of receipts" rows="2"></textarea>
              </div>

              <div class="form-group">
                <label>Show on Receipt</label>
                <div class="checkbox-group">
                  <label class="checkbox-container">
                    <input type="checkbox" v-model="receiptSettings.showLogo" />
                    <span class="checkmark"></span>
                    Store Logo
                  </label>

                  <label class="checkbox-container">
                    <input type="checkbox" v-model="receiptSettings.showCashier" />
                    <span class="checkmark"></span>
                    Cashier Name
                  </label>

                  <label class="checkbox-container">
                    <input type="checkbox" v-model="receiptSettings.showTaxBreakdown" />
                    <span class="checkmark"></span>
                    Tax Breakdown
                  </label>

                  <label class="checkbox-container">
                    <input type="checkbox" v-model="receiptSettings.showBarcode" />
                    <span class="checkmark"></span>
                    Order Barcode
                  </label>
                </div>
              </div>

              <div class="form-group">
                <label>Paper Size</label>
                <select v-model="receiptSettings.paperSize">
                  <option value="80mm">80mm (Standard)</option>
                  <option value="58mm">58mm (Compact)</option>
                  <option value="a4">A4 Paper</option>
                </select>
              </div>

              <div class="form-actions">
                <button class="btn-save" @click="saveReceiptSettings">
                  <i class="material-icons">save</i> Save Changes
                </button>
                <button class="btn-secondary" @click="previewReceipt">
                  <i class="material-icons">visibility</i> Preview
                </button>
              </div>
            </div>
          </div>

          <!-- User Management Section -->
          <div v-if="activeSection === 'users'" class="settings-section">
            <div class="section-header">
              <div class="section-icon">
                <i class="material-icons">group</i>
              </div>
              <h3>User Management</h3>
            </div>

            <div class="settings-panel">
              <div class="user-stats">
                <div class="stat-card">
                  <div class="stat-icon">
                    <i class="material-icons">people</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ userStats.total }}</h4>
                    <p>Total Users</p>
                  </div>
                </div>

                <div class="stat-card">
                  <div class="stat-icon admin">
                    <i class="material-icons">admin_panel_settings</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ userStats.admins }}</h4>
                    <p>Administrators</p>
                  </div>
                </div>

                <div class="stat-card">
                  <div class="stat-icon cashier">
                    <i class="material-icons">point_of_sale</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ userStats.cashiers }}</h4>
                    <p>Cashiers</p>
                  </div>
                </div>
              </div>

              <div class="user-list">
                <h4 class="sub-heading">User Accounts</h4>
                <div class="user-grid">
                  <div v-for="user in users" :key="user.id" class="user-card">
                    <div class="user-avatar">
                      <span>{{ getUserInitials(user.name) }}</span>
                    </div>
                    <div class="user-details">
                      <h5>{{ user.name }}</h5>
                      <span :class="['user-role', user.role.toLowerCase()]">{{ user.role }}</span>
                    </div>
                    <div class="user-status">
                      <span :class="['status-indicator', user.active ? 'online' : 'offline']"></span>
                      <span class="status-text">{{ user.active ? 'Active' : 'Inactive' }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-actions">
                <router-link to="/users" class="btn-primary">
                  <i class="material-icons">settings</i> Manage Users
                </router-link>
              </div>
            </div>
          </div>

          <!-- System Preferences Section -->
          <div v-if="activeSection === 'system'" class="settings-section">
            <div class="section-header">
              <div class="section-icon">
                <i class="material-icons">tune</i>
              </div>
              <h3>System Preferences</h3>
            </div>

            <div class="settings-panel">
              <div class="form-group">
                <label>Date Format</label>
                <select v-model="systemSettings.dateFormat">
                  <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                  <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                  <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                </select>
              </div>

              <div class="form-group">
                <label>Time Format</label>
                <select v-model="systemSettings.timeFormat">
                  <option value="12">12 Hour (AM/PM)</option>
                  <option value="24">24 Hour</option>
                </select>
              </div>

              <div class="form-group">
                <label>Default Language</label>
                <select v-model="systemSettings.language">
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="zh">Chinese</option>
                </select>
              </div>

              <div class="form-group">
                <label>Interface Theme</label>
                <div class="theme-options">
                  <label class="theme-option" :class="{ active: systemSettings.theme === 'light' }">
                    <input type="radio" v-model="systemSettings.theme" value="light" />
                    <div class="theme-preview light-theme">
                      <div class="preview-header"></div>
                      <div class="preview-content"></div>
                    </div>
                    <span>Light</span>
                  </label>

                  <label class="theme-option" :class="{ active: systemSettings.theme === 'dark' }">
                    <input type="radio" v-model="systemSettings.theme" value="dark" />
                    <div class="theme-preview dark-theme">
                      <div class="preview-header"></div>
                      <div class="preview-content"></div>
                    </div>
                    <span>Dark</span>
                  </label>

                  <label class="theme-option" :class="{ active: systemSettings.theme === 'auto' }">
                    <input type="radio" v-model="systemSettings.theme" value="auto" />
                    <div class="theme-preview auto-theme">
                      <div class="preview-split">
                        <div class="light-half"></div>
                        <div class="dark-half"></div>
                      </div>
                    </div>
                    <span>Auto</span>
                  </label>
                </div>
              </div>

              <div class="form-actions">
                <button class="btn-save" @click="saveSystemSettings">
                  <i class="material-icons">save</i> Save Changes
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Toast Message -->
        <transition name="toast">
          <div v-if="toast.show" :class="['toast', toast.type]">
            <i class="material-icons">{{ toast.type === 'success' ? 'check_circle' : 'error' }}</i>
            <span>{{ toast.message }}</span>
            <button class="toast-close" @click="toast.show = false">
              <i class="material-icons">close</i>
            </button>
          </div>
        </transition>
      </div>
    </main>
  </div>
  <!-- Receipt Preview Modal -->
<div v-if="showPreview" class="receipt-preview-overlay">
  <div class="receipt-preview">
    <div class="receipt-paper" :class="receiptSettings.paperSize">
      <div class="receipt-header" v-if="receiptSettings.showLogo">
        <img v-if="logoUrl" :src="logoUrl" alt="Logo" class="receipt-logo" />
      </div>
      <div class="receipt-header-text">{{ receiptSettings.header }}</div>

      <div class="receipt-body">
        <p><strong>Date:</strong> {{ new Date().toLocaleString() }}</p>
        <p><strong>Sample Product:</strong> Laptop XYZ</p>
        <p><strong>Quantity:</strong> 1</p>
        <p><strong>Price:</strong> $1000</p>
        <p><strong>Total:</strong> $1000</p>
      </div>

      <div class="receipt-footer-text">{{ receiptSettings.footer }}</div>
    </div>
    <div class="modal-actions">
      <button @click="printPreview">Print</button>
      <button @click="closePreview">Close</button>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'SettingsView',
  data() {
    return {
      showPreview: false, //REceipt Preview
       logoUrl: '', // Will be set if a logo is uploaded
      // Navigation and layout data
      isDarkMode: localStorage.getItem('darkMode') === 'true',
      isSidebarCollapsed: localStorage.getItem('sidebarCollapsed') === 'true',
      isMobileView: window.innerWidth < 768,
      isUserMenuOpen: false,
      currentDate: new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }),
      searchQuery: '',
      //Receipt Settings
      receiptSettings: {
        header: '',
        footer: '',
        showLogo: true,
        showCashier: true,
        showTaxBreakdown: true,
        showBarcode: true,
        paperSize: '80mm'
      },

      // Settings sections
      activeSection: 'store',
      settingsSections: [
        { id: 'store', name: 'Store Profile', icon: 'store' },
        { id: 'currency', name: 'Currency', icon: 'payments' },
        { id: 'taxes', name: 'Taxes', icon: 'account_balance' },
        { id: 'discounts', name: 'Discounts', icon: 'local_offer' },
        { id: 'receipt', name: 'Receipt', icon: 'receipt' },
        { id: 'users', name: 'Users', icon: 'group' },
        { id: 'system', name: 'System', icon: 'tune' }
      ],

      // Store settings
      storeSettings: {
        name: 'PeakPOS Store',
        address: '123 Commerce Street, Business District',
        phone: '+1 (555) 123-4567',
        email: 'info@peakpos.com',
        logoUrl: null
      },

      // Currency settings
      currencySettings: {
        currency: 'USD',
        symbolPosition: 'before',
        thousandSeparator: ',',
        decimalSeparator: '.',
        decimalPlaces: '2'
      },

      // Tax settings
      taxSettings: {
        enableTax: true,
        taxMode: 'exclusive',
        defaultRate: 7.0,
        taxNumber: '',
        showTaxOnReceipt: true
      },

      // Discount data
      discounts: [
        { id: 1, name: 'Summer Sale', discount_type: 'percentage', value: 15, active: true },
        { id: 2, name: 'Loyal Customer', discount_type: 'percentage', value: 10, active: true },
        { id: 3, name: 'New Customer', discount_type: 'fixed', value: 5, active: false }
      ],
      discountStats: {
        total: 3,
        active: 2,
        inactive: 1
      },

      // Receipt settings
      receiptSettingss: {
        header: 'Thank you for shopping with us!',
        footer: 'Please come again soon',
        showLogo: true,
        showCashier: true,
        showTaxBreakdown: true,
        showBarcode: true,
        paperSize: '80mm'
      },

      // User data
      users: [
        { id: 1, name: 'John Smith', role: 'Admin', active: true },
        { id: 2, name: 'Sarah Johnson', role: 'Cashier', active: true },
        { id: 3, name: 'Michael Brown', role: 'Cashier', active: false }
      ],
      userStats: {
        total: 3,
        admins: 1,
        cashiers: 2
      },

      // System settings
      systemSettings: {
        dateFormat: 'MM/DD/YYYY',
        timeFormat: '12',
        language: 'en',
        theme: 'light'
      },

      // Toast notification
      toast: {
        show: false,
        message: '',
        type: 'success',
        timeout: null
      }
    };
  },

  methods: {
    // Receipt Settings
    switchToReceipt() {
    this.activeSection = 'receipt';
    this.loadReceiptSettings();
  },
    async loadReceiptSettings() {
      try{
        const response = await fetch('/api/receipt-settings');
        if(!response.ok) throw new Error('Failed to Fetch Settings');

        const data = await response.json();
        this.receiptSettings.header = data.header_text || '';
        this.receiptSettings.footer = data.footer_text || '';
        this.receiptSettings.showLogo = true; //default
        this.receiptSettings.showCashier = true;
        this.receiptSettings.showTaxBreakdown = true;
        this.receiptSettings.showBarcode = true;
        this.receiptSettings.paperSize = '80mm';
      } catch(err){
        console.error("Error Loading Receipt Settings",err);
      }
    },
    //Save Receipt Settings

    // Navigation methods
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
      localStorage.setItem('sidebarCollapsed', this.isSidebarCollapsed);
    },

    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('darkMode', this.isDarkMode);
    },

    toggleUserMenu() {
      this.isUserMenuOpen = !this.isUserMenuOpen;
    },

    handleClickOutside() {
      this.isUserMenuOpen = false;
    },

    handleResize() {
      this.isMobileView = window.innerWidth < 768;
    },

    // Store profile methods
    handleLogoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.storeSettings.logoUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    saveStoreSettings() {
      // Save store settings API call would go here
      this.showToastMessage('Store settings saved successfully');
    },

    // Currency methods
    formatCurrencyPreview(amount) {
      // Basic formatting for preview
      const value = Number(amount).toFixed(parseInt(this.currencySettings.decimalPlaces));
      const [integerPart, decimalPart] = value.split('.');

      // Format integer part with thousand separator
      let formattedInteger = '';
      for (let i = 0; i < integerPart.length; i++) {
        if (i > 0 && (integerPart.length - i) % 3 === 0) {
          formattedInteger += this.currencySettings.thousandSeparator;
        }
        formattedInteger += integerPart[i];
      }

      // Combine with decimal part
      let formattedValue = formattedInteger;
      if (decimalPart) {
        formattedValue += this.currencySettings.decimalSeparator + decimalPart;
      }

      // Add currency symbol
      const symbol = this.getCurrencySymbol(this.currencySettings.currency);
      return this.currencySettings.symbolPosition === 'before'
        ? `${symbol}${formattedValue}`
        : `${formattedValue}${symbol}`;
    },

    getCurrencySymbol(currencyCode) {
      const symbols = {
        USD: '$',
        EUR: '€',
        GBP: '£',
        JPY: '¥',
        CAD: 'C$',
        AUD: 'A$',
        CNY: '¥',
        INR: '₹'
      };
      return symbols[currencyCode] || currencyCode;
    },

    saveCurrencySettings() {
      // Save currency settings API call would go here
      this.showToastMessage('Currency settings saved successfully');
    },

    // Tax methods
    saveTaxSettings() {
      // Save tax settings API call would go here
      this.showToastMessage('Tax settings saved successfully');
    },

    // Receipt methods
    async saveReceiptSettings() {
    try {
      const response = await fetch('/api/receipt-settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          header_text: this.receiptSettings.header,
          footer_text: this.receiptSettings.footer,
          // Phase 1 doesn't persist checkboxes and paperSize yet; include them in Phase 2.
        }),
      });

      if (!response.ok) throw new Error('Failed to save settings');

     // const result = await response.json();
      alert('Receipt settings saved successfully');
    } catch (err) {
      console.error('Error saving receipt settings:', err);
    }
  },
    async uploadLogo(event) {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append('logo', file);

  try {
    const response = await fetch('/api/receipt-settings/logo', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) throw new Error('Failed to upload logo');
    const result = await response.json();
    alert('Logo uploaded: ' + result.filename);
  } catch (err) {
    console.error('Logo upload error:', err);
  }
},

    previewReceipt() {
    // Set logo URL if available
    this.logoUrl = '/static/logo.png'; // Change path based on your setup
    this.showPreview = true;
  },
    closePreview() {
    this.showPreview = false;
  },

    // System settings methods
    saveSystemSettings() {
      // Save system settings API call would go here
      // Also apply theme if changed
      if (this.systemSettings.theme === 'dark') {
        this.isDarkMode = true;
        localStorage.setItem('darkMode', 'true');
      } else if (this.systemSettings.theme === 'light') {
        this.isDarkMode = false;
        localStorage.setItem('darkMode', 'false');
      } else if (this.systemSettings.theme === 'auto') {
        // Logic to detect system preference would go here
        this.isDarkMode = false;
        localStorage.setItem('darkMode', 'false');
      }

      this.showToastMessage('System settings saved successfully');
    },

    // User helper methods
    getUserInitials(name) {
      if (!name) return '??';
      return name.split(' ')
        .map(part => part.charAt(0).toUpperCase())
        .join('')
        .substring(0, 2);
    },

    // Toast notification
    showToastMessage(message, type = 'success') {
      // Clear existing timeout if there is one
      if (this.toast.timeout) {
        clearTimeout(this.toast.timeout);
      }

      // Set toast properties
      this.toast.show = true;
      this.toast.message = message;
      this.toast.type = type;

      // Hide toast after 3 seconds
      this.toast.timeout = setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    }
  },

  created() {
    document.addEventListener('click', this.handleClickOutside);
    window.addEventListener('resize', this.handleResize);

    // Here you would fetch actual settings from your API
    // For example:
    // this.fetchStoreSettings();
    // this.fetchCurrencySettings();
    // etc.

    // Fetch discount stats
    this.discountStats = {
      total: this.discounts.length,
      active: this.discounts.filter(d => d.active).length,
      inactive: this.discounts.filter(d => !d.active).length
    };
  },

  unmounted() {
    document.removeEventListener('click', this.handleClickOutside);
    window.removeEventListener('resize', this.handleResize);

    // Clear any active toast timeout
    if (this.toast.timeout) {
      clearTimeout(this.toast.timeout);
    }
  }
}
</script>

<style scoped>
/* Receipt Modal CSS */
.receipt-preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.receipt-preview {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}
.receipt-paper.80mm {
  width: 80mm;
}
.receipt-paper.58mm {
  width: 58mm;
}
.receipt-paper.a4 {
  width: 210mm;
}
.receipt-logo {
  display: block;
  max-height: 60px;
  margin: 0 auto;
}
.modal-actions {
  text-align: center;
  margin-top: 20px;
}
.modal-actions button {
  margin: 0 10px;
}
/* Ends here */
/* Main Layout Styles */
.dashboard-app {
  display: flex;
  min-height: 100vh;
  background-color: var(--background-color-body, #f8fafc);
  color: var(--text-color-primary, #1e293b);
  position: relative;
}

.dark-mode {
  --background-color-body: #0f172a;
  --background-color-primary: #1e293b;
  --background-color-secondary: #334155;
  --text-color-primary: #f1f5f9;
  --text-color-secondary: #94a3b8;
  --border-color: #334155;
  --primary-color: #818cf8;
  --primary-color-light: #4f46e5;
  --primary-color-dark: #4338ca;
  --success-color: #34d399;
  --warning-color: #fbbf24;
  --danger-color: #f87171;
  --shadow-color: rgba(0, 0, 0, 0.5);
}

/* Settings Management Container */
.settings-management {
  padding: 0 24px 40px;
}

/* Metrics Grid - Settings Summary Cards */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.metric-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  height: 180px;
}

.metric-card-inner {
  position: relative;
  height: 100%;
  background-color: var(--background-color-primary, white);
  border-radius: inherit;
  padding: 20px;
  display: flex;
  flex-direction: column;
  z-index: 2;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.metric-card-inner:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
}

.metric-icon-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.metric-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.metric-icon.success {
  background-color: rgba(52, 211, 153, 0.2);
  color: var(--success-color, #34d399);
}

.metric-icon i {
  font-size: 24px;
}

.metric-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-color-secondary, #64748b);
}

.metric-trend.positive {
  color: var(--success-color, #34d399);
}

.trend-value {
  font-weight: 600;
}

.metric-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.metric-label {
  color: var(--text-color-secondary, #64748b);
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.metric-value {
  margin-bottom: 10px;
}

.value-number {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.value-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.value-label {
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
  margin-left: 5px;
}

.metric-action {
  margin-top: auto;
}

.btn-configure {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 8px 15px;
  border: none;
  border-radius: 8px;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-configure:hover {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.metric-card-backdrop, .metric-card-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.metric-card-backdrop {
  background: radial-gradient(
    circle at 50% 0%,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0) 75%
  );
}

.metric-card-glow {
  background: radial-gradient(
    circle at 50% 50%,
    rgba(79, 70, 229, 0.1) 0%,
    rgba(79, 70, 229, 0) 70%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
}

.metric-card-inner:hover .metric-card-glow {
  opacity: 1;
}

/* Settings Navigation Filters */
.filter-section {
  margin-bottom: 24px;
}

.settings-nav {
  display: flex;
  flex-wrap: nowrap;
  gap: 12px;
  overflow-x: auto;
  padding: 5px 0;
  scrollbar-width: thin;
}

.settings-nav::-webkit-scrollbar {
  height: 4px;
}

.settings-nav::-webkit-scrollbar-thumb {
  background-color: var(--border-color, #e2e8f0);
  border-radius: 4px;
}

.settings-nav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background-color: var(--background-color-primary, white);
  color: var(--text-color-secondary, #64748b);
  font-size: 0.875rem;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.settings-nav-btn.active {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.settings-nav-btn:hover:not(.active) {
  background-color: var(--background-color-secondary, #f8fafc);
}

.settings-nav-btn i {
  font-size: 18px;
}

/* Settings Content */
.settings-content {
  margin-top: 24px;
}

.settings-section {
  background-color: var(--background-color-primary, white);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 24px;
}

.section-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.section-icon i {
  font-size: 24px;
}

.section-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.settings-panel {
  padding: 24px;
}

/* Form Elements */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  color: var(--text-color-primary, #1e293b);
}

.form-group input[type="text"],
.form-group input[type="tel"],
.form-group input[type="email"],
.form-group input[type="number"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 8px;
  font-size: 0.9rem;
  background-color: var(--background-color-primary, white);
  color: var(--text-color-primary, #1e293b);
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color, #4f46e5);
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  margin-bottom: 8px;
}

.checkbox-container input[type="checkbox"] {
  margin: 0;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-option input[type="radio"] {
  margin: 0;
}

.file-upload {
  display: flex;
  align-items: center;
}

.file-upload input[type="file"] {
  display: none;
}

.upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
  border-radius: 6px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.upload-btn:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

/* Store Profile Section */
.store-preview {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  margin-bottom: 20px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 10px;
}

.store-logo {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.store-logo img {
  max-width: 100%;
  max-height: 100%;
}

.logo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.logo-placeholder i {
  font-size: 24px;
}

.store-info h4 {
  margin: 0 0 5px 0;
  font-size: 1rem;
  color: var(--text-color-primary, #1e293b);
}

.store-info p {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
}

/* Currency Settings Section */
.form-preview {
  margin-top: 20px;
}

.form-preview label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  color: var(--text-color-primary, #1e293b);
}

.preview-box {
  padding: 12px;
  border-radius: 8px;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-primary, #1e293b);
  font-size: 1.1rem;
  text-align: center;
  font-weight: 600;
}

/* Discount Settings Section */
.discount-stats {
  display: flex;
  gap: 15px;
  margin-bottom: 24px;
}

.stat-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 8px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.stat-icon.active {
  background-color: rgba(52, 211, 153, 0.2);
  color: var(--success-color, #34d399);
}

.stat-icon.inactive {
  background-color: rgba(148, 163, 184, 0.2);
  color: var(--text-color-secondary, #94a3b8);
}

.stat-icon.admin {
  background-color: rgba(79, 70, 229, 0.2);
  color: var(--primary-color, #4f46e5);
}

.stat-icon.cashier {
  background-color: rgba(245, 158, 11, 0.2);
  color: var(--warning-color, #f59e0b);
}

.stat-icon i {
  font-size: 20px;
}

.stat-info h4 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--text-color-primary, #1e293b);
}

.stat-info p {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-color-secondary, #64748b);
}

.sub-heading {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.discount-list table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
  background-color: var(--background-color-primary, white);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.discount-list th,
.discount-list td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.discount-list th {
  font-weight: 600;
  color: var(--text-color-secondary, #64748b);
  background-color: var(--background-color-secondary, #f8fafc);
}

.discount-list tr:last-child td {
  border-bottom: none;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.active {
  background-color: rgba(52, 211, 153, 0.1);
  color: var(--success-color, #34d399);
}

.status-badge.inactive {
  background-color: rgba(148, 163, 184, 0.1);
  color: var(--text-color-secondary, #94a3b8);
}

.no-data-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 8px;
  color: var(--text-color-secondary, #64748b);
}

.no-data-message i {
  font-size: 40px;
  margin-bottom: 15px;
  opacity: 0.5;
}

.no-data-message p {
  margin: 0;
}

/* User Management Section */
.user-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 15px;
}

.user-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 8px;
  text-align: center;
}

.user-avatar {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
  font-weight: 600;
  font-size: 1.25rem;
  margin-bottom: 15px;
}

.user-details h5 {
  margin: 0 0 5px 0;
  font-size: 1rem;
  color: var(--text-color-primary, #1e293b);
}

.user-role {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: 10px;
}

.user-role.admin {
  background-color: rgba(79, 70, 229, 0.1);
  color: var(--primary-color, #4f46e5);
}

.user-role.cashier {
  background-color: rgba(245, 158, 11, 0.1);
  color: var(--warning-color, #f59e0b);
}

.user-status {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.status-indicator.online {
  background-color: var(--success-color, #34d399);
}

.status-indicator.offline {
  background-color: var(--text-color-secondary, #94a3b8);
}

.status-text {
  font-size: 0.75rem;
  color: var(--text-color-secondary, #64748b);
}

/* Theme Chooser */
.theme-options {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.theme-option {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.theme-option input[type="radio"] {
  display: none;
}

.theme-preview {
  width: 100%;
  height: 80px;
  border-radius: 8px;
  margin-bottom: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: border-color 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.theme-option.active .theme-preview {
  border-color: var(--primary-color, #4f46e5);
}

.light-theme {
  background-color: white;
}

.light-theme .preview-header {
  height: 20px;
  background-color: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.light-theme .preview-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 5px;
}

.light-theme .preview-content::before,
.light-theme .preview-content::after {
  content: "";
  height: 6px;
  background-color: #f1f5f9;
  border-radius: 3px;
}

.dark-theme {
  background-color: #1e293b;
}

.dark-theme .preview-header {
  height: 20px;
  background-color: #0f172a;
  border-bottom: 1px solid #334155;
}

.dark-theme .preview-content {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 5px;
}

.dark-theme .preview-content::before,
.dark-theme .preview-content::after {
  content: "";
  height: 6px;
  background-color: #334155;
  border-radius: 3px;
}

.auto-theme {
  position: relative;
  overflow: hidden;
  background-color: #f1f5f9;
}

.preview-split {
  display: flex;
  width: 100%;
  height: 100%;
}

.light-half {
  width: 50%;
  height: 100%;
  background-color: white;
}

.dark-half {
  width: 50%;
  height: 100%;
  background-color: #1e293b;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-save, .btn-secondary, .btn-primary {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.btn-save {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.btn-save:hover {
  background-color: var(--primary-color-dark, #4338ca);
}

.btn-secondary {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
}

.btn-secondary:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

.btn-primary {
  background-color: var(--primary-color, #4f46e5);
  color: white;
  text-decoration: none;
}

.btn-primary:hover {
  background-color: var(--primary-color-dark, #4338ca);
}

/* Toast Notification */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1001;
}

.toast.success {
  background-color: var(--success-color, #10b981);
}

.toast.error {
  background-color: var(--danger-color, #ef4444);
}

.toast-close {
  background: transparent;
  border: none;
  color: white;
  opacity: 0.7;
  cursor: pointer;
  display: flex;
  padding: 0;
}

.toast-close:hover {
  opacity: 1;
}

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Responsive Styles */
@media (max-width: 1200px) {
  .metrics-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .settings-management {
    padding: 0 15px 30px;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .discount-stats {
    flex-direction: column;
  }

  .theme-options {
    flex-wrap: wrap;
  }

  .theme-option {
    flex: 0 0 calc(50% - 7.5px);
  }
}

@media (max-width: 480px) {
  .form-actions {
    flex-direction: column;
  }

  .btn-save, .btn-secondary, .btn-primary {
    width: 100%;
    justify-content: center;
  }

  .settings-nav-btn span {
    display: none;
  }

  .section-header h3 {
    font-size: 1rem;
  }

  .user-grid {
    grid-template-columns: 1fr;
  }
}
</style>