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
          <span class="item-count" v-if="cartStore.items.length">{{ cartStore.items.length }}</span>
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
            <button class="btn-cart-action" @click="clearCart" v-if="cartStore.items.length" title="Clear Cart">
              <i class="material-icons">remove_shopping_cart</i>
            </button>
            <button class="close-cart" @click="toggleMobileCart">
              <i class="material-icons">close</i>
            </button>
          </div>
        </div>

        <div v-if="cartStore.items.length === 0" class="empty-cart">
          <i class="material-icons">shopping_cart</i>
          <h3>Your cart is empty</h3>
          <p>Add products to begin a new order</p>
          <button class="browse-products-btn" @click="focusOnProducts">Browse Products</button>
        </div>

        <div v-else class="cart-content">
          <div class="cart-items">
            <transition-group name="cart-item">
              <div class="cart-item" v-for="(item, index) in cartStore.items" :key="item.id">
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

          <!-- Fixed Cart Summary Section -->
          <div class="cart-summary">
            <div class="order-details">
              <h4>Order Summary</h4>

              <div class="summary-rows">
                <div class="summary-row">
                  <span>Subtotal</span>
                  <span>${{ cartStore.subtotal.toFixed(2) }}</span>
                </div>

                <div class="summary-row">
                  <span>Tax (7%)</span>
                  <span>${{ cartStore.tax.toFixed(2) }}</span>
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
                        {{ discount.name }}
                        ({{ discount.discount_type === 'percentage' ? discount.value + '%' : '$' + discount.value }} off)
                      </option>
                    </select>

                    <span class="discount-amount" v-if="cartStore.selectedDiscountId">
                      -${{ cartStore.discountAmount.toFixed(2) }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="order-total">
                <span>Total</span>
                <span class="total-amount">${{ cartStore.total.toFixed(2) }}</span>
              </div>
            </div>

            <div class="checkout-container">
              <button
                class="btn-checkout"
                @click="placeOrder"
                :disabled="cartStore.items.length === 0"
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
                <span class="original-price" v-if="isOnSale(selectedProduct)">
                  ${{ (selectedProduct.price * 1.2).toFixed(2) }}
                </span>
              </div>

              <div class="badges">
                <span class="badge new" v-if="isNewProduct(selectedProduct)">NEW</span>
                <span class="badge sale" v-if="isOnSale(selectedProduct)">SALE</span>
              </div>
            </div>

            <div class="inventory-status">
              <div class="stock-indicator modal-stock" :class="getStockClass(selectedProduct)">
                <i class="material-icons">{{ getStockIcon(selectedProduct) }}</i>
                <span class="stock-label">{{ getStockLabel(selectedProduct) }}</span>
              </div>
              <div class="stock-count" v-if="selectedProduct.stock > 0">
                {{ selectedProduct.stock }} units available
              </div>
            </div>

            <div class="product-description">
              <p>{{ selectedProduct.description || 'No description available for this product.' }}</p>
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
                <input
                  type="number"
                  v-model.number="modalQuantity"
                  min="1"
                  :max="selectedProduct.stock"
                />
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

    <!-- Order Success Modal -->
    <div class="modal order-success-modal" v-if="orderCompleted" @click.self="closeOrderSuccessModal">
      <div class="modal-content order-success-content">
        <div class="success-icon">
          <i class="material-icons">check_circle</i>
        </div>
        <h2>Order Completed!</h2>
        <p>Your order has been successfully placed.</p>
        <p class="order-number">Order #{{ orderNumber }}</p>
        <div class="order-success-buttons">
          <button class="btn-success-action btn-primary" @click="closeOrderSuccessModal">
            <i class="material-icons">arrow_back</i>
            Back to Sales
          </button>
          <button class="btn-success-action btn-secondary" @click="viewOrderDetails">
            <i class="material-icons">receipt</i>
            View Receipt
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useCartStore } from '@/stores/cartStore';
import apiClient from '@/services/api';

const cartStore = useCartStore();

// UI State
const viewMode = ref('grid');
const searchTerm = ref('');
const isLoading = ref(true);
const activeCategory = ref('all');
const isMobileCartVisible = ref(false);
const selectedProduct = ref(null);
const modalQuantity = ref(1);
const availableDiscounts = ref([]);
const selectedDiscountId = ref(null);
const orderCompleted = ref(false);
const orderNumber = ref('');

// Data
const products = ref([]);
const filteredProducts = computed(() => {
  let result = [...products.value];

  // Apply category filter
  if (activeCategory.value === 'popular') {
    result = result.filter(p => p.popular);
  } else if (activeCategory.value === 'new') {
    result = result.filter(p => isNewProduct(p));
  } else if (activeCategory.value === 'sale') {
    result = result.filter(p => isOnSale(p));
  }

  // Apply search filter
  if (searchTerm.value) {
    const search = searchTerm.value.toLowerCase();
    result = result.filter(
      p => p.name.toLowerCase().includes(search) ||
           (p.category && p.category.toLowerCase().includes(search))
    );
  }

  return result;
});

// Watch for discount changes
watch(selectedDiscountId, (newVal) => {
  cartStore.setDiscount(newVal);
});

// Methods
function loadProducts() {
  isLoading.value = true;

  apiClient.get('/products')
    .then(response => {
      products.value = response.data.map(product => ({
        ...product,
        image: product.image || 'https://via.placeholder.com/200'
      }));
      isLoading.value = false;
    })
    .catch(error => {
      console.error('Error loading products:', error);
      isLoading.value = false;
    });
}

function loadDiscounts() {
  apiClient.get('/discounts')
    .then(response => {
      availableDiscounts.value = response.data;
    })
    .catch(error => {
      console.error('Error loading discounts:', error);
    });
}

function filterByCategory(category) {
  activeCategory.value = category;
}

function searchProducts() {
  // Debounce search if needed
}

function clearSearch() {
  searchTerm.value = '';
}

function resetFilters() {
  searchTerm.value = '';
  activeCategory.value = 'all';
}

function addToCart(product) {
  cartStore.addItem(product, 1);
}

function increaseQuantity(index) {
  cartStore.updateQuantity(index, cartStore.items[index].quantity + 1);
}

function decreaseQuantity(index) {
  cartStore.updateQuantity(index, cartStore.items[index].quantity - 1);
}

function removeItem(index) {
  cartStore.removeItem(index);
}

function clearCart() {
  cartStore.clearCart();
}

function toggleMobileCart() {
  isMobileCartVisible.value = !isMobileCartVisible.value;
}

function focusOnProducts() {
  // Scroll to products or close mobile cart
  if (isMobileCartVisible.value) {
    toggleMobileCart();
  }
}

function showProductQuickView(product) {
  selectedProduct.value = product;
  modalQuantity.value = 1;
}

function closeQuickView() {
  selectedProduct.value = null;
}

function increaseModalQuantity() {
  if (modalQuantity.value < selectedProduct.value.stock) {
    modalQuantity.value++;
  }
}

function decreaseModalQuantity() {
  if (modalQuantity.value > 1) {
    modalQuantity.value--;
  }
}

function addToCartFromModal() {
  if (selectedProduct.value) {
    cartStore.addItem(selectedProduct.value, modalQuantity.value);
    closeQuickView();
  }
}

function placeOrder() {
  // Get items from cart
  const items = cartStore.items.map(item => ({
    product_id: item.id,
    quantity: item.quantity,
    price: item.price
  }));

  // Order data
  const orderData = {
    items,
    subtotal: cartStore.subtotal,
    tax: cartStore.tax,
    discount_id: cartStore.selectedDiscountId,
    discount_amount: cartStore.discountAmount,
    total: cartStore.total
  };

  // Send to API
  apiClient.post('/checkout', orderData)
    .then(response => {
      // Show success modal
      orderNumber.value = response.data.order_id || 'POS-' + Math.floor(100000 + Math.random() * 900000);
      orderCompleted.value = true;

      // Clear cart after order is processed
      cartStore.clearCart();
    })
    .catch(error => {
      console.error('Error processing order:', error);
      alert('There was an error processing your order. Please try again.');
    });
}

function closeOrderSuccessModal() {
  orderCompleted.value = false;
}

function viewOrderDetails() {
  // Implement order details view
  alert(`Viewing details for order #${orderNumber.value}`);
}

// Helper functions
function isNewProduct(product) {
  // Consider a product new if it was created in the last 7 days
  if (!product.created_at) return false;
  const createdDate = new Date(product.created_at);
  const sevenDaysAgo = new Date();
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
  return createdDate >= sevenDaysAgo;
}

function isOnSale(product) {
  return product.on_sale;
}

function getStockClass(product) {
  if (product.stock <= 0) return 'out-of-stock';
  if (product.stock < 5) return 'low-stock';
  return 'in-stock';
}

function getStockIcon(product) {
  if (product.stock <= 0) return 'cancel';
  if (product.stock < 5) return 'error_outline';
  return 'check_circle';
}

function getStockLabel(product) {
  if (product.stock <= 0) return 'Out of Stock';
  if (product.stock < 5) return 'Low Stock';
  return 'In Stock';
}

// Initialize component
onMounted(() => {
  loadProducts();
  loadDiscounts();
});
</script>

<style scoped>
:root {
  --primary-50: #f0f9ff;
  --primary-100: #e0f2fe;
  --primary-200: #bae6fd;
  --primary-300: #7dd3fc;
  --primary-400: #38bdf8;
  --primary-500: #0ea5e9;
  --primary-600: #0284c7;
  --primary-700: #0369a1;
  --primary-800: #075985;
  --primary-900: #0c4a6e;

  --neutral-50: #f9fafb;
  --neutral-100: #f3f4f6;
  --neutral-200: #e5e7eb;
  --neutral-300: #d1d5db;
  --neutral-400: #9ca3af;
  --neutral-500: #6b7280;
  --neutral-600: #4b5563;
  --neutral-700: #374151;
  --neutral-800: #1f2937;
  --neutral-900: #111827;

  --success-color: #22c55e;
  --success-light: #dcfce7;
  --warning-color: #f59e0b;
  --warning-light: #fef3c7;
  --danger-color: #ef4444;
  --danger-light: #fee2e2;

  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);

  --transition-base: 0.2s ease;

  --bg-color: var(--neutral-50);
  --card-bg: white;
  --text-primary: var(--neutral-900);
  --text-secondary: var(--neutral-600);
  --border-color: var(--neutral-200);
}

.dark-mode {
  --bg-color: var(--neutral-900);
  --card-bg: var(--neutral-800);
  --text-primary: white;
  --text-secondary: var(--neutral-400);
  --border-color: var(--neutral-700);
}

.sales-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: var(--bg-color);
  overflow: hidden;
}

.sales-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
}

.page-title {
  display: flex;
  flex-direction: column;
}

.page-title h2 {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.page-title .subtitle {
  font-size: 14px;
  color: var(--text-secondary);
  margin: var(--spacing-xs) 0 0 0;
}

.action-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.search-control {
  position: relative;
  width: 280px;
}

.search-icon {
  position: absolute;
  left: var(--spacing-sm);
  top: 50%;
  transform: translateY(-50%);
  color: var(--neutral-500);
  font-size: 20px;
}

.search-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-sm) var(--spacing-sm) 36px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
  color: var(--text-primary);
  font-size: 14px;
  transition: all var(--transition-base);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-400);
  box-shadow: 0 0 0 3px var(--primary-100);
}

.clear-search {
  position: absolute;
  right: var(--spacing-sm);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--neutral-500);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.view-controls {
  display: flex;
  gap: var(--spacing-xs);
  border-radius: var(--radius-md);
  overflow: hidden;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
}

.view-btn {
  background: none;
  border: none;
  padding: var(--spacing-sm);
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
}

.view-btn.active {
  background-color: var(--primary-50);
  color: var(--primary-600);
}

.view-btn:hover:not(.active) {
  background-color: var(--neutral-100);
}

.mobile-cart-toggle {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-primary);
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  cursor: pointer;
  position: relative;
  display: none;
  transition: all var(--transition-base);
}

.mobile-cart-toggle:hover {
  background-color: var(--primary-50);
  color: var(--primary-600);
}

.item-count {
  position: absolute;
  top: -6px;
  right: -6px;
  background-color: var(--primary-500);
  color: white;
  font-size: 10px;
  font-weight: 600;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background-color: var(--card-bg);
  box-shadow: var(--shadow-xs);
  z-index: 1;
}

.category-pills {
  display: flex;
  gap: var(--spacing-sm);
  overflow-x: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
  padding-bottom: var(--spacing-xs);
}

.category-pills::-webkit-scrollbar {
  display: none;
}

.category-pill {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-full);
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  cursor: pointer;
  transition: all var(--transition-base);
}

.category-pill:hover {
  background-color: var(--neutral-100);
}

.category-pill.active {
  background-color: var(--primary-50);
  color: var(--primary-700);
  border-color: var(--primary-200);
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
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.refresh-btn:hover {
  background-color: var(--primary-50);
  color: var(--primary-600);
  transform: rotate(180deg);
}

.content-grid {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.product-section {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-lg);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.spinner-wrapper {
  width: 40px;
  height: 40px;
  margin-bottom: var(--spacing-md);
}

.spinner {
  width: 100%;
  height: 100%;
  border: 3px solid var(--primary-100);
  border-top-color: var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.no-products {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 300px;
}

.empty-state i {
  font-size: 48px;
  color: var(--neutral-400);
  margin-bottom: var(--spacing-md);
}

.empty-state h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.empty-state p {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-lg);
}

.reset-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
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

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--spacing-md);
}

.product-card {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: all var(--transition-base);
  cursor: pointer;
  position: relative;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-200);
}

.card-badges {
  position: absolute;
  top: var(--spacing-sm);
  right: var(--spacing-sm);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  z-index: 1;
}

.badge {
  font-size: 10px;
  font-weight: 600;
  padding: 3px 6px;
  border-radius: var(--radius-sm);
}

.badge.new {
  background-color: var(--primary-500);
  color: white;
}

.badge.sale {
  background-color: var(--danger-color);
  color: white;
}

.product-img {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
  background-color: var(--bg-color);
  overflow: hidden;
}

.product-img img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.product-card:hover .product-img img {
  transform: scale(1.1);
}

.product-info {
  padding: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.product-info h4 {
  font-weight: 600;
  font-size: 16px;
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-weight: 600;
  color: var(--primary-600);
  font-size: 18px;
  margin: 0;
}

.stock-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  padding: 3px 6px;
  border-radius: var(--radius-full);
}

.in-stock {
  background-color: var(--success-light);
  color: var(--success-color);
}

.low-stock {
  background-color: var(--warning-light);
  color: var(--warning-color);
}

.out-of-stock {
  background-color: var(--danger-light);
  color: var(--danger-color);
}

.stock-indicator i {
  font-size: 14px;
}

.stock-label {
  white-space: nowrap;
}

.product-actions {
  padding: 0 var(--spacing-md) var(--spacing-md);
}

.btn-quick-add {
  width: 100%;
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  background-color: var(--primary-500);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.btn-quick-add:hover:not(:disabled) {
  background-color: var(--primary-600);
}

.btn-quick-add:disabled {
  background-color: var(--neutral-300);
  cursor: not-allowed;
}

/* List View Styles */
.product-list-table {
  display: block;
}

.product-table {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background-color: var(--card-bg);
}

.table-header {
  display: grid;
  grid-template-columns: 3fr 1fr 1fr 1fr;
  background-color: var(--bg-color);
  padding: var(--spacing-md);
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
}

.table-row {
  display: grid;
  grid-template-columns: 3fr 1fr 1fr 1fr;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  align-items: center;
  transition: all var(--transition-base);
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background-color: var(--bg-color);
}

.col-product {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.product-img-small {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-md);
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  padding: var(--spacing-xs);
  flex-shrink: 0;
}

.product-img-small img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.product-name {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.product-name h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.badges-inline {
  display: flex;
  gap: var(--spacing-xs);
}

.mini-badge {
  font-size: 9px;
  font-weight: 600;
  padding: 2px 4px;
  border-radius: 3px;
}

.mini-badge.new {
  background-color: var(--primary-500);
  color: white;
}

.mini-badge.sale {
  background-color: var(--danger-color);
  color: white;
}

.col-price {
  font-weight: 600;
  color: var(--primary-600);
}

.col-stock {
  display: flex;
  justify-content: flex-start;
}

.col-action {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-start;
}

.btn-list-add, .btn-list-view {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: none;
  transition: all var(--transition-base);
}

.btn-list-add {
  background-color: var(--primary-500);
  color: white;
}

.btn-list-add:hover:not(:disabled) {
  background-color: var(--primary-600);
  transform: scale(1.1);
}

.btn-list-add:disabled {
  background-color: var(--neutral-300);
  cursor: not-allowed;
}

.btn-list-view {
  background-color: var(--bg-color);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-list-view:hover {
  background-color: var(--primary-50);
  color: var(--primary-600);
  transform: scale(1.1);
}

/* Cart Styles */
.cart-section {
  width: 380px;
  background-color: var(--card-bg);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-color);
}

.cart-header h3 {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.cart-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.btn-cart-action {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-cart-action:hover {
  background-color: var(--danger-light);
  color: var(--danger-color);
  border-color: var(--danger-color);
}

.close-cart {
  display: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.close-cart:hover {
  background-color: var(--primary-50);
  color: var(--primary-600);
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--spacing-xl);
  flex: 1;
}

.empty-cart i {
  font-size: 48px;
  color: var(--neutral-300);
  margin-bottom: var(--spacing-md);
}

.empty-cart h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.empty-cart p {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-lg);
}

.browse-products-btn {
  padding: var(--spacing-sm) var(--spacing-md);
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
  height: 100%; /* Make sure it takes full height */
  position: relative; /* Position relative for absolute child */
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
  margin-bottom: 250px; /* Fixed space for order summary */
  height: calc(100% - 250px); /* Adjust height to account for order summary */
}

.cart-item {
  display: flex;
  gap: var(--spacing-md);
  background-color: var(--bg-color);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  position: relative;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  width: 100%;
}

.cart-item:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
  border-color: var(--primary-200);
}

.item-img {
  width: 70px;
  height: 70px;
  background-color: white;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-sm);
  flex-shrink: 0;
  box-shadow: var(--shadow-xs);
  overflow: hidden;
}

.item-img img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.cart-item:hover .item-img img {
  transform: scale(1.1);
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.item-info h4 {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 2px;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-price {
  font-size: 12px;
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
  background-color: var(--card-bg);
  border-radius: var(--radius-full);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.btn-quantity {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-quantity:hover:not(.disabled) {
  background-color: var(--primary-50);
  color: var(--primary-700);
}

.btn-quantity.disabled {
  color: var(--neutral-400);
  cursor: not-allowed;
}

.quantity {
  font-weight: 600;
  min-width: 28px;
  text-align: center;
  color: var(--text-primary);
}

.item-subtotal {
  font-weight: 600;
  color: var(--primary-600);
  font-size: 14px;
}

.btn-remove {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  color: var(--danger-color);
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-remove:hover {
  background-color: var(--danger-light);
  border-color: var(--danger-color);
  transform: rotate(90deg);
}

.cart-summary {
  background-color: var(--card-bg);
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-lg);
  /* Ensure proper display */
  display: block !important;
  width: 100%;
  position: sticky;
  bottom: 0;
  z-index: 5; /* Ensure it stays on top */
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.order-details {
  /* Override any flex display that might be coming from elsewhere */
  display: block !important;
  background-color: var(--card-bg);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.order-details h4 {
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
}

.summary-rows {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  color: var(--text-secondary);
  font-size: 14px;
}

.discount-row {
  margin-top: var(--spacing-sm);
  padding-top: var(--spacing-sm);
  border-top: 1px dashed var(--border-color);
}

.discount-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--primary-600);
}

.discount-selector {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.discount-select {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
  color: var(--text-primary);
}

.discount-amount {
  font-weight: 600;
  color: var(--danger-color);
}

.order-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
  margin-bottom: var(--spacing-lg);
  color: var(--text-primary);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-color);
}

.total-amount {
  font-size: 18px;
  color: var(--primary-600);
}

.btn-checkout {
  width: 100%;
  padding: var(--spacing-md);
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

.btn-checkout:hover:not(:disabled) {
  background-color: var(--primary-600);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-checkout:disabled {
  background-color: var(--neutral-400);
  cursor: not-allowed;
  transform: none;
}

/* Product Quick View Modal */
.product-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: var(--spacing-lg);
}

.modal-content {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
  z-index: 10;
}

.close-modal:hover {
  background-color: var(--primary-50);
  color: var(--primary-700);
  border-color: var(--primary-200);
  transform: rotate(90deg);
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 400px;
}

.product-image-large {
  padding: var(--spacing-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-color);
  position: relative;
  overflow: hidden;
}

.product-image-large::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, transparent 60%, rgba(0, 0, 0, 0.03) 100%);
}

.product-image-large img {
  max-width: 80%;
  max-height: 300px;
  object-fit: contain;
  z-index: 1;
  animation: float 5s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

.product-details {
  padding: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  max-height: 500px;
}

.product-details h2 {
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  line-height: 1.3;
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
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-600);
}

.original-price {
  font-size: 16px;
  color: var(--text-secondary);
  text-decoration: line-through;
}

.badges {
  display: flex;
  gap: var(--spacing-xs);
}

.modal-stock {
  padding: var(--spacing-sm) var(--spacing-md);
}

.modal-stock .stock-label {
  display: inline;
}

.inventory-status {
  margin-bottom: var(--spacing-lg);
}

.stock-count {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: var(--spacing-sm);
}

.product-description {
  margin-bottom: var(--spacing-lg);
  color: var(--text-secondary);
}

.product-description p {
  line-height: 1.6;
}

.quick-view-actions {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.quantity-selector {
  display: flex;
  align-items: center;
  background-color: var(--bg-color);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.qty-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.qty-btn:hover:not(:disabled) {
  background-color: var(--primary-50);
  color: var(--primary-700);
}

.qty-btn:disabled {
  color: var(--neutral-400);
  cursor: not-allowed;
}

.quantity-selector input {
  width: 40px;
  padding: var(--spacing-sm);
  border: none;
  background: transparent;
  font-weight: 600;
  text-align: center;
  color: var(--text-primary);
  -moz-appearance: textfield;
}

.quantity-selector input::-webkit-outer-spin-button,
.quantity-selector input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.add-to-cart-btn {
  flex: 1;
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

.add-to-cart-btn:hover:not(:disabled) {
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
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 40;
  display: none;
}

/* Order Success Modal */
.order-success-modal {
  z-index: 110;
}

.order-success-content {
  max-width: 500px;
  padding: var(--spacing-xl);
  text-align: center;
}

.success-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: var(--success-light);
  color: var(--success-color);
  font-size: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--spacing-lg);
}

.success-icon i {
  font-size: 48px;
}

.order-success-content h2 {
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
}

.order-success-content p {
  margin-bottom: var(--spacing-lg);
  color: var(--text-secondary);
}

.order-number {
  font-family: monospace;
  font-size: 16px;
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--bg-color);
  border-radius: var(--radius-md);
  border: 1px dashed var(--border-color);
  margin-bottom: var(--spacing-lg);
  color: var(--primary-600);
  font-weight: 600;
}

.order-success-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

.btn-success-action {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.btn-primary {
  background-color: var(--primary-500);
  color: white;
  border: none;
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
  background-color: var(--primary-600);
  transform: translateY(-2px);
}

.btn-secondary {
  background-color: var(--bg-color);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--neutral-100);
  border-color: var(--neutral-300);
}

/* Animations */
.cart-item-enter-active, .cart-item-leave-active {
  transition: all 0.3s ease;
}

.cart-item-enter-from, .cart-item-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.product-fade-enter-active, .product-fade-leave-active {
  transition: all 0.3s ease-out;
}

.product-fade-enter-from, .product-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.list-fade-enter-active, .list-fade-leave-active {
  transition: all 0.3s ease-out;
}

.list-fade-enter-from, .list-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .content-grid {
    flex-direction: column;
  }

  .cart-section {
    width: 100%;
    height: 400px;
    border-left: none;
    border-top: 1px solid var(--border-color);
  }

  .product-section {
    padding: var(--spacing-md);
  }

  .modal-grid {
    grid-template-columns: 1fr;
  }

  .product-image-large {
    padding: var(--spacing-lg);
  }

  .product-image-large img {
    max-height: 200px;
  }

  .product-details {
    padding: var(--spacing-lg);
    max-height: 400px;
  }

  .quick-view-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .quantity-selector {
    margin-bottom: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .sales-action-bar {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-md);
  }

  .action-controls {
    flex-wrap: wrap;
  }

  .search-control {
    width: 100%;
    order: 1;
  }

  .view-controls {
    order: 2;
  }

  .mobile-cart-toggle {
    display: flex;
    order: 3;
    margin-left: auto;
  }

  .filter-bar {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .category-pills {
    width: 100%;
  }

  .filter-stats {
    width: 100%;
    justify-content: space-between;
  }

  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .product-img {
    height: 120px;
  }

  .cart-section {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 300px;
    height: 100%;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    z-index: 50;
    border: none;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
    overflow-y: auto;
  }

  .cart-section.mobile-cart-visible {
    transform: translateX(0);
  }

  .mobile-cart-overlay.mobile-cart-visible {
    display: block;
  }

  .close-cart {
    display: flex;
  }

  .table-header .col-stock,
  .table-row .col-stock {
    display: none;
  }

  .table-header,
  .table-row {
    grid-template-columns: 3fr 1fr 1fr;
  }

  .order-success-buttons {
    flex-direction: column;
    gap: var(--spacing-md);
  }
}

@media (max-width: 480px) {
  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }

  .product-img {
    height: 100px;
  }

  .price-row {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }

  .table-header .col-price,
  .table-row .col-price {
    display: none;
  }

  .table-header,
  .table-row {
    grid-template-columns: 3fr 1fr;
  }

  .modal-content {
    border-radius: 0;
    max-height: 100vh;
    height: 100%;
    width: 100%;
  }
}
</style>