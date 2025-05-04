<template>
  <div class="sales-view">
    <!-- Top Action Bar -->
    <div class="sales-action-bar">
      <div class="page-title">
        <h2><i class="material-icons">point_of_sale</i> Sales</h2>
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
          <i class="material-icons">shopping_cart</i>
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
        <button class="refresh-btn" @click="loadProducts" title="Refresh Products">
          <i class="material-icons">refresh</i>
        </button>
      </div>
    </div>

    <!-- Content Grid -->
    <div class="content-grid">
      <!-- Product List -->
      <div class="product-section">
        <div v-if="isLoading" class="loading-container">
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
                <img :src="product.image" :alt="product.name" />
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
                    <img :src="product.image" :alt="product.name" />
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

      <!-- Enhanced Cart Section -->
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
                  <img :src="item.image" :alt="item.name" />
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

                    <button class="btn-remove" @click.stop="removeItem(index)" title="Remove Item">
                      <i class="material-icons">delete</i>
                    </button>
                  </div>
                </div>
              </div>
            </transition-group>
          </div>

          <!-- Enhanced Cart Summary -->
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
                      v-model="selectedDiscountId"
                      class="discount-select"
                    >
                      <option :value="null">No discount</option>
                      <option
                        v-for="discount in availableDiscounts"
                        :key="discount.id"
                        :value="discount.id"
                      >
                        {{ discount.name }} ({{ discount.percent }}% off)
                      </option>
                    </select>

                    <span class="discount-amount" v-if="selectedDiscountId">
                      -${{ calculateDiscountAmount().toFixed(2) }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="order-total">
                <span>Total</span>
                <span class="total-amount">${{ calculateTotal().toFixed(2) }}</span>
              </div>

              <button
                class="btn-checkout"
                @click="placeOrder"
                :disabled="cart.length === 0"
              >
                <i class="material-icons">payment</i>
                <span>Complete Order</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Quick View Modal -->
    <div class="product-modal" v-if="selectedProduct" @click.self="closeQuickView">
      <div class="modal-content">
        <button class="close-modal" @click="closeQuickView">
          <i class="material-icons">close</i>
        </button>

        <div class="modal-grid">
          <div class="product-image-large">
            <img :src="selectedProduct.image" :alt="selectedProduct.name">
          </div>

          <div class="product-details">
            <h2>{{ selectedProduct.name }}</h2>

            <div class="pricing-row">
              <div class="product-price">
                <span class="current-price">${{ selectedProduct.price.toFixed(2) }}</span>
                <span class="original-price" v-if="isOnSale(selectedProduct)">${{ (selectedProduct.price * 1.2).toFixed(2) }}</span>
              </div>

              <div class="badges">
                <span class="badge new" v-if="isNewProduct(selectedProduct)">NEW</span>
                <span class="badge sale" v-if="isOnSale(selectedProduct)">SALE</span>
              </div>
            </div>

            <div class="inventory-status">
              <div class="stock-indicator modal-stock" :class="getStockClass(selectedProduct)">
                <i class="material-icons">{{ getStockIcon(selectedProduct) }}</i>
                <span>{{ getStockLabel(selectedProduct) }}</span>
              </div>
              <p class="stock-count">{{ selectedProduct.stock }} units available</p>
            </div>

            <div class="product-description">
              <p>{{ getProductDescription(selectedProduct) }}</p>
            </div>

            <div class="quick-view-actions">
              <div class="quantity-selector">
                <button
                  class="qty-btn"
                  @click="decreaseModalQuantity"
                  :disabled="modalQuantity <= 1"
                >
                  <i class="material-icons">remove</i>
                </button>
                <input type="number" v-model="modalQuantity" min="1" :max="selectedProduct.stock">
                <button
                  class="qty-btn"
                  @click="increaseModalQuantity"
                  :disabled="modalQuantity >= selectedProduct.stock"
                >
                  <i class="material-icons">add</i>
                </button>
              </div>

              <button
                class="add-to-cart-btn"
                @click="addToCartFromModal"
                :disabled="selectedProduct.stock <= 0"
              >
                <i class="material-icons">add_shopping_cart</i>
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Cart Overlay -->
    <div
      v-if="isMobileCartVisible"
      class="mobile-cart-overlay"
      @click="toggleMobileCart"
    ></div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted} from 'vue';

export default {
  name: 'SalesView',
  setup() {
    // State variables
    const searchTerm = ref('');
    const products = ref([]);
    const cart = ref([]);
    const filteredProducts = ref([]);
    const availableDiscounts = ref([]);
    const selectedDiscountId = ref(null);
    const isLoading = ref(true);
    const isMobileCartVisible = ref(false);
    const viewMode = ref('grid'); // 'grid' or 'list'
    const activeCategory = ref('all');
    const selectedProduct = ref(null);
    const modalQuantity = ref(1);

    const apiBaseUrl = "http://127.0.0.1:5000/api";

    // Load products from API
    const loadProducts = async () => {
      isLoading.value = true;
      try {
        const response = await axios.get(`${apiBaseUrl}/products`);
        // Enhance products with additional properties for UI display
        products.value = response.data.map(product => ({
          ...product,
          isNew: Math.random() > 0.7, // Simulate new products
          isOnSale: Math.random() > 0.7, // Simulate sale products
          isPopular: Math.random() > 0.5, // Simulate popular products
          description: getProductDescription(product)
        }));
        applyFilters();
      } catch (error) {
        console.error("Failed to load products:", error);
        // Show error notification
      } finally {
        isLoading.value = false;
      }
    };

    // Fetch available discounts
    const fetchDiscounts = async () => {
      try {
        const response = await axios.get(`${apiBaseUrl}/discounts`);
        availableDiscounts.value = response.data;
      } catch (error) {
        console.error("Failed to fetch discounts:", error);
      }
    };

    // Apply all active filters and search
    const applyFilters = () => {
      let result = [...products.value];

      // Apply category filter
      if (activeCategory.value !== 'all') {
        if (activeCategory.value === 'new') {
          result = result.filter(p => p.isNew);
        } else if (activeCategory.value === 'sale') {
          result = result.filter(p => p.isOnSale);
        } else if (activeCategory.value === 'popular') {
          result = result.filter(p => p.isPopular);
        }
      }

      // Apply search filter
      if (searchTerm.value) {
        const term = searchTerm.value.toLowerCase();
        result = result.filter(product =>
          product.name.toLowerCase().includes(term)
        );
      }

      filteredProducts.value = result;
    };

    // Search products
    const searchProducts = () => {
      applyFilters();
    };

    const clearSearch = () => {
      searchTerm.value = '';
      applyFilters();
    };

    const resetFilters = () => {
      searchTerm.value = '';
      activeCategory.value = 'all';
      applyFilters();
    };

    const filterByCategory = (category) => {
      activeCategory.value = category;
      applyFilters();
    };

    // Cart operations
    const addToCart = (product) => {
      if (product.stock <= 0) return;

      const existingItem = cart.value.find(item => item.id === product.id);
      if (existingItem) {
        increaseQuantity(cart.value.indexOf(existingItem));
      } else {
        cart.value.push({ ...product, quantity: 1 });
      }
    };

    const increaseQuantity = (index) => {
      const product = products.value.find(p => p.id === cart.value[index].id);
      if (cart.value[index].quantity < product.stock) {
        cart.value[index].quantity++;
      }
    };

    const decreaseQuantity = (index) => {
      if (cart.value[index].quantity > 1) {
        cart.value[index].quantity--;
      } else {
        removeItem(index);
      }
    };

    const removeItem = (index) => {
      cart.value.splice(index, 1);
    };

    const clearCart = () => {
      if (confirm('Are you sure you want to clear the entire cart?')) {
        cart.value = [];
        selectedDiscountId.value = null;
      }
    };

    // Calculations
    const calculateSubtotal = () => {
      return cart.value.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    };

    const calculateTax = () => {
      return calculateSubtotal() * 0.07;
    };

    const calculateDiscountAmount = () => {
      if (!selectedDiscountId.value) return 0;

      const selectedDiscount = availableDiscounts.value.find(
        d => d.id === selectedDiscountId.value
      );

      const discountPercent = selectedDiscount ? selectedDiscount.percent : 0;
      return calculateSubtotal() * (discountPercent / 100);
    };

    const calculateTotal = () => {
      const subtotal = calculateSubtotal();
      const tax = calculateTax();
      const discountAmount = calculateDiscountAmount();

      return subtotal + tax - discountAmount;
    };

    // Stock and badge display
    const isNewProduct = (product) => {
      return product.isNew;
    };

    const isOnSale = (product) => {
      return product.isOnSale;
    };

    const getStockClass = (product) => {
      if (product.stock <= 0) return 'out-of-stock';
      if (product.stock < 5) return 'low-stock';
      return 'in-stock';
    };

    const getStockIcon = (product) => {
      if (product.stock <= 0) return 'cancel';
      if (product.stock < 5) return 'error_outline';
      return 'check_circle';
    };

    const getStockLabel = (product) => {
      if (product.stock <= 0) return 'Out of Stock';
      if (product.stock < 5) return 'Low Stock';
      return 'In Stock';
    };

    // Product Quick View Modal
    const showProductQuickView = (product) => {
      selectedProduct.value = product;
      modalQuantity.value = 1;
    };

    const closeQuickView = () => {
      selectedProduct.value = null;
    };

    const addToCartFromModal = () => {
      if (!selectedProduct.value || selectedProduct.value.stock <= 0) return;

      const product = selectedProduct.value;
      const existingItem = cart.value.find(item => item.id === product.id);

      if (existingItem) {
        const index = cart.value.indexOf(existingItem);
        // Add the modal quantity to the existing quantity, but not exceeding stock
        const newQuantity = Math.min(existingItem.quantity + modalQuantity.value, product.stock);
        cart.value[index].quantity = newQuantity;
      } else {
        cart.value.push({ ...product, quantity: modalQuantity.value });
      }

      closeQuickView();
    };

    const increaseModalQuantity = () => {
      if (selectedProduct.value && modalQuantity.value < selectedProduct.value.stock) {
        modalQuantity.value++;
      }
    };

    const decreaseModalQuantity = () => {
      if (modalQuantity.value > 1) {
        modalQuantity.value--;
      }
    };

    // Helper functions
    const getProductDescription = (product) => {
      // Generate a placeholder description if none exists
      return product.description || `${product.name} - High-quality product available for immediate purchase. Perfect for all your needs with excellent durability and performance.`;
    };

    const focusOnProducts = () => {
      // Close mobile cart and focus user attention on products
      isMobileCartVisible.value = false;
      document.querySelector('.product-section')?.scrollIntoView({ behavior: 'smooth' });
    };

    // Place order
    const placeOrder = async () => {
      if (cart.value.length === 0) {
        alert('Please add items to your cart first.');
        return;
      }

      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please login first.");
        return;
      }

      try {
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          }
        };

        // Add items to backend cart
        for (const item of cart.value) {
          await axios.post(`${apiBaseUrl}/cart/add`, {
            product_id: item.id,
            quantity: item.quantity
          }, config);
        }

        // Checkout with discount if selected
        const checkoutPayload = {};
        if (selectedDiscountId.value) {
          checkoutPayload.discount_id = selectedDiscountId.value;
        }

        const res = await axios.post(`${apiBaseUrl}/checkout`, checkoutPayload, config);

        alert(`✅ Order placed successfully! Order ID: ${res.data.order_id}`);
        cart.value = [];
        selectedDiscountId.value = null;
      } catch (error) {
        console.error("Failed to place order", error);
        alert("❌ Failed to place order.");
      }
    };

    // UI toggles
    const toggleMobileCart = () => {
      isMobileCartVisible.value = !isMobileCartVisible.value;
    };

    // Initialize data
    onMounted(() => {
      loadProducts();
      fetchDiscounts();

      // Listen for window resize to handle responsive behavior
      window.addEventListener('resize', handleResize);
      handleResize();
    });

    const handleResize = () => {
      // Auto-collapse cart on smaller screens
      if (window.innerWidth < 768) {
        isMobileCartVisible.value = false;
      }
    };

    return {
      // State variables
      searchTerm,
      products,
      cart,
      filteredProducts,
      availableDiscounts,
      selectedDiscountId,
      isLoading,
      isMobileCartVisible,
      viewMode,
      activeCategory,
      selectedProduct,
      modalQuantity,

      // Methods
      loadProducts,
      fetchDiscounts,
      searchProducts,
      clearSearch,
      resetFilters,
      filterByCategory,
      addToCart,
      increaseQuantity,
      decreaseQuantity,
      removeItem,
      clearCart,
      calculateSubtotal,
      calculateTax,
      calculateDiscountAmount,
      calculateTotal,
      placeOrder,
      toggleMobileCart,

      // Stock and product display helpers
      isNewProduct,
      isOnSale,
      getStockClass,
      getStockIcon,
      getStockLabel,
      getProductDescription,

      // Modal functionality
      showProductQuickView,
      closeQuickView,
      addToCartFromModal,
      increaseModalQuantity,
      decreaseModalQuantity,
      focusOnProducts
    };
  }
};
</script>

<style scoped>
/* Sales View Container */
.sales-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - var(--top-header-height));
  background-color: var(--bg-color);
  position: relative;
}

/* Top Action Bar */
.sales-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--card-bg);
  box-shadow: var(--shadow-sm);
  border-bottom: 1px solid var(--border-color);
  z-index: 10;
}

.page-title {
  display: flex;
  flex-direction: column;
}

.page-title h2 {
  display: flex;
  align-items: center;
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.page-title h2 i {
  margin-right: var(--spacing-sm);
  color: var(--primary-600);
}

.subtitle {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.action-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.search-control {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.search-input {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-md) var(--spacing-xl);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
  color: var(--text-primary);
  transition: all var(--transition-base);
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.15);
}

.clear-search {
  position: absolute;
  right: var(--spacing-sm);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  background: rgba(0, 0, 0, 0.05);
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: none;
  transition: all var(--transition-base);
}

.clear-search:hover {
  background: rgba(0, 0, 0, 0.1);
  color: var(--text-primary);
}

.view-controls {
  display: flex;
  background-color: var(--bg-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.view-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-secondary);
  background: transparent;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
}

.view-btn.active {
  background-color: var(--primary-50);
  color: var(--primary-700);
}

.view-btn:not(.active):hover {
  background-color: var(--neutral-100);
}

.mobile-cart-toggle {
  display: none;
  position: relative;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background-color: var(--primary-500);
  color: white;
  border: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.mobile-cart-toggle:hover {
  background-color: var(--primary-600);
  transform: translateY(-2px);
}

.item-count {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: var(--danger-color);
  color: white;
  font-size: 11px;
  font-weight: 700;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--card-bg);
}

/* Filter Controls */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--bg-color);
  border-bottom: 1px solid var(--border-color);
}

.category-pills {
  display: flex;
  gap: var(--spacing-sm);
  overflow-x: auto;
  padding-bottom: var(--spacing-sm);
  /* Hide scrollbar for Chrome */
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.category-pills::-webkit-scrollbar {
  display: none;
}

.category-pill {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
  white-space: nowrap;
}

.category-pill i {
  font-size: 16px;
}

.category-pill:hover {
  background-color: var(--primary-50);
  border-color: var(--primary-200);
  color: var(--primary-700);
}

.category-pill.active {
  background-color: var(--primary-500);
  border-color: var(--primary-500);
  color: white;
}

.filter-stats {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.results-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.refresh-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--primary-500);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
}

.refresh-btn:hover {
  background-color: var(--primary-50);
  transform: rotate(180deg);
}

/* Content Grid */
.content-grid {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Product Section */
.product-section {
  flex: 1;
  padding: var(--spacing-lg);
  overflow-y: auto;
  background-color: var(--bg-color);
}

/* Loading Container */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--text-secondary);
}

.spinner-wrapper {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-md);
  position: relative;
}

.spinner {
  width: 44px;
  height: 44px;
  border: 3px solid rgba(33, 150, 243, 0.1);
  border-left-color: var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 3px dashed rgba(33, 150, 243, 0.2);
  border-radius: 50%;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.no-products {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  color: var(--text-secondary);
  text-align: center;
  height: 300px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
}

.empty-state i {
  font-size: 52px;
  margin-bottom: var(--spacing-md);
  color: var(--neutral-400);
}

.empty-state h3 {
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.empty-state p {
  margin-bottom: var(--spacing-lg);
  color: var(--text-secondary);
}

.reset-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background-color: var(--primary-50);
  color: var(--primary-700);
  border: 1px solid var(--primary-200);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
}

.reset-btn:hover {
  background-color: var(--primary-100);
}

/* Product List Grid View */
.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--spacing-lg);
}

.product-card {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  cursor: pointer;
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid transparent;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-200);
}

.card-badges {
  position: absolute;
  top: var(--spacing-md);
  left: var(--spacing-md);
  display: flex;
  gap: var(--spacing-xs);
  z-index: 2;
}

.badge {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge.new {
  background-color: var(--primary-500);
  color: white;
}

.badge.sale {
  background-color: var(--danger-color);
  color: white;
}

.mini-badge {
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.mini-badge.new {
  background-color: var(--primary-500);
  color: white;
}

.mini-badge.sale {
  background-color: var(--danger-color);
  color: white;
}

.product-img {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-color);
  padding: var(--spacing-md);
  overflow: hidden;
  position: relative;
}

.product-img::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, transparent 60%, rgba(0, 0, 0, 0.03) 100%);
}

.product-img img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
  z-index: 1;
  transition: transform var(--transition-base);
}

.product-card:hover .product-img img {
  transform: scale(1.05);
}

.product-info {
  padding: var(--spacing-lg);
  flex: 1;
  display: flex;
  flex-direction: column;
  border-top: 1px solid var(--border-color);
}

.product-info h4 {
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
  font-size: 16px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 44px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.price {
  font-weight: 700;
  color: var(--primary-600);
  font-size: 18px;
}

.stock-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: var(--radius-full);
}

.stock-indicator i {
  font-size: 14px;
}

.stock-indicator.in-stock {
  background-color: var(--success-light);
  color: var(--success-color);
}

.stock-indicator.low-stock {
  background-color: var(--warning-light);
  color: var(--warning-color);
}

.stock-indicator.out-of-stock {
  background-color: var(--danger-light);
  color: var(--danger-color);
}

.stock-label {
  font-weight: 600;
  display: none;
}

.product-actions {
  padding: 0 var(--spacing-md) var(--spacing-md);
}

.btn-quick-add {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--primary-500);
  color: white;
  border-radius: var(--radius-md);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.btn-quick-add:hover {
  background-color: var(--primary-600);
  transform: translateY(-2px);
}

.btn-quick-add:disabled {
  background-color: var(--neutral-400);
  cursor: not-allowed;
  transform: none;
}

/* Product List Table View */
.product-list-table {
  width: 100%;
}

.product-table {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.table-header {
  display: grid;
  grid-template-columns: 3fr 1fr 1fr 1fr;
  background-color: var(--primary-50);
  color: var(--primary-800);
  font-weight: 600;
  font-size: 14px;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.table-row {
  display: grid;
  grid-template-columns: 3fr 1fr 1fr 1fr;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  align-items: center;
  transition: background-color var(--transition-base);
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background-color: var(--primary-50);
}

.col-product {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.product-img-small {
  width: 50px;
  height: 50px;
  background-color: white;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm);
  flex-shrink: 0;
}

.product-img-small img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

.product-name h4 {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 14px;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.badges-inline {
  display: flex;
  gap: var(--spacing-xs);
}

.col-price {
  font-weight: 700;
  color: var(--primary-600);
}

.col-stock, .col-action {
  display: flex;
  justify-content: center;
}

.col-action {
  display: flex;
  gap: var(--spacing-sm);
}

.btn-list-add, .btn-list-view {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-list-add {
  background-color: var(--primary-500);
  color: white;
}

.btn-list-add:hover {
  background-color: var(--primary-600);
  transform: translateY(-2px);
}

.btn-list-add:disabled {
  background-color: var(--neutral-400);
  cursor: not-allowed;
  transform: none;
}

.btn-list-view {
  background-color: var(--bg-color);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-list-view:hover {
  background-color: var(--primary-50);
  color: var(--primary-700);
  border-color: var(--primary-200);
}

/* Enhanced Cart Section */
.cart-section {
  width: 400px;
  background-color: var(--card-bg);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-base);
  box-shadow: var(--shadow-md);
  z-index: 20;
}

.cart-header {
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-header h3 {
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.cart-header h3 i {
  color: var(--primary-500);
}

.cart-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.btn-cart-action {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--danger-light);
  color: var(--danger-color);
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-cart-action:hover {
  background-color: var(--danger-color);
  color: white;
}

.close-cart {
  display: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--bg-color);
  color: var(--text-secondary);
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
}

.close-cart:hover {
  background-color: var(--neutral-200);
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  color: var(--text-secondary);
  text-align: center;
  flex: 1;
}

.empty-cart i {
  font-size: 64px;
  margin-bottom: var(--spacing-lg);
  color: var(--neutral-300);
}

.empty-cart h3 {
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.browse-products-btn {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-sm) var(--spacing-lg);
  background-color: var(--primary-50);
  color: var(--primary-700);
  border: 1px solid var(--primary-200);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
}

.browse-products-btn:hover {
  background-color: var(--primary-100);
}

.cart-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

.cart-item {
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  background-color: var(--bg-color);
  margin-bottom: var(--spacing-md);
  display: flex;
  position: relative;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.cart-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background-color: var(--primary-500);
}

.item-img {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-sm);
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
  overflow: hidden;
  border: 1px solid var(--border-color);
  flex-shrink: 0;
}

.item-img img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.item-info h4 {
  font-weight: 500;
  font-size: 14px;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.item-price {
  font-size: 13px;
  color: var(--text-secondary);
}

.item-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quantity-controls {
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
  padding: 2px;
}

.btn-quantity {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: var(--bg-color);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
  border: none;
}

.btn-quantity:hover {
  background-color: var(--primary-50);
  color: var(--primary-700);
}

.btn-quantity.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity {
  margin: 0 var(--spacing-sm);
  font-weight: 600;
  min-width: 24px;
  text-align: center;
}

.item-subtotal {
  font-weight: 700;
  color: var(--primary-600);
  font-size: 15px;
}

.btn-remove {
  background: none;
  border: none;
  color: var(--danger-color);
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all var(--transition-base);
}

.btn-remove:hover {
  background-color: var(--danger-light);
}

/* Enhanced Cart Summary */
.cart-summary {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  background-color: var(--bg-color);
}

.order-details {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.order-details h4 {
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: 18px;
}

.summary-rows {
  margin-bottom: var(--spacing-md);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
  padding: var(--spacing-sm) 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.discount-row {
  border-top: 1px dashed var(--border-color);
  padding-top: var(--spacing-md);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.discount-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--primary-500);
  font-weight: 500;
}

.discount-selector {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.discount-select {
  flex: 1;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background-color: white;
  font-size: 14px;
  outline: none;
  transition: border-color var(--transition-base);
  color: var(--text-primary);
}

.discount-select:focus {
  border-color: var(--primary-500);
}

.discount-amount {
  color: var(--danger-color);
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}

.order-total {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-md) 0;
  border-top: 2px solid var(--border-color);
  font-weight: 700;
  font-size: 18px;
  color: var(--text-primary);
}

.total-amount {
  color: var(--primary-700);
}

.btn-checkout {
  width: 100%;
  padding: var(--spacing-md);
  margin-top: var(--spacing-md);
  background-color: var(--primary-500);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-md);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.btn-checkout::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to bottom right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(45deg);
  transition: all 0.8s;
}

.btn-checkout:hover {
  background-color: var(--primary-600);
  transform: translateY(-2px);
}

.btn-checkout:hover::after {
  left: 100%;
}

.btn-checkout:disabled {
  background-color: var(--neutral-400);
  transform: none;
}

.btn-checkout i {
  font-size: 18px;
}

/* Product Modal */
.product-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
  backdrop-filter: blur(3px);
}

.modal-content {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  position: relative;
}

.close-modal {
  position: absolute;
  top: var(--spacing-md);
  right: var(--spacing-md);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--bg-color);
  color: var(--text-secondary);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all var(--transition-base);
}

.close-modal:hover {
  background-color: var(--neutral-300);
  color: var(--text-primary);
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-xl);
  padding: var(--spacing-xl);
}

.product-image-large {
  background-color: var(--bg-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  height: 350px;
  border: 1px solid var(--border-color);
}

.product-image-large img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

.product-details {
  display: flex;
  flex-direction: column;
}

.product-details h2 {
  font-weight: 700;
  font-size: 24px;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  line-height: 1.4;
}

.pricing-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.product-price {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.current-price {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-700);
}

.original-price {
  font-size: 18px;
  color: var(--text-secondary);
  text-decoration: line-through;
}

.inventory-status {
  margin-bottom: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.modal-stock {
  padding: var(--spacing-sm) var(--spacing-md);
  width: fit-content;
}

.modal-stock .stock-label {
  display: inline;
}

.stock-count {
  font-size: 14px;
  color: var(--text-secondary);
}

.product-description {
  margin-bottom: var(--spacing-xl);
  line-height: 1.6;
  color: var(--text-secondary);
}

.quick-view-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.quantity-selector {
  display: flex;
  align-items: center;
  width: 100%;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.qty-btn {
  width: 40px;
  height: 40px;
  background-color: var(--bg-color);
  color: var(--text-primary);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color var(--transition-base);
}

.qty-btn:hover {
  background-color: var(--primary-50);
}

.qty-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-selector input {
  flex: 1;
  width: 40px;
  height: 40px;
  border: none;
  border-left: 1px solid var(--border-color);
  border-right: 1px solid var(--border-color);
  text-align: center;
  font-weight: 600;
  color: var(--text-primary);
  -moz-appearance: textfield;
}

.quantity-selector input::-webkit-outer-spin-button,
.quantity-selector input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.add-to-cart-btn {
  width: 100%;
  padding: var(--spacing-md);
  background-color: var(--primary-500);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

.add-to-cart-btn:hover {
  background-color: var(--primary-600);
  transform: translateY(-2px);
}

.add-to-cart-btn:disabled {
  background-color: var(--neutral-400);
  cursor: not-allowed;
  transform: none;
}

/* Mobile Cart Overlay */
.mobile-cart-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 15;
  backdrop-filter: blur(3px);
}

/* Animations */
.product-fade-enter-active, .product-fade-leave-active,
.list-fade-enter-active, .list-fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.product-fade-enter, .product-fade-leave-to,
.list-fade-enter, .list-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.cart-item-enter-active, .cart-item-leave-active {
  transition: all 0.3s ease;
}

.cart-item-enter, .cart-item-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* Responsive Styles */
@media screen and (max-width: 1280px) {
  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  }

  .cart-section {
    width: 360px;
  }
}

@media screen and (max-width: 992px) {
  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }

  .search-control {
    width: 200px;
  }

  .cart-section {
    width: 320px;
  }

  .modal-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }

  .product-image-large {
    height: 280px;
  }
}

@media screen and (max-width: 768px) {
  .sales-action-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .action-controls {
    width: 100%;
    justify-content: space-between;
  }

  .search-control {
    flex: 1;
    width: auto;
  }

  .mobile-cart-toggle {
    display: flex;
  }

  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .product-img {
    height: 140px;
  }

  .product-info {
    padding: var(--spacing-md);
  }

  .stock-label {
    display: none;
  }

  .cart-section {
    position: fixed;
    top: 0;
    right: 0;
    width: 100%;
    max-width: 380px;
    height: 100%;
    transform: translateX(100%);
    z-index: 40;
  }

  .cart-section.mobile-cart-visible {
    transform: translateX(0);
  }

  .close-cart {
    display: flex;
  }

  .mobile-cart-overlay {
    display: block;
  }

  .table-header {
    grid-template-columns: 2fr 1fr 1fr 1fr;
    padding: var(--spacing-sm) var(--spacing-md);
  }

  .table-row {
    grid-template-columns: 2fr 1fr 1fr 1fr;
    padding: var(--spacing-sm) var(--spacing-md);
  }
}

@media screen and (max-width: 576px) {
  .page-title h2 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.8rem;
  }

  .filter-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .category-pills {
    width: 100%;
  }

  .filter-stats {
    width: 100%;
    justify-content: space-between;
  }

  .product-section {
    padding: var(--spacing-md);
  }

  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: var(--spacing-md);
  }

  .btn-quick-add span {
    display: none;
  }

  .cart-section {
    max-width: 100%;
  }

  .table-header {
    grid-template-columns: 3fr 1fr auto;
  }

  .table-row {
    grid-template-columns: 3fr 1fr auto;
  }

  .col-stock {
    display: none;
  }

  .btn-list-view {
    display: none;
  }
}
</style>