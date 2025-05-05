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

          <!-- Enhanced Cart Summary -->
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

    <!-- Order Success Modal -->
    <div class="modal order-success-modal" v-if="orderCompleted" @click.self="closeOrderSuccessModal">
      <div class="modal-content order-success-content">
        <div class="success-icon">
          <i class="material-icons">check_circle</i>
        </div>
        <h2>Order Completed!</h2>
        <p>Your order has been successfully placed.</p>
        <p class="order-number">Order #{{ orderNumber }}</p>
        <div class="success-actions">
          <button class="btn-primary" @click="closeOrderSuccessModal">
            <i class="material-icons">arrow_back</i>
            Back to Sales
          </button>
          <button class="btn-secondary" @click="viewOrderDetails">
            <i class="material-icons">receipt</i>
            View Receipt
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { useCartStore } from '@/stores/cartStore';
import apiClient from '@/services/api';

export default {
  name: 'SalesView',
  setup() {
    // Use the cart store
    const cartStore = useCartStore();

    // Products & Filtering
    const products = ref([]);
    const filteredProducts = ref([]);
    const isLoading = ref(true);
    const searchTerm = ref('');
    const activeCategory = ref('all');
    const viewMode = ref('grid');

    // Mobile Responsiveness
    const isMobileCartVisible = ref(false);

    // Quick View Modal
    const selectedProduct = ref(null);
    const modalQuantity = ref(1);

    // Order Success Modal
    const orderCompleted = ref(false);
    const orderNumber = ref('');

    // Discounts
    const availableDiscounts = ref([]);

    // Selected Discount - two-way binding with cart store
    const selectedDiscountId = computed({
      get: () => cartStore.selectedDiscountId,
      set: (value) => cartStore.setDiscount(value)
    });

    // Load products using apiClient service
    const loadProducts = async () => {
      isLoading.value = true;
      try {
        const response = await apiClient.get('/products');
        products.value = response.data;
        filteredProducts.value = [...products.value];
        console.log('Products loaded successfully:', products.value.length);
      } catch (error) {
        console.error('Error loading products:', error);
      } finally {
        isLoading.value = false;
      }
    };

    // Load available discounts using apiClient service
    const loadDiscounts = async () => {
      try {
        const response = await apiClient.get('/discounts');
        availableDiscounts.value = response.data;
        console.log('Discounts loaded successfully:', availableDiscounts.value.length);
      } catch (error) {
        console.error('Error loading discounts:', error);
      }
    };

    // Filter products by search term
    const searchProducts = () => {
      if (!searchTerm.value.trim()) {
        filteredProducts.value = products.value;
        return;
      }

      const term = searchTerm.value.toLowerCase();
      filteredProducts.value = products.value.filter(product => {
        return (
          product.name.toLowerCase().includes(term) ||
          product.category.toLowerCase().includes(term) ||
          product.description.toLowerCase().includes(term)
        );
      });
    };

    // Clear search
    const clearSearch = () => {
      searchTerm.value = '';
      searchProducts();
    };

    // Filter products by category
    const filterByCategory = (category) => {
      activeCategory.value = category;

      if (category === 'all') {
        filteredProducts.value = products.value;
        return;
      }

      if (category === 'popular') {
        filteredProducts.value = products.value.filter(p => p.popular);
        return;
      }

      if (category === 'new') {
        filteredProducts.value = products.value.filter(p => isNewProduct(p));
        return;
      }

      if (category === 'sale') {
        filteredProducts.value = products.value.filter(p => isOnSale(p));
        return;
      }
    };

    // Reset filters
    const resetFilters = () => {
      searchTerm.value = '';
      activeCategory.value = 'all';
      filteredProducts.value = [...products.value];
    };

    // Check if product is new (< 30 days)
    const isNewProduct = (product) => {
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return new Date(product.created_at) > thirtyDaysAgo;
    };

    // Check if product is on sale
    const isOnSale = (product) => {
      return product.on_sale || product.id % 3 === 0; // Mock logic based on ID for demo
    };

    // Get stock level class for styling
    const getStockClass = (product) => {
      if (product.stock <= 0) return 'out-of-stock';
      if (product.stock < 5) return 'low-stock';
      return 'in-stock';
    };

    // Get stock icon based on availability
    const getStockIcon = (product) => {
      if (product.stock <= 0) return 'remove_circle';
      if (product.stock < 5) return 'error';
      return 'check_circle';
    };

    // Get stock label
    const getStockLabel = (product) => {
      if (product.stock <= 0) return 'Out of Stock';
      if (product.stock < 5) return 'Low Stock';
      return 'In Stock';
    };

    // Get mock product description
    const getProductDescription = (product) => {
      return product.description || `${product.name} - High-quality product perfect for your needs. Features include premium materials, reliable performance, and excellent durability. Order now while supplies last!`;
    };

    // Cart Functions - Now using the Pinia store

    // Add a product to the cart
    const addToCart = (product) => {
      console.log('Adding product to cart:', product);
      cartStore.addItem(product);
      console.log('Cart items after adding:', cartStore.items);

      // Force cart visibility on mobile when adding items
      if (window.innerWidth < 768) {
        isMobileCartVisible.value = true;
      }

      // Show success notification
      showNotification(`${product.name} added to cart`);
    };

    // Increase item quantity
    const increaseQuantity = (index) => {
      cartStore.increaseQuantity(index);
    };

    // Decrease item quantity
    const decreaseQuantity = (index) => {
      cartStore.decreaseQuantity(index);
    };

    // Remove item from cart
    const removeItem = (index) => {
      cartStore.removeItem(index);
    };

    // Clear the cart
    const clearCart = () => {
      cartStore.clearCart();
    };

    // Toggle mobile cart visibility
    const toggleMobileCart = () => {
      isMobileCartVisible.value = !isMobileCartVisible.value;
    };

    // Focus on products section (for mobile)
    const focusOnProducts = () => {
      isMobileCartVisible.value = false;
      // Scroll to product section if needed
    };

    // Product Quick View Modal
    const showProductQuickView = (product) => {
      selectedProduct.value = product;
      modalQuantity.value = 1;
    };

    const closeQuickView = () => {
      selectedProduct.value = null;
    };

    const increaseModalQuantity = () => {
      if (modalQuantity.value < selectedProduct.value.stock) {
        modalQuantity.value++;
      }
    };

    const decreaseModalQuantity = () => {
      if (modalQuantity.value > 1) {
        modalQuantity.value--;
      }
    };

    const addToCartFromModal = () => {
      if (selectedProduct.value) {
        console.log('Adding product from modal with quantity:', modalQuantity.value);
        cartStore.addItem(selectedProduct.value, modalQuantity.value);
        console.log('Cart items after adding from modal:', cartStore.items);

        // Force cart visibility on mobile
        if (window.innerWidth < 768) {
          isMobileCartVisible.value = true;
        }

        showNotification(`${selectedProduct.value.name} added to cart`);
        closeQuickView();
      }
    };

    // Show temporary notification
    const showNotification = (message) => {
      // Implement notification UI
      console.log('Notification:', message);
      // You could implement a toast notification system here
    };

    // Place order
    const placeOrder = async () => {
      const result = await cartStore.checkout();

      if (result.success) {
        // Show success message
        orderNumber.value = result.order.order_id || "12345"; // Fallback ID if none provided
        orderCompleted.value = true;
      } else {
        // Show error notification
        showNotification(`Error: ${result.error || 'Could not process order'}`, 'error');
      }
    };

    // Close order success modal
    const closeOrderSuccessModal = () => {
      orderCompleted.value = false;
    };

    // View order details
    const viewOrderDetails = () => {
      // Navigate to order details page
      // This would typically use router.push to go to a receipt page
      console.log('View order details for order #', orderNumber.value);
    };

    // Load data on component mount
    onMounted(() => {
      loadProducts();
      loadDiscounts();
      cartStore.loadFromLocalStorage();
      cartStore.loadDiscounts();
    });

    // If discount formats are different between store and component, sync them
    watch(availableDiscounts, () => {
      // If needed, format discounts for the cart store
    });

    return {
      // Store
      cartStore,

      // State
      products,
      filteredProducts,
      isLoading,
      searchTerm,
      activeCategory,
      viewMode,
      isMobileCartVisible,
      selectedProduct,
      modalQuantity,
      orderCompleted,
      orderNumber,
      availableDiscounts,
      selectedDiscountId,

      // Methods
      loadProducts,
      searchProducts,
      clearSearch,
      filterByCategory,
      resetFilters,
      isNewProduct,
      isOnSale,
      getStockClass,
      getStockIcon,
      getStockLabel,
      getProductDescription,

      // Cart methods
      addToCart,
      increaseQuantity,
      decreaseQuantity,
      removeItem,
      clearCart,
      placeOrder,

      // UI methods
      toggleMobileCart,
      focusOnProducts,
      showProductQuickView,
      closeQuickView,
      increaseModalQuantity,
      decreaseModalQuantity,
      addToCartFromModal,
      closeOrderSuccessModal,
      viewOrderDetails
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
  max-width: 100vw;
  background-color: var(--card-bg);
  border-left: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  position: relative;
  transition: transform 0.3s ease;
  overflow: hidden;
  height: 100%;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.cart-header h3 {
  display: flex;
  align-items: center;
  font-size: 1.2rem;
  color: var(--text-primary);
  gap: var(--spacing-sm);
}

.cart-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.btn-cart-action {
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
}

.btn-cart-action:hover {
  background-color: var(--primary-50);
  color: var(--primary-700);
  border-color: var(--primary-200);
}

.close-cart {
  display: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--bg-color);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--spacing-xl);
  flex: 1;
  color: var(--text-secondary);
}

.empty-cart i {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
  color: var(--neutral-300);
}

.empty-cart h3 {
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  color: var(--text-primary);
}

.empty-cart p {
  margin-bottom: var(--spacing-xl);
}

.browse-products-btn {
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
  display: flex;
}

.summary-rows {
  display: block;
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
}

@media (max-width: 1024px) {
  .content-grid {
    flex-direction: column;
  }

  .cart-section {
    width: 100%;
    border-left: none;
    border-top: 1px solid var(--border-color);
  }

  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  .sales-action-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .action-controls {
    width: 100%;
  }

  .search-control {
    width: 100%;
  }

  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: var(--spacing-md);
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

  .mobile-cart-toggle {
    display: flex;
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 30;
    width: 56px;
    height: 56px;
    box-shadow: var(--shadow-md);
  }

  .cart-section {
    position: fixed;
    top: 0;
    right: 0;
    width: 100%;
    height: 100%;
    z-index: 50;
    transform: translateX(100%);
    border: none;
    transition: transform 0.3s ease-in-out;
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

  .table-header, .table-row {
    grid-template-columns: 2fr 1fr 1fr;
  }

  .col-stock {
    display: none;
  }

  .item-controls {
    flex-wrap: wrap;
    gap: var(--spacing-sm);
  }

  .cart-item {
    padding: var(--spacing-md) var(--spacing-sm);
  }

  .discount-selector {
    flex-direction: column;
    align-items: flex-end;
  }
}

@media (max-width: 480px) {
  .product-list {
    grid-template-columns: 1fr;
  }

  .table-header, .table-row {
    grid-template-columns: 2fr 1fr;
    padding: var(--spacing-sm);
  }

  .col-action {
    display: none;
  }

  .product-table {
    margin-bottom: var(--spacing-md);
  }

  .product-card {
    margin-bottom: var(--spacing-md);
  }

  .product-img {
    height: 140px;
  }

  .quick-view-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .quantity-selector {
    margin-bottom: var(--spacing-md);
  }
}
</style>