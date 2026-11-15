<template>
  <div class="pos-layout">
    <!-- Top Enterprise Navigation Header -->
    <header class="pos-header">
      <div class="header-left">
        <div class="brand-container">
          <img src="../assets/logo-pp.png" alt="PeakPOS Logo" class="brand-logo" />
          <div class="brand-meta">
            <h1 class="brand-name">Peak<span>POS</span></h1>
            <span class="register-pill">
              <span class="pulse-dot"></span>
              POS Terminal &bull; Active
            </span>
          </div>
        </div>

        <!-- Quick View Links -->
        <nav class="header-nav">
          <router-link to="/dashboard" class="nav-pill" title="Dashboard">
            <i class="material-icons">dashboard</i>
            <span>Dashboard</span>
          </router-link>
          <router-link to="/sales" class="nav-pill active" title="Sales Counter">
            <i class="material-icons">point_of_sale</i>
            <span>Sales</span>
          </router-link>
          <router-link to="/admin/products" class="nav-pill" title="Products">
            <i class="material-icons">inventory_2</i>
            <span>Products</span>
          </router-link>
          <router-link to="/admin/settings" class="nav-pill" title="Settings">
            <i class="material-icons">settings</i>
            <span>Settings</span>
          </router-link>
        </nav>
      </div>

      <div class="header-right">
        <!-- Live Clock & Date -->
        <div class="clock-widget">
          <span class="clock-time">{{ currentTime }}</span>
          <span class="clock-date">{{ currentDate }}</span>
        </div>

        <!-- Cashier Profile Badge -->
        <div class="cashier-badge">
          <div class="cashier-avatar">
            <i class="material-icons">person</i>
          </div>
          <div class="cashier-info">
            <span class="cashier-name">{{ cashierName }}</span>
            <span class="cashier-role">{{ cashierRole }}</span>
          </div>
        </div>

        <!-- Mobile Cart Trigger -->
        <button class="mobile-cart-btn" @click="toggleMobileCart" :class="{ 'has-items': cart.length > 0 }">
          <i class="material-icons">shopping_bag</i>
          <span class="badge" v-if="cartTotalItems > 0">{{ cartTotalItems }}</span>
        </button>
      </div>
    </header>

    <!-- Main POS Body: Catalog (Left) + Cart Sidebar (Right) -->
    <div class="pos-main">
      <!-- Catalog Section -->
      <section class="catalog-section">
        <!-- Control Bar (Search, Categories & View Toggle) -->
        <div class="catalog-toolbar">
          <div class="search-box">
            <i class="material-icons search-ico">search</i>
            <input
              type="text"
              v-model="searchTerm"
              @input="searchProducts"
              placeholder="Search by name, SKU or category..."
              class="search-input"
            />
            <button v-if="searchTerm" @click="clearSearch" class="search-clear-btn" title="Clear search">
              <i class="material-icons">close</i>
            </button>
          </div>

          <div class="toolbar-actions">
            <!-- View Mode Switch -->
            <div class="view-switch">
              <button
                class="view-toggle-btn"
                :class="{ active: viewMode === 'grid' }"
                @click="viewMode = 'grid'"
                title="Grid View"
              >
                <i class="material-icons">grid_view</i>
              </button>
              <button
                class="view-toggle-btn"
                :class="{ active: viewMode === 'list' }"
                @click="viewMode = 'list'"
                title="List View"
              >
                <i class="material-icons">view_list</i>
              </button>
            </div>

            <!-- Reload Products Button -->
            <button class="refresh-catalog-btn" @click="fetchProducts" title="Reload products">
              <i class="material-icons" :class="{ 'spin': loading }">refresh</i>
            </button>
          </div>
        </div>

        <!-- Category Horizontal Scrolling Filter Strip -->
        <div class="category-strip">
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'all' }"
            @click="filterByCategory('all')"
          >
            <i class="material-icons">apps</i>
            <span>All Items</span>
            <span class="chip-count">{{ products.length }}</span>
          </button>
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'popular' }"
            @click="filterByCategory('popular')"
          >
            <i class="material-icons">trending_up</i>
            <span>Popular</span>
          </button>
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'new' }"
            @click="filterByCategory('new')"
          >
            <i class="material-icons">bolt</i>
            <span>New</span>
          </button>
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'sale' }"
            @click="filterByCategory('sale')"
          >
            <i class="material-icons">local_offer</i>
            <span>On Sale</span>
          </button>

          <!-- Dynamic Categories from DB -->
          <button
            v-for="cat in categories"
            :key="cat.id"
            class="category-chip"
            :class="{ active: activeCategory === String(cat.id) }"
            @click="filterByCategory(String(cat.id))"
          >
            <i class="material-icons">folder_open</i>
            <span>{{ cat.name }}</span>
          </button>
        </div>

        <!-- Product Grid / List Scroll Area -->
        <div class="catalog-scroll-area">
          <!-- Loading Skeleton -->
          <div v-if="loading" class="state-container">
            <div class="pos-spinner"></div>
            <p class="state-title">Loading Catalog...</p>
          </div>

          <!-- Empty Catalog State -->
          <div v-else-if="filteredProducts.length === 0" class="state-container empty-state">
            <div class="empty-icon-wrap">
              <i class="material-icons">inventory_2</i>
            </div>
            <h3 class="state-title">No products found</h3>
            <p class="state-desc">Try clearing your search query or selecting a different category filter.</p>
            <button class="btn-reset-filter" @click="resetFilters">
              <i class="material-icons">refresh</i>
              Reset Filters
            </button>
          </div>

          <!-- Grid View Mode -->
          <div v-else-if="viewMode === 'grid'" class="product-grid">
            <div
              v-for="product in filteredProducts"
              :key="product.id"
              class="pos-card"
              :class="{ 'is-out-of-stock': product.stock <= 0 }"
              @click="handleCardClick(product)"
            >
              <div class="card-image-box">
                <img
                  :src="getProductImageUrl(product)"
                  :alt="product.name"
                  loading="lazy"
                  @error="handleImageError"
                />
                <div class="card-badges">
                  <span class="badge sale" v-if="isOnSale(product)">SALE</span>
                  <span class="badge new" v-else-if="isNewProduct(product)">NEW</span>
                  <span class="badge oos" v-if="product.stock <= 0">Out of Stock</span>
                  <span class="badge low-stock" v-else-if="product.stock < 10">Low ({{ product.stock }})</span>
                </div>
              </div>

              <div class="card-content">
                <span class="card-category">{{ getCategoryName(product.category_id) }}</span>
                <h3 class="card-title" :title="product.name">{{ product.name }}</h3>

                <div class="card-footer">
                  <div class="price-stack">
                    <span class="currency-symbol">$</span>
                    <span class="price-value">{{ product.price.toFixed(2) }}</span>
                  </div>

                  <button
                    class="btn-add-cart"
                    :disabled="product.stock <= 0"
                    @click.stop="addToCart(product)"
                    title="Add to order"
                  >
                    <i class="material-icons">add</i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- List View Mode -->
          <div v-else class="product-table-wrapper">
            <table class="product-table">
              <thead>
                <tr>
                  <th class="th-item">Product</th>
                  <th class="th-cat">Category</th>
                  <th class="th-stock">Stock Level</th>
                  <th class="th-price">Price</th>
                  <th class="th-action">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="product in filteredProducts"
                  :key="product.id"
                  class="table-row"
                  :class="{ 'row-oos': product.stock <= 0 }"
                  @click="showProductQuickView(product)"
                >
                  <td class="td-item">
                    <img :src="getProductImageUrl(product)" :alt="product.name" class="row-thumb" @error="handleImageError" />
                    <div class="row-meta">
                      <span class="row-title">{{ product.name }}</span>
                      <span class="row-sku">ID #{{ product.id }}</span>
                    </div>
                  </td>
                  <td class="td-cat">
                    <span class="cat-tag">{{ getCategoryName(product.category_id) }}</span>
                  </td>
                  <td class="td-stock">
                    <span class="stock-pill" :class="getStockClass(product)">
                      <i class="material-icons">{{ getStockIcon(product) }}</i>
                      {{ product.stock }} in stock
                    </span>
                  </td>
                  <td class="td-price">${{ product.price.toFixed(2) }}</td>
                  <td class="td-action">
                    <button
                      class="btn-table-add"
                      :disabled="product.stock <= 0"
                      @click.stop="addToCart(product)"
                      title="Add to cart"
                    >
                      <i class="material-icons">add_shopping_cart</i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- Cart / Cashier Order Sidebar -->
      <aside class="pos-cart" :class="{ 'mobile-open': isMobileCartVisible }">
        <div class="cart-card">
          <!-- Cart Top Title & Header Actions -->
          <div class="cart-top">
            <div class="cart-title-wrap">
              <div class="cart-icon-bubble">
                <i class="material-icons">receipt_long</i>
              </div>
              <div>
                <h2 class="cart-heading">Current Sale</h2>
                <span class="cart-subheading">{{ cart.length }} line items &bull; {{ cartTotalItems }} units</span>
              </div>
            </div>

            <div class="cart-top-actions">
              <button
                class="btn-cart-clear"
                v-if="cart.length > 0"
                @click="clearCart"
                title="Empty Cart"
              >
                <i class="material-icons">delete_sweep</i>
                <span>Clear</span>
              </button>
              <button class="btn-close-mobile-cart" @click="toggleMobileCart" title="Close Cart">
                <i class="material-icons">close</i>
              </button>
            </div>
          </div>

          <!-- Cart Scrollable Items List -->
          <div class="cart-body">
            <div v-if="cart.length === 0" class="cart-empty-state">
              <div class="cart-empty-icon">
                <i class="material-icons">shopping_cart</i>
              </div>
              <h4>No Items in Cart</h4>
              <p>Select products from the catalog to build your order.</p>
            </div>

            <div v-else class="cart-items-list">
              <div v-for="(item, index) in cart" :key="item.id" class="cart-row">
                <div class="cart-item-thumb">
                  <img :src="getProductImageUrl(item)" :alt="item.name" @error="handleImageError" />
                </div>

                <div class="cart-item-details">
                  <div class="cart-item-main">
                    <h4 class="cart-item-name" :title="item.name">{{ item.name }}</h4>
                    <span class="cart-item-unit-price">${{ item.price.toFixed(2) }} ea</span>
                  </div>

                  <div class="cart-item-subline">
                    <!-- Quantity Stepper -->
                    <div class="qty-stepper">
                      <button
                        class="qty-btn"
                        @click.stop="decreaseQuantity(index)"
                        :disabled="item.quantity <= 1"
                        title="Decrease"
                      >
                        <i class="material-icons">remove</i>
                      </button>
                      <span class="qty-value">{{ item.quantity }}</span>
                      <button
                        class="qty-btn"
                        @click.stop="increaseQuantity(index)"
                        :disabled="item.quantity >= item.stock"
                        title="Increase"
                      >
                        <i class="material-icons">add</i>
                      </button>
                    </div>

                    <div class="cart-item-total">
                      ${{ (item.price * item.quantity).toFixed(2) }}
                    </div>

                    <button class="btn-item-del" @click.stop="removeFromCart(index)" title="Remove item">
                      <i class="material-icons">close</i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Financial Summary -->
          <div class="cart-footer">
            <div class="summary-breakdown">
              <div class="calc-row">
                <span class="calc-label">Subtotal</span>
                <span class="calc-val">${{ calculateSubtotal().toFixed(2) }}</span>
              </div>

              <!-- Discount Selector Row -->
              <div class="calc-row discount-selection-row">
                <div class="discount-lead">
                  <i class="material-icons">local_offer</i>
                  <span>Discount</span>
                </div>
                <div class="discount-inputs">
                  <select v-model="selectedDiscount" class="pos-select-discount">
                    <option :value="null">No Discount</option>
                    <option v-for="d in discounts" :key="d.id" :value="d.id">
                      {{ d.name }} ({{ d.discount_type === 'percentage' ? d.value + '%' : '$' + d.value }})
                    </option>
                  </select>
                  <span class="discount-deduction" v-if="selectedDiscount">
                    -${{ calculateDiscountAmount().toFixed(2) }}
                  </span>
                </div>
              </div>

              <div class="calc-row">
                <span class="calc-label">Tax (7%)</span>
                <span class="calc-val">${{ calculateTax().toFixed(2) }}</span>
              </div>

              <div class="calc-divider"></div>

              <div class="calc-row grand-total-row">
                <span class="grand-total-label">Total Due</span>
                <span class="grand-total-val">${{ calculateTotal().toFixed(2) }}</span>
              </div>
            </div>

            <!-- Complete Purchase Action Button -->
            <button
              class="btn-checkout-primary"
              :disabled="cart.length === 0 || processingOrder"
              @click="proceedToCheckout"
            >
              <i class="material-icons" :class="{ 'spin': processingOrder }">
                {{ processingOrder ? 'autorenew' : 'check_circle' }}
              </i>
              <span>{{ processingOrder ? 'Processing Transaction...' : `Charge $${calculateTotal().toFixed(2)}` }}</span>
            </button>
          </div>
        </div>
      </aside>

      <!-- Mobile Backdrop Overlay -->
      <div
        class="mobile-backdrop"
        v-if="isMobileCartVisible"
        @click="toggleMobileCart"
      ></div>
    </div>

    <!-- Product Quick View Modal -->
    <transition name="fade-modal">
      <div class="modal-overlay" v-if="quickViewProduct" @click="closeQuickView">
        <div class="modal-dialog" @click.stop>
          <button class="modal-close-icon" @click="closeQuickView">
            <i class="material-icons">close</i>
          </button>

          <div class="modal-body-split">
            <div class="modal-img-col">
              <img :src="getProductImageUrl(quickViewProduct)" :alt="quickViewProduct.name" @error="handleImageError" />
              <div class="modal-stock-badge" :class="getStockClass(quickViewProduct)">
                <i class="material-icons">{{ getStockIcon(quickViewProduct) }}</i>
                <span>{{ getStockLabel(quickViewProduct) }} ({{ quickViewProduct.stock }} in stock)</span>
              </div>
            </div>

            <div class="modal-info-col">
              <span class="modal-category">{{ getCategoryName(quickViewProduct.category_id) }}</span>
              <h2 class="modal-title">{{ quickViewProduct.name }}</h2>
              <p class="modal-price">${{ quickViewProduct.price.toFixed(2) }}</p>

              <div class="modal-desc" v-if="quickViewProduct.description">
                {{ quickViewProduct.description }}
              </div>

              <div class="modal-action-box">
                <div class="modal-qty-control">
                  <span class="qty-prompt">Quantity:</span>
                  <div class="qty-stepper modal-stepper">
                    <button class="qty-btn" @click="decreaseModalQuantity" :disabled="modalQuantity <= 1">
                      <i class="material-icons">remove</i>
                    </button>
                    <span class="qty-value">{{ modalQuantity }}</span>
                    <button class="qty-btn" @click="increaseModalQuantity" :disabled="modalQuantity >= quickViewProduct.stock">
                      <i class="material-icons">add</i>
                    </button>
                  </div>
                </div>

                <button
                  class="btn-modal-add-cart"
                  :disabled="quickViewProduct.stock <= 0"
                  @click="addFromModal"
                >
                  <i class="material-icons">add_shopping_cart</i>
                  <span>Add {{ modalQuantity }} to Order</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Order Complete / Receipt Modal -->
    <transition name="fade-modal">
      <div class="modal-overlay" v-if="showOrderComplete" @click="closeOrderComplete">
        <div class="order-success-dialog" @click.stop>
          <div class="success-top-badge">
            <div class="check-ring">
              <i class="material-icons">done</i>
            </div>
            <h2>Transaction Approved!</h2>
            <p>Order #{{ orderSummary.order_id || '---' }} has been successfully placed and recorded.</p>
          </div>

          <div class="receipt-preview-ticket">
            <div class="ticket-header">
              <h3>PeakPOS Store</h3>
              <p>Receipt #{{ orderSummary.order_id }}</p>
            </div>

            <div class="ticket-items">
              <div v-for="item in orderSummary.items" :key="item.id" class="ticket-row">
                <span class="ticket-item-title">{{ item.name }} &times; {{ item.quantity }}</span>
                <span class="ticket-item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>

            <div class="ticket-totals">
              <div class="ticket-calc-row">
                <span>Subtotal</span>
                <span>${{ orderSummary.subtotal.toFixed(2) }}</span>
              </div>
              <div class="ticket-calc-row">
                <span>Tax</span>
                <span>${{ orderSummary.tax.toFixed(2) }}</span>
              </div>
              <div class="ticket-calc-row" v-if="orderSummary.discount > 0">
                <span>Discount</span>
                <span>-${{ orderSummary.discount.toFixed(2) }}</span>
              </div>
              <div class="ticket-calc-row ticket-grand-total">
                <span>Total Paid</span>
                <span>${{ orderSummary.total.toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <div class="success-actions">
            <button class="btn-thermal-print" @click="printReceipt">
              <i class="material-icons">receipt</i>
              <span>Print Receipt</span>
            </button>
            <button class="btn-new-order" @click="closeOrderComplete">
              <i class="material-icons">add_shopping_cart</i>
              <span>New Sale</span>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modern Toast Notification -->
    <transition name="toast-slide">
      <div v-if="toast.show" class="pos-toast" :class="toast.type">
        <i class="material-icons toast-ico">{{ toast.icon }}</i>
        <div class="toast-body">
          <h5 class="toast-heading">{{ toast.title }}</h5>
          <p class="toast-msg">{{ toast.message }}</p>
        </div>
        <button class="toast-dismiss" @click="toast.show = false">
          <i class="material-icons">close</i>
        </button>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'SalesView',
  data() {
    return {
      // Products & Categories Data
      products: [],
      categories: [],
      loading: true,
      searchTerm: '',
      viewMode: localStorage.getItem('salesViewMode') || 'grid',
      activeCategory: 'all',

      // Cart State
      cart: [],
      isMobileCartVisible: false,
      selectedDiscount: null,
      discounts: [],
      discountLoading: false,
      processingOrder: false,

      // Modals State
      quickViewProduct: null,
      modalQuantity: 1,
      showOrderComplete: false,
      orderSummary: {
        items: [],
        subtotal: 0,
        tax: 0,
        discount: 0,
        total: 0,
        order_id: null
      },

      // Cashier and Time state
      cashierName: localStorage.getItem('username') || 'Cashier',
      cashierRole: localStorage.getItem('role') || 'Staff',
      currentTime: '',
      currentDate: '',
      clockInterval: null,

      // Toast State
      toast: {
        show: false,
        type: 'success',
        title: '',
        message: '',
        icon: 'check_circle',
        timeout: null
      }
    };
  },
  computed: {
    cartTotalItems() {
      return this.cart.reduce((sum, item) => sum + item.quantity, 0);
    },
    filteredProducts() {
      let result = [...this.products];

      if (this.searchTerm) {
        const query = this.searchTerm.toLowerCase().trim();
        result = result.filter(product => {
          const nameMatch = product.name && product.name.toLowerCase().includes(query);
          const descMatch = product.description && product.description.toLowerCase().includes(query);
          const catMatch = this.getCategoryName(product.category_id).toLowerCase().includes(query);
          return nameMatch || descMatch || catMatch;
        });
      }

      if (this.activeCategory !== 'all') {
        switch (this.activeCategory) {
          case 'popular':
            result = result.filter(p => p.sales_count && p.sales_count > 5);
            result.sort((a, b) => (b.sales_count || 0) - (a.sales_count || 0));
            break;
          case 'new':
            result = result.filter(p => this.isNewProduct(p));
            break;
          case 'sale':
            result = result.filter(p => this.isOnSale(p));
            break;
          default:
            if (!isNaN(parseInt(this.activeCategory))) {
              result = result.filter(p => p.category_id === parseInt(this.activeCategory));
            }
        }
      }

      return result;
    }
  },
  methods: {
    updateClock() {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      this.currentDate = now.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' });
    },

    getProductImageUrl(product) {
      if (!product) return this.getPlaceholderImage();
      const imagePath = product.image_url || product.image;
      if (!imagePath) return this.getPlaceholderImage();

      if (/^https?:\/\//.test(imagePath)) return imagePath;

      const backendBase = 'http://127.0.0.1:5000';
      const cleanPath = imagePath.replace(/^\/+|\/+$/g, '');
      let finalPath;

      if (cleanPath.startsWith('static/')) {
        finalPath = cleanPath;
      } else if (cleanPath.startsWith('product_images/')) {
        finalPath = `static/${cleanPath}`;
      } else {
        finalPath = `static/product_images/${cleanPath}`;
      }

      return `${backendBase}/${finalPath}`;
    },

    handleImageError(e) {
      e.target.src = this.getPlaceholderImage();
    },

    getPlaceholderImage() {
      return 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlMmU4ZjAiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIyMCIgZm9udC13ZWlnaHQ9IjYwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZvbnQtZmFtaWx5PSJzeXN0ZW0tdWksIHNhbnMtc2VyaWYiIGZpbGw9IiM5NGEzYjgiPlBlYWtQT1M8L3RleHQ+PC9zdmc+';
    },

    isNewProduct(product) {
      if (!product || !product.created_at) return false;
      const createdDate = new Date(product.created_at);
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return createdDate > thirtyDaysAgo;
    },

    isOnSale(product) {
      return !!(product.on_sale || product.discount_price);
    },

    getStockClass(product) {
      if (product.stock <= 0) return 'out-of-stock';
      if (product.stock < 10) return 'low-stock';
      return 'in-stock';
    },

    getStockIcon(product) {
      if (product.stock <= 0) return 'block';
      if (product.stock < 10) return 'warning';
      return 'check_circle';
    },

    getStockLabel(product) {
      if (product.stock <= 0) return 'Out of Stock';
      if (product.stock < 10) return 'Low Stock';
      return 'In Stock';
    },

    getCategoryName(categoryId) {
      const cat = this.categories.find(c => c.id === categoryId);
      return cat ? cat.name : 'General';
    },

    handleCardClick(product) {
      if (product.stock > 0) {
        this.addToCart(product);
      } else {
        this.showProductQuickView(product);
      }
    },

    async fetchProducts() {
      this.loading = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/products');
        if (response.ok) {
          this.products = await response.json();
          this.restoreCartFromStorage();
        } else {
          this.showToast('Error', 'Failed to load products.', 'error');
        }
      } catch (error) {
        this.showToast('Network Error', 'Cannot connect to server.', 'error');
      } finally {
        this.loading = false;
      }
    },

    async fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/categories');
        if (response.ok) {
          this.categories = await response.json();
        }
      } catch (err) {
        console.error('Error fetching categories:', err);
      }
    },

    async fetchDiscounts() {
      this.discountLoading = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/discounts');
        if (response.ok) {
          this.discounts = await response.json();
        }
      } catch (err) {
        console.error('Error fetching discounts:', err);
      } finally {
        this.discountLoading = false;
      }
    },

    searchProducts() {},

    clearSearch() {
      this.searchTerm = '';
    },

    filterByCategory(category) {
      this.activeCategory = category;
    },

    resetFilters() {
      this.searchTerm = '';
      this.activeCategory = 'all';
    },

    addToCart(product) {
      if (product.stock <= 0) return;

      const existingIndex = this.cart.findIndex(item => item.id === product.id);
      if (existingIndex >= 0) {
        if (this.cart[existingIndex].quantity < product.stock) {
          this.cart[existingIndex].quantity++;
          this.showToast('Updated Order', `Added another ${product.name}`, 'success');
        } else {
          this.showToast('Max Stock Reached', `Only ${product.stock} available.`, 'warning');
        }
      } else {
        this.cart.push({ ...product, quantity: 1 });
        this.showToast('Added to Cart', `${product.name} added`, 'success');
      }
      this.saveCartToStorage();
    },

    removeFromCart(index) {
      const removed = this.cart[index];
      this.cart.splice(index, 1);
      this.saveCartToStorage();
      if (removed) {
        this.showToast('Removed', `${removed.name} removed from order.`, 'info');
      }
    },

    increaseQuantity(index) {
      const item = this.cart[index];
      if (item && item.quantity < item.stock) {
        item.quantity++;
        this.saveCartToStorage();
      }
    },

    decreaseQuantity(index) {
      const item = this.cart[index];
      if (item && item.quantity > 1) {
        item.quantity--;
        this.saveCartToStorage();
      }
    },

    clearCart() {
      if (!this.cart.length) return;
      this.cart = [];
      localStorage.removeItem('peak_pos_cart');
      this.showToast('Cart Cleared', 'All items have been removed.', 'info');
    },

    saveCartToStorage() {
      localStorage.setItem('peak_pos_cart', JSON.stringify(this.cart));
    },

    restoreCartFromStorage() {
      const saved = localStorage.getItem('peak_pos_cart');
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          this.cart = parsed.filter(item => {
            const current = this.products.find(p => p.id === item.id);
            if (!current) return false;
            item.price = current.price;
            item.stock = current.stock;
            if (item.quantity > current.stock) {
              item.quantity = Math.max(1, current.stock);
            }
            return true;
          });
          if (parsed.length !== this.cart.length) {
            this.saveCartToStorage();
          }
        } catch (e) {
          localStorage.removeItem('peak_pos_cart');
        }
      }
    },

    toggleMobileCart() {
      this.isMobileCartVisible = !this.isMobileCartVisible;
    },

    calculateSubtotal() {
      return this.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    },

    calculateTax() {
      return this.calculateSubtotal() * 0.07;
    },

    calculateDiscountAmount() {
      if (!this.selectedDiscount) return 0;
      const discount = this.discounts.find(d => d.id === this.selectedDiscount);
      if (!discount) return 0;
      const sub = this.calculateSubtotal();
      if (discount.discount_type === 'percentage') {
        return sub * (discount.value / 100);
      }
      return Math.min(sub, discount.value);
    },

    calculateTotal() {
      const total = this.calculateSubtotal() + this.calculateTax() - this.calculateDiscountAmount();
      return Math.max(0, total);
    },

    showProductQuickView(product) {
      this.quickViewProduct = product;
      this.modalQuantity = 1;
    },

    closeQuickView() {
      this.quickViewProduct = null;
    },

    increaseModalQuantity() {
      if (this.quickViewProduct && this.modalQuantity < this.quickViewProduct.stock) {
        this.modalQuantity++;
      }
    },

    decreaseModalQuantity() {
      if (this.modalQuantity > 1) {
        this.modalQuantity--;
      }
    },

    addFromModal() {
      if (!this.quickViewProduct || this.quickViewProduct.stock <= 0) return;

      const existingIndex = this.cart.findIndex(i => i.id === this.quickViewProduct.id);
      if (existingIndex >= 0) {
        const nextQty = this.cart[existingIndex].quantity + this.modalQuantity;
        if (nextQty <= this.quickViewProduct.stock) {
          this.cart[existingIndex].quantity = nextQty;
        } else {
          this.cart[existingIndex].quantity = this.quickViewProduct.stock;
        }
      } else {
        this.cart.push({
          ...this.quickViewProduct,
          quantity: this.modalQuantity
        });
      }
      this.saveCartToStorage();
      this.showToast('Order Updated', `Added ${this.modalQuantity} × ${this.quickViewProduct.name}`, 'success');
      this.closeQuickView();
    },

    async proceedToCheckout() {
      if (this.cart.length === 0 || this.processingOrder) return;
      this.processingOrder = true;

      try {
        const orderData = {
          cart: this.cart.map(c => ({
            id: c.id,
            quantity: c.quantity,
            price: c.price
          })),
          discount_id: this.selectedDiscount,
          subtotal: this.calculateSubtotal(),
          tax: this.calculateTax(),
          total: this.calculateTotal()
        };

        const response = await fetch('http://127.0.0.1:5000/api/checkout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(orderData)
        });

        if (!response.ok) {
          throw new Error('Failed to process order');
        }

        const orderResponse = await response.json();
        const orderId = orderResponse.order_id || orderResponse.order?.id;

        this.orderSummary = {
          items: [...this.cart],
          subtotal: this.calculateSubtotal(),
          tax: this.calculateTax(),
          discount: this.calculateDiscountAmount(),
          total: this.calculateTotal(),
          order_id: orderId
        };

        // Create snapshot receipt
        const receiptPayload = {
          order_id: this.orderSummary.order_id,
          snapshot: {
            items: this.cart.map(item => ({
              id: item.id,
              name: item.name,
              price: item.price,
              quantity: item.quantity
            })),
            subtotal: this.orderSummary.subtotal,
            tax: this.orderSummary.tax,
            discount: this.orderSummary.discount,
            total: this.orderSummary.total
          }
        };

        try {
          await fetch('http://127.0.0.1:5000/api/receipts', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(receiptPayload)
          });
        } catch (err) {
          console.error('Receipt generation error:', err);
        }

        this.showOrderComplete = true;
        this.cart = [];
        localStorage.removeItem('peak_pos_cart');
      } catch (error) {
        console.error('Checkout error:', error);
        this.showToast('Checkout Failed', 'Failed to complete transaction. Please try again.', 'error');
      } finally {
        this.processingOrder = false;
      }
    },

    async printReceipt() {
      if (!this.orderSummary || !this.orderSummary.order_id) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/receipts/${this.orderSummary.order_id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) throw new Error('Failed to fetch receipt');
        const receipt = await response.json();

        const receiptHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Receipt #${receipt.receipt_id} - PeakPOS</title>
  <style>
    body {
      font-family: 'Courier New', monospace;
      padding: 18px;
      max-width: 320px;
      margin: 0 auto;
      color: #111;
      font-size: 13px;
    }
    .head { text-align: center; border-bottom: 1px dashed #444; padding-bottom: 10px; margin-bottom: 10px; }
    .head h2 { margin: 0; font-size: 18px; text-transform: uppercase; letter-spacing: 1px; }
    .meta { font-size: 11px; margin-top: 5px; color: #555; }
    .items { width: 100%; border-bottom: 1px dashed #444; padding-bottom: 8px; margin-bottom: 8px; }
    .item-line { display: flex; justify-content: space-between; margin-bottom: 4px; }
    .totals-line { display: flex; justify-content: space-between; margin-bottom: 4px; }
    .grand { font-weight: bold; font-size: 15px; border-top: 1px solid #111; padding-top: 6px; margin-top: 6px; }
    .foot { text-align: center; margin-top: 15px; font-size: 11px; color: #555; }
    @media print {
      body { padding: 0; }
    }
  </style>
</head>
<body>
  <div class="head">
    <h2>PeakPOS Store</h2>
    <div class="meta">
      <div>Order #${receipt.receipt_id}</div>
      <div>Date: ${new Date(receipt.created_at || Date.now()).toLocaleString()}</div>
    </div>
  </div>
  <div class="items">
    ${receipt.snapshot.items.map(it => `
      <div class="item-line">
        <span>${it.name} &times; ${it.quantity}</span>
        <span>$${(it.price * it.quantity).toFixed(2)}</span>
      </div>
    `).join('')}
  </div>
  <div>
    <div class="totals-line"><span>Subtotal:</span><span>$${receipt.snapshot.subtotal.toFixed(2)}</span></div>
    <div class="totals-line"><span>Tax (7%):</span><span>$${receipt.snapshot.tax.toFixed(2)}</span></div>
    ${receipt.snapshot.discount > 0 ? `<div class="totals-line"><span>Discount:</span><span>-$${receipt.snapshot.discount.toFixed(2)}</span></div>` : ''}
    <div class="totals-line grand"><span>Total:</span><span>$${receipt.snapshot.total.toFixed(2)}</span></div>
  </div>
  <div class="foot">
    <p>Thank you for your purchase!</p>
    <p>PeakPOS &bull; www.peakpos.com</p>
  </div>
</body>
</html>`;

        const win = window.open('', '_blank');
        win.document.open();
        win.document.write(receiptHtml);
        win.document.close();
        win.onload = () => {
          setTimeout(() => {
            win.focus();
            win.print();
          }, 300);
        };
      } catch (err) {
        console.error('Print receipt error:', err);
      }
    },

    closeOrderComplete() {
      this.showOrderComplete = false;
      this.selectedDiscount = null;
    },

    showToast(title, message, type = 'success') {
      if (this.toast.timeout) clearTimeout(this.toast.timeout);
      let icon = 'check_circle';
      if (type === 'error') icon = 'error_outline';
      else if (type === 'warning') icon = 'warning_amber';
      else if (type === 'info') icon = 'info_outline';

      this.toast = {
        show: true,
        type,
        title,
        message,
        icon,
        timeout: setTimeout(() => {
          this.toast.show = false;
        }, 3500)
      };
    }
  },
  created() {
    this.$watch('viewMode', newMode => {
      localStorage.setItem('salesViewMode', newMode);
    });
    this.fetchProducts();
    this.fetchCategories();
    this.fetchDiscounts();
    this.updateClock();
    this.clockInterval = setInterval(this.updateClock, 1000);
  },
  beforeUnmount() {
    if (this.clockInterval) clearInterval(this.clockInterval);
  }
};
</script>

<style scoped>
/* ==========================================================================
   PeakPOS Modern Enterprise Design System & Responsive Styles
   ========================================================================== */

.pos-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  background-color: #f8fafc;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #0f172a;
  overflow: hidden;
}

/* --------------------------------------------------------------------------
   Header Bar
   -------------------------------------------------------------------------- */
.pos-header {
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
  z-index: 20;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 32px;
}

.brand-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  height: 40px;
  width: auto;
  max-width: 48px;
  object-fit: contain;
}

.brand-meta {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin: 0;
}

.brand-name span {
  color: #4f46e5;
}

.register-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.7rem;
  font-weight: 600;
  color: #059669;
  letter-spacing: 0.02em;
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 6px;
}

.nav-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  text-decoration: none;
  transition: all 0.15s ease;
}

.nav-pill i {
  font-size: 1.1rem;
}

.nav-pill:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.nav-pill.active {
  background: #eef2ff;
  color: #4f46e5;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.clock-widget {
  display: flex;
  flex-direction: column;
  text-align: right;
  line-height: 1.2;
}

.clock-time {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1e293b;
  font-variant-numeric: tabular-nums;
}

.clock-date {
  font-size: 0.72rem;
  color: #94a3b8;
  font-weight: 500;
}

.cashier-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 12px 4px 6px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
}

.cashier-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #e0e7ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cashier-avatar i {
  font-size: 1.1rem;
}

.cashier-info {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.cashier-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #0f172a;
}

.cashier-role {
  font-size: 0.68rem;
  color: #64748b;
  text-transform: capitalize;
}

.mobile-cart-btn {
  display: none;
  position: relative;
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: #4f46e5;
  color: #ffffff;
  border: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.mobile-cart-btn .badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: #fff;
  font-size: 0.7rem;
  font-weight: 800;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* --------------------------------------------------------------------------
   Main Content Layout
   -------------------------------------------------------------------------- */
.pos-main {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* --------------------------------------------------------------------------
   Catalog Section
   -------------------------------------------------------------------------- */
.catalog-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f8fafc;
  padding: 16px 20px 20px 24px;
}

.catalog-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 12px;
}

.search-box {
  flex: 1;
  max-width: 520px;
  position: relative;
  display: flex;
  align-items: center;
}

.search-ico {
  position: absolute;
  left: 14px;
  color: #94a3b8;
  font-size: 1.25rem;
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 44px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0 42px 0 42px;
  font-size: 0.9rem;
  color: #0f172a;
  outline: none;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

.search-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.search-clear-btn {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
}

.search-clear-btn:hover {
  color: #0f172a;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.view-switch {
  display: flex;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 2px;
}

.view-toggle-btn {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.view-toggle-btn.active {
  background: #4f46e5;
  color: #ffffff;
}

.refresh-catalog-btn {
  width: 42px;
  height: 42px;
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.refresh-catalog-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

/* Category Horizontal Strip */
.category-strip {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 12px;
  scrollbar-width: none;
  flex-shrink: 0;
}

.category-strip::-webkit-scrollbar {
  display: none;
}

.category-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.15s ease;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
}

.category-chip i {
  font-size: 1.1rem;
}

.chip-count {
  font-size: 0.72rem;
  padding: 1px 6px;
  border-radius: 9999px;
  background: #f1f5f9;
  color: #64748b;
}

.category-chip:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}

.category-chip.active {
  background: #1e293b;
  color: #ffffff;
  border-color: #1e293b;
}

.category-chip.active .chip-count {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

/* Catalog Scroll Container */
.catalog-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}

.catalog-scroll-area::-webkit-scrollbar {
  width: 6px;
}

.catalog-scroll-area::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

/* Product Cards Grid */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(185px, 1fr));
  gap: 16px;
  padding-bottom: 24px;
}

.pos-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
}

.pos-card:hover {
  transform: translateY(-2px);
  border-color: #cbd5e1;
  box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.08);
}

.pos-card.is-out-of-stock {
  opacity: 0.65;
}

.card-image-box {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #f1f5f9;
  overflow: hidden;
}

.card-image-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.pos-card:hover .card-image-box img {
  transform: scale(1.04);
}

.card-badges {
  position: absolute;
  top: 8px;
  left: 8px;
  right: 8px;
  display: flex;
  justify-content: space-between;
  pointer-events: none;
}

.badge {
  font-size: 0.68rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.badge.sale {
  background: #ef4444;
  color: #fff;
}

.badge.new {
  background: #3b82f6;
  color: #fff;
}

.badge.low-stock {
  background: #f59e0b;
  color: #fff;
}

.badge.oos {
  background: #64748b;
  color: #fff;
}

.card-content {
  padding: 12px 14px 14px 14px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-category {
  font-size: 0.72rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 2px;
}

.card-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.3;
  margin: 0 0 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 2.6em;
}

.card-footer {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 8px;
  border-top: 1px dashed #f1f5f9;
}

.price-stack {
  display: flex;
  align-items: baseline;
  color: #0f172a;
}

.currency-symbol {
  font-size: 0.8rem;
  font-weight: 700;
  color: #4f46e5;
  margin-right: 1px;
}

.price-value {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
}

.btn-add-cart {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: #eef2ff;
  color: #4f46e5;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-add-cart:hover:not(:disabled) {
  background: #4f46e5;
  color: #ffffff;
}

.btn-add-cart:disabled {
  background: #f1f5f9;
  color: #cbd5e1;
  cursor: not-allowed;
}

/* Product Table Mode */
.product-table-wrapper {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
}

.product-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.product-table th {
  background: #f8fafc;
  padding: 12px 16px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  border-bottom: 1px solid #e2e8f0;
}

.product-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.table-row {
  cursor: pointer;
  transition: background 0.15s ease;
}

.table-row:hover {
  background: #f8fafc;
}

.td-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.row-thumb {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  object-fit: cover;
  background: #f1f5f9;
}

.row-title {
  display: block;
  font-weight: 700;
  font-size: 0.9rem;
  color: #0f172a;
}

.row-sku {
  font-size: 0.72rem;
  color: #94a3b8;
}

.cat-tag {
  font-size: 0.78rem;
  padding: 3px 8px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
  font-weight: 600;
}

.stock-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.78rem;
  font-weight: 600;
}

.stock-pill i {
  font-size: 0.95rem;
}

.stock-pill.in-stock { color: #059669; }
.stock-pill.low-stock { color: #d97706; }
.stock-pill.out-of-stock { color: #dc2626; }

.td-price {
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
}

.btn-table-add {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #4f46e5;
  color: #fff;
  border: none;
  cursor: pointer;
}

/* --------------------------------------------------------------------------
   Cart Sidebar (Right Register Counter)
   -------------------------------------------------------------------------- */
.pos-cart {
  width: 380px;
  flex-shrink: 0;
  background: #ffffff;
  border-left: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  z-index: 10;
}

.cart-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.cart-top {
  padding: 16px 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cart-title-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cart-icon-bubble {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #eef2ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-heading {
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1.2;
}

.cart-subheading {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.cart-top-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-cart-clear {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-cart-clear:hover {
  background: #fecaca;
}

.btn-close-mobile-cart {
  display: none;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
}

/* Cart Body Items */
.cart-body {
  flex: 1;
  overflow-y: auto;
  padding: 12px 16px;
}

.cart-body::-webkit-scrollbar {
  width: 5px;
}

.cart-body::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 4px;
}

.cart-empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #94a3b8;
  padding: 24px;
}

.cart-empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  color: #94a3b8;
}

.cart-empty-icon i {
  font-size: 2rem;
}

.cart-empty-state h4 {
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
  margin: 0 0 4px 0;
}

.cart-empty-state p {
  font-size: 0.82rem;
  line-height: 1.4;
  margin: 0;
}

.cart-items-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cart-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  transition: all 0.15s ease;
}

.cart-row:hover {
  border-color: #cbd5e1;
  background: #ffffff;
}

.cart-item-thumb {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
  background: #e2e8f0;
  flex-shrink: 0;
}

.cart-item-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cart-item-details {
  flex: 1;
  min-width: 0;
}

.cart-item-main {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 6px;
  margin-bottom: 6px;
}

.cart-item-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cart-item-unit-price {
  font-size: 0.72rem;
  color: #64748b;
  font-weight: 500;
  white-space: nowrap;
}

.cart-item-subline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.qty-stepper {
  display: inline-flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 1px;
}

.qty-btn {
  width: 24px;
  height: 24px;
  background: none;
  border: none;
  color: #475569;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 4px;
}

.qty-btn i {
  font-size: 0.95rem;
}

.qty-btn:hover:not(:disabled) {
  background: #f1f5f9;
  color: #0f172a;
}

.qty-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qty-value {
  padding: 0 6px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #0f172a;
  min-width: 20px;
  text-align: center;
}

.cart-item-total {
  font-size: 0.9rem;
  font-weight: 800;
  color: #0f172a;
}

.btn-item-del {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 2px;
  display: flex;
}

.btn-item-del:hover {
  color: #ef4444;
}

/* Cart Footer Calculations & Pay Button */
.cart-footer {
  border-top: 1px solid #e2e8f0;
  background: #ffffff;
  padding: 16px 20px 20px 20px;
}

.summary-breakdown {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.calc-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.84rem;
  color: #64748b;
  font-weight: 500;
}

.calc-val {
  font-weight: 700;
  color: #1e293b;
}

.discount-selection-row {
  padding: 4px 0;
}

.discount-lead {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #4f46e5;
  font-weight: 600;
}

.discount-lead i {
  font-size: 1rem;
}

.discount-inputs {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pos-select-discount {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 3px 6px;
  font-size: 0.78rem;
  font-weight: 600;
  color: #334155;
  outline: none;
}

.discount-deduction {
  color: #dc2626;
  font-weight: 700;
  font-size: 0.85rem;
}

.calc-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 4px 0;
}

.grand-total-row {
  margin-top: 2px;
}

.grand-total-label {
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
}

.grand-total-val {
  font-size: 1.45rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.btn-checkout-primary {
  width: 100%;
  height: 50px;
  border-radius: 12px;
  background: #4f46e5;
  color: #ffffff;
  border: none;
  font-size: 1rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: background 0.15s ease, transform 0.1s ease;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
}

.btn-checkout-primary:hover:not(:disabled) {
  background: #4338ca;
  transform: translateY(-1px);
}

.btn-checkout-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-checkout-primary:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
  box-shadow: none;
}

/* --------------------------------------------------------------------------
   Modals
   -------------------------------------------------------------------------- */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 16px;
}

.modal-dialog {
  background: #ffffff;
  border-radius: 20px;
  max-width: 680px;
  width: 100%;
  position: relative;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-close-icon {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.modal-body-split {
  display: flex;
  min-height: 340px;
}

.modal-img-col {
  width: 45%;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  border-right: 1px solid #f1f5f9;
  position: relative;
}

.modal-img-col img {
  max-width: 100%;
  max-height: 220px;
  object-fit: contain;
}

.modal-stock-badge {
  margin-top: 16px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 9999px;
}

.modal-stock-badge.in-stock { background: #dcfce7; color: #166534; }
.modal-stock-badge.low-stock { background: #fef3c7; color: #92400e; }
.modal-stock-badge.out-of-stock { background: #fee2e2; color: #991b1b; }

.modal-info-col {
  width: 55%;
  padding: 32px 28px 24px 28px;
  display: flex;
  flex-direction: column;
}

.modal-category {
  font-size: 0.75rem;
  font-weight: 700;
  color: #4f46e5;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 8px 0;
  line-height: 1.25;
}

.modal-price {
  font-size: 1.5rem;
  font-weight: 900;
  color: #0f172a;
  margin-bottom: 12px;
}

.modal-desc {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 20px;
  flex: 1;
}

.modal-action-box {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-qty-control {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.qty-prompt {
  font-size: 0.85rem;
  font-weight: 700;
  color: #334155;
}

.modal-stepper {
  padding: 2px;
}

.modal-stepper .qty-btn {
  width: 30px;
  height: 30px;
}

.btn-modal-add-cart {
  width: 100%;
  height: 46px;
  border-radius: 10px;
  background: #4f46e5;
  color: #ffffff;
  border: none;
  font-size: 0.95rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
}

.btn-modal-add-cart:disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
}

/* Order Complete Dialog */
.order-success-dialog {
  background: #ffffff;
  border-radius: 20px;
  max-width: 440px;
  width: 100%;
  padding: 28px 24px;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.check-ring {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: #dcfce7;
  color: #16a34a;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.check-ring i {
  font-size: 2.2rem;
}

.success-top-badge h2 {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 4px 0;
}

.success-top-badge p {
  font-size: 0.82rem;
  color: #64748b;
  margin: 0 0 16px 0;
}

.receipt-preview-ticket {
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 20px;
  text-align: left;
}

.ticket-header {
  border-bottom: 1px dashed #e2e8f0;
  padding-bottom: 8px;
  margin-bottom: 8px;
  text-align: center;
}

.ticket-header h3 {
  font-size: 0.95rem;
  font-weight: 800;
  margin: 0;
  color: #0f172a;
}

.ticket-header p {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
}

.ticket-items {
  max-height: 120px;
  overflow-y: auto;
  border-bottom: 1px dashed #e2e8f0;
  padding-bottom: 8px;
  margin-bottom: 8px;
}

.ticket-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  margin-bottom: 3px;
  color: #334155;
}

.ticket-totals {
  display: flex;
  flex-direction: column;
  gap: 3px;
  font-size: 0.78rem;
}

.ticket-calc-row {
  display: flex;
  justify-content: space-between;
  color: #64748b;
}

.ticket-grand-total {
  font-size: 0.92rem;
  font-weight: 800;
  color: #0f172a;
  border-top: 1px solid #cbd5e1;
  padding-top: 4px;
  margin-top: 2px;
}

.success-actions {
  display: flex;
  gap: 10px;
}

.btn-thermal-print {
  flex: 1;
  height: 46px;
  border-radius: 10px;
  background: #1e293b;
  color: #ffffff;
  border: none;
  font-weight: 700;
  font-size: 0.88rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
}

.btn-new-order {
  flex: 1;
  height: 46px;
  border-radius: 10px;
  background: #4f46e5;
  color: #ffffff;
  border: none;
  font-weight: 700;
  font-size: 0.88rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
}

/* --------------------------------------------------------------------------
   Toast Notifications
   -------------------------------------------------------------------------- */
.pos-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #ffffff;
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  z-index: 100;
  max-width: 360px;
}

.pos-toast.success { border-left: 4px solid #10b981; }
.pos-toast.warning { border-left: 4px solid #f59e0b; }
.pos-toast.error   { border-left: 4px solid #ef4444; }
.pos-toast.info    { border-left: 4px solid #3b82f6; }

.pos-toast.success .toast-ico { color: #10b981; }
.pos-toast.warning .toast-ico { color: #f59e0b; }
.pos-toast.error .toast-ico   { color: #ef4444; }
.pos-toast.info .toast-ico    { color: #3b82f6; }

.toast-body {
  flex: 1;
}

.toast-heading {
  font-size: 0.85rem;
  font-weight: 700;
  margin: 0;
  color: #0f172a;
}

.toast-msg {
  font-size: 0.78rem;
  color: #64748b;
  margin: 2px 0 0 0;
}

.toast-dismiss {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
}

/* --------------------------------------------------------------------------
   Animations & Transitions
   -------------------------------------------------------------------------- */
.spin {
  animation: spin-anim 0.8s linear infinite;
}

@keyframes spin-anim {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.pos-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin-anim 0.8s linear infinite;
  margin-bottom: 12px;
}

.state-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px;
}

.state-title {
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
  margin: 0 0 6px 0;
}

.state-desc {
  font-size: 0.82rem;
  color: #64748b;
  max-width: 320px;
  margin: 0 0 16px 0;
}

.btn-reset-filter {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  background: #1e293b;
  color: #ffffff;
  border: none;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.fade-modal-enter-active,
.fade-modal-leave-active {
  transition: opacity 0.2s ease;
}

.fade-modal-enter-from,
.fade-modal-leave-to {
  opacity: 0;
}

.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.25s ease;
}

.toast-slide-enter-from,
.toast-slide-leave-to {
  transform: translateY(20px);
  opacity: 0;
}

/* --------------------------------------------------------------------------
   Responsive Breakpoints (Tablet & Mobile)
   -------------------------------------------------------------------------- */
@media (max-width: 1024px) {
  .header-nav {
    display: none;
  }

  .mobile-cart-btn {
    display: flex;
  }

  .pos-cart {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 380px;
    max-width: 90vw;
    z-index: 40;
    transform: translateX(100%);
    transition: transform 0.25s ease;
    box-shadow: -10px 0 25px rgba(0, 0, 0, 0.15);
  }

  .pos-cart.mobile-open {
    transform: translateX(0);
  }

  .btn-close-mobile-cart {
    display: flex;
  }

  .mobile-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(2px);
    z-index: 35;
  }
}

@media (max-width: 640px) {
  .pos-header {
    padding: 0 16px;
  }

  .clock-widget {
    display: none;
  }

  .catalog-section {
    padding: 12px 14px;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .pos-card {
    border-radius: 10px;
  }

  .card-content {
    padding: 8px 10px 10px 10px;
  }

  .card-title {
    font-size: 0.82rem;
  }

  .price-value {
    font-size: 1rem;
  }

  .modal-body-split {
    flex-direction: column;
  }

  .modal-img-col {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #f1f5f9;
  }

  .modal-info-col {
    width: 100%;
    padding: 20px;
  }
}
</style>
