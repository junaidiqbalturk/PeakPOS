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
          <router-link to="/categories" class="nav-item active">
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

    <!-- Main Content Area with improved responsive design -->
    <main class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <header class="top-header">
        <div class="header-left">
          <button class="mobile-toggle" @click="toggleSidebar">
            <i class="material-icons">menu</i>
          </button>

          <div class="page-info">
            <h1 class="page-title">Category Management</h1>
            <div class="breadcrumb">
              <span>PeakPOS</span>
              <i class="material-icons">chevron_right</i>
              <span class="current">Categories</span>
            </div>
          </div>
        </div>

        <div class="header-middle">
          <div class="search-container">
            <i class="material-icons">search</i>
            <input type="text" v-model="searchQuery" placeholder="Search categories..." class="search-input" />
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
              <i class="material-icons">add</i> <span>New Category</span>
            </button>
          </div>
        </div>
      </header>

      <div class="categories-management">
        <!-- Dashboard Summary -->
        <div class="dashboard-summary">
          <div class="welcome-message">
            <h2>Category Management</h2>
            <p>Organize your product catalog with custom categories. Categories help customers find products quickly and improve your inventory management.</p>
          </div>
        </div>

        <!-- Modern Metrics Grid with Animated 3D Cards -->
        <div class="metrics-grid">
          <!-- Total Categories Card -->
          <div class="metric-card categories" :style="{ '--delay': '0.1s' }">
            <div class="metric-card-inner">
              <div class="metric-card-backdrop"></div>
    <div class="metric-card-glow"></div>
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">category</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">folder</i>
                  <span class="trend-value">{{ categories.length }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Total Categories</div>
                <div class="metric-value">
                  <span class="value-number">{{ categories.length }}</span>
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

          <!-- Products per Category Card -->
          <div class="metric-card sales" :style="{ '--delay': '0.2s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">view_module</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span class="trend-value">{{ avgProductsPerCategory.toFixed(1) }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Avg Products / Category</div>
                <div class="metric-value">
                  <span class="value-number">{{ avgProductsPerCategory.toFixed(1) }}</span>
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

          <!-- Most Popular Category Card -->
          <div class="metric-card items" :style="{ '--delay': '0.3s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon success">
                  <i class="material-icons">star</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span style="display: none;" class="trend-value">{{ mostPopularCategory ? mostPopularCategory.name : 'None' }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Most Popular Category</div>
                <div class="metric-value">
                  <span class="value-number">{{ mostPopularCategory ? mostPopularCategory.name : 'None' }}</span>
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

        <!-- Filter and Controls Section -->
        <div class="filters-section">
          <div class="filter-header">
            <h3>Categories</h3>
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
              <label for="category-sort">Sort By</label>
              <select
                id="category-sort"
                v-model="categorySortBy"
                class="filter-select"
              >
                <option value="name-asc">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
                <option value="products-asc">Products (Low to High)</option>
                <option value="products-desc">Products (High to Low)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading categories...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="categories.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="material-icons">category</i>
          </div>
          <h3>No Categories Yet</h3>
          <p>You haven't created any product categories yet. Categories help organize your products for easier management.</p>
          <button @click="showAddForm = true" class="btn-primary">
            <i class="material-icons">add</i>
            Create First Category
          </button>
        </div>

        <!-- Category Grid View -->
        <div v-else-if="viewMode === 'grid'" class="category-grid">
          <div v-for="category in filteredCategories" :key="category.id" class="category-card">
            <div class="category-header"
              :style="{
                background: `linear-gradient(135deg, ${getCategoryColor(category.id).start}, ${getCategoryColor(category.id).end})`
              }">
              <div class="category-icon">
                <i class="material-icons">category</i>
              </div>
              <div class="category-product-count">
                {{ getProductCountForCategory(category.id) }} Products
              </div>
            </div>

            <div class="category-details">
              <h3 class="category-name">{{ category.name }}</h3>

              <div class="category-stats">
                <div class="product-distribution">
                  <div class="stat-item">
                    <span class="stat-label">In Stock:</span>
                    <span class="stat-value">{{ getInStockCountForCategory(category.id) }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Low Stock:</span>
                    <span class="stat-value">{{ getLowStockCountForCategory(category.id) }}</span>
                  </div>
                </div>
              </div>


              <div class="category-actions">
                <button @click="editCategory(category)" class="edit-btn">
                  <i class="material-icons">edit</i>
                  Edit
                </button>
                <button @click="confirmDelete(category)" class="delete-btn">
                  <i class="material-icons">delete</i>
                  Delete
                </button>
              </div>
            </div>
          </div>

          <!-- Add New Category Card -->
          <div class="category-card add-new-card" @click="showAddForm = true">
            <div class="add-new-content">
              <div class="add-icon">
                <i class="material-icons">add_circle</i>
              </div>
              <span>Add New Category</span>
            </div>
          </div>
        </div>

        <!-- Category List View -->
        <div v-else class="category-list">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Products</th>
                <th>In Stock</th>
                <th>Low Stock</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in filteredCategories" :key="category.id">
                <td>
                  <div class="category-name-cell">
                    <div class="category-color-indicator"
                      :style="{
                        backgroundColor: getCategoryColor(category.id).start
                      }">
                    </div>
                    {{ category.name }}
                  </div>
                </td>
                <td>{{ getProductCountForCategory(category.id) }}</td>
                <td>{{ getInStockCountForCategory(category.id) }}</td>
                <td>{{ getLowStockCountForCategory(category.id) }}</td>
                <td>
                  <div class="action-icons">
                    <button @click="editCategory(category)" class="action-icon edit">
                      <i class="material-icons">edit</i>
                    </button>
                    <button @click="confirmDelete(category)" class="action-icon delete">
                      <i class="material-icons">delete</i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Add/Edit Category Modal -->
        <transition name="modal">
          <div class="modal-overlay" v-if="showAddForm">
            <div class="modal-container" @click.stop>
              <div class="modal-header">
                <h2>{{ editingCategory ? 'Edit Category' : 'Add New Category' }}</h2>
                <button @click="cancelForm" class="close-button">
                  <i class="material-icons">close</i>
                </button>
              </div>

              <div class="modal-body">
                <form @submit.prevent="saveCategory" class="category-form">
                  <div class="form-group">
                    <label for="categoryName">Category Name</label>
                    <input
                      type="text"
                      id="categoryName"
                      v-model="formData.name"
                      required
                      class="form-input"
                      placeholder="Enter category name"
                    />
                    <span class="error-message" v-if="errors.name">{{ errors.name }}</span>
                  </div>

                  <div class="form-group">
                    <label for="categoryDescription">Description (Optional)</label>
                    <textarea
                      id="categoryDescription"
                      v-model="formData.description"
                      class="form-input textarea"
                      placeholder="Enter category description"
                      rows="3"
                    ></textarea>
                  </div>

                  <!-- Color Preview -->
                  <div class="form-group color-preview-section">
                    <label>Category Color Preview</label>
                    <div class="color-preview" :style="{
                      background: editingCategory
                        ? `linear-gradient(135deg, ${getCategoryColor(editingCategory.id).start}, ${getCategoryColor(editingCategory.id).end})`
                        : 'linear-gradient(135deg, #4f46e5, #ec4899)'
                    }">
                      <div class="preview-content">
                        <i class="material-icons">category</i>
                        <span>{{ formData.name || 'New Category' }}</span>
                      </div>
                    </div>
                    <p class="color-note">Colors are automatically generated based on the category name.</p>
                  </div>

                  <div class="form-actions">
                    <button type="button" @click="cancelForm" class="btn-cancel">
                      Cancel
                    </button>
                    <button type="submit" class="btn-save">
                      <i class="material-icons">save</i>
                      {{ editingCategory ? 'Update Category' : 'Save Category' }}
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
                <p>Are you sure you want to delete the category <strong>{{ categoryToDelete ? categoryToDelete.name : '' }}</strong>?</p>
                <p class="delete-warning">This action cannot be undone. Products in this category will not be deleted but will no longer have a category assigned.</p>
              </div>
              <div class="confirm-modal-footer">
                <button @click="cancelDelete" class="btn-cancel">Cancel</button>
                <button @click="deleteCategory" class="btn-delete">Delete Category</button>
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
  name: 'CategoryManagement',
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

      // Category management data
      categories: [],
      products: [], // Need to fetch products to count per category
      isLoading: false,
      viewMode: localStorage.getItem('categoryViewMode') || 'grid',
      searchQuery: '',
      categorySortBy: 'name-asc',

      // Form data
      showAddForm: false,
      editingCategory: null,
      formData: {
        name: '',
        description: ''
      },
      errors: {
        name: ''
      },

      // Delete confirmation
      showDeleteModal: false,
      categoryToDelete: null,

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
    filteredCategories() {
      return this.categories
        .filter(category => {
          // Apply search filter
          if (this.searchQuery) {
            return category.name.toLowerCase().includes(this.searchQuery.toLowerCase());
          }
          return true;
        })
        .sort((a, b) => {
          // Apply sorting
          switch (this.categorySortBy) {
            case 'name-asc':
              return a.name.localeCompare(b.name);
            case 'name-desc':
              return b.name.localeCompare(a.name);
            case 'products-asc':
              return this.getProductCountForCategory(a.id) - this.getProductCountForCategory(b.id);
            case 'products-desc':
              return this.getProductCountForCategory(b.id) - this.getProductCountForCategory(a.id);
            default:
              return a.name.localeCompare(b.name);
          }
        });
    },

    avgProductsPerCategory() {
      if (this.categories.length === 0) return 0;
      return this.products.length / this.categories.length;
    },

    mostPopularCategory() {
      if (this.categories.length === 0) return null;

      // Create a map of category IDs to product counts
      const categoryCounts = {};
      this.products.forEach(product => {
        if (product.category_id) {
          categoryCounts[product.category_id] = (categoryCounts[product.category_id] || 0) + 1;
        }
      });

      // Find the category with the most products
      let maxCount = 0;
      let popularCategoryId = null;

      Object.entries(categoryCounts).forEach(([categoryId, count]) => {
        if (count > maxCount) {
          maxCount = count;
          popularCategoryId = parseInt(categoryId);
        }
      });

      return this.categories.find(c => c.id === popularCategoryId) || null;
    }
  },

  methods: {
    setupCardHoverEffects() {
    // Apply hover effects to category cards
    document.querySelectorAll('.category-card-inner').forEach(card => {
      card.addEventListener('mouseenter', function() {
        this.querySelector('.category-card-backdrop').style.opacity = 1;
        this.querySelector('.category-card-glow').style.opacity = 0.8;
      });

      card.addEventListener('mouseleave', function() {
        this.querySelector('.category-card-backdrop').style.opacity = 0;
        this.querySelector('.category-card-glow').style.opacity = 0;
      });

      card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        this.querySelector('.category-card-glow').style.background =
          `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 60%)`;
      });
    });
  },

  // Add a method to generate dynamic colors for categories
  getCategoryColor(categoryId) {
    // Create a unique but consistent color for each category
    if (!categoryId) return { start: '#4f46e5', end: '#ec4899' }; // Default colors

    // Generate colors based on category ID or name
    const colors = [
      { start: '#4f46e5', end: '#8b5cf6' }, // Indigo to Purple
      { start: '#84cc16', end: '#10b981' }, // Lime to Emerald
      { start: '#ec4899', end: '#f97316' }, // Pink to Orange
      { start: '#0ea5e9', end: '#06b6d4' }, // Sky to Cyan
      { start: '#f59e0b', end: '#f43f5e' }, // Amber to Rose
      { start: '#6366f1', end: '#14b8a6' }, // Indigo to Teal
      { start: '#8b5cf6', end: '#ec4899' }  // Purple to Pink
    ];

    // Use the category ID to select a color (modulo to cycle through colors)
    return colors[categoryId % colors.length] || colors[0];
  },

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

    // Category management helper methods
    getProductCountForCategory(categoryId) {
      return this.products.filter(product => product.category_id === categoryId).length;
    },

    getInStockCountForCategory(categoryId) {
      return this.products.filter(product =>
        product.category_id === categoryId && product.stock > 0
      ).length;
    },

    getLowStockCountForCategory(categoryId) {
      return this.products.filter(product =>
        product.category_id === categoryId &&
        product.stock > 0 &&
        product.stock < 10
      ).length;
    },

    getCategoryColorr(categoryId) {
      // Create a unique but consistent color for each category
      if (!categoryId) return { start: '#4f46e5', end: '#ec4899' }; // Default colors

      // Generate a pseudorandom but consistent color based on the category ID
      const seed = categoryId * 9973; // Use a prime number to spread out the values
      const hue1 = (seed % 360);
      const hue2 = ((seed * 271) % 360); // 271 is prime, giving a different hue

      // Use vibrant, attractive colors with good saturation and lightness
      return {
        start: `hsl(${hue1}, 85%, 60%)`,
        end: `hsl(${hue2}, 85%, 50%)`
      };
    },

    // CRUD operations
    async fetchCategories() {
      this.isLoading = true;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/categories');

        if (response.ok) {
          this.categories = await response.json();
        } else {
          this.showToastMessage('Failed to load categories', 'error');
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.showToastMessage('Network error. Please try again.', 'error');
      } finally {
        this.isLoading = false;
      }
    },

    async fetchProducts() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/products');

        if (response.ok) {
          this.products = await response.json();
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },

    editCategory(category) {
      this.editingCategory = category;
      this.formData = {
        name: category.name,
        description: category.description || ''
      };
      this.errors = { name: '' };
      this.showAddForm = true;
    },

    cancelForm() {
      this.showAddForm = false;
      this.editingCategory = null;
      this.formData = { name: '', description: '' };
      this.errors = { name: '' };
    },

    async saveCategory() {
      // Validate form data
      this.errors = { name: '' };

      if (!this.formData.name.trim()) {
        this.errors.name = 'Category name is required';
        return;
      }

      this.isLoading = true;

      try {
        const url = this.editingCategory
          ? `http://127.0.0.1:5000/api/categories/${this.editingCategory.id}`
          : 'http://127.0.0.1:5000/api/categories';

        const method = this.editingCategory ? 'PUT' : 'POST';

        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        });

        const data = await response.json();

        if (response.ok) {
          // Update local data
          if (this.editingCategory) {
            const index = this.categories.findIndex(c => c.id === this.editingCategory.id);
            if (index !== -1) {
              this.categories[index] = data.category;
            }
          } else {
            this.categories.push(data.category);
          }

          this.showAddForm = false;
          this.editingCategory = null;
          this.formData = { name: '', description: '' };

          this.showToastMessage(
            `Category ${this.editingCategory ? 'updated' : 'created'} successfully`,
            'success'
          );
        } else {
          // Handle error
          this.errors.name = data.error || 'Failed to save category';
        }
      } catch (error) {
        console.error('Error saving category:', error);
        this.showToastMessage('Network error. Please try again.', 'error');
      } finally {
        this.isLoading = false;
      }
    },

    confirmDelete(category) {
      this.categoryToDelete = category;
      this.showDeleteModal = true;
    },

    cancelDelete() {
      this.showDeleteModal = false;
      this.categoryToDelete = null;
    },

    async deleteCategory() {
      if (!this.categoryToDelete) return;

      this.isLoading = true;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/categories/${this.categoryToDelete.id}`, {
          method: 'DELETE'
        });

        if (response.ok) {
          // Remove from local array
          const index = this.categories.findIndex(c => c.id === this.categoryToDelete.id);
          if (index !== -1) {
            this.categories.splice(index, 1);
          }

          this.showToastMessage('Category deleted successfully', 'success');
        } else {
          const data = await response.json();
          this.showToastMessage(data.error || 'Failed to delete category', 'error');
        }
      } catch (error) {
        console.error('Error deleting category:', error);
        this.showToastMessage('Network error. Please try again.', 'error');
      } finally {
        this.isLoading = false;
        this.showDeleteModal = false;
        this.categoryToDelete = null;
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

    // Fetch data when component is created
    this.fetchCategories();
    this.fetchProducts();
    this.$nextTick(() => {
    this.setupCardHoverEffects();
  });
  },

  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
    window.removeEventListener('resize', this.handleResize);

    // Save view mode preference
    localStorage.setItem('categoryViewMode', this.viewMode);

    // Clear any active toast timeout
    if (this.toast.timeout) {
      clearTimeout(this.toast.timeout);
    }
  }
}
</script>

<style scoped>
/* Main Layout Styles */
.top-header {
  height: 70px;
  background-color: var(--card-bg);
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  padding: 0 24px;
  position: fixed;
  top: 0;
  z-index: 10;
}
/* Category Card Styles with Hover Effects */
.category-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  background-color: var(--card-bg);
  height: 100%;
  transform-style: preserve-3d;
  perspective: 1000px;
}

.category-card-inner {
  position: relative;
  height: 100%;
  z-index: 1;
  overflow: hidden;
  background-color: var(--card-bg);
  border-radius: 12px;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  backface-visibility: hidden;
}

.category-card:hover {
  transform: translateY(-8px) rotate3d(1, 5, 0, 2deg);
  box-shadow: var(--shadow-lg);
}

.category-card:hover .category-card-inner {
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
}

.category-card-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
    rgba(79, 70, 229, 0.65) 0%,
    rgba(219, 39, 119, 0.65) 50%,
    rgba(236, 72, 153, 0.65) 100%);
  opacity: 0;
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: -1;
  transform: scale(0.95);
  border-radius: 12px;
  box-shadow: 0 0 30px rgba(79, 70, 229, 0.4);
  filter: blur(0px);
}

.category-card:hover .category-card-backdrop {
  opacity: 0.85;
  transform: scale(1.02);
  box-shadow: 0 0 40px rgba(236, 72, 153, 0.5);
}

.category-card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.9), rgba(255,255,255,0) 70%);
  opacity: 0;
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: -1;
  pointer-events: none;
  mix-blend-mode: overlay;
  transform: translate(-50%, -50%) scale(0.5);
  left: 50%;
  top: 50%;
  width: 200%;
  height: 200%;
}

.category-card:hover .category-card-glow {
  opacity: 0.9;
  animation: move-glow 3s infinite alternate;
}

/* Add this if not already defined */
@keyframes move-glow {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
  }
  100% {
    transform: translate(-49%, -48%) scale(0.55);
  }
}
.metric-card.items .metric-content {
  /*min-width: 0; */ /* Critical for flexbox children to respect overflow */
  padding: 0 10px;
}

/* Fix for Most Popular Category card */
.metric-card.items .metric-value .value-number {
      /* Keep text in one line */
  overflow: hidden;         /* Hide overflow */
  text-overflow: ellipsis;  /* Add "..." if text is too long */
  max-width: 100%;         /* Respect card width */
  display: block;          /* Required for ellipsis */
}
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

/* Category Grid View Styles */
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.category-card {
  background: var(--background-color-primary, white);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.category-header {
  padding: 25px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.category-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
}

.category-icon i {
  font-size: 24px;
}

.category-product-count {
  font-weight: 600;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 10px;
  border-radius: 20px;
}

.category-details {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.category-name {
  font-size: 18px;
  margin: 0 0 15px 0;
  color: var(--text-color-primary, #1e293b);
}

.category-stats {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-distribution {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.stat-item {
  font-size: 13px;
  background: var(--background-color-secondary, #f8fafc);
  padding: 6px 12px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.stat-label {
  color: var(--text-color-secondary, #64748b);
}

.stat-value {
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.category-actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.category-actions .edit-btn,
.category-actions .delete-btn {
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
  transition: background 0.2s ease;
}

.category-actions .edit-btn {
  background: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.category-actions .delete-btn {
  background: var(--danger-color-light, #fee2e2);
  color: var(--danger-color, #ef4444);
}

.category-actions .edit-btn:hover {
  background: var(--primary-color-dark, #4338ca);
  color: white;
}

.category-actions .delete-btn:hover {
  background: var(--danger-color, #ef4444);
  color: white;
}

/* Add New Category Card */
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

/* Category List View */
.category-list {
  margin-top: 20px;
  overflow-x: auto;
}

.category-list table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.category-list th,
.category-list td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.category-list th {
  color: var(--text-color-secondary, #64748b);
  font-weight: 600;
  background: var(--background-color-secondary, #f8fafc);
}

.category-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-color-indicator {
  width: 16px;
  height: 16px;
  border-radius: 4px;
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
}

.action-icon.edit {
  background-color: var(--primary-color-light, #ede9fe);
  color: var(--primary-color, #4f46e5);
}

.action-icon.delete {
  background-color: var(--danger-color-light, #fee2e2);
  color: var(--danger-color, #ef4444);
}

.action-icon.edit:hover {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.action-icon.delete:hover {
  background-color: var(--danger-color, #ef4444);
  color: white;
}

/* Modal Styles */
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

.category-form {
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

.form-input.textarea {
  resize: vertical;
  min-height: 80px;
}

.error-message {
  color: var(--danger-color, #ef4444);
  font-size: 12px;
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

.btn-save:hover {
  background-color: var(--primary-color-dark, #4338ca);
}

/* Color Preview in Form */
.color-preview-section {
  margin-top: 10px;
}

.color-preview {
  height: 80px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 10px;
}

.preview-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.preview-content i {
  font-size: 24px;
}

.color-note {
  font-size: 12px;
  color: var(--text-color-secondary, #64748b);
  margin: 0;
}

/* Delete Confirmation Modal */
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
}

.btn-delete:hover {
  background-color: #dc2626; /* darker red */
}

/* Loading State */
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

/* Empty State */
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

  .category-grid {
    grid-template-columns: 1fr;
  }

  .modal-container {
    width: 90%;
  }

  .category-list table {
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