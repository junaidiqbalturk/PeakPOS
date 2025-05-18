<template>
  <div class="dashboard-app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Left Navigation Sidebar with responsive behavior -->
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
          <router-link to="/" class="nav-item">
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
          <router-link to="/inventory" class="nav-item">
            <i class="material-icons">inventory</i>
            <span class="nav-label">Inventory</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Inventory</div>
          </router-link>
          <router-link to="/products" class="nav-item">
            <i class="material-icons">category</i>
            <span class="nav-label">Products</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Products</div>
          </router-link>
          <router-link to="/discounts" class="nav-item active">
            <i class="material-icons">local_offer</i>
            <span class="nav-label">Discounts</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Discounts</div>
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
          <router-link to="/settings" class="nav-item">
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

    <!-- Main Content Area with responsive design -->
    <main class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <header class="top-header">
        <div class="header-left">
          <button class="mobile-toggle" @click="toggleSidebar">
            <i class="material-icons">menu</i>
          </button>

          <div class="page-info">
            <h1 class="page-title">Discount Management</h1>
            <div class="breadcrumb">
              <span>PeakPOS</span>
              <i class="material-icons">chevron_right</i>
              <span class="current">Discounts</span>
            </div>
          </div>
        </div>

        <div class="header-middle">
          <div class="search-container">
            <i class="material-icons">search</i>
            <input type="text" v-model="searchQuery" placeholder="Search discounts..." class="search-input" />
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

            <button @click="showAddForm = true" class="btn-add header-btn">
              <i class="material-icons">add</i> <span>New Discount</span>
            </button>
          </div>
        </div>
      </header>

      <div class="discounts-management">
        <!-- Dashboard Summary -->
        <div class="dashboard-summary">
          <div class="welcome-message">
            <h2>Discount Management</h2>
            <p>Create and manage special offers and discounts for your customers.</p>
          </div>
        </div>

        <!-- Modern Metrics Grid with Animated 3D Cards -->
        <div class="metrics-grid">
          <!-- Total Discounts Card -->
          <div class="metric-card discounts" :style="{ '--delay': '0.1s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">local_offer</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span class="trend-value">{{ discounts.length }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Total Discounts</div>
                <div class="metric-value">
                  <span class="value-number">{{ discounts.length }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in [50, 60, 70, 65, 80, 75, 90]"
                         :key="index"
                         :style="{ height: `${value}%`, animationDelay: `${index * 0.1}s` }"></div>
                  </div>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>

          <!-- Active Discounts Card -->
          <div class="metric-card active" :style="{ '--delay': '0.2s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">check_circle</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span class="trend-value">{{ activeDiscountsCount }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Active Discounts</div>
                <div class="metric-value">
                  <span class="value-number">{{ activeDiscountsCount }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in [40, 50, 60, 70, 65, 75, 80]"
                        :key="index"
                        :style="{ height: `${value}%`, animationDelay: `${index * 0.1}s` }"></div>
                  </div>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>

          <!-- Highest Discount Card -->
          <div class="metric-card highest" :style="{ '--delay': '0.3s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon success">
                  <i class="material-icons">star</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span class="trend-value">{{ highestDiscountDisplay }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Highest Discount</div>
                <div class="metric-value">
                  <span class="value-number">{{ highestDiscountDisplay }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in [80, 70, 60, 50, 55, 45, 60]"
                        :key="index"
                        :style="{ height: `${value}%`, animationDelay: `${index * 0.1}s` }"></div>
                  </div>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>
        </div>

        <!-- Filter and Controls -->
        <div class="filters-section">
          <div class="filter-header">
            <h3>All Discounts</h3>
            <div class="view-controls">
              <button
                @click="viewMode = 'grid'"
                :class="['view-btn', { active: viewMode === 'grid' }]"
              >
                <i class="material-icons">grid_view</i>
              </button>
              <button
                @click="viewMode = 'list'"
                :class="['view-btn', { active: viewMode === 'list' }]"
              >
                <i class="material-icons">view_list</i>
              </button>
            </div>
          </div>

          <div class="filters-row">
            <div class="filter-group">
              <label for="status-filter">Status</label>
              <select
                id="status-filter"
                v-model="statusFilter"
                class="filter-select"
              >
                <option value="all">All Statuses</option>
                <option value="active">Active Only</option>
                <option value="inactive">Inactive Only</option>
              </select>
            </div>

            <div class="filter-group">
              <label for="type-filter">Type</label>
              <select
                id="type-filter"
                v-model="typeFilter"
                class="filter-select"
              >
                <option value="all">All Types</option>
                <option value="percentage">Percentage</option>
                <option value="fixed">Fixed Amount</option>
              </select>
            </div>

            <div class="filter-group">
              <label for="sort-select">Sort By</label>
              <select
                id="sort-select"
                v-model="sortBy"
                class="filter-select"
              >
                <option value="name-asc">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
                <option value="value-asc">Value (Low to High)</option>
                <option value="value-desc">Value (High to Low)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading discounts...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredDiscounts.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="material-icons">local_offer</i>
          </div>
          <h3>No Discounts Found</h3>
          <p v-if="searchQuery || statusFilter !== 'all' || typeFilter !== 'all'">Try adjusting your filters or search criteria.</p>
          <p v-else>You haven't created any discounts yet. Create your first discount to get started.</p>
          <button @click="showAddForm = true" class="btn-primary">
            <i class="material-icons">add</i>
            Create First Discount
          </button>
        </div>

        <!-- Grid View -->
        <div v-else-if="viewMode === 'grid'" class="discount-grid">
          <div v-for="discount in filteredDiscounts" :key="discount.id" class="discount-card" :class="{ 'inactive': !discount.active }">
            <div class="discount-header" :class="{ 'percentage': discount.discount_type === 'percentage', 'fixed': discount.discount_type === 'fixed' }">
              <div class="discount-icon">
                <i class="material-icons">{{ discount.discount_type === 'percentage' ? 'percent' : 'payments' }}</i>
              </div>
              <div class="discount-badge">
                {{ discount.discount_type === 'percentage' ? discount.value + '%' : '$' + discount.value.toFixed(2) }}
              </div>
            </div>

            <div class="discount-details">
              <div class="discount-status">
                <span :class="{ 'active-status': discount.active, 'inactive-status': !discount.active }">
                  {{ discount.active ? 'Active' : 'Inactive' }}
                </span>
              </div>
              <h3 class="discount-name">{{ discount.name }}</h3>
              <p class="discount-type">
                {{ discount.discount_type === 'percentage' ? 'Percentage discount' : 'Fixed amount discount' }}
              </p>
            </div>

            <div class="discount-actions">
              <button @click="editDiscount(discount)" class="edit-btn">
                <i class="material-icons">edit</i>
                Edit
              </button>
              <button @click="confirmDelete(discount)" class="delete-btn">
                <i class="material-icons">delete</i>
                Delete
              </button>
            </div>
          </div>

          <!-- Add New Discount Card -->
          <div class="discount-card add-new-card" @click="showAddForm = true">
            <div class="add-new-content">
              <div class="add-icon">
                <i class="material-icons">add_circle</i>
              </div>
              <span>Add New Discount</span>
            </div>
          </div>
        </div>

        <!-- List View -->
        <div v-else class="discount-list">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Value</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="discount in filteredDiscounts" :key="discount.id" :class="{ 'inactive-row': !discount.active }">
                <td>
                  <div class="discount-name-cell">
                    <div class="discount-color-indicator" :class="{ 'percentage': discount.discount_type === 'percentage', 'fixed': discount.discount_type === 'fixed' }"></div>
                    {{ discount.name }}
                  </div>
                </td>
                <td>{{ discount.discount_type === 'percentage' ? 'Percentage' : 'Fixed Amount' }}</td>
                <td>{{ discount.discount_type === 'percentage' ? discount.value + '%' : '$' + discount.value.toFixed(2) }}</td>
                <td>
                  <span :class="{ 'active-status': discount.active, 'inactive-status': !discount.active }">
                    {{ discount.active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <div class="action-icons">
                    <button @click="toggleDiscountStatus(discount)" class="action-icon toggle">
                      <i class="material-icons">{{ discount.active ? 'toggle_on' : 'toggle_off' }}</i>
                    </button>
                    <button @click="editDiscount(discount)" class="action-icon edit">
                      <i class="material-icons">edit</i>
                    </button>
                    <button @click="confirmDelete(discount)" class="action-icon delete">
                      <i class="material-icons">delete</i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Add/Edit Discount Modal -->
        <transition name="modal">
          <div class="modal-overlay" v-if="showAddForm">
            <div class="modal-container" @click.stop>
              <div class="modal-header">
                <h2>{{ editingDiscount ? 'Edit Discount' : 'Add New Discount' }}</h2>
                <button @click="cancelForm" class="close-button">
                  <i class="material-icons">close</i>
                </button>
              </div>

              <div class="modal-body">
                <form @submit.prevent="saveDiscount" class="discount-form">
                  <div class="form-group">
                    <label for="discountName">Discount Name</label>
                    <input
                      type="text"
                      id="discountName"
                      v-model="formData.name"
                      required
                      class="form-input"
                      placeholder="Enter discount name"
                    />
                    <span class="error-message" v-if="errors.name">{{ errors.name }}</span>
                  </div>

                  <div class="form-group">
                    <label for="discountType">Discount Type</label>
                    <select
                      id="discountType"
                      v-model="formData.discount_type"
                      required
                      class="form-input"
                    >
                      <option value="percentage">Percentage (%)</option>
                      <option value="fixed">Fixed Amount ($)</option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="discountValue">
                      {{ formData.discount_type === 'percentage' ? 'Percentage Value' : 'Amount' }}
                    </label>
                    <div class="value-input-container">
                      <input
                        type="number"
                        id="discountValue"
                        v-model.number="formData.value"
                        required
                        min="0"
                        step="0.01"
                        class="form-input"
                        placeholder="Enter value"
                      />
                      <span class="value-suffix">{{ formData.discount_type === 'percentage' ? '%' : '$' }}</span>
                    </div>
                    <span class="error-message" v-if="errors.value">{{ errors.value }}</span>
                  </div>

                  <div class="form-group checkbox-group">
                    <label class="checkbox-container">
                      <input type="checkbox" v-model="formData.active" />
                      <span class="checkmark"></span>
                      Active
                    </label>
                    <span class="help-text">Inactive discounts won't be available in checkout.</span>
                  </div>

                  <div class="form-actions">
                    <button type="button" @click="cancelForm" class="btn-cancel">
                      Cancel
                    </button>
                    <button type="submit" class="btn-save" :disabled="isSubmitting">
                      <i class="material-icons">{{ isSubmitting ? 'hourglass_top' : 'save' }}</i>
                      {{ isSubmitting ? 'Saving...' : (editingDiscount ? 'Update Discount' : 'Save Discount') }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </transition>

        <!-- Delete Confirmation Modal -->
        <transition name="modal">
          <div class="modal-overlay" v-if="showDeleteModal">
            <div class="confirm-modal">
              <div class="confirm-modal-header">
                <i class="material-icons warning">warning</i>
                <h3>Confirm Delete</h3>
              </div>
              <div class="confirm-modal-body">
                <p>Are you sure you want to delete the discount <strong>{{ discountToDelete ? discountToDelete.name : '' }}</strong>?</p>
                <p class="delete-warning">This action cannot be undone. This discount will no longer be available in checkout.</p>
              </div>
              <div class="confirm-modal-footer">
                <button @click="cancelDelete" class="btn-cancel">Cancel</button>
                <button @click="deleteDiscount" class="btn-delete" :disabled="isDeleting">
                  <i class="material-icons" v-if="isDeleting">hourglass_top</i>
                  <span>{{ isDeleting ? 'Deleting...' : 'Delete Discount' }}</span>
                </button>
              </div>
            </div>
          </div>
        </transition>

        <!-- Success/Error Toast Message -->
        <transition name="toast">
          <div v-if="toast.show" :class="['toast', toast.type]">
            <i class="material-icons">{{ toast.type === 'success' ? 'check_circle' : 'error' }}</i>
            <span>{{ toast.message }}</span>
          </div>
        </transition>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'DiscountManagement',
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

      // Discount management data
      discounts: [],
      loading: false,
      viewMode: localStorage.getItem('discountViewMode') || 'grid',
      searchQuery: '',
      statusFilter: 'all',
      typeFilter: 'all',
      sortBy: 'name-asc',

      // Form data
      showAddForm: false,
      editingDiscount: null,
      formData: {
        name: '',
        discount_type: 'percentage',
        value: 0,
        active: true
      },
      errors: {
        name: '',
        value: ''
      },
      isSubmitting: false,

      // Delete confirmation
      showDeleteModal: false,
      discountToDelete: null,
      isDeleting: false,

      // Toast notification
      toast: {
        show: false,
        message: '',
        type: 'success',
        timeout: null
      }
    };
  },

  computed: {
    filteredDiscounts() {
      return this.discounts
        .filter(discount => {
          // Apply search filter
          if (this.searchQuery) {
            return discount.name.toLowerCase().includes(this.searchQuery.toLowerCase());
          }
          return true;
        })
        .filter(discount => {
          // Apply status filter
          if (this.statusFilter === 'all') return true;
          if (this.statusFilter === 'active') return discount.active;
          if (this.statusFilter === 'inactive') return !discount.active;
          return true;
        })
        .filter(discount => {
          // Apply type filter
          if (this.typeFilter === 'all') return true;
          return discount.discount_type === this.typeFilter;
        })
        .sort((a, b) => {
          // Apply sorting
          switch (this.sortBy) {
            case 'name-asc':
              return a.name.localeCompare(b.name);
            case 'name-desc':
              return b.name.localeCompare(a.name);
            case 'value-asc':
              return a.value - b.value;
            case 'value-desc':
              return b.value - a.value;
            default:
              return a.name.localeCompare(b.name);
          }
        });
    },

    activeDiscountsCount() {
      return this.discounts.filter(discount => discount.active).length;
    },

    highestDiscount() {
      if (this.discounts.length === 0) return null;

      // Find the highest percentage and fixed discounts
      let highestPercentage = { value: 0, type: 'percentage' };
      let highestFixed = { value: 0, type: 'fixed' };

      this.discounts.forEach(discount => {
        if (discount.discount_type === 'percentage' && discount.value > highestPercentage.value) {
          highestPercentage = { value: discount.value, type: 'percentage' };
        } else if (discount.discount_type === 'fixed' && discount.value > highestFixed.value) {
          highestFixed = { value: discount.value, type: 'fixed' };
        }
      });

      // Return the highest one (preferring percentage if equal)
      if (highestPercentage.value > 0) {
        return highestPercentage;
      } else if (highestFixed.value > 0) {
        return highestFixed;
      }

      return null;
    },

    highestDiscountDisplay() {
      if (!this.highestDiscount) return 'None';
      return this.highestDiscount.type === 'percentage'
        ? `${this.highestDiscount.value}%`
        : `$${this.highestDiscount.value.toFixed(2)}`;
    }
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

    // CRUD operations
    async fetchDiscounts() {
      this.loading = true;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/discounts');

        if (response.ok) {
          const discounts = await response.json();
          // Ensure each discount has an active property
          this.discounts = discounts.map(d => ({
            ...d,
            active: d.active !== undefined ? d.active : true
          }));
        } else {
          this.showToastMessage('Failed to load discounts', 'error');
        }
      } catch (error) {
        console.error('Error fetching discounts:', error);
        this.showToastMessage('Network error. Please try again.', 'error');
      } finally {
        this.loading = false;
      }
    },

    editDiscount(discount) {
      this.editingDiscount = discount;
      this.formData = {
        name: discount.name,
        discount_type: discount.discount_type,
        value: discount.value,
        active: discount.active !== undefined ? discount.active : true
      };
      this.errors = { name: '', value: '' };
      this.showAddForm = true;
    },

    toggleDiscountStatus(discount) {
      const newStatus = !discount.active;
      this.updateDiscountStatus(discount, newStatus);
    },

    async updateDiscountStatus(discount, newStatus) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/discounts/${discount.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({ active: newStatus })
        });

        if (response.ok) {
          // Update local state
          const index = this.discounts.findIndex(d => d.id === discount.id);
          if (index !== -1) {
            this.discounts[index].active = newStatus;
          }

          this.showToastMessage(
            `Discount ${newStatus ? 'activated' : 'deactivated'} successfully`,
            'success'
          );
        } else {
          this.showToastMessage('Failed to update discount status', 'error');
        }
      } catch (error) {
        console.error('Error updating discount status:', error);
        this.showToastMessage('Network error. Please try again.', 'error');
      }
    },

    cancelForm() {
      this.showAddForm = false;
      this.editingDiscount = null;
      this.formData = {
        name: '',
        discount_type: 'percentage',
        value: 0,
        active: true
      };
      this.errors = { name: '', value: '' };
    },

    async saveDiscount() {
      // Validate form data
      this.errors = { name: '', value: '' };

      if (!this.formData.name.trim()) {
        this.errors.name = 'Discount name is required';
        return;
      }

      if (this.formData.value <= 0) {
        this.errors.value = 'Value must be greater than 0';
        return;
      }

      if (this.formData.discount_type === 'percentage' && this.formData.value > 100) {
        this.errors.value = 'Percentage value cannot exceed 100%';
        return;
      }

      this.isSubmitting = true;

      try {
        const url = this.editingDiscount
          ? `http://127.0.0.1:5000/api/discounts/${this.editingDiscount.id}`
          : 'http://127.0.0.1:5000/api/discounts';

        const method = this.editingDiscount ? 'PUT' : 'POST';

        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.formData)
        });

        const data = await response.json();

        if (response.ok) {
          // Update local data
          if (this.editingDiscount) {
            const index = this.discounts.findIndex(d => d.id === this.editingDiscount.id);
            if (index !== -1) {
              // Ensure active property is included
              this.discounts[index] = {
                ...data.discount,
                active: data.discount.active !== undefined ? data.discount.active : true
              };
            }
          } else {
            // Add active property if needed
            this.discounts.push({
              ...data.discount,
              active: data.discount.active !== undefined ? data.discount.active : true
            });
          }

          this.showAddForm = false;
          this.editingDiscount = null;
          this.formData = {
            name: '',
            discount_type: 'percentage',
            value: 0,
            active: true
          };

          this.showToastMessage(
            `Discount ${this.editingDiscount ? 'updated' : 'created'} successfully`,
            'success'
          );
        } else {
          // Handle error
          this.showToastMessage(data.error || 'Failed to save discount', 'error');
        }
      } catch (error) {
        console.error('Error saving discount:', error);
        this.showToastMessage('Network error. Please try again.', 'error');
      } finally {
        this.isSubmitting = false;
      }
    },

    confirmDelete(discount) {
      this.discountToDelete = discount;
      this.showDeleteModal = true;
    },

    cancelDelete() {
      this.showDeleteModal = false;
      this.discountToDelete = null;
    },

    async deleteDiscount() {
      if (!this.discountToDelete) return;

      this.isDeleting = true;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/discounts/${this.discountToDelete.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          // Remove from local array
          const index = this.discounts.findIndex(d => d.id === this.discountToDelete.id);
          if (index !== -1) {
            this.discounts.splice(index, 1);
          }

          this.showToastMessage('Discount deleted successfully', 'success');
        } else {
          const data = await response.json();
          this.showToastMessage(data.error || 'Failed to delete discount', 'error');
        }
      } catch (error) {
        console.error('Error deleting discount:', error);
        this.showToastMessage('Network error. Please try again.', 'error');
      } finally {
        this.isDeleting = false;
        this.showDeleteModal = false;
        this.discountToDelete = null;
      }
    },

    // UI helpers
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

    // Fetch discounts when component is created
    this.fetchDiscounts();
  },

  unmounted() {
    document.removeEventListener('click', this.handleClickOutside);
    window.removeEventListener('resize', this.handleResize);

    // Save view mode preference
    localStorage.setItem('discountViewMode', this.viewMode);

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

/* Discount Card Grid Styles */
.discount-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.discount-card {
  background: var(--background-color-primary, white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
}

.discount-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.discount-card.inactive {
  opacity: 0.7;
}

.discount-header {
  padding: 25px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.discount-header.percentage {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
}

.discount-header.fixed {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.discount-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
}

.discount-icon i {
  font-size: 24px;
}

.discount-badge {
  font-weight: 600;
  font-size: 18px;
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 16px;
  border-radius: 20px;
}

.discount-details {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.discount-status {
  margin-bottom: 5px;
}

.active-status, .inactive-status {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.active-status {
  background-color: rgba(52, 211, 153, 0.1);
  color: var(--success-color, #34d399);
}

.inactive-status {
  background-color: rgba(148, 163, 184, 0.1);
  color: var(--text-color-secondary, #94a3b8);
}

.discount-name {
  font-size: 18px;
  margin: 0;
  color: var(--text-color-primary, #1e293b);
}

.discount-type {
  font-size: 14px;
  color: var(--text-color-secondary, #64748b);
  margin: 0;
}

.discount-actions {
  display: flex;
  gap: 10px;
  padding: 0 20px 20px 20px;
}

.discount-actions .edit-btn,
.discount-actions .delete-btn {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.discount-actions .edit-btn {
  background: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.discount-actions .delete-btn {
  background: var(--danger-color-light, #fee2e2);
  color: var(--danger-color, #ef4444);
}

.discount-actions .edit-btn:hover {
  background: var(--primary-color-dark, #4338ca);
  color: white;
}

.discount-actions .delete-btn:hover {
  background: var(--danger-color, #ef4444);
  color: white;
}

/* Add New Discount Card */
.add-new-card {
  background: var(--background-color-secondary, #f8fafc);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px dashed var(--border-color, #e2e8f0);
  transition: all 0.2s ease;
}

.add-new-card:hover {
  border-color: var(--primary-color, #4f46e5);
  background: var(--primary-color-light, #ede9fe);
  color: white;
}

.add-new-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 40px 20px;
  color: var(--text-color-secondary, #64748b);
}

.add-icon {
  font-size: 32px;
  color: var(--primary-color, #4f46e5);
}

/* Discount List View */
.discount-list {
  margin-top: 20px;
  overflow-x: auto;
}

.discount-list table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.discount-list th,
.discount-list td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.discount-list th {
  color: var(--text-color-secondary, #64748b);
  font-weight: 600;
  background: var(--background-color-secondary, #f8fafc);
}

.discount-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.discount-color-indicator {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.discount-color-indicator.percentage {
  background-color: #6366f1;
}

.discount-color-indicator.fixed {
  background-color: #f59e0b;
}

.action-icons {
  display: flex;
  gap: 8px;
}

.action-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  background: transparent;
}

.action-icon.toggle {
  color: var(--primary-color, #4f46e5);
  font-size: 20px;
}

.action-icon.edit {
  color: var(--primary-color, #4f46e5);
}

.action-icon.delete {
  color: var(--danger-color, #ef4444);
}

.action-icon.edit:hover {
  background-color: var(--primary-color-light, #ede9fe);
}

.action-icon.delete:hover {
  background-color: var(--danger-color-light, #fee2e2);
}

.inactive-row {
  opacity: 0.7;
  background-color: var(--background-color-secondary, #f8fafc);
}

/* Modal Styles for Add/Edit Form */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: var(--background-color-primary, white);
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
  color: var(--text-color-primary, #1e293b);
}

.close-button {
  background: transparent;
  border: none;
  color: var(--text-color-secondary, #64748b);
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-button:hover {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-primary, #1e293b);
}

.modal-body {
  padding: 20px;
}

.discount-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-color-secondary, #64748b);
}

.form-input {
  padding: 10px 12px;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s ease;
  background-color: var(--background-color-primary, white);
  color: var(--text-color-primary, #1e293b);
}

.form-input:focus {
  border-color: var(--primary-color, #4f46e5);
  outline: none;
}

.value-input-container {
  position: relative;
}

.value-suffix {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-color-secondary, #64748b);
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.help-text {
  font-size: 12px;
  color: var(--text-color-secondary, #64748b);
}

.error-message {
  color: var(--danger-color, #ef4444);
  font-size: 12px;
  margin-top: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.btn-cancel, .btn-save {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.btn-cancel {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
}

.btn-save {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.btn-cancel:hover {
  background-color: var(--border-color, #e2e8f0);
}

.btn-save:hover:not(:disabled) {
  background-color: var(--primary-color-dark, #4338ca);
}

.btn-save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Confirmation Modal */
.confirm-modal {
  background-color: var(--background-color-primary, white);
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
  overflow: hidden;
}

.confirm-modal-header {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.confirm-modal-header i.warning {
  color: var(--warning-color, #f59e0b);
  font-size: 24px;
}

.confirm-modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--text-color-primary, #1e293b);
}

.confirm-modal-body {
  padding: 20px;
}

.delete-warning {
  color: var(--danger-color, #ef4444);
  font-size: 14px;
  margin-top: 10px;
}

.confirm-modal-footer {
  padding: 15px 20px;
  border-top: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-delete {
  background-color: var(--danger-color, #ef4444);
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-delete:hover:not(:disabled) {
  background-color: #dc2626; /* darker red */
}

.btn-delete:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Loading and Empty States */
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
  border: 3px solid rgba(var(--primary-color-rgb, 79, 70, 229), 0.2);
  border-radius: 50%;
  border-top-color: var(--primary-color, #4f46e5);
  animation: spin 1s infinite linear;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 48px;
  height: 80px;
  width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--primary-color, #4f46e5);
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 18px;
  margin: 0 0 10px 0;
}

.empty-state p {
  color: var(--text-color-secondary, #64748b);
  margin-bottom: 20px;
}

.btn-primary {
  background-color: var(--primary-color, #4f46e5);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
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

.toast-enter-active, .toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from, .toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Modal Transitions */
.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-enter-from .confirm-modal {
  transform: translateY(20px);
}

/* Responsive Styles */
@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .discount-grid {
    grid-template-columns: 1fr;
  }

  .modal-container {
    width: 90%;
  }

  .discount-list table {
    min-width: 600px;
  }
}

@media (max-width: 480px) {
  .form-actions {
    flex-direction: column;
  }

  .btn-cancel, .btn-save {
    width: 100%;
    justify-content: center;
  }

  .confirm-modal-footer {
    flex-direction: column;
  }
}
</style>