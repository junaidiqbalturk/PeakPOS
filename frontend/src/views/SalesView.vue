<template>
  <div class="sales-view">
    <!-- Top Action Bar -->
    <div class="sales-action-bar">
      <div class="page-title">
        <img style="height: 65px; width: 100px;" src="../assets/logo-pp.png"><!--<h2><i class="material-icons">point_of_sale</i> Sales</h2>-->
        <p class="subtitle">Manage transactions and checkout</p>
      </div>

      <div class="action-controls">
        <div class="search-control">
          <i class="material-icons search-icon">search</i>
          <input
            type="text"
            v-model="searchTerm"
            @input="searchProducts"
            placeholder="Search products by name, category..."
            class="search-input"
          />
          <button v-if="searchTerm" @click="clearSearch" class="clear-search">
            <i class="material-icons">close</i>
          </button>
        </div>

        <div class="view-controls">
          <button
            class="view-btn"
            :class="{ active: viewMode === 'grid' }"
            @click="viewMode = 'grid'"
            title="Grid View"
          >
            <i class="material-icons">grid_view</i>
          </button>
          <button
            class="view-btn"
            :class="{ active: viewMode === 'list' }"
            @click="viewMode = 'list'"
            title="List View"
          >
            <i class="material-icons">view_list</i>
          </button>
        </div>

        <button class="mobile-cart-toggle" @click="toggleMobileCart">
          <i class="material-icons">shopping_bag</i>
          <span class="item-count" v-if="cart.length">{{ cart.length }}</span>
        </button>
      </div>
    </div>

    <!-- Filter Controls & Product Tags (Desktop) -->
    <div class="filter-bar">
      <div class="category-pills">
        <button
          class="category-pill"
          :class="{ active: activeCategory === 'all' }"
          @click="filterByCategory('all')"
        >
          <i class="material-icons">category</i>
          All Products
        </button>
        <button
          class="category-pill"
          :class="{ active: activeCategory === 'popular' }"
          @click="filterByCategory('popular')"
        >
          <i class="material-icons">trending_up</i>
          Popular Items
        </button>
        <button
          class="category-pill"
          :class="{ active: activeCategory === 'new' }"
          @click="filterByCategory('new')"
        >
          <i class="material-icons">new_releases</i>
          New Arrivals
        </button>
        <button
          class="category-pill"
          :class="{ active: activeCategory === 'sale' }"
          @click="filterByCategory('sale')"
        >
          <i class="material-icons">local_offer</i>
          On Sale
        </button>
      </div>

      <div class="filter-stats">
        <span class="results-count">{{ filteredProducts.length }} products</span>
        <button class="refresh-btn" @click="fetchProducts" title="Refresh Products">
          <i class="material-icons">refresh</i>
        </button>
      </div>
    </div>

    <!-- Content Grid -->
    <div class="content-grid">
      <!-- Product List -->
      <div class="product-section">
        <div v-if="loading" class="loading-container">
          <div class="spinner-wrapper">
            <div class="spinner"></div>
          </div>
          <p>Loading products...</p>
        </div>

        <div v-else-if="filteredProducts.length === 0" class="no-products">
          <div class="empty-state">
            <i class="material-icons">search_off</i>
            <h3>No products found</h3>
            <p>Try adjusting your search or filters</p>
            <button class="reset-btn" @click="resetFilters">
              <i class="material-icons">refresh</i>
              Reset Filters
            </button>
          </div>
        </div>

        <div v-else :class="{'product-list': viewMode === 'grid', 'product-list-table': viewMode === 'list'}">
          <!-- Grid View -->
          <transition-group name="product-fade" v-if="viewMode === 'grid'">
            <div
              class="product-card"
              v-for="product in filteredProducts"
              :key="product.id"
              @click="showProductQuickView(product)"
            >
              <div class="card-badges">
                <span class="badge new" v-if="isNewProduct(product)">NEW</span>
                <span class="badge sale" v-if="isOnSale(product)">SALE</span>
              </div>

              <div class="product-img">
                <img :src="getProductImageUrl(product)" :alt="product.name" @error="handleImageError" />
              </div>

              <div class="product-info">
                <h4>{{ product.name }}</h4>
                <div class="price-row">
                  <p class="price">${{ product.price.toFixed(2) }}</p>
                  <div class="stock-indicator" :class="getStockClass(product)">
                    <i class="material-icons">{{ getStockIcon(product) }}</i>
                    <span class="stock-label">{{ getStockLabel(product) }}</span>
                  </div>
                </div>
              </div>

              <div class="product-actions">
                <button
                  class="btn-quick-add"
                  @click.stop="addToCart(product)"
                  :disabled="product.stock <= 0"
                >
                  <i class="material-icons">add_shopping_cart</i>
                  <span>Add to Cart</span>
                </button>
              </div>
            </div>
          </transition-group>

          <!-- List View -->
          <div class="product-table" v-if="viewMode === 'list'">
            <div class="table-header">
              <div class="col-product">Product</div>
              <div class="col-price">Price</div>
              <div class="col-stock">Stock</div>
              <div class="col-action">Action</div>
            </div>

            <transition-group name="list-fade">
              <div
                class="table-row"
                v-for="product in filteredProducts"
                :key="product.id"
              >
                <div class="col-product">
                  <div class="product-img-small">
                    <img :src="getProductImageUrl(product)" :alt="product.name" @error="handleImageError" />
                  </div>
                  <div class="product-name">
                    <h4>{{ product.name }}</h4>
                    <div class="badges-inline">
                      <span class="mini-badge new" v-if="isNewProduct(product)">NEW</span>
                      <span class="mini-badge sale" v-if="isOnSale(product)">SALE</span>
                    </div>
                  </div>
                </div>

                <div class="col-price">${{ product.price.toFixed(2) }}</div>

                <div class="col-stock">
                  <div class="stock-indicator" :class="getStockClass(product)">
                    <i class="material-icons">{{ getStockIcon(product) }}</i>
                    <span>{{ product.stock }}</span>
                  </div>
                </div>

                <div class="col-action">
                  <button
                    class="btn-list-add"
                    @click.stop="addToCart(product)"
                    :disabled="product.stock <= 0"
                  >
                    <i class="material-icons">add_shopping_cart</i>
                  </button>
                  <button class="btn-list-view" @click.stop="showProductQuickView(product)">
                    <i class="material-icons">visibility</i>
                  </button>
                </div>
              </div>
            </transition-group>
          </div>
        </div>
      </div>

      <!-- Cart Section -->
      <div class="cart-section" :class="{ 'mobile-cart-visible': isMobileCartVisible }">
        <div class="cart-header">
          <h3>
            <i class="material-icons">shopping_bag</i>
            Current Order
          </h3>
          <div class="cart-actions">
            <button class="btn-cart-action" @click="clearCart" v-if="cart.length" title="Clear Cart">
              <i class="material-icons">remove_shopping_cart</i>
            </button>
            <button class="close-cart" @click="toggleMobileCart">
              <i class="material-icons">close</i>
            </button>
          </div>
        </div>

        <div v-if="cart.length === 0" class="empty-cart">
          <i class="material-icons">shopping_cart</i>
          <h3>Your cart is empty</h3>
          <p>Add products to begin a new order</p>
          <button class="browse-products-btn" @click="focusOnProducts">Browse Products</button>
        </div>

        <div v-else class="cart-content">
          <div class="cart-items">
            <transition-group name="cart-item">
              <div class="cart-item" v-for="(item, index) in cart" :key="item.id">
                <div class="item-img">
                  <img :src="getProductImageUrl(item)" :alt="item.name" @error="handleImageError" />
                </div>
                <div class="item-details">
                  <div class="item-info">
                    <h4>{{ item.name }}</h4>
                    <p class="item-price">${{ item.price.toFixed(2) }} each</p>
                  </div>

                  <div class="item-controls">
                    <div class="quantity-controls">
                      <button
                        class="btn-quantity"
                        @click.stop="decreaseQuantity(index)"
                        :class="{ 'disabled': item.quantity <= 1 }"
                      >
                        <i class="material-icons">remove</i>
                      </button>
                      <span class="quantity">{{ item.quantity }}</span>
                      <button
                        class="btn-quantity"
                        @click.stop="increaseQuantity(index)"
                        :class="{ 'disabled': item.quantity >= item.stock }"
                      >
                        <i class="material-icons">add</i>
                      </button>
                    </div>

                    <div class="item-subtotal">
                      ${{ (item.price * item.quantity).toFixed(2) }}
                    </div>

                    <button class="btn-remove" @click.stop="removeFromCart(index)" title="Remove Item">
                      <i class="material-icons">delete</i>
                    </button>
                  </div>
                </div>
              </div>
            </transition-group>
          </div>

          <!-- Cart Summary Section -->
          <div class="cart-summary">
            <div class="order-details">
              <h4>Order Summary</h4>

              <div class="summary-rows">
                <div class="summary-row">
                  <span>Subtotal</span>
                  <span>${{ calculateSubtotal().toFixed(2) }}</span>
                </div>

                <div class="summary-row">
                  <span>Tax (7%)</span>
                  <span>${{ calculateTax().toFixed(2) }}</span>
                </div>

                <div class="summary-row discount-row">
                  <div class="discount-label">
                    <i class="material-icons">local_offer</i>
                    <span>Discount</span>
                  </div>

                  <div class="discount-selector">
                    <select
                      v-model="selectedDiscount"
                      class="discount-select"
                    >
                      <option :value="null">No discount</option>
                      <option
                        v-for="discount in discounts"
                        :key="discount.id"
                        :value="discount.id"
                      >
                        {{ discount.name }}
                        ({{ discount.discount_type === 'percentage' ? discount.value + '%' : '$' + discount.value }} off)
                      </option>
                    </select>

                    <span class="discount-amount" v-if="selectedDiscount">
                      -${{ calculateDiscountAmount().toFixed(2) }}
                    </span>
                  </div>
                </div>

                <div class="summary-row">
                  <span>Shipping</span>
                  <span>Free</span>
                </div>
              </div>

              <div class="order-total">
                <span>Total</span>
                <span>${{ calculateTotal().toFixed(2) }}</span>
              </div>
            </div>

            <button
              class="btn-checkout"
              :disabled="cart.length === 0 || processingOrder"
              @click="proceedToCheckout"
            >
              <i class="material-icons">{{ processingOrder ? 'hourglass_top' : 'shopping_cart_checkout' }}</i>
              <span>{{ processingOrder ? 'Processing...' : 'Complete Purchase' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Quick View Modal -->
    <transition name="modal">
      <div class="modal-overlay" v-if="quickViewProduct" @click="closeQuickView">
        <div class="quick-view-modal" @click.stop>
          <button class="close-modal" @click="closeQuickView">
            <i class="material-icons">close</i>
          </button>

          <div class="quick-view-content">
            <div class="modal-product-img">
              <img :src="getProductImageUrl(quickViewProduct)" :alt="quickViewProduct.name" @error="handleImageError" />
              <div class="modal-badges">
                <span class="badge new" v-if="isNewProduct(quickViewProduct)">NEW</span>
                <span class="badge sale" v-if="isOnSale(quickViewProduct)">SALE</span>
              </div>
            </div>

            <div class="modal-product-details">
              <h2>{{ quickViewProduct.name }}</h2>

              <div class="product-price-group">
                <p class="product-price">${{ quickViewProduct.price.toFixed(2) }}</p>
                <div class="stock-status" :class="getStockClass(quickViewProduct)">
                  <i class="material-icons">{{ getStockIcon(quickViewProduct) }}</i>
                  <span>{{ getStockLabel(quickViewProduct) }}</span>
                </div>
              </div>

              <div class="product-description" v-if="quickViewProduct.description">
                <h4>Description</h4>
                <p>{{ quickViewProduct.description }}</p>
              </div>

              <div class="product-category" v-if="quickViewProduct.category_id">
                <h4>Category</h4>
                <div class="category-tag">
                  <i class="material-icons">category</i>
                  <span>{{ getCategoryName(quickViewProduct.category_id) }}</span>
                </div>
              </div>

              <div class="modal-controls">
                <div class="quantity-selector">
                  <span class="quantity-label">Quantity:</span>
                  <div class="quantity-controls">
                    <button
                      class="btn-quantity"
                      @click="decreaseModalQuantity"
                      :disabled="modalQuantity <= 1"
                    >
                      <i class="material-icons">remove</i>
                    </button>
                    <span class="quantity">{{ modalQuantity }}</span>
                    <button
                      class="btn-quantity"
                      @click="increaseModalQuantity"
                      :disabled="modalQuantity >= quickViewProduct.stock"
                    >
                      <i class="material-icons">add</i>
                    </button>
                  </div>
                </div>

                <button
                  class="btn-modal-add"
                  @click="addFromModal"
                  :disabled="quickViewProduct.stock <= 0"
                >
                  <i class="material-icons">add_shopping_cart</i>
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Order Complete Modal -->
    <transition name="modal">
      <div class="modal-overlay" v-if="showOrderComplete" @click="closeOrderComplete">
        <div class="order-complete-modal" @click.stop>
          <div class="order-complete-content">
            <div class="order-success">
              <div class="success-icon">
                <i class="material-icons">check_circle</i>
              </div>
              <h2>Order Completed!</h2>
              <p>Your order has been successfully processed.</p>
            </div>

            <div class="order-summary">
              <h3>Order Summary</h3>

              <div class="order-items">
                <div class="order-item" v-for="item in orderSummary.items" :key="item.id">
                  <div class="item-name">{{ item.name }} x {{ item.quantity }}</div>
                  <div class="item-price">${{ (item.price * item.quantity).toFixed(2) }}</div>
                </div>
              </div>

              <div class="totals">
                <div class="total-row">
                  <span>Subtotal</span>
                  <span>${{ orderSummary.subtotal.toFixed(2) }}</span>
                </div>
                <div class="total-row">
                  <span>Tax</span>
                  <span>${{ orderSummary.tax.toFixed(2) }}</span>
                </div>
                <div class="total-row" v-if="orderSummary.discount > 0">
                  <span>Discount</span>
                  <span>-${{ orderSummary.discount.toFixed(2) }}</span>
                </div>
                <div class="total-row grand-total">
                  <span>Total</span>
                  <span>${{ orderSummary.total.toFixed(2) }}</span>
                </div>
              </div>
            </div>

            <div class="order-complete-actions">
              <button class="btn-continue" @click="closeOrderComplete">
                <i class="material-icons">shopping_cart</i>
                New Order
              </button>
              <button class="btn-receipt">
                <i class="material-icons">receipt</i>
                Print Receipt
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Toast Notification -->
    <transition name="toast">
      <div class="toast" v-if="toast.show" :class="toast.type">
        <i class="material-icons">{{ toast.icon }}</i>
        <div class="toast-content">
          <h4>{{ toast.title }}</h4>
          <p>{{ toast.message }}</p>
        </div>
        <button class="toast-close" @click="toast.show = false">
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
      // Products Data
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

      // Modal State
      quickViewProduct: null,
      modalQuantity: 1,
      showOrderComplete: false,
      orderSummary: {
        items: [],
        subtotal: 0,
        tax: 0,
        discount: 0,
        total: 0
      },

      // Toast Notification
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
    filteredProducts() {
      let result = [...this.products];

      // Apply search filter if there's a search term
      if (this.searchTerm) {
        const searchLower = this.searchTerm.toLowerCase();
        result = result.filter(product => {
          const nameMatch = product.name.toLowerCase().includes(searchLower);
          const descMatch = product.description && product.description.toLowerCase().includes(searchLower);
          const categoryMatch = this.getCategoryName(product.category_id).toLowerCase().includes(searchLower);
          return nameMatch || descMatch || categoryMatch;
        });
      }

      // Apply category filter
      if (this.activeCategory !== 'all') {
        switch (this.activeCategory) {
          case 'popular': { // Assuming that products with higher sales count are more popular
            result = result.filter(product => product.sales_count && product.sales_count > 5);
            result.sort((a, b) => (b.sales_count || 0) - (a.sales_count || 0));
            break;
          }

          case 'new':{ // Filter products created in the last 30 days
            const thirtyDaysAgo = new Date();
            thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
            result = result.filter(product => this.isNewProduct(product));
            break;}

          case 'sale': {// Filter products that are on sale (has discount or sale flag)
            result = result.filter(product => this.isOnSale(product));
            break;}

          default:
            // If the activeCategory matches a category ID
            if (!isNaN(parseInt(this.activeCategory))) {
              result = result.filter(product => product.category_id === parseInt(this.activeCategory));
            }
        }
      }

      return result;
    }
  },
  methods: {
    // Product Image Handling
getProductImageUrl(product) {
  if (!product) {
    console.warn('Missing product object');
    return this.getPlaceholderImage();
  }

  const imagePath = product.image_url || product.image;
  if (!imagePath){
    console.warn(`Product ${product.id} (${product.name}) has no image path`);
    return this.getPlaceholderImage();
  }

  // Handle absolute URLs (http/https)
  if (/^https?:\/\//.test(imagePath)) {
    return imagePath;
  }

  const backendBase = process.env.VUE_APP_API_BASE || 'http://localhost:5000';

  // Normalize the path - remove leading/trailing slashes
  const cleanPath = imagePath.replace(/^\/+|\/+$/g, '');

  // Determine the correct base path
  let finalPath;

  if (cleanPath.startsWith('static/')) {
    // If path already includes static, use as-is
    finalPath = cleanPath;
  } else if (cleanPath.startsWith('product_images/')) {
    // If path starts with product_images, add static prefix
    finalPath = `static/${cleanPath}`;
  } else {
    // Default case - assume it's a product image
    finalPath = `static/product_images/${cleanPath}`;
  }

  // Add cache-busting parameter
  return `${backendBase}/${finalPath}?t=${Date.now()}`;
},

    handleImageError(e) {
      // Replace with placeholder image
      e.target.src = this.getPlaceholderImage();
    },

    getPlaceholderImage() {
      return 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlOWVjZWYiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIyNCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZvbnQtZmFtaWx5PSJzYW5zLXNlcmlmIiBmaWxsPSIjNmM3NTdkIj5ObyBJbWFnZTwvdGV4dD48cGF0aCBkPSJNODAgOTAgTDEyMCAxMzAgTTE2MCA5MCBMODAgMTcwIiBzdHJva2U9IiM2Yzc1N2QiIHN0cm9rZS13aWR0aD0iMyIvPjwvc3ZnPg==';
    },

    // Product Display Helpers
    isNewProduct(product) {
      if (!product || !product.created_at) return false;

      // Check if the product was created within the last 30 days
      const createdDate = new Date(product.created_at);
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

      return createdDate > thirtyDaysAgo;
    },

    isOnSale(product) {
      // Check if the product is marked as on sale or has a discount
      return product.on_sale || product.discount_price;
    },

    getStockClass(product) {
      if (product.stock <= 0) return 'out-of-stock';
      if (product.stock < 10) return 'low-stock';
      return 'in-stock';
    },

    getStockIcon(product) {
      if (product.stock <= 0) return 'inventory_2';
      if (product.stock < 10) return 'inventory';
      return 'inventory';
    },

    getStockLabel(product) {
      if (product.stock <= 0) return 'Out of Stock';
      if (product.stock < 10) return 'Low Stock';
      return 'In Stock';
    },

    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId);
      return category ? category.name : 'Uncategorized';
    },

    // Data Fetching
    async fetchProducts() {
      this.loading = true;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/products');

        if (response.ok) {
          const data = await response.json();
          this.products = data;

          // Try to restore the cart from localStorage
          this.restoreCartFromStorage();
        } else {
          this.showToast('Error', 'Failed to load products. Please try again.', 'error');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        this.showToast('Network Error', 'Could not connect to the server. Please check your connection.', 'error');
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
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },

    async fetchDiscounts() {
      this.discountLoading = true;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/discounts');

        if (response.ok) {
          this.discounts = await response.json();
        } else {
          console.error('Failed to load discounts');
        }
      } catch (error) {
        console.error('Error loading discounts:', error);
      } finally {
        this.discountLoading = false;
      }
    },

    // Search and Filtering
    searchProducts() {
      // Already handled in the filteredProducts computed property
    },

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

    // Cart Operations
    addToCart(product) {
      if (product.stock <= 0) return;

      // Check if product is already in cart
      const existingIndex = this.cart.findIndex(item => item.id === product.id);

      if (existingIndex >= 0) {
        // Increase quantity if product already in cart
        if (this.cart[existingIndex].quantity < product.stock) {
          this.cart[existingIndex].quantity++;
          this.showToast('Updated Cart', `Increased ${product.name} quantity.`, 'success');
        } else {
          this.showToast('Maximum Reached', `You've reached the maximum available stock for ${product.name}.`, 'warning');
        }
      } else {
        // Add new product to cart
        this.cart.push({
          ...product,
          quantity: 1
        });
        this.showToast('Added to Cart', `${product.name} has been added to your cart.`, 'success');
      }

      // Save cart to localStorage
      this.saveCartToStorage();
    },

    removeFromCart(index) {
      const removedItem = this.cart[index];
      this.cart.splice(index, 1);
      this.showToast('Removed from Cart', `${removedItem.name} has been removed from your cart.`, 'success');

      // Save cart to localStorage
      this.saveCartToStorage();
    },

    increaseQuantity(index) {
      const item = this.cart[index];
      if (item.quantity < item.stock) {
        item.quantity++;
        this.saveCartToStorage();
      }
    },

    decreaseQuantity(index) {
      const item = this.cart[index];
      if (item.quantity > 1) {
        item.quantity--;
        this.saveCartToStorage();
      }
    },

    clearCart() {
      this.cart = [];
      localStorage.removeItem('peak_pos_cart');
      this.showToast('Cart Cleared', 'All items have been removed from your cart.', 'success');
    },

    saveCartToStorage() {
      localStorage.setItem('peak_pos_cart', JSON.stringify(this.cart));
    },

    restoreCartFromStorage() {
      const savedCart = localStorage.getItem('peak_pos_cart');
      if (savedCart) {
        try {
          // Parse the saved cart
          const parsedCart = JSON.parse(savedCart);

          // Make sure all items in the cart still exist and have valid stock
          this.cart = parsedCart.filter(item => {
            const currentProduct = this.products.find(p => p.id === item.id);
            if (!currentProduct) return false;

            // Update the cart item with current product data
            item.price = currentProduct.price;
            item.stock = currentProduct.stock;

            // Adjust quantity if it exceeds current stock
            if (item.quantity > currentProduct.stock) {
              item.quantity = Math.max(1, currentProduct.stock);
            }

            return true;
          });

          // If cart items were filtered out, save the updated cart
          if (parsedCart.length !== this.cart.length) {
            this.saveCartToStorage();
          }
        } catch (e) {
          console.error('Error restoring cart:', e);
          localStorage.removeItem('peak_pos_cart');
        }
      }
    },

    // Mobile Cart Toggle
    toggleMobileCart() {
      this.isMobileCartVisible = !this.isMobileCartVisible;
      if (this.isMobileCartVisible) {
        document.body.classList.add('mobile-cart-open');
      } else {
        document.body.classList.remove('mobile-cart-open');
      }
    },

    focusOnProducts() {
      this.isMobileCartVisible = false;
      document.body.classList.remove('mobile-cart-open');
    },

    // Cart Calculations
    calculateSubtotal() {
      return this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },

    calculateTax() {
      return this.calculateSubtotal() * 0.07; // 7% tax
    },

    calculateDiscountAmount() {
      if (!this.selectedDiscount) return 0;

      const discount = this.discounts.find(d => d.id === this.selectedDiscount);
      if (!discount) return 0;

      const subtotal = this.calculateSubtotal();

      if (discount.discount_type === 'percentage') {
        return subtotal * (discount.value / 100);
      } else {
        // Fixed amount discount
        return Math.min(subtotal, discount.value); // Don't discount more than the subtotal
      }
    },

    calculateTotal() {
      const subtotal = this.calculateSubtotal();
      const tax = this.calculateTax();
      const discount = this.calculateDiscountAmount();

      return subtotal + tax - discount;
    },

    // Product Quick View
    showProductQuickView(product) {
      this.quickViewProduct = product;
      this.modalQuantity = 1;
    },

    closeQuickView() {
      this.quickViewProduct = null;
    },

    increaseModalQuantity() {
      if (this.modalQuantity < this.quickViewProduct.stock) {
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

      // Check if product is already in cart
      const existingIndex = this.cart.findIndex(item => item.id === this.quickViewProduct.id);

      if (existingIndex >= 0) {
        // Update quantity if already in cart
        const newQuantity = this.cart[existingIndex].quantity + this.modalQuantity;

        if (newQuantity <= this.quickViewProduct.stock) {
          this.cart[existingIndex].quantity = newQuantity;
          this.showToast('Updated Cart', `Added ${this.modalQuantity} more ${this.quickViewProduct.name} to your cart.`, 'success');
        } else {
          this.showToast('Maximum Reached', `You can only add ${this.quickViewProduct.stock - this.cart[existingIndex].quantity} more of this item.`, 'warning');
          return;
        }
      } else {
        // Add new product to cart
        this.cart.push({
          ...this.quickViewProduct,
          quantity: this.modalQuantity
        });
        this.showToast('Added to Cart', `${this.modalQuantity} ${this.quickViewProduct.name} added to your cart.`, 'success');
      }

      // Save cart to localStorage
      this.saveCartToStorage();

      // Close the modal
      this.closeQuickView();
    },

    // Checkout Process
    async proceedToCheckout() {
      if (this.cart.length === 0 || this.processingOrder) return;

      this.processingOrder = true;

      try {
        // Prepare order data
        const orderData = {
          items: this.cart.map(item => ({
            product_id: item.id,
            quantity: item.quantity,
            price: item.price
          })),
          discount_id: this.selectedDiscount,
          subtotal: this.calculateSubtotal(),
          tax: this.calculateTax(),
          total: this.calculateTotal()
        };

        // Send the order to the backend
        const response = await fetch('http://127.0.0.1:5000/api/orders', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(orderData)
        });

        if (!response.ok) {
          throw new Error('Failed to process order');
        }

        // Process successful order
        const orderResponse = await response.json();

        // Store order summary for receipt
        this.orderSummary = {
          items: [...this.cart],
          subtotal: this.calculateSubtotal(),
          tax: this.calculateTax(),
          discount: this.calculateDiscountAmount(),
          total: this.calculateTotal(),
          order_id: orderResponse.id
        };

        // Show success modal
        this.showOrderComplete = true;

        // Clear the cart
        this.cart = [];
        localStorage.removeItem('peak_pos_cart');

      } catch (error) {
        console.error('Error processing order:', error);
        this.showToast('Order Error', 'Failed to process your order. Please try again.', 'error');
      } finally {
        this.processingOrder = false;
      }
    },

    closeOrderComplete() {
      this.showOrderComplete = false;
      // Reset discount too
      this.selectedDiscount = null;
    },

    // Toast Notifications
    showToast(title, message, type = 'success') {
      // Clear any existing timeout
      if (this.toast.timeout) {
        clearTimeout(this.toast.timeout);
      }

      // Set icon based on type
      let icon = 'check_circle';
      if (type === 'error') icon = 'error';
      else if (type === 'warning') icon = 'warning';
      else if (type === 'info') icon = 'info';

      // Update toast data
      this.toast = {
        show: true,
        type,
        title,
        message,
        icon,
        timeout: null
      };

      // Auto-hide after 4 seconds
      this.toast.timeout = setTimeout(() => {
        this.toast.show = false;
      }, 4000);
    }
  },
  created() {
    // Store the view mode preference
    this.$watch('viewMode', (newMode) => {
      localStorage.setItem('salesViewMode', newMode);
    });

    // Fetch data when the component is created
    this.fetchProducts();
    this.fetchCategories();
    this.fetchDiscounts();
  },
  mounted() {
    // Add keyboard shortcuts for common actions
    document.addEventListener('keydown', (e) => {
      // ESC to close modals
      if (e.key === 'Escape') {
        if (this.quickViewProduct) this.closeQuickView();
        if (this.showOrderComplete) this.closeOrderComplete();
        if (this.isMobileCartVisible) this.toggleMobileCart();
      }
    });
  },
  beforeUnmount() {
    // Clean up by removing the mobile cart open class
    document.body.classList.remove('mobile-cart-open');

    // Remove keyboard event listeners
    document.removeEventListener('keydown', this.handleKeyDown);
  }
};
</script>

<style scoped>
.sales-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--background-color-body, #f8fafc);
  color: var(--text-color-primary, #1e293b);
}

/* Top Action Bar */
.sales-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: var(--background-color-primary, white);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  z-index: 10;
}

.page-title {
  display: flex;
  flex-direction: column;
}

.page-title h2 {
  margin: 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-title .subtitle {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
}

.action-controls {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-control {
  position: relative;
  width: 320px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-color-secondary, #64748b);
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 38px;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 8px;
  font-size: 0.875rem;
  background-color: var(--background-color-primary, white);
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color, #4f46e5);
}

.clear-search {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--text-color-secondary, #64748b);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view-controls {
  display: flex;
  gap: 8px;
}

.view-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-color-secondary, #f8fafc);
  border: none;
  color: var(--text-color-secondary, #64748b);
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-btn.active {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.view-btn:hover:not(.active) {
  background-color: var(--border-color, #e2e8f0);
}

.mobile-cart-toggle {
  display: none;
  position: relative;
  background-color: var(--primary-color, #4f46e5);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  align-items: center;
  justify-content: center;
}

.mobile-cart-toggle .item-count {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: var(--danger-color, #ef4444);
  color: white;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Filter Bar */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background-color: var(--background-color-primary, white);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.category-pills {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
  scrollbar-width: thin;
}

.category-pills::-webkit-scrollbar {
  height: 4px;
}

.category-pills::-webkit-scrollbar-thumb {
  background-color: var(--border-color, #e2e8f0);
  border-radius: 4px;
}

.category-pill {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid var(--border-color, #e2e8f0);
  background-color: var(--background-color-primary, white);
  color: var(--text-color-secondary, #64748b);
  font-size: 0.875rem;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-pill.active {
  background-color: var(--primary-color, #4f46e5);
  border-color: var(--primary-color, #4f46e5);
  color: white;
}

.category-pill:hover:not(.active) {
  background-color: var(--background-color-secondary, #f8fafc);
}

.filter-stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.results-count {
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
}

.refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

/* Content Grid */
.content-grid {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.product-section {
  flex: 3;
  overflow-y: auto;
  padding: 24px;
}

.cart-section {
  flex: 1.2;
  background-color: var(--background-color-primary, white);
  border-left: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  flex-direction: column;
  max-width: 380px;
  transition: transform 0.3s ease;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
}

.spinner-wrapper {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.spinner {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 3px solid rgba(var(--primary-color, #4f46e5), 0.1);
  border-top-color: var(--primary-color, #4f46e5);
  animation: spinner 0.8s linear infinite;
}

@keyframes spinner {
  to {
    transform: rotate(360deg);
  }
}

/* Empty State */
.no-products {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 320px;
}

.empty-state i {
  font-size: 48px;
  color: var(--text-color-secondary, #64748b);
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  color: var(--text-color-primary, #1e293b);
}

.empty-state p {
  margin: 0 0 20px 0;
  color: var(--text-color-secondary, #64748b);
}

.reset-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background-color: var(--primary-color, #4f46e5);
  color: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-btn:hover {
  background-color: var(--primary-color-dark, #4338ca);
}

/* Product Grid View */
.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 24px;
}

.product-card {
  background-color: var(--background-color-primary, white);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.card-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  gap: 8px;
  z-index: 5;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.new {
  background-color: var(--success-color, #10b981);
  color: white;
}

.badge.sale {
  background-color: var(--danger-color, #ef4444);
  color: white;
}

.product-img {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-color-secondary, #f8fafc);
  overflow: hidden;
}

.product-img img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.product-card:hover .product-img img {
  transform: scale(1.05);
}

.product-info {
  padding: 16px;
}

.product-info h4 {
  margin: 0 0 8px 0;
  font-size: 1rem;
  color: var(--text-color-primary, #1e293b);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  height: 40px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.stock-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
}

.stock-indicator.in-stock {
  color: var(--success-color, #10b981);
}

.stock-indicator.low-stock {
  color: var(--warning-color, #f59e0b);
}

.stock-indicator.out-of-stock {
  color: var(--danger-color, #ef4444);
}

.stock-indicator i {
  font-size: 14px;
}

.stock-label {
  display: none;
}

.product-actions {
  padding: 0 16px 16px;
}

.btn-quick-add {
  width: 100%;
  padding: 8px 0;
  border-radius: 8px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: var(--primary-color, #4f46e5);
  color: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-quick-add:hover:not(:disabled) {
  background-color: var(--primary-color-dark, #4338ca);
}

.btn-quick-add:disabled {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-secondary, #64748b);
  cursor: not-allowed;
}

/* Product List View */
.product-list-table {
  padding: 0;
}

.product-table {
  background-color: var(--background-color-primary, white);
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 3fr 1fr 1fr 1fr;
  padding: 12px 16px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  font-weight: 600;
  color: var(--text-color-secondary, #64748b);
}

.table-row {
  display: grid;
  grid-template-columns: 3fr 1fr 1fr 1fr;
  padding: 12px 16px;
  align-items: center;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  transition: background-color 0.2s ease;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background-color: var(--background-color-secondary, #f8fafc);
}

.col-product {
  display: flex;
  align-items: center;
  gap: 16px;
}

.product-img-small {
  width: 60px;
  height: 60px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-img-small img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.product-name {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-name h4 {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-color-primary, #1e293b);
}

.badges-inline {
  display: flex;
  gap: 4px;
}

.mini-badge {
  font-size: 0.6875rem;
  padding: 2px 6px;
  border-radius: 4px;
}

.mini-badge.new {
  background-color: var(--success-color, #10b981);
  color: white;
}

.mini-badge.sale {
  background-color: var(--danger-color, #ef4444);
  color: white;
}

.col-price {
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
}

.col-action {
  display: flex;
  gap: 8px;
}

.btn-list-add,
.btn-list-view {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-list-add {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.btn-list-view {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
}

.btn-list-add:hover:not(:disabled) {
  background-color: var(--primary-color-dark, #4338ca);
}

.btn-list-view:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

.btn-list-add:disabled {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-secondary, #64748b);
  cursor: not-allowed;
}

/* Cart Section */
.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  background-color: var(--background-color-primary, white);
}

.cart-header h3 {
  margin: 0;
  font-size: 1.125rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.cart-actions {
  display: flex;
  gap: 8px;
}

.btn-cart-action {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: none;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cart-action:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

.close-cart {
  display: none;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
  flex-grow: 1;
}

.empty-cart i {
  font-size: 48px;
  color: var(--text-color-secondary, #64748b);
  margin-bottom: 16px;
}

.empty-cart h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
  color: var(--text-color-primary, #1e293b);
}

.empty-cart p {
  margin: 0 0 20px 0;
  color: var(--text-color-secondary, #64748b);
}

.browse-products-btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  background-color: var(--primary-color, #4f46e5);
  color: white;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.browse-products-btn:hover {
  background-color: var(--primary-color-dark, #4338ca);
}

.cart-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: hidden;
  height: 100%; /* Add this */
}

.cart-items {
  flex-grow: 1;
  overflow-y: auto;
  padding: 8px 0;
  min-height: 0; /* Important for flex children to scroll properly */
}

.cart-item {
  display: flex;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  transition: background-color 0.2s ease;
}

.cart-item:hover {
  background-color: var(--background-color-secondary, #f8fafc);
}

.item-img {
  width: 60px;
  height: 60px;
  background-color: var(--background-color-secondary, #f8fafc);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.item-img img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.item-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-info h4 {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-color-primary, #1e293b);
}

.item-price {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
}

.item-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.btn-quantity {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color, #e2e8f0);
  background-color: var(--background-color-primary, white);
  color: var(--text-color-secondary, #64748b);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-quantity:hover:not(.disabled) {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-primary, #1e293b);
}

.btn-quantity.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity {
  width: 24px;
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-color-primary, #1e293b);
}

.item-subtotal {
  font-weight: 600;
  font-size: 0.9375rem;
  color: var(--text-color-primary, #1e293b);
}

.btn-remove {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background-color: transparent;
  color: var(--danger-color, #ef4444);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-remove:hover {
  background-color: var(--danger-color-light, #fee2e2);
}

.cart-summary {
  padding: 16px;
  background-color: var(--background-color-primary, white);
  border-top: 1px solid var(--border-color, #e2e8f0);
  flex-shrink: 0; /* Prevent summary from shrinking */
  min-height: 200px; /* Adjust as needed */
}

.order-details h4 {
  margin: 0 0 12px 0;
  font-size: 1rem;
  color: var(--text-color-primary, #1e293b);
}

.summary-rows {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
}

.discount-row {
  align-items: flex-start;
}

.discount-label {
  display: flex;
  align-items: center;
  gap: 4px;
}

.discount-selector {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.discount-select {
  font-size: 0.875rem;
  padding: 4px 8px;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 6px;
  background-color: var(--background-color-primary, white);
  color: var(--text-color-primary, #1e293b);
  max-width: 200px;
}

.discount-amount {
  font-size: 0.875rem;
  color: var(--danger-color, #ef4444);
  font-weight: 500;
}

.order-total {
  display: flex;
  justify-content: space-between;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
  padding-top: 12px;
  border-top: 1px solid var(--border-color, #e2e8f0);
  margin-bottom: 20px;
}

.btn-checkout {
  width: 100%;
  padding: 12px 0;
  border-radius: 8px;
  border: none;
  background-color: var(--success-color, #10b981);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-checkout:hover:not(:disabled) {
  background-color: #0d9488;
}

.btn-checkout:disabled {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-secondary, #64748b);
  cursor: not-allowed;
}

/* Modals */
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
  z-index: 100;
}

/* Product Quick View Modal */
.quick-view-modal {
  background-color: var(--background-color-primary, white);
  width: 90%;
  max-width: 800px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
}

.close-modal {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-color-secondary, #f8fafc);
  border: none;
  color: var(--text-color-secondary, #64748b);
  cursor: pointer;
  z-index: 5;
  transition: all 0.2s ease;
}

.close-modal:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

.quick-view-content {
  display: flex;
  max-height: 80vh;
}

.modal-product-img {
  flex: 1;
  padding: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-color-secondary, #f8fafc);
  position: relative;
  overflow: hidden;
}

.modal-product-img img {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
}

.modal-badges {
  position: absolute;
  top: 16px;
  left: 16px;
  display: flex;
  gap: 8px;
}

.modal-product-details {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}

.modal-product-details h2 {
  margin: 0 0 16px 0;
  font-size: 1.5rem;
  color: var(--text-color-primary, #1e293b);
}

.product-price-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.product-price {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
  margin: 0;
}

.stock-status {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.875rem;
  padding: 4px 10px;
  border-radius: 16px;
}

.stock-status.in-stock {
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success-color, #10b981);
}

.stock-status.low-stock {
  background-color: rgba(245, 158, 11, 0.1);
  color: var(--warning-color, #f59e0b);
}

.stock-status.out-of-stock {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--danger-color, #ef4444);
}

.product-description,
.product-category {
  margin-bottom: 24px;
}

.product-description h4,
.product-category h4 {
  margin: 0 0 8px 0;
  font-size: 1rem;
  color: var(--text-color-primary, #1e293b);
}

.product-description p {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-color-secondary, #64748b);
  line-height: 1.5;
}

.category-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 16px;
  background-color: var(--background-color-secondary, #f8fafc);
  font-size: 0.875rem;
  color: var(--text-color-secondary, #64748b);
}

.modal-controls {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-label {
  font-size: 0.9375rem;
  color: var(--text-color-primary, #1e293b);
}

.btn-modal-add {
  padding: 12px 0;
  border-radius: 8px;
  border: none;
  background-color: var(--primary-color, #4f46e5);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-modal-add:hover:not(:disabled) {
  background-color: var(--primary-color-dark, #4338ca);
}

.btn-modal-add:disabled {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-secondary, #64748b);
  cursor: not-allowed;
}

/* Order Complete Modal */
.order-complete-modal {
  background-color: var(--background-color-primary, white);
  width: 90%;
  max-width: 500px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.order-complete-content {
  padding: 32px;
}

.order-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 24px;
}

.success-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: var(--success-color-light, #d1fae5);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.success-icon i {
  font-size: 32px;
  color: var(--success-color, #10b981);
}

.order-success h2 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  color: var(--text-color-primary, #1e293b);
}

.order-success p {
  margin: 0;
  color: var(--text-color-secondary, #64748b);
}

.order-summary {
  margin-bottom: 24px;
}

.order-summary h3 {
  margin: 0 0 16px 0;
  font-size: 1.125rem;
  color: var(--text-color-primary, #1e293b);
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.9375rem;
}

.item-name {
  color: var(--text-color-secondary, #64748b);
}

.item-price {
  font-weight: 500;
  color: var(--text-color-primary, #1e293b);
}

.totals {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9375rem;
  color: var(--text-color-secondary, #64748b);
}

.grand-total {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-color-primary, #1e293b);
  padding-top: 8px;
  margin-top: 8px;
  border-top: 1px solid var(--border-color, #e2e8f0);
}

.order-complete-actions {
  display: flex;
  gap: 12px;
}

.btn-continue,
.btn-receipt {
  flex: 1;
  padding: 10px 0;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-continue {
  background-color: var(--primary-color, #4f46e5);
  color: white;
  border: none;
}

.btn-receipt {
  background-color: var(--background-color-secondary, #f8fafc);
  color: var(--text-color-secondary, #64748b);
  border: 1px solid var(--border-color, #e2e8f0);
}

.btn-continue:hover {
  background-color: var(--primary-color-dark, #4338ca);
}

.btn-receipt:hover {
  background-color: var(--border-color, #e2e8f0);
  color: var(--text-color-primary, #1e293b);
}

/* Toast Notification */
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 350px;
  z-index: 200;
}

.toast.success {
  background-color: var(--success-color, #10b981);
  color: white;
}

.toast.error {
  background-color: var(--danger-color, #ef4444);
  color: white;
}

.toast.warning {
  background-color: var(--warning-color, #f59e0b);
  color: white;
}

.toast.info {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.toast i {
  font-size: 24px;
}

.toast-content {
  flex: 1;
}

.toast-content h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
}

.toast-content p {
  margin: 0;
  font-size: 0.875rem;
  opacity: 0.9;
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

/* Animations */
.product-fade-enter-active,
.product-fade-leave-active,
.list-fade-enter-active,
.list-fade-leave-active,
.cart-item-enter-active,
.cart-item-leave-active,
.modal-enter-active,
.modal-leave-active,
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.product-fade-enter-from,
.product-fade-leave-to,
.list-fade-enter-from,
.list-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.cart-item-enter-from,
.cart-item-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .quick-view-modal,
.modal-enter-from .order-complete-modal {
  transform: scale(0.9);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* Responsive Styles */
@media (max-width: 1200px) {
  .cart-section {
    max-width: 320px;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

}

@media (max-width: 1024px) {
  .quick-view-content {
    flex-direction: column;
  }

  .modal-product-img {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .search-control {
    width: 200px;
  }

  .sales-action-bar {
    padding: 12px 16px;
  }

  .filter-bar {
    padding: 8px 16px;
  }

  .product-section {
    padding: 16px;
  }

  .cart-section {
    position: fixed;
    top: 0;
    right: 0;
    height: 100%;
    width: 100%;
    max-width: 100%;
    transform: translateX(100%);
    z-index: 50;
  }

  .mobile-cart-visible {
    transform: translateX(0);
  }

  .mobile-cart-toggle,
  .close-cart {
    display: flex;
  }

  .content-grid {
    display: block;
  }
}

@media (max-width: 640px) {
  .page-title {
    margin-bottom: 12px;
  }

  .sales-action-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-controls {
    width: 100%;
    justify-content: space-between;
  }

  .search-control {
    width: 100%;
    max-width: none;
  }

  .view-controls {
    margin-left: auto;
  }

  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
  }

  .product-img {
    height: 140px;
  }

  .product-info h4 {
    font-size: 0.875rem;
  }

  .order-complete-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .filter-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .filter-stats {
    width: 100%;
    justify-content: space-between;
  }

  .category-pills {
    width: 100%;
  }

  .quick-view-modal {
    height: 90vh;
    width: 95%;
  }

  .modal-product-img {
    height: 200px;
  }

  .modal-product-details {
    padding: 16px;
  }
}
</style>