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

      <div class="settings-container">
        <!-- Dashboard Summary -->
        <div class="dashboard-summary">
          <div class="welcome-message">
            <h2>Point of Sales Configurations & Settings</h2>
            <p>Configure your store settings from a single dashboard with ease.</p>
          </div>
        </div>

        <!-- Settings Navigation -->
        <div class="settings-nav">
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

        <!-- Settings Cards Grid -->
        <div class="settings-cards">
          <!-- Store Profile Card -->
          <div v-if="activeSection === 'store' || activeSection === 'all'" class="settings-card store-profile">
            <div class="settings-card-header">
              <div class="settings-card-icon">
                <i class="material-icons">store</i>
              </div>
              <h3>Store Profile</h3>
            </div>
            <div class="settings-card-content">
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
                  <input type="file" id="logo-upload" @change="handleStoreLogoUpload" accept="image/*" />
                  <label for="logo-upload" class="upload-btn">
                    <i class="material-icons">cloud_upload</i> Upload Logo
                  </label>
                </div>
              </div>
            </div>
            <div class="settings-card-footer">
              <button class="btn-save" @click="saveStoreSettings">
                <i class="material-icons">save</i> Save Changes
              </button>
            </div>
          </div>

          <!-- Currency Settings Card -->
          <div v-if="activeSection === 'currency' || activeSection === 'all'" class="settings-card currency-settings">
            <div class="settings-card-header">
              <div class="settings-card-icon">
                <i class="material-icons">payments</i>
              </div>
              <h3>Currency Settings</h3>
            </div>
            <div class="settings-card-content">
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
            </div>
            <div class="settings-card-footer">
              <button class="btn-save" @click="saveCurrencySettings">
                <i class="material-icons">save</i> Save Changes
              </button>
            </div>
          </div>

          <!-- Tax Settings Card -->
          <div v-if="activeSection === 'taxes' || activeSection === 'all'" class="settings-card tax-settings">
            <div class="settings-card-header">
              <div class="settings-card-icon">
                <i class="material-icons">account_balance</i>
              </div>
              <h3>Tax Settings</h3>
            </div>
            <div class="settings-card-content">
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
            </div>
            <div class="settings-card-footer">
              <button class="btn-save" @click="saveTaxSettings">
                <i class="material-icons">save</i> Save Changes
              </button>
            </div>
          </div>

          <!-- Discounts Management Card -->
          <div v-if="activeSection === 'discounts' || activeSection === 'all'" class="settings-card discounts-settings">
            <div class="settings-card-header">
              <div class="settings-card-icon">
                <i class="material-icons">local_offer</i>
              </div>
              <h3>Discounts Management</h3>
            </div>
            <div class="settings-card-content">
              <div class="discount-stats">
                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="material-icons">local_offer</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ discountStats.total }}</h4>
                    <p>Total Discounts</p>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon active">
                    <i class="material-icons">check_circle</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ discountStats.active }}</h4>
                    <p>Active Discounts</p>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon inactive">
                    <i class="material-icons">block</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ discountStats.inactive }}</h4>
                    <p>Inactive Discounts</p>
                  </div>
                </div>
              </div>

              <div class="discount-list-preview">
                <h4>Recent Discounts</h4>
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
                    <tr v-for="discount in discounts.slice(0, 3)" :key="discount.id">
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
                <div v-else class="no-discounts">
                  <p>No discounts created yet</p>
                </div>
              </div>
            </div>
            <div class="settings-card-footer">
              <router-link to="/discounts" class="btn-manage">
                <i class="material-icons">settings</i> Manage Discounts
              </router-link>
            </div>
          </div>

          <!-- Receipt Settings Card -->
          <div v-if="activeSection === 'receipt' || activeSection === 'all'" class="settings-card receipt-settings">
            <div class="settings-card-header">
              <div class="settings-card-icon">
                <i class="material-icons">receipt</i>
              </div>
              <h3>Receipt Settings</h3>
            </div>
            <div class="settings-card-content">
              <!-- Loading State -->
              <div v-if="receiptLoading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>Loading receipt settings...</p>
              </div>

              <!-- Receipt Settings Form -->
              <div v-else>
                <div class="form-group">
                  <label>Business Name</label>
                  <input
                    type="text"
                    v-model="receiptSettings.business_name"
                    placeholder="Enter your business name"
                  />
                </div>

                <div class="form-group">
                  <label>Receipt Header Text</label>
                  <textarea
                    v-model="receiptSettings.header_text"
                    placeholder="Enter text to display at the top of receipts"
                    rows="2"
                  ></textarea>
                </div>

                <div class="form-group">
                  <label>Receipt Footer Text</label>
                  <textarea
                    v-model="receiptSettings.footer_text"
                    placeholder="Enter text to display at the bottom of receipts"
                    rows="2"
                  ></textarea>
                </div>

                <div class="form-group">
                  <label>Legal Text</label>
                  <textarea
                    v-model="receiptSettings.legal_text"
                    placeholder="Enter legal text or return policy"
                    rows="3"
                  ></textarea>
                </div>

                <div class="form-group">
                  <label>Store Logo</label>
                  <div class="logo-upload-section">
                    <div v-if="receiptSettings.logo_filename" class="current-logo">
                      <img :src="getLogoUrl(receiptSettings.logo_filename)" alt="Store Logo" class="logo-preview">
                      <button @click="removeLogo" class="remove-logo-btn">
                        <i class="material-icons">delete</i>
                      </button>
                    </div>
                    <div class="file-upload">
                      <input
                        type="file"
                        id="receipt-logo-upload"
                        @change="handleLogoUpload"
                        accept="image/*"
                        ref="logoInput"
                      />
                      <label for="receipt-logo-upload" class="upload-btn">
                        <i class="material-icons">cloud_upload</i>
                        {{ receiptSettings.logo_filename ? 'Change Logo' : 'Upload Logo' }}
                      </label>
                    </div>
                    <p class="help-text">Recommended size: 200x100px or smaller. Max file size: 2MB</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="settings-card-footer">
              <button
                class="btn-save"
                @click="saveReceiptSettings"
                :disabled="receiptSaving"
              >
                <i class="material-icons">{{ receiptSaving ? 'hourglass_top' : 'save' }}</i>
                {{ receiptSaving ? 'Saving...' : 'Save Changes' }}
              </button>
              <button class="btn-preview" @click="previewReceipt">
                <i class="material-icons">visibility</i> Preview
              </button>
            </div>
          </div>

          <!-- User Management Card -->
          <div v-if="activeSection === 'users' || activeSection === 'all'" class="settings-card users-settings">
            <div class="settings-card-header">
              <div class="settings-card-icon">
                <i class="material-icons">group</i>
              </div>
              <h3>User Management</h3>
            </div>
            <div class="settings-card-content">
              <div class="user-stats">
                <div class="stat-item">
                  <div class="stat-icon">
                    <i class="material-icons">people</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ userStats.total }}</h4>
                    <p>Total Users</p>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon admin">
                    <i class="material-icons">admin_panel_settings</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ userStats.admins }}</h4>
                    <p>Administrators</p>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon cashier">
                    <i class="material-icons">point_of_sale</i>
                  </div>
                  <div class="stat-info">
                    <h4>{{ userStats.cashiers }}</h4>
                    <p>Cashiers</p>
                  </div>
                </div>
              </div>

              <div class="recent-users">
                <h4>Recent Users</h4>
                <div class="user-list">
                  <div v-for="user in users.slice(0, 3)" :key="user.id" class="user-item">
                    <div class="user-avatar">
                      <span>{{ getUserInitials(user.name) }}</span>
                    </div>
                    <div class="user-details">
                      <h5>{{ user.name }}</h5>
                      <span :class="['user-role', user.role.toLowerCase()]">{{ user.role }}</span>
                    </div>
                    <div class="user-status">
                      <span :class="['status-indicator', user.active ? 'online' : 'offline']"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="settings-card-footer">
              <router-link to="/users" class="btn-manage">
                <i class="material-icons">settings</i> Manage Users
              </router-link>
            </div>
          </div>

          <!-- System Preferences Card -->
          <div v-if="activeSection === 'system' || activeSection === 'all'" class="settings-card system-settings">
            <div class="settings-card-header">
              <div class="settings-card-icon">
                <i class="material-icons">tune</i>
              </div>
              <h3>System Preferences</h3>
            </div>
            <div class="settings-card-content">
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
            </div>
            <div class="settings-card-footer">
              <button class="btn-save" @click="saveSystemSettings">
                <i class="material-icons">save</i> Save Changes
              </button>
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
</template>

<script>
export default {
  name: 'SettingsView',
  data() {
    return {
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

      // Settings sections
      activeSection: 'all',
      settingsSections: [
        { id: 'all', name: 'All Settings', icon: 'dashboard' },
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

      // Receipt settings - Updated to match API
      receiptSettings: {
        business_name: '',
        header_text: '',
        footer_text: '',
        legal_text: '',
        logo_filename: null
      },
      receiptLoading: false,
      receiptSaving: false,

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
    handleStoreLogoUpload(event) {
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

    // Receipt API methods
    async fetchReceiptSettings() {
      this.receiptLoading = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/receipt-settings', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.receiptSettings = {
            business_name: data.business_name || '',
            header_text: data.header_text || '',
            footer_text: data.footer_text || '',
            legal_text: data.legal_text || '',
            logo_filename: data.logo_filename || null
          };
        } else if (response.status === 404) {
          // No settings found, use defaults
          this.receiptSettings = {
            business_name: '',
            header_text: '',
            footer_text: '',
            legal_text: '',
            logo_filename: null
          };
        } else {
          console.error('Failed to fetch receipt settings');
          this.showToastMessage('Failed to load receipt settings', 'error');
        }
      } catch (error) {
        console.error('Error fetching receipt settings:', error);
        this.showToastMessage('Network error while loading settings', 'error');
      } finally {
        this.receiptLoading = false;
      }
    },

    async saveReceiptSettings() {
      this.receiptSaving = true;
      try {
        const payload = {
          business_name: this.receiptSettings.business_name,
          header_text: this.receiptSettings.header_text,
          footer_text: this.receiptSettings.footer_text,
          legal_text: this.receiptSettings.legal_text
        };

        const response = await fetch('http://127.0.0.1:5000/api/receipt-settings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          this.showToastMessage('Receipt settings saved successfully', 'success');
        } else {
          const errorData = await response.json();
          this.showToastMessage(errorData.message || 'Failed to save settings', 'error');
        }
      } catch (error) {
        console.error('Error saving receipt settings:', error);
        this.showToastMessage('Network error while saving settings', 'error');
      } finally {
        this.receiptSaving = false;
      }
    },

    async handleLogoUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      // Validate file type
      if (!file.type.startsWith('image/')) {
        this.showToastMessage('Please select a valid image file', 'error');
        return;
      }

      // Validate file size (max 2MB)
      if (file.size > 2 * 1024 * 1024) {
        this.showToastMessage('Image size should be less than 2MB', 'error');
        return;
      }

      const formData = new FormData();
      formData.append('logo', file);

      try {
        const response = await fetch('http://127.0.0.1:5000/api/receipt-settings/logo', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const data = await response.json();
          this.receiptSettings.logo_filename = data.filename;
          this.showToastMessage('Logo uploaded successfully', 'success');
        } else {
          const errorData = await response.json();
          this.showToastMessage(errorData.error || 'Failed to upload logo', 'error');
        }
      } catch (error) {
        console.error('Error uploading logo:', error);
        this.showToastMessage('Network error while uploading logo', 'error');
      }

      // Clear the input
      this.$refs.logoInput.value = '';
    },

    removeLogo() {
      this.receiptSettings.logo_filename = null;
      this.showToastMessage('Logo removed. Save changes to apply.', 'success');
    },

    getLogoUrl(filename) {
      if (!filename) return null;
      return `http://127.0.0.1:5000/static/receipt_logos/${filename}`;
    },

    previewReceipt() {
      const sampleReceipt = {
        receipt_id: 'SAMPLE-001',
        created_at: new Date().toISOString(),
        cashier_name: 'John Doe',
        snapshot: {
          items: [
            { name: 'Sample Product 1', quantity: 2, price: 29.98 },
            { name: 'Sample Product 2', quantity: 1, price: 15.99 }
          ],
          subtotal: 45.97,
          tax: 3.68,
          discount: 0,
          total: 49.65
        }
      };

      // Open preview in new window
      const previewWindow = window.open('', '_blank', 'width=400,height=600');
      previewWindow.document.write(`
        <html>
          <head>
            <title>Receipt Preview - ${this.receiptSettings.business_name || 'Your Business'}</title>
            <style>
              body {
                font-family: 'Courier New', monospace;
                margin: 20px;
                max-width: 300px;
              }
              .preview-note {
                background: #f0f0f0;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
              }
              .receipt {
                border: 1px solid #ccc;
                padding: 15px;
                background: white;
              }
              .center { text-align: center; }
              .logo { max-width: 100px; max-height: 60px; margin: 10px auto; }
              .divider { border-top: 1px dashed #000; margin: 10px 0; padding-top: 5px; }
              .flex { display: flex; justify-content: space-between; }
              .bold { font-weight: bold; }
              .small { font-size: 0.9em; }
            </style>
          </head>
          <body>
            <div class="preview-note">
              <strong>Preview Mode</strong><br>
              This shows how your receipt will look with current settings.
            </div>

            <div class="receipt">
              ${this.receiptSettings.logo_filename ?
                `<div class="center">
                   <img src="${this.getLogoUrl(this.receiptSettings.logo_filename)}" class="logo">
                 </div>` : ''}

              <div class="center bold">
                ${this.receiptSettings.business_name || 'YOUR BUSINESS NAME'}
              </div>

              ${this.receiptSettings.header_text ?
                `<div class="center small" style="margin: 10px 0;">
                   ${this.receiptSettings.header_text}
                 </div>` : ''}

              <div class="divider">
                <div class="center">
                  Receipt #${sampleReceipt.receipt_id}<br>
                  ${new Date(sampleReceipt.created_at).toLocaleString()}<br>
                  Cashier: ${sampleReceipt.cashier_name}
                </div>
              </div>

              <div class="divider">
                ${sampleReceipt.snapshot.items.map(item =>
                  `<div class="flex">
                     <span>${item.name} (${item.quantity}x)</span>
                     <span>$${item.price.toFixed(2)}</span>
                   </div>`
                ).join('')}
              </div>

              <div class="divider">
                <div class="flex">
                  <span>Subtotal:</span>
                  <span>$${sampleReceipt.snapshot.subtotal.toFixed(2)}</span>
                </div>
                <div class="flex">
                  <span>Tax:</span>
                  <span>$${sampleReceipt.snapshot.tax.toFixed(2)}</span>
                </div>
                <div class="flex bold" style="border-top: 1px solid #000; padding-top: 5px; margin-top: 5px;">
                  <span>Total:</span>
                  <span>$${sampleReceipt.snapshot.total.toFixed(2)}</span>
                </div>
              </div>

              ${this.receiptSettings.footer_text ?
                `<div class="center small divider">
                   ${this.receiptSettings.footer_text}
                 </div>` : ''}

              ${this.receiptSettings.legal_text ?
                `<div class="center small divider">
                   ${this.receiptSettings.legal_text}
                 </div>` : ''}

              <div class="center divider">
                <div style="height: 20px; background: repeating-linear-gradient(90deg, #000, #000 1px, #fff 1px, #fff 2px); margin: 10px 0;"></div>
                <div class="small">${sampleReceipt.receipt_id}</div>
              </div>
            </div>
          </body>
        </html>
      `);
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
        // For now, we'll just use light mode
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

  watch: {
    // Auto-load receipt settings when receipt tab is clicked
    activeSection(newSection) {
      if (newSection === 'receipt') {
        this.fetchReceiptSettings();
      }
    }
  },

  created() {
    document.addEventListener('click', this.handleClickOutside);
    window.addEventListener('resize', this.handleResize);

    // Load receipt settings if receipt section is active on page load
    if (this.activeSection === 'receipt') {
      this.fetchReceiptSettings();
    }

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

/* Settings Container */
.settings-container {
  padding: 0 20px 40px;
}

/* Settings Navigation */
.settings-nav {
  display: flex;
  flex-wrap: nowrap;
  gap: 10px;
  padding: 10px 0;
  margin-bottom: 20px;
  overflow-x: auto;
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.settings-nav-btn.active {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.settings-nav-btn:hover:not(.active) {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-primary, #1e293b);
}

.settings-nav-btn i {
  font-size: 18px;
}

/* Settings Cards */
.settings-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.settings-card {
  background-color: var(--background-color-primary, white);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.settings-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.settings-card-header {
  padding: 15px 20px;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  align-items: center;
  gap: 12px;
}

.settings-card-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.settings-card-icon i {
  font-size: 24px;
}

.settings-card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.settings-card-content {
  padding: 20px;
}

.settings-card-footer {
  padding: 15px 20px;
  border-top: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* Form Elements */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 0.875rem;
  color: var(--text-color-primary, #1e293b);
}

.form-group input[type="text"],
.form-group input[type="tel"],
.form-group input[type="email"],
.form-group input[type="number"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 6px;
  font-size: 0.875rem;
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

/* Store Profile Card */
.store-preview {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
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

/* Currency Settings Card */
.form-preview {
  margin-top: 20px;
}

.preview-box {
  padding: 10px;
  border-radius: 6px;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-primary, #1e293b);
  font-size: 1rem;
  text-align: center;
  font-weight: 600;
}

/* Discount Settings Card */
.discount-stats {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.stat-item {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
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

.discount-list-preview h4,
.recent-users h4 {
  margin-top: 0;
  margin-bottom: 10px;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-color-secondary, #64748b);
}

.discount-list-preview table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.discount-list-preview th,
.discount-list-preview td {
  padding: 8px 10px;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.discount-list-preview th {
  font-weight: 600;
  color: var(--text-color-secondary, #64748b);
}

.discount-list-preview tr:last-child td {
  border-bottom: none;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
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

.no-discounts {
  padding: 20px;
  text-align: center;
  color: var(--text-color-secondary, #64748b);
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 6px;
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
  border-radius: 6px;
  margin-bottom: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: border-color 0.2s ease;
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

/* User List */
.user-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user-item {
  display: flex;
  align-items: center;
  padding: 8px 10px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 8px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
  font-weight: 600;
  font-size: 0.875rem;
  margin-right: 10px;
}

.user-details {
  flex: 1;
}

.user-details h5 {
  margin: 0 0 2px 0;
  font-size: 0.875rem;
  color: var(--text-color-primary, #1e293b);
}

.user-role {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 1px 6px;
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

/* Buttons */
.btn-save, .btn-preview, .btn-manage {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
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

.btn-preview {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
}

.btn-preview:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

.btn-manage {
  background-color: var(--primary-color, #4f46e5);
  color: white;
  text-decoration: none;
}

.btn-manage:hover {
  background-color: var(--primary-color-dark, #4338ca);
}

/* Toast Notification */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 6px;
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
  .settings-cards {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .settings-container {
    padding: 0 15px 30px;
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
  .settings-card-footer {
    flex-direction: column;
  }

  .btn-save, .btn-preview, .btn-manage {
    width: 100%;
    justify-content: center;
  }

  .settings-nav-btn {
    padding: 8px 12px;
  }

  .settings-nav-btn span {
    display: none;
  }

  .settings-card-header h3 {
    font-size: 1rem;
  }
}

/* Receipt Settings Specific Styles */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  gap: 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(79, 70, 229, 0.2);
  border-radius: 50%;
  border-top-color: #4f46e5;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.logo-upload-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.current-logo {
  position: relative;
  display: inline-block;
}

.logo-preview {
  max-width: 200px;
  max-height: 100px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid #e2e8f0;
}

.remove-logo-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #ef4444;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: background-color 0.2s ease;
}

.remove-logo-btn:hover {
  background-color: #dc2626;
}

.help-text {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>