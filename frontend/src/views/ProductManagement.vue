<template>
  <div class="dashboard-app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Improved Left Navigation Sidebar with better responsive behavior -->
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
            <h1 class="logo">Peak<span>POS</span></h1>
          </div>
        </div>
        <button class="toggle-btn" @click="toggleSidebar" aria-label="Toggle sidebar">
          <i class="material-icons">{{ isSidebarCollapsed ? 'menu_open' : 'menu' }}</i>
        </button>
      </div>

      <div class="sidebar-content">
        <!-- Mobile-specific Add Product button that only shows on mobile -->
        <div class="mobile-add-button" @click="showAddForm = true">
          <i class="material-icons">add_circle</i>
          <span>New Product</span>
        </div>

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
          <router-link to="/products" class="nav-item active">
            <i class="material-icons">category</i>
            <span class="nav-label">Products</span>
            <span class="nav-indicator"></span>
            <div class="tooltip" v-if="isSidebarCollapsed">Products</div>
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
            <h1 class="page-title">Product Management</h1>
            <div class="breadcrumb">
              <span>PeakPOS</span>
              <i class="material-icons">chevron_right</i>
              <span class="current">Products</span>
            </div>
          </div>
        </div>

        <div class="header-middle">
          <div class="search-container">
            <i class="material-icons">search</i>
            <input type="text" v-model="searchQuery" placeholder="Search products..." class="search-input" />
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
              <i class="material-icons">add</i> <span>New Product</span>
            </button>
          </div>
        </div>
      </header>

      <div class="products-management">

    <!-- Dashboard Summary -->
    <div class="dashboard-summary">
      <div class="welcome-message">
        <h2>Product Management</h2>
        <p>Manage your products, update stock, and organize categories.</p>
      </div>
    </div>

    <!-- Modern Metrics Grid with Animated 3D Cards -->
    <div class="metrics-grid">
      <!-- Total Products Metric Card -->
      <div class="metric-card products" :style="{ '--delay': '0.1s' }">
        <div class="metric-card-inner">
          <div class="metric-icon-container">
            <div class="metric-icon">
              <i class="material-icons">category</i>
            </div>
            <div class="metric-trend positive">
              <i class="material-icons trend-icon">inventory</i>
              <span class="trend-value">{{ products.length }}</span>
            </div>
          </div>
          <div class="metric-content">
            <div class="metric-label">Total Products</div>
            <div class="metric-value">
              <span class="value-number">{{ products.length }}</span>
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

      <!-- In Stock Items Card -->
      <div class="metric-card sales" :style="{ '--delay': '0.2s' }">
        <div class="metric-card-inner">
          <div class="metric-icon-container">
            <div class="metric-icon">
              <i class="material-icons">check_circle</i>
            </div>
            <div class="metric-trend positive">
              <i class="material-icons trend-icon">trending_up</i>
              <span class="trend-value">{{ totalInStock }}</span>
            </div>
          </div>
          <div class="metric-content">
            <div class="metric-label">In Stock</div>
            <div class="metric-value">
              <span class="value-number">{{ totalInStock }}</span>
            </div>
            <div class="metric-chart">
              <div class="mini-sparkline">
                <div class="sparkline-bar" v-for="(value, index) in [40, 45, 55, 60, 70, 75, 80]"
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

      <!-- Low Stock Items Card -->
      <div class="metric-card items" :style="{ '--delay': '0.3s' }">
        <div class="metric-card-inner">
          <div class="metric-icon-container">
            <div class="metric-icon warning">
              <i class="material-icons">warning</i>
            </div>
            <div class="metric-trend negative">
              <i class="material-icons trend-icon">trending_down</i>
              <span class="trend-value">{{ lowStockCount }}</span>
            </div>
          </div>
          <div class="metric-content">
            <div class="metric-label">Low Stock Items</div>
            <div class="metric-value">
              <span class="value-number">{{ lowStockCount }}</span>
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

      <!-- Categories Metric Card -->
      <div class="metric-card orders" :style="{ '--delay': '0.4s' }">
        <div class="metric-card-inner">
          <div class="metric-icon-container">
            <div class="metric-icon">
              <i class="material-icons">format_list_bulleted</i>
            </div>
            <div class="metric-trend positive">
              <i class="material-icons trend-icon">folder</i>
              <span class="trend-value">{{ categories.length }}</span>
            </div>
          </div>
          <div class="metric-content">
            <div class="metric-label">Categories</div>
            <div class="metric-value">
              <span class="value-number">{{ categories.length }}</span>
            </div>
            <div class="metric-chart">
              <div class="mini-sparkline">
                <div class="sparkline-bar" v-for="(value, index) in [35, 40, 50, 55, 65, 70, 75]"
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

    <!-- Filter and Controls Section with Enhanced UI - Horizontal Layout -->
    <div class="filters-section">
      <div class="filter-header">
        <h3>Filter Products</h3>
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
          <label for="category-filter">Category</label>
          <select
            id="category-filter"
            v-model="categoryFilter"
            class="filter-select"
          >
            <option value="">All Categories</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label for="stock-filter">Stock Level</label>
          <select
            id="stock-filter"
            v-model="stockFilter"
            class="filter-select"
          >
            <option value="all">All Stock Levels</option>
            <option value="in-stock">In Stock</option>
            <option value="low-stock">Low Stock</option>
            <option value="out-of-stock">Out of Stock</option>
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
            <option value="price-asc">Price (Low to High)</option>
            <option value="price-desc">Price (High to Low)</option>
            <option value="stock-asc">Stock (Low to High)</option>
            <option value="stock-desc">Stock (High to Low)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Product List View -->
    <div v-if="viewMode === 'list'" class="product-list">
      <table>
        <thead>
          <tr>
            <th>Image</th>
            <th>Name</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Category</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td class="image-cell">
              <div class="product-thumbnail-container">
                <img
                  :src="getProductImageUrl(product)"
                  :alt="product.name"
                  class="product-thumbnail"
                  @error="handleImageError"
                />
              </div>
            </td>
            <td>{{ product.name }}</td>
            <td>${{ product.price.toFixed(2) }}</td>
            <td :class="{ 'low-stock': product.stock < 10, 'out-of-stock': product.stock === 0 }">
              {{ product.stock }}
            </td>
            <td>{{ getCategoryName(product.category_id) }}</td>
            <td>
              <div class="action-icons">
                <button @click="editProduct(product)" class="action-icon edit">
                  <i class="mdi mdi-pencil"></i>
                </button>
                <button @click="confirmDelete(product)" class="action-icon delete">
                  <i class="mdi mdi-delete"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Product Grid View with Enhanced Dashboard Style -->
    <div v-else class="product-grid">
      <div v-for="product in filteredProducts" :key="product.id" class="product-card">
        <div class="product-card-inner">
          <div class="product-image-container">
            <img
              :src="getProductImageUrl(product)"
              :alt="product.name"
              class="product-image"
              @error="handleImageError"
            />
            <div class="product-category-badge"
              v-if="getCategoryName(product.category_id)"
              :style="{
                backgroundColor: getCategoryColor(product.category_id).start,
                color: 'white'
              }">
              {{ getCategoryName(product.category_id) }}
            </div>
            <div
              class="product-stock-badge"
              :class="{
                'low-stock': product.stock < 10 && product.stock > 0,
                'out-of-stock': product.stock === 0,
                'in-stock': product.stock >= 10
              }"
            >
              {{ product.stock === 0 ? 'Out of Stock' : product.stock < 10 ? 'Low Stock' : 'In Stock' }}
            </div>
          </div>

          <div class="product-details">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-description" v-if="product.description">{{ truncateText(product.description, 80) }}</p>

            <div class="product-stats">
              <div class="product-price">
                <i class="material-icons">attach_money</i>
                <span>${{ product.price.toFixed(2) }}</span>
              </div>
              <div class="product-stock">
                <i class="material-icons">inventory_2</i>
                <span>{{ product.stock }} in stock</span>
              </div>
            </div>

            <div class="product-actions">
              <button @click="editProduct(product)" class="action-button edit">
                <i class="material-icons">edit</i>
                <span>Edit</span>
              </button>
              <button @click="confirmDelete(product)" class="action-button delete">
                <i class="material-icons">delete</i>
                <span>Delete</span>
              </button>
            </div>
          </div>

          <!-- Interactive hover effect elements with dynamic category colors -->
          <div class="product-card-backdrop"
            :style="{
              background: `linear-gradient(135deg,
                ${getCategoryColor(product.category_id).start} 0%,
                ${getCategoryColor(product.category_id).end} 100%)`
            }">
          </div>
          <div class="product-card-glow"></div>
        </div>
      </div>
    </div>

    <!-- Enhanced Empty State -->
    <div v-if="filteredProducts.length === 0" class="empty-state">
      <div class="empty-state-content">
        <div class="empty-state-icon">
          <i class="material-icons">inventory_2</i>
        </div>
        <h3>No Products Found</h3>
        <p>Try adjusting your search or filters, or add a new product.</p>
        <button @click="showAddForm = true" class="btn-add">
          <i class="material-icons">add_circle</i>
          <span>Add New Product</span>
        </button>
      </div>
    </div>

    <!-- Add/Edit Product Modal -->
    <transition name="modal">
      <div class="modal-overlay" v-if="showAddForm || editingProduct">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <h2>{{ editingProduct ? 'Edit Product' : 'Add New Product' }}</h2>
            <button @click="cancelForm" class="close-button">
              <i class="mdi mdi-close"></i>
            </button>
          </div>

          <div class="modal-body">
            <form @submit.prevent="saveProduct" class="product-form">
              <div class="form-layout">
                <div class="form-column">
                  <div class="form-group">
                    <label for="name">Product Name</label>
                    <input
                      type="text"
                      id="name"
                      v-model="formData.name"
                      required
                      class="form-input"
                      placeholder="Enter product name"
                    />
                  </div>

                  <div class="form-row">
                    <div class="form-group">
                      <label for="price">Price ($)</label>
                      <input
                        type="number"
                        id="price"
                        v-model.number="formData.price"
                        min="0"
                        step="0.01"
                        required
                        class="form-input"
                        placeholder="0.00"
                      />
                    </div>

                    <div class="form-group">
                      <label for="stock">Stock</label>
                      <input
                        type="number"
                        id="stock"
                        v-model.number="formData.stock"
                        min="0"
                        required
                        class="form-input"
                        placeholder="0"
                      />
                    </div>
                  </div>

                  <div class="form-group">
                    <label for="category">Category</label>
                    <select id="category" v-model="formData.category_id" required class="form-select">
                      <option disabled value="">Select a category</option>
                      <option v-for="category in categories" :key="category.id" :value="category.id">
                        {{ category.name }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="description">Description (Optional)</label>
                    <textarea
                      id="description"
                      v-model="formData.description"
                      class="form-textarea"
                      placeholder="Enter product description"
                      rows="3"
                    ></textarea>
                  </div>
                </div>

                <div class="form-column">
                  <div class="form-group">
                    <label for="image">Product Image</label>
                    <div class="image-upload-container">
                      <div
                        class="image-drop-area"
                        :class="{ 'has-image': imagePreview || formData.image_url }"
                        @dragover.prevent
                        @drop.prevent="handleFileDrop"
                      >
                        <div v-if="!imagePreview && !formData.image_url" class="upload-placeholder">
                          <i class="mdi mdi-cloud-upload"></i>
                          <p>Drag & drop image or click to browse</p>
                        </div>

                        <img
                          v-else-if="imagePreview"
                          :src="imagePreview"
                          alt="Image Preview"
                          class="image-preview"
                        />

                        <img
                          v-else
                          :src="getProductImageUrl(formData)"
                          alt="Current Image"
                          class="image-preview"
                        />

                        <input
                          type="file"
                          id="image"
                          ref="fileInput"
                          @change="handleImageChange"
                          accept="image/png, image/jpeg, image/gif, image/webp"
                          class="file-input"
                        />
                      </div>

                      <div class="image-controls">
                        <button type="button" @click="triggerFileInput" class="btn-upload">
                          <i class="mdi mdi-folder-image"></i> Browse Files
                        </button>
                        <button
                          v-if="imagePreview || formData.image_url"
                          type="button"
                          @click="clearImage"
                          class="btn-clear"
                        >
                          <i class="mdi mdi-close"></i> Clear
                        </button>
                      </div>

                      <p class="image-help-text">
                        Recommended size: 600×600px. Max size: 5MB.
                        Supports: JPG, PNG, GIF, WEBP
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="form-actions">
                <button type="button" @click="cancelForm" class="btn-cancel">
                  Cancel
                </button>
                <button type="submit" class="btn-save">
                  <i class="mdi mdi-content-save"></i>
                  {{ editingProduct ? 'Update Product' : 'Save Product' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </transition>

    <!-- Delete Confirmation Modal -->
    <transition name="modal">
      <div class="modal-overlay" v-if="showDeleteConfirm">
        <div class="confirm-modal">
          <div class="confirm-header">
            <i class="mdi mdi-alert-circle"></i>
            <h3>Confirm Delete</h3>
          </div>
          <p>Are you sure you want to delete <strong>{{ productToDelete?.name }}</strong>?</p>
          <p class="warning-text">This action cannot be undone.</p>
          <div class="confirm-actions">
            <button @click="showDeleteConfirm = false" class="btn-cancel">Cancel</button>
            <button @click="deleteProduct" class="btn-delete">
              <i class="mdi mdi-delete"></i> Delete
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Loading Overlay -->
    <div class="loading-overlay" v-if="isLoading">
      <div class="spinner"></div>
    </div>
      </div>
      </main>
    </div>
  </template>

<script>
export default {
  name: 'ProductsManagement',
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

      // Products management data
      products: [],
      categories: [],
      isLoading: false,
      viewMode: 'grid',
      searchQuery: '',
      categoryFilter: '',
      stockFilter: 'all',
      sortBy: 'name-asc',
      showAddForm: false,
      editingProduct: null,
      formData: {
        name: '',
        price: 0,
        stock: 0,
        category_id: '',
        description: '',
        image_url: null
      },
      selectedImage: null,
      imagePreview: null,
      showDeleteConfirm: false,
      productToDelete: null,
      lowStockThreshold: 10
    };
  },

  computed: {
    filteredProducts() {
      let result = [...this.products];

      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(product =>
          product.name.toLowerCase().includes(query)
        );
      }

      // Category filter
      if (this.categoryFilter) {
        result = result.filter(product =>
          product.category_id === parseInt(this.categoryFilter)
        );
      }

      // Stock filter
      if (this.stockFilter !== 'all') {
        if (this.stockFilter === 'in-stock') {
          result = result.filter(product => product.stock > this.lowStockThreshold);
        } else if (this.stockFilter === 'low-stock') {
          result = result.filter(product =>
            product.stock > 0 && product.stock <= this.lowStockThreshold
          );
        } else if (this.stockFilter === 'out-of-stock') {
          result = result.filter(product => product.stock === 0);
        }
      }

      // Sorting
      result.sort((a, b) => {
        switch (this.sortBy) {
          case 'name-asc':
            return a.name.localeCompare(b.name);
          case 'name-desc':
            return b.name.localeCompare(a.name);
          case 'price-asc':
            return a.price - b.price;
          case 'price-desc':
            return b.price - a.price;
          case 'stock-asc':
            return a.stock - b.stock;
          case 'stock-desc':
            return b.stock - a.stock;
          default:
            return 0;
        }
      });

      return result;
    },

    totalInStock() {
      return this.products.filter(product => product.stock > 0).length;
    },

    lowStockCount() {
      return this.products.filter(product =>
        product.stock > 0 && product.stock <= this.lowStockThreshold
      ).length;
    }
  },

  mounted() {
    this.fetchProducts();
    this.fetchCategories();

    // Listen for window resize events
    window.addEventListener('resize', this.handleResize);

    // Listen for keyboard shortcuts
    document.addEventListener('keydown', this.handleKeyShortcuts);

    // Listen for clicks outside user menu
    document.addEventListener('click', this.handleClickOutside);

    // Setup hover effects for cards
    this.$nextTick(() => {
      this.setupCardHoverEffects();
    });
  },

  beforeUnmount() {
    // Clean up event listeners
    window.removeEventListener('resize', this.handleResize);
    document.removeEventListener('keydown', this.handleKeyShortcuts);
    document.removeEventListener('click', this.handleClickOutside);
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
      this.isUserMenuOpen = false;
    },

    toggleUserMenu() {
      this.isUserMenuOpen = !this.isUserMenuOpen;
    },

    handleResize() {
      this.isMobileView = window.innerWidth < 768;
      if (this.isMobileView && !this.isSidebarCollapsed) {
        this.isSidebarCollapsed = true;
      }
    },

    handleClickOutside(e) {
      // Close user menu when clicking outside
      const userProfile = document.querySelector('.user-profile');
      const userMenu = document.querySelector('.user-dropdown');

      if (userProfile && userMenu && this.isUserMenuOpen) {
        if (!userProfile.contains(e.target) && !userMenu.contains(e.target)) {
          this.isUserMenuOpen = false;
        }
      }
    },

    handleKeyShortcuts(e) {
      // Handle keyboard shortcuts
      if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
          e.preventDefault();
          searchInput.focus();
        }
      }

      // Toggle sidebar with keyboard shortcut
      if (e.key === 'b' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.toggleSidebar();
      }
    },

    // Setup hover effects for metric cards and product cards
    setupCardHoverEffects() {
      // Apply hover effects to metric cards
      document.querySelectorAll('.metric-card-inner').forEach(card => {
        card.addEventListener('mouseenter', function() {
          this.querySelector('.metric-card-backdrop').style.opacity = 1;
          this.querySelector('.metric-card-glow').style.opacity = 0.8;
        });

        card.addEventListener('mouseleave', function() {
          this.querySelector('.metric-card-backdrop').style.opacity = 0;
          this.querySelector('.metric-card-glow').style.opacity = 0;
        });

        card.addEventListener('mousemove', function(e) {
          const rect = this.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;

          this.querySelector('.metric-card-glow').style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 60%)`;
        });
      });

      // Apply hover effects to product cards
      document.querySelectorAll('.product-card-inner').forEach(card => {
        card.addEventListener('mouseenter', function() {
          this.querySelector('.product-card-backdrop').style.opacity = 1;
          this.querySelector('.product-card-glow').style.opacity = 0.8;
        });

        card.addEventListener('mouseleave', function() {
          this.querySelector('.product-card-backdrop').style.opacity = 0;
          this.querySelector('.product-card-glow').style.opacity = 0;
        });

        card.addEventListener('mousemove', function(e) {
          const rect = this.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;

          this.querySelector('.product-card-glow').style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 60%)`;
        });
      });
    },

    // Product management methods
    async fetchProducts() {
      this.isLoading = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/products');
        if (response.ok) {
          this.products = await response.json();
        } else {
          console.error('Failed to fetch products');
          this.showToast('Failed to load products. Please try again.', 'error');
        }
      } catch (error) {
        console.error('Error:', error);
        this.showToast('Network error while loading products.', 'error');
      } finally {
        this.isLoading = false;
      }
    },

    async fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/categories');
        if (response.ok) {
          this.categories = await response.json();
        } else {
          console.error('Failed to fetch categories');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },

    getProductImageUrl(product) {
      // The backend sends the image_url field as 'image' in the API response
      const imageUrl = product && (product.image_url || product.image);

      if (imageUrl) {
        // Handle different formats of image URL
        if (imageUrl.startsWith('http')) {
          // If it's an absolute URL, return it as is
          return imageUrl;
        } else {
          // Use the environment-specific backend URL
          const isReplit = window.location.hostname.includes('replit');
          const backendUrl = isReplit
            ? window.location.origin.replace('-00-', '-01-')  // Replit environment
            : ' C:\\Users\\junai\\PeakPOS\\backend\\app\\static\\';  // Local development

          // For relative paths, prefix with backend URL
          if (imageUrl.startsWith('/static/')) {
            // Already has leading slash
            return `${backendUrl}${imageUrl}`;
          } else if (imageUrl.startsWith('static/')) {
            // Add leading slash
            return `${backendUrl}/${imageUrl}`;
          } else if (imageUrl.startsWith('product_images/')) {
            // Product images inside static/product_images
            return `${backendUrl}/static/${imageUrl}`;
          } else {
            // For any other format, assume it's relative to static folder
            return `${backendUrl}/static/${imageUrl}`;
          }
        }
      }

      // Log the missing image for debugging
      console.log('No image URL found for product:', product?.id, product?.name);


      // Use a data URL placeholder instead of fetching from server
      return 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlOWVjZWYiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIyNCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZvbnQtZmFtaWx5PSJzYW5zLXNlcmlmIiBmaWxsPSIjNmM3NTdkIj5ObyBJbWFnZTwvdGV4dD48cGF0aCBkPSJNODAgOTAgTDEyMCAxMzAgTTE2MCA5MCBMODAgMTcwIiBzdHJva2U9IiM2Yzc1N2QiIHN0cm9rZS13aWR0aD0iMyIvPjwvc3ZnPg==';
    },

    handleImageError(e) {
      // Use a data URL placeholder instead of fetching from server
      e.target.src = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlOWVjZWYiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIyNCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZvbnQtZmFtaWx5PSJzYW5zLXNlcmlmIiBmaWxsPSIjNmM3NTdkIj5ObyBJbWFnZTwvdGV4dD48cGF0aCBkPSJNODAgOTAgTDEyMCAxMzAgTTE2MCA5MCBMODAgMTcwIiBzdHJva2U9IiM2Yzc1N2QiIHN0cm9rZS13aWR0aD0iMyIvPjwvc3ZnPg==';
    },

    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId);
      return category ? category.name : 'Uncategorized';
    },

    getCategoryColor(categoryId) {
      // Create a unique but consistent color for each category
      if (!categoryId) return { start: '#4f46e5', end: '#ec4899' }; // Default colors

      const category = this.categories.find(c => c.id === categoryId);
      const categoryName = category ? category.name : 'Uncategorized';

      // Generate colors based on category name
      const colors = {
        'Equipment': { start: '#4f46e5', end: '#8b5cf6' }, // Indigo to Purple
        'Beans': { start: '#84cc16', end: '#10b981' }, // Lime to Emerald
        'Syrups': { start: '#ec4899', end: '#f97316' }, // Pink to Orange
        'Cups': { start: '#0ea5e9', end: '#06b6d4' }, // Sky to Cyan
        'Food': { start: '#f59e0b', end: '#f43f5e' }, // Amber to Rose
        'Merchandise': { start: '#6366f1', end: '#14b8a6' }, // Indigo to Teal
        'Uncategorized': { start: '#8b5cf6', end: '#ec4899' } // Purple to Pink
      };

      return colors[categoryName] || colors['Uncategorized'];
    },

    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleFileDrop(event) {
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.handleImageFile(files[0]);
      }
    },

    handleImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.handleImageFile(file);
      }
    },

    handleImageFile(file) {
      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
      if (!allowedTypes.includes(file.type)) {
        this.showToast('Please select a valid image (JPG, PNG, GIF, WEBP)', 'error');
        return;
      }

      // Validate file size (5MB max)
      if (file.size > 5 * 1024 * 1024) {
        this.showToast('Image must be less than 5MB', 'error');
        return;
      }

      this.selectedImage = file;

      // Create a preview
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    clearImage() {
      this.selectedImage = null;
      this.imagePreview = null;
      if (this.editingProduct) {
        this.formData.image_url = null;
      }
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    },

    editProduct(product) {
      this.editingProduct = product;
      this.formData = {
        ...product,
        description: product.description || ''
      };
      this.imagePreview = null;
      this.selectedImage = null;
      this.showAddForm = false; // Make sure we're in edit mode, not add mode
    },

    confirmDelete(product) {
      this.productToDelete = product;
      this.showDeleteConfirm = true;
    },

    async deleteProduct() {
      if (!this.productToDelete) return;

      this.isLoading = true;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/products/${this.productToDelete.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.ok) {
          // Remove from local array
          const index = this.products.findIndex(p => p.id === this.productToDelete.id);
          if (index !== -1) {
            this.products.splice(index, 1);
          }

          this.showToast(`${this.productToDelete.name} has been deleted`, 'success');
          this.showDeleteConfirm = false;
          this.productToDelete = null;
        } else {
          const error = await response.json();
          throw new Error(error.error || 'Failed to delete product');
        }
      } catch (error) {
        console.error('Error:', error);
        this.showToast(error.message, 'error');
      } finally {
        this.isLoading = false;
      }
    },

    cancelForm() {
      if (this.showAddForm) {
        this.showAddForm = false;
      } else if (this.editingProduct) {
        this.editingProduct = null;
      }

      this.formData = {
        name: '',
        price: 0,
        stock: 0,
        category_id: this.categories.length > 0 ? this.categories[0].id : '',
        description: '',
        image_url: null
      };

      this.selectedImage = null;
      this.imagePreview = null;
    },

    async saveProduct() {
      this.isLoading = true;

      try {
        // Create a FormData object to handle file upload
        const formData = new FormData();
        formData.append('name', this.formData.name);
        formData.append('price', this.formData.price);
        formData.append('stock', this.formData.stock);
        formData.append('category_id', this.formData.category_id);

        if (this.formData.description) {
          formData.append('description', this.formData.description);
        }

        // Only append image if a new one is selected
        if (this.selectedImage) {
          formData.append('image', this.selectedImage);
        }

        let response;
        let url;

        if (this.editingProduct) {
          // Use the image-specific endpoint if we have a new image
          url = this.selectedImage
            ? `http://127.0.0.1:5000/api/products/${this.editingProduct.id}/with-image`
            : `http://127.0.0.1:5000/api/products/${this.editingProduct.id}`;

          // For non-image updates, use JSON
          if (!this.selectedImage) {
            response = await fetch(url, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              },
              body: JSON.stringify(this.formData)
            });
          } else {
            response = await fetch(url, {
              method: 'PUT',
              body: formData,
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              }
            });
          }
        } else {
          // Use the image-specific endpoint if we have an image
          url = this.selectedImage
            ? 'http://127.0.0.1:5000/api/products/with-image'
            : 'http://127.0.0.1:5000/api/products';

          // For products without images, use JSON
          if (!this.selectedImage) {
            response = await fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              },
              body: JSON.stringify(this.formData)
            });
          } else {
            response = await fetch(url, {
              method: 'POST',
              body: formData,
              headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
              }
            });
          }
        }

        if (response.ok) {
          // Just parse the response but don't store it since we don't use it
          await response.json();

          // Refresh the products list
          await this.fetchProducts();

          // Show success message
          const action = this.editingProduct ? 'updated' : 'added';
          this.showToast(`Product ${action} successfully`, 'success');

          // Close the form
          this.cancelForm();
        } else {
          const error = await response.json();
          throw new Error(error.error || `Failed to ${this.editingProduct ? 'update' : 'add'} product`);
        }
      } catch (error) {
        console.error('Error:', error);
        this.showToast(error.message, 'error');
      } finally {
        this.isLoading = false;
      }
    },

    showToast(message, type = 'info') {
      // Implement a toast notification system
      // This is a simple implementation - you might want to use a more robust solution
      const toast = document.createElement('div');
      toast.className = `toast toast-${type}`;
      toast.innerHTML = `
        <div class="toast-icon">
          <i class="mdi mdi-${type === 'success' ? 'check-circle' : type === 'error' ? 'alert-circle' : 'information'}"></i>
        </div>
        <div class="toast-message">${message}</div>
      `;

      document.body.appendChild(toast);

      // Animate in
      setTimeout(() => {
        toast.classList.add('show');
      }, 10);

      // Remove after 3 seconds
      setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
          document.body.removeChild(toast);
        }, 300);
      }, 3000);
    }
  }
};
</script>

<style scoped>
/* Dashboard Layout Styles */
.dashboard-app {
  display: flex;
  min-height: 100vh;
  background-color: var(--background);
  color: var(--text-primary);
  transition: background-color 0.3s, color 0.3s;
}

/* Sidebar Styles */
.sidebar {
  width: 280px;
  background-color: var(--card-bg);
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  transition: width 0.3s, transform 0.3s;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar.mobile-open {
  transform: translateX(0);
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 99;
  display: none;
}

.sidebar-header {
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
}

.brand {
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  min-width: 36px;
  min-height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background-color: var(--primary-color);
  color: white;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
  margin: 0;
}

.logo span {
  color: var(--primary-color);
}

.toggle-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.toggle-btn:hover {
  background-color: var(--card-bg-secondary);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 0 8px;
  color: var(--text-secondary);
  transition: all 0.2s;
  position: relative;
  text-decoration: none;
}

.nav-item:hover {
  background-color: var(--card-bg-secondary);
  color: var(--text-primary);
  text-decoration: none;
}

.nav-item.active {
  background-color: var(--primary-color);
  color: white;
}

.nav-item i {
  font-size: 24px;
  min-width: 24px;
}

.nav-label {
  margin-left: 16px;
  font-weight: 500;
  transition: opacity 0.3s, transform 0.3s;
  white-space: nowrap;
}

.nav-indicator {
  position: absolute;
  width: 4px;
  height: 24px;
  background-color: var(--primary-color);
  border-radius: 0 2px 2px 0;
  left: -8px;
  opacity: 0;
  transition: opacity 0.2s;
}

.nav-item.active .nav-indicator {
  opacity: 1;
}

.tooltip {
  position: absolute;
  left: 70px;
  background-color: var(--card-bg);
  padding: 8px 12px;
  border-radius: 4px;
  box-shadow: var(--shadow-md);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  white-space: nowrap;
  color: var(--text-primary);
  z-index: 10;
}

.sidebar.collapsed .nav-item:hover .tooltip {
  opacity: 1;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-color);
  position: relative;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: var(--card-bg-secondary);
}

.avatar-wrapper {
  min-width: 40px;
}

.avatar {
  width: 40px;
  height: 40px;
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  position: relative;
}

.avatar.small {
  width: 32px;
  height: 32px;
  font-size: 14px;
}

.status-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  position: absolute;
  bottom: 0;
  right: 0;
  border: 2px solid var(--card-bg);
}

.status-indicator.online {
  background-color: #10b981;
}

.user-info {
  flex: 1;
  overflow: hidden;
  transition: opacity 0.3s, max-width 0.3s;
}

.user-name {
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  display: block;
  font-size: 14px;
}

.user-role {
  color: var(--text-secondary);
  font-size: 12px;
  white-space: nowrap;
  display: block;
}

.user-menu-toggle {
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.user-dropdown {
  position: absolute;
  top: -5px;
  left: 16px;
  right: 16px;
  transform: translateY(-100%);
  background-color: var(--card-bg);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  z-index: 10;
  padding: 8px 0;
  overflow: hidden;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: var(--text-primary);
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: var(--card-bg-secondary);
}

.dropdown-item i {
  font-size: 20px;
  color: var(--text-secondary);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 8px 0;
}

.dropdown-item.logout {
  color: #ef4444;
}

.dropdown-item.logout i {
  color: #ef4444;
}

/* Main Content Styles */
.main-content {
  flex: 1;
  min-height: 100vh;
  margin-left: 280px;
  padding-top: 90px; /* Added padding to account for fixed header */
  transition: margin-left 0.3s;
  max-width: 100%;
}

.main-content.sidebar-collapsed {
  margin-left: 70px;
}

/* Header Styles */
.top-header {
  height: 70px;
  background-color: var(--card-bg);
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  height: 100%;
  gap: 16px;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 24px;
  color: var(--text-secondary);
  cursor: pointer;
}

.page-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  margin-left: 15px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  line-height: 1.2;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.2;
  margin-top: 4px;
}

.breadcrumb .current {
  color: var(--primary-color);
}

.header-middle {
  flex: 1;
  display: flex;
  justify-content: center;
}

.search-container {
  position: relative;
  max-width: 500px;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 10px 16px 10px 40px;
  border-radius: 8px;
  background-color: var(--card-bg-secondary);
  border: 1px solid transparent;
  color: var(--text-primary);
  transition: all 0.2s;
}

.search-input:focus {
  background-color: var(--card-bg);
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
  outline: none;
}

.search-container i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  font-size: 20px;
}

.search-shortcut {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 12px;
  padding: 2px 6px;
  background-color: var(--card-bg);
  border-radius: 4px;
  border: 1px solid var(--border-color);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.date-display {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 14px;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.action-btn:hover {
  background-color: var(--card-bg-secondary);
  color: var(--text-primary);
}

.action-btn.theme-btn {
  color: var(--accent-color);
}

.notification-btn.has-notifications::after {
  content: '';
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ef4444;
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #ef4444;
  color: white;
  font-size: 10px;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}

.mobile-avatar {
  display: none;
  cursor: pointer;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: var(--primary-color-dark);
}

.btn-add i {
  font-size: 20px;
}

/* Main Container */
.products-management {
  padding: 24px;
  background-color: var(--background);
  position: relative;
}

/* Header */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 16px;
  align-items: center;
}

.btn-add {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.btn-add:hover {
  background-color: #4338ca;
}

/* Special styling for the header button */
.header-btn {
  height: 40px;
  line-height: 1;
  margin-top: 0;
  display: flex;
  align-items: center;
  vertical-align: middle;
}

.search-container {
  position: relative;
}

.search-input {
  padding: 8px 12px 8px 36px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  width: 240px;
  background-color: white;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-input:focus {
  border-color: #4f46e5;
  outline: none;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
}

/* Stats Cards */
.stats-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.blue {
  background-color: #3b82f6;
}

.stat-icon.green {
  background-color: #10b981;
}

.stat-icon.red {
  background-color: #ef4444;
}

.stat-icon.purple {
  background-color: #8b5cf6;
}

.stat-content h3 {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: #1e293b;
}

.stat-content p {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

/* Filters */
.filters-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
}

.view-toggles {
  display: flex;
  gap: 8px;
}

.view-toggle {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 20px;
  color: #64748b;
  transition: all 0.2s;
}

.view-toggle.active {
  background-color: #4f46e5;
  color: white;
  border-color: #4f46e5;
}

.filters {
  display: flex;
  gap: 16px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: white;
  min-width: 140px;
  color: #1e293b;
}

/* Product List */
.product-list {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 24px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #f8fafc;
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #475569;
  border-bottom: 1px solid #e2e8f0;
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
  color: #1e293b;
}

.image-cell {
  width: 80px;
}

.product-thumbnail-container {
  width: 60px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  background-color: #f8fafc;
}

.product-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.low-stock {
  color: #f59e0b;
  font-weight: 600;
}

.out-of-stock {
  color: #ef4444;
  font-weight: 600;
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
  font-size: 16px;
  transition: background-color 0.2s;
}

.action-icon.edit {
  background-color: #3b82f6;
  color: white;
}

.action-icon.edit:hover {
  background-color: #2563eb;
}

.action-icon.delete {
  background-color: #ef4444;
  color: white;
}

.action-icon.delete:hover {
  background-color: #dc2626;
}

/* Product Grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.product-card {
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

.product-card-inner {
  position: relative;
  height: 100%;
  z-index: 1;
  overflow: hidden;
  background-color: var(--card-bg);
  border-radius: 12px;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  backface-visibility: hidden;
}

.product-card:hover {
  transform: translateY(-8px) rotate3d(1, 5, 0, 2deg);
  box-shadow: var(--shadow-lg);
}

.product-card:hover .product-card-inner {
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);
}

.product-image-container {
  height: 200px;
  position: relative;
  background-color: var(--background-color-secondary);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  opacity: 0;
  transition: opacity 0.2s;
}

.product-image-container:hover .product-overlay {
  opacity: 1;
}

.overlay-btn {
  width: 40px;
  height: 40px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  font-size: 18px;
  transition: transform 0.2s;
}

.overlay-btn:hover {
  transform: scale(1.1);
}

.overlay-btn.edit {
  background-color: #3b82f6;
  color: white;
}

.overlay-btn.delete {
  background-color: #ef4444;
  color: white;
}

.product-category-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background-color: var(--primary-color);
  color: white;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
  z-index: 5;
}

.product-stock-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
  z-index: 5;
  background-color: #10b981; /* green */
  color: white;
}

.product-stock-badge.low-stock {
  background-color: #f59e0b; /* amber */
}

.product-stock-badge.out-of-stock {
  background-color: #ef4444; /* red */
}

.product-details {
  padding: 16px;
  display: flex;
  flex-direction: column;
  height: calc(100% - 200px); /* Subtract image height */
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.product-price {
  font-weight: 700;
  color: #1e293b;
}

.product-stock {
  font-size: 14px;
  color: #64748b;
}

.product-stock.low-stock {
  color: #f59e0b;
}

.product-stock.out-of-stock {
  color: #ef4444;
}

.product-category {
  font-size: 14px;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Empty State */
.empty-state {
  background-color: white;
  border-radius: 8px;
  padding: 48px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.empty-state i {
  font-size: 48px;
  color: #94a3b8;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #1e293b;
}

.empty-state p {
  font-size: 16px;
  color: #64748b;
  margin: 0 0 24px 0;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: #1e293b;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 16px;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

.modal-body {
  padding: 24px;
}

/* Form */
.product-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.form-input,
.form-select,
.form-textarea {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: #4f46e5;
  outline: none;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.image-upload-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.image-drop-area {
  border: 2px dashed #e2e8f0;
  border-radius: 6px;
  padding: 16px;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s;
  position: relative;
}

.image-drop-area:hover {
  border-color: #94a3b8;
}

.image-drop-area.has-image {
  border-style: solid;
  border-color: #4f46e5;
  padding: 0;
  overflow: hidden;
}

.upload-placeholder {
  text-align: center;
  color: #94a3b8;
}

.upload-placeholder i {
  font-size: 36px;
  margin-bottom: 8px;
}

.upload-placeholder p {
  margin: 0;
}

.image-preview {
  width: 100%;
  height: 100%;
  object-fit: contain;
  max-height: 300px;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.image-controls {
  display: flex;
  gap: 8px;
}

.btn-upload {
  padding: 8px 16px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.btn-upload:hover {
  background-color: #4338ca;
}

.btn-clear {
  padding: 8px 16px;
  background-color: #f1f5f9;
  color: #64748b;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s, color 0.2s;
}

.btn-clear:hover {
  background-color: #e2e8f0;
  color: #1e293b;
}

.image-help-text {
  font-size: 12px;
  color: #64748b;
  margin: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 16px;
}

.btn-cancel {
  padding: 8px 16px;
  background-color: #f1f5f9;
  color: #64748b;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s, color 0.2s;
}

.btn-cancel:hover {
  background-color: #e2e8f0;
  color: #1e293b;
}

.btn-save {
  padding: 8px 16px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.btn-save:hover {
  background-color: #4338ca;
}

/* Confirm Modal */
.confirm-modal {
  background-color: white;
  border-radius: 8px;
  padding: 24px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.confirm-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.confirm-header i {
  font-size: 36px;
  color: #ef4444;
}

.confirm-header h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: #1e293b;
}

.warning-text {
  font-size: 14px;
  color: #ef4444;
  margin: 8px 0 16px 0;
}

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

.btn-delete {
  padding: 8px 16px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.2s;
}

.btn-delete:hover {
  background-color: #dc2626;
}

/* Loading Overlay */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 900;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(79, 70, 229, 0.2);
  border-left-color: #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Toast Notifications */
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 16px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(100px);
  opacity: 0;
  transition: transform 0.3s, opacity 0.3s;
  z-index: 1100;
  max-width: 400px;
}

.toast.show {
  transform: translateY(0);
  opacity: 1;
}

.toast-icon {
  font-size: 20px;
}

.toast-success {
  background-color: #10b981;
  color: white;
}

.toast-error {
  background-color: #ef4444;
  color: white;
}

.toast-info {
  background-color: #3b82f6;
  color: white;
}

.toast-message {
  font-size: 14px;
  font-weight: 500;
}

/* Transitions */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .filters-container {
    flex-direction: column;
    gap: 16px;
  }

  .filters {
    overflow-x: auto;
    padding-bottom: 8px;
  }

  .form-layout {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .header-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .action-buttons {
    width: 100%;
    justify-content: space-between;
  }

  .search-container {
    width: 100%;
  }

  .search-input {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .product-grid {
    grid-template-columns: 1fr;
  }

  .product-thumbnail-container {
    width: 40px;
    height: 40px;
  }

  th, td {
    padding: 8px;
  }

  th:nth-child(4), td:nth-child(4),
  th:nth-child(5), td:nth-child(5) {
    display: none;
  }

  .action-icons {
    flex-direction: column;
    gap: 4px;
  }

  .modal-container {
    width: 95%;
  }
}

/* Additional enhanced product card styles to match dashboard */
/* Product Card Colorful Effects */
.product-card-backdrop {
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

.product-card:hover .product-card-backdrop {
  opacity: 0.85;
  transform: scale(1.02);
  box-shadow: 0 0 40px rgba(236, 72, 153, 0.5);
}

.product-card-glow {
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

.product-card:hover .product-card-glow {
  opacity: 0.9;
  animation: move-glow 3s infinite alternate;
}

@keyframes move-glow {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
  }
  100% {
    transform: translate(-49%, -48%) scale(0.55);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.7);
  }
  70% {
    box-shadow: 0 0 0 15px rgba(79, 70, 229, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(79, 70, 229, 0);
  }
}

.product-stats {
  display: flex;
  justify-content: space-between;
  margin: 12px 0 16px;
  align-items: center;
}

.product-price, .product-stock {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: var(--background-color-secondary);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
}

.product-price {
  font-weight: 700;
  color: var(--primary-color);
}

.product-price i, .product-stock i {
  font-size: 18px;
  color: var(--text-secondary);
}

.product-stock span {
  font-weight: 500;
  color: var(--text-secondary);
}

.product-actions {
  display: flex;
  gap: 8px;
}

.action-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.action-button.edit {
  background-color: var(--primary-color);
  color: white;
}

.action-button.delete {
  background-color: var(--danger-color);
  color: white;
}

.action-button:hover {
  transform: translateY(-2px);
}

/* Empty state styling to match dashboard */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  margin-top: 24px;
}

.empty-state-icon {
  font-size: 48px;
  color: var(--text-muted);
  background-color: var(--card-bg-secondary);
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: 24px;
  max-width: 400px;
}

/* Dashboard Summary styles */
.dashboard-summary {
  margin-bottom: 24px;
}

.welcome-message h2 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.welcome-message p {
  color: var(--text-secondary);
  font-size: 16px;
}

/* Enhanced Filter Styles */
.filters-section {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 20px;
  margin-bottom: 24px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.filter-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.view-controls {
  display: flex;
  gap: 8px;
}

.view-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  border-radius: 6px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: background-color 0.2s, color 0.2s;
}

.view-btn.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

/* Horizontal filter layout */
.filters-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: flex-end;
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: var(--text-secondary);
}

.filter-select {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  color: var(--text-primary);
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.filter-select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
  outline: none;
}

/* Fix header alignment with sidebar */
.top-header {
  position: fixed;
  top: 0;
  right: 0;
  left: var(--sidebar-width);
  height: 70px;
  background-color: var(--background-color);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  border-bottom: 1px solid var(--border-color);
  transition: left 0.3s ease;
  width: calc(100% - var(--sidebar-width));
}

/* When sidebar is collapsed, adjust header width */
.sidebar-collapsed .top-header {
  left: 70px;
  width: calc(100% - 70px);
}

.sidebar-header {
  height: 70px;
}

/* Mobile Add Button - Hidden by default on desktop */
.mobile-add-button {
  display: none;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  padding: 16px 20px;
  background-color: var(--primary-color);
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-bottom: 10px;
}

.mobile-add-button:hover {
  background-color: var(--primary-color-dark);
}

.mobile-add-button i {
  font-size: 24px;
}

/* Media Queries for Responsive Design */
@media (max-width: 768px) {
  /* Show the mobile add button in mobile view */
  .mobile-add-button {
    display: flex;
  }
  .sidebar {
    transform: translateX(-100%);
    z-index: 200;
    position: fixed;
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .main-content {
    margin-left: 0 !important;
    width: 100% !important;
    padding-top: 90px;
  }

  .top-header {
    left: 0 !important;
    width: 100% !important;
    padding: 0 16px;
  }

  .mobile-toggle {
    display: flex !important;
  }

  .header-middle {
    display: none;
  }

  /* Responsive controls for action buttons */
  .header-right {
    justify-content: flex-end;
    display: flex !important;
  }

  .header-right .date-display {
    display: none;
  }

  /* Make sure the action buttons are properly spaced and always displayed */
  .action-buttons {
    display: flex !important;
    align-items: center;
    gap: 8px;
  }

  /* Make sure the New Product button is always visible and properly styled */
  .action-buttons .btn-add, .header-btn {
    display: flex !important;
    visibility: visible !important;
    align-items: center;
    justify-content: center;
    height: 40px;
    min-width: 80px;
    padding: 0 12px;
    border-radius: 6px;
    background-color: var(--primary-color) !important;
    color: white !important;
    margin-left: 0;
    z-index: 100;
  }

  /* Hide other buttons on very small screens */
  .action-btn {
    display: none !important;
  }

  /* On extra small screens, make it an icon-only button */
  @media (max-width: 480px) {
    .action-buttons .btn-add span, .header-btn span {
      display: none !important;
    }

    .action-buttons .btn-add i, .header-btn i {
      margin-right: 0 !important;
    }

    .action-buttons .btn-add, .header-btn {
      width: 40px !important;
      min-width: 40px !important;
      padding: 0 !important;
    }
  }
}
</style>