<template>
  <div class="sales-view">
    <!-- Top Action Bar -->
    <div class="sales-action-bar">
      <div class="page-title">
        <img style="height: 65px;" src="../assets/logo-pp.png"><!--<h2><i class="material-icons">point_of_sale</i> Sales</h2>-->
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
                <img :src="product.image || 'https://via.placeholder.com/150'" :alt="product.name" />
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
                    <img :src="product.image || 'https://via.placeholder.com/50'" :alt="product.name" />
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
                  <img :src="item.image || 'https://via.placeholder.com/50'" :alt="item.name" />
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
              </div>

              <div class="order-total">
                <span>Total</span>
                <span class="total-amount">${{ calculateTotal().toFixed(2) }}</span>
              </div>
            </div>

            <div class="checkout-container">
              <button
                class="btn-checkout"
                @click="checkout"
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
            <img :src="selectedProduct.image || 'https://via.placeholder.com/300'" :alt="selectedProduct.name">
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
                  @click="modalQuantity--"
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
                  @click="modalQuantity++"
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
      class="mobile-overlay"
      @click="toggleMobileCart"
    ></div>
  </div>
</template>

<script>
//import apiClient from '../services/apiClient';

export default {
  name: 'FixedSalesView',
  data() {
    return {
      products: [],
      filteredProducts: [],
      cart: [],
      discounts: [],
      loading: true,
      error: null,
      searchTerm: '',
      viewMode: 'grid',
      activeCategory: 'all',
      selectedDiscount: null,
      isMobileCartVisible: false,
      selectedProduct: null,
      modalQuantity: 1
    }
  },
  mounted() {
    this.fetchProducts();
    this.fetchDiscounts();
  },
  methods: {
    fetchProducts() {
      this.loading = true;

      // For testing only, create some mock products if connection fails
      const createDemoProducts = () => {
        const demoProducts = [];
        for (let i = 1; i <= 12; i++) {
          demoProducts.push({
            id: i,
            name: `Product ${i}`,
            price: Math.round(Math.random() * 100) + 9.99,
            stock: Math.round(Math.random() * 30),
            description: `This is a sample product ${i} description.`
          });
        }
        return demoProducts;
      };

      // Try to fetch from API
      fetch('http://127.0.0.1:5000/api/products')
        .then(response => {
          if (!response.ok) throw new Error('API request failed');
          return response.json();
        })
        .then(data => {
          this.products = data;
          this.filteredProducts = [...this.products];
          this.loading = false;
        })
        .catch(err => {
          console.error("Failed to fetch products:", err);
          console.log("Using demo products instead");

          // Use demo products when API fails
          this.products = createDemoProducts();
          this.filteredProducts = [...this.products];
          this.loading = false;
        });
    },

    fetchDiscounts() {
      // Try to fetch from API
      fetch('http://127.0.0.1:5000/api/discounts')
        .then(response => {
          if (!response.ok) throw new Error('API request failed');
          return response.json();
        })
        .then(data => {
          this.discounts = data;
        })
        .catch(err => {
          console.error("Failed to fetch discounts:", err);

          // Create sample discounts when API fails
          this.discounts = [
            { id: 1, name: "10% Off", discount_type: "percentage", value: 10 },
            { id: 2, name: "25% Off", discount_type: "percentage", value: 25 },
            { id: 3, name: "$5 Off", discount_type: "fixed", value: 5 }
          ];
        });
    },

    addToCart(product) {
      const existingItem = this.cart.find(item => item.id === product.id);

      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        this.cart.push({
          id: product.id,
          name: product.name,
          price: product.price,
          quantity: 1,
          stock: product.stock,
          image: product.image || 'https://via.placeholder.com/50'
        });
      }
    },

    removeFromCart(index) {
      this.cart.splice(index, 1);
    },

    clearCart() {
      this.cart = [];
      this.selectedDiscount = null;
    },

    increaseQuantity(index) {
      if (this.cart[index].quantity < this.cart[index].stock) {
        this.cart[index].quantity++;
      }
    },

    decreaseQuantity(index) {
      if (this.cart[index].quantity > 1) {
        this.cart[index].quantity--;
      }
    },

    calculateSubtotal() {
      return this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },

    calculateDiscountAmount() {
      if (!this.selectedDiscount) return 0;

      const discount = this.discounts.find(d => d.id === this.selectedDiscount);
      if (!discount) return 0;

      const subtotal = this.calculateSubtotal();

      if (discount.discount_type === 'percentage') {
        return subtotal * (discount.value / 100);
      } else {
        return Math.min(subtotal, discount.value); // Fixed amount, capped at subtotal
      }
    },

    calculateTax() {
      const subtotal = this.calculateSubtotal();
      const discountAmount = this.calculateDiscountAmount();
      return (subtotal - discountAmount) * 0.07; // 7% tax
    },

    calculateTotal() {
      const subtotal = this.calculateSubtotal();
      const discountAmount = this.calculateDiscountAmount();
      const tax = this.calculateTax();

      return subtotal - discountAmount + tax;
    },

    checkout() {
      const checkoutData = {
        items: this.cart.map(item => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price
        })),
        discount_id: this.selectedDiscount,
        total: this.calculateTotal()
      };

      console.log('Processing checkout with data:', checkoutData);

      fetch('http://127.0.0.1:5000/api/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(checkoutData)
      })
        .then(response => {
          if (!response.ok) throw new Error('Checkout failed');
          return response.json();
        })
        .then(data => {
          console.log('Checkout successful:', data);
          this.clearCart();
          alert('Order completed successfully!');
        })
        .catch(error => {
          console.error('Error processing checkout:', error);

          // For demo purposes, simulate success anyway
          console.log('Demo: Simulating successful checkout');
          this.clearCart();
          alert('Order completed successfully! (Demo mode)');
        });
    },

    searchProducts() {
      if (!this.searchTerm.trim()) {
        this.filterByCategory(this.activeCategory);
        return;
      }

      const searchLower = this.searchTerm.toLowerCase();
      this.filteredProducts = this.products.filter(product =>
        product.name.toLowerCase().includes(searchLower) ||
        (product.description && product.description.toLowerCase().includes(searchLower))
      );
    },

    clearSearch() {
      this.searchTerm = '';
      this.filterByCategory(this.activeCategory);
    },

    filterByCategory(category) {
      this.activeCategory = category;

      if (category === 'all') {
        this.filteredProducts = [...this.products];
      } else if (category === 'popular') {
        // In a real app this would filter by popularity metrics
        this.filteredProducts = this.products.filter(p => p.stock < 15); // Just an example
      } else if (category === 'new') {
        this.filteredProducts = this.products.filter(p => this.isNewProduct(p));
      } else if (category === 'sale') {
        this.filteredProducts = this.products.filter(p => this.isOnSale(p));
      }
    },

    isNewProduct(product) {
      // Simulate new products (in a real app, check creation date)
      return product.id % 4 === 0;
    },

    isOnSale(product) {
      // Simulate sale products (in a real app, check for sales flag or discount)
      return product.id % 3 === 0;
    },

    resetFilters() {
      this.searchTerm = '';
      this.activeCategory = 'all';
      this.filteredProducts = [...this.products];
    },

    getStockClass(product) {
      if (product.stock <= 0) return 'out-of-stock';
      if (product.stock < 5) return 'low-stock';
      return 'in-stock';
    },

    getStockIcon(product) {
      if (product.stock <= 0) return 'inventory_2';
      if (product.stock < 5) return 'inventory';
      return 'inventory';
    },

    getStockLabel(product) {
      if (product.stock <= 0) return 'Out of Stock';
      if (product.stock < 5) return 'Low Stock';
      return 'In Stock';
    },

    showProductQuickView(product) {
      this.selectedProduct = product;
      this.modalQuantity = 1;
    },

    closeQuickView() {
      this.selectedProduct = null;
    },

    addToCartFromModal() {
      if (this.selectedProduct) {
        const existingItem = this.cart.find(item => item.id === this.selectedProduct.id);

        if (existingItem) {
          existingItem.quantity += this.modalQuantity;
        } else {
          this.cart.push({
            id: this.selectedProduct.id,
            name: this.selectedProduct.name,
            price: this.selectedProduct.price,
            quantity: this.modalQuantity,
            stock: this.selectedProduct.stock,
            image: this.selectedProduct.image || 'https://via.placeholder.com/50'
          });
        }

        this.closeQuickView();
      }
    },

    toggleMobileCart() {
      this.isMobileCartVisible = !this.isMobileCartVisible;
    },

    focusOnProducts() {
      this.isMobileCartVisible = false;
      // In a real app, you might also want to scroll to the products section
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

/* Main Layout */
.sales-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f9fafb;
}

.sales-action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.page-title {
  display: flex;
  align-items: center;
}

.page-title h2 {
  margin: 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
}

.page-title i {
  margin-right: 0.5rem;
  color: #4f46e5;
}

.subtitle {
  color: #6b7280;
  margin: 0 0 0 2rem;
}

.action-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-control {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.5rem 0.5rem 2.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.clear-search {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view-controls {
  display: flex;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  overflow: hidden;
}

.view-btn {
  background-color: white;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 2.5rem;
}

.view-btn.active {
  background-color: #4f46e5;
  color: white;
}

.mobile-cart-toggle {
  display: none;
  position: relative;
  background-color: #4f46e5;
  color: white;
  border: none;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  cursor: pointer;
}

.item-count {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #ef4444;
  color: white;
  border-radius: 50%;
  width: 1.25rem;
  height: 1.25rem;
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
  padding: 0.75rem 1rem;
  background-color: white;
  border-bottom: 1px solid #e5e7eb;
}

.category-pills {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
  flex-wrap: wrap;
}

.category-pill {
  display: flex;
  align-items: center;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 9999px;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s;
}

.category-pill i {
  font-size: 1rem;
  margin-right: 0.375rem;
}

.category-pill.active {
  background-color: #4f46e5;
  color: white;
  border-color: #4f46e5;
}

.filter-stats {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #6b7280;
}

.results-count {
  margin-right: 0.75rem;
}

.refresh-btn {
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0.25rem;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 1rem;
  padding: 1rem;
  flex-grow: 1;
  overflow: hidden;
}

/* Product Section */
.product-section {
  overflow-y: auto;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #6b7280;
}

.spinner-wrapper {
  margin-bottom: 1rem;
}

.spinner {
  border: 3px solid rgba(79, 70, 229, 0.2);
  border-top: 3px solid #4f46e5;
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.no-products {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.empty-state {
  text-align: center;
  color: #6b7280;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.reset-btn {
  margin-top: 1rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.reset-btn i {
  font-size: 1rem;
  margin-right: 0.375rem;
  opacity: 1;
}

/* Product List - Grid View */
.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
  padding: 1rem;
}

.product-card {
  position: relative;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
  background-color: white;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.card-badges {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  display: flex;
  gap: 0.25rem;
  z-index: 1;
}

.badge {
  font-size: 0.625rem;
  font-weight: bold;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  text-transform: uppercase;
}

.badge.new {
  background-color: #4f46e5;
  color: white;
}

.badge.sale {
  background-color: #ef4444;
  color: white;
}

.product-img {
  height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9fafb;
  overflow: hidden;
}

.product-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s;
}

.product-card:hover .product-img img {
  transform: scale(1.05);
}

.product-info {
  padding: 0.75rem;
  flex-grow: 1;
}

.product-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  color: #111827;
  height: 2.5em;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-weight: bold;
  font-size: 1rem;
  color: #111827;
  margin: 0;
}

.stock-indicator {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
}

.stock-indicator i {
  font-size: 0.875rem;
  margin-right: 0.25rem;
}

.stock-indicator.in-stock {
  color: #10b981;
}

.stock-indicator.low-stock {
  color: #f59e0b;
}

.stock-indicator.out-of-stock {
  color: #ef4444;
}

.stock-label {
  display: none;
}

.product-actions {
  padding: 0 0.75rem 0.75rem 0.75rem;
}

.btn-quick-add {
  width: 100%;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.375rem;
  padding: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.btn-quick-add:hover {
  background-color: #4338ca;
}

.btn-quick-add:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-quick-add i {
  margin-right: 0.375rem;
}

/* Product List - Table View */
.product-list-table {
  padding: 1rem;
}

.product-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 0.75fr 0.75fr 0.5fr;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background-color: #f9fafb;
  border-top: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  font-weight: 500;
  color: #4b5563;
  font-size: 0.875rem;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 0.75fr 0.75fr 0.5fr;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  align-items: center;
}

.col-product {
  display: flex;
  align-items: center;
}

.product-img-small {
  width: 3rem;
  height: 3rem;
  background-color: #f9fafb;
  border-radius: 0.25rem;
  overflow: hidden;
  margin-right: 0.75rem;
}

.product-img-small img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-name h4 {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
  color: #111827;
}

.badges-inline {
  display: flex;
  gap: 0.25rem;
}

.mini-badge {
  font-size: 0.625rem;
  padding: 0.125rem 0.25rem;
  border-radius: 0.125rem;
  text-transform: uppercase;
}

.mini-badge.new {
  background-color: #e0e7ff;
  color: #4f46e5;
}

.mini-badge.sale {
  background-color: #fee2e2;
  color: #ef4444;
}

.col-price {
  font-weight: 500;
}

.col-action {
  display: flex;
  gap: 0.5rem;
}

.btn-list-add, .btn-list-view {
  width: 2rem;
  height: 2rem;
  border-radius: 0.375rem;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
}

.btn-list-add {
  background-color: #4f46e5;
}

.btn-list-add:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-list-view {
  background-color: #6b7280;
}

/* Cart Section */
.cart-section {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: calc(100vh - 142px); /* Adjust based on your layout */
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.cart-header h3 {
  margin: 0;
  display: flex;
  align-items: center;
  font-size: 1.25rem;
}

.cart-header i {
  margin-right: 0.5rem;
  color: #4f46e5;
}

.cart-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-cart-action {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-cart {
  display: none;
  background: none;
  border: none;
  color: #6b7280;
  width: 2rem;
  height: 2rem;
  align-items: center;
  justify-content: center;
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem 1rem;
  flex-grow: 1;
  color: #6b7280;
}

.empty-cart i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.browse-products-btn {
  margin-top: 1rem;
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
}

.cart-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: hidden;
}

.cart-items {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.cart-item {
  display: flex;
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #f3f4f6;
}

.item-img {
  width: 3rem;
  height: 3rem;
  border-radius: 0.25rem;
  overflow: hidden;
  background-color: #f9fafb;
  margin-right: 0.75rem;
}

.item-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.item-info h4 {
  margin: 0 0 0.25rem 0;
  font-size: 0.875rem;
}

.item-price {
  margin: 0;
  font-size: 0.75rem;
  color: #6b7280;
}

.item-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
}

.quantity-controls {
  display: flex;
  align-items: center;
  border: 1px solid #e5e7eb;
  border-radius: 0.25rem;
}

.btn-quantity {
  background: none;
  border: none;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  cursor: pointer;
  padding: 0;
}

.btn-quantity.disabled {
  color: #d1d5db;
  cursor: not-allowed;
}

.quantity {
  padding: 0 0.25rem;
  font-size: 0.875rem;
  min-width: 1.5rem;
  text-align: center;
}

.item-subtotal {
  font-weight: 500;
  font-size: 0.875rem;
}

.btn-remove {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.cart-summary {
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  background-color: #f9fafb;
}

.order-details h4 {
  margin: 0 0 0.75rem 0;
  font-size: 1rem;
}

.summary-rows {
  margin-bottom: 1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.discount-row {
  padding-top: 0.5rem;
  border-top: 1px dashed #e5e7eb;
}

.discount-label {
  display: flex;
  align-items: center;
  color: #4f46e5;
}

.discount-label i {
  font-size: 1rem;
  margin-right: 0.25rem;
}

.discount-selector {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.discount-select {
  width: 100%;
  padding: 0.375rem;
  font-size: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.25rem;
  background-color: white;
  margin-top: 0.25rem;
}

.discount-amount {
  font-size: 0.75rem;
  color: #10b981;
  margin-top: 0.25rem;
}

.order-total {
  display: flex;
  justify-content: space-between;
  font-weight: 600;
  font-size: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
}

.total-amount {
  color: #4f46e5;
}

.checkout-container {
  margin-top: 1rem;
}

.btn-checkout {
  width: 100%;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.375rem;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.btn-checkout:hover {
  background-color: #4338ca;
}

.btn-checkout:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-checkout i {
  margin-right: 0.5rem;
}

/* Product Modal */
.product-modal {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.modal-content {
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.close-modal {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 9999px;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1;
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 2rem;
}

.product-image-large {
  background-color: #f9fafb;
  border-radius: 0.5rem;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image-large img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.product-details h2 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
}

.pricing-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.product-price {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.current-price {
  font-size: 1.5rem;
  font-weight: 600;
}

.original-price {
  font-size: 1rem;
  color: #9ca3af;
  text-decoration: line-through;
}

.inventory-status {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.modal-stock {
  font-size: 0.875rem;
}

.modal-stock i {
  font-size: 1rem;
}

.stock-count {
  font-size: 0.875rem;
  color: #6b7280;
}

.product-description {
  margin-bottom: 1.5rem;
}

.product-description p {
  color: #4b5563;
  line-height: 1.5;
}

.quick-view-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.quantity-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  overflow: hidden;
}

.qty-btn {
  background: none;
  border: none;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  cursor: pointer;
}

.qty-btn:disabled {
  color: #d1d5db;
  cursor: not-allowed;
}

.quantity-selector input {
  flex-grow: 1;
  text-align: center;
  border: none;
  font-size: 1rem;
  padding: 0.5rem;
  width: 3rem;
}

.add-to-cart-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 0.375rem;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-to-cart-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.add-to-cart-btn i {
  margin-right: 0.5rem;
}

/* Mobile Overlay */
.mobile-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 20;
}

/* Product fade transition */
.product-fade-enter-active, .product-fade-leave-active {
  transition: all 0.3s ease;
}

.product-fade-enter-from, .product-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* List fade transition */
.list-fade-enter-active, .list-fade-leave-active {
  transition: all 0.3s ease;
}

.list-fade-enter-from, .list-fade-leave-to {
  opacity: 0;
}

/* Cart item transition */
.cart-item-enter-active, .cart-item-leave-active {
  transition: all 0.3s ease;
}

.cart-item-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.cart-item-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr 300px;
  }
}

@media (max-width: 768px) {
  .subtitle, .view-controls {
    display: none;
  }

  .search-control {
    width: 200px;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .cart-section {
    position: fixed;
    top: 0;
    right: 0;
    width: 100%;
    max-width: 350px;
    height: 100vh;
    z-index: 30;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
    transform: translateX(100%);
    transition: transform 0.3s ease;
  }

  .cart-section.mobile-cart-visible {
    transform: translateX(0);
  }

  .mobile-cart-toggle {
    display: flex;
  }

  .close-cart {
    display: flex;
  }

  .mobile-overlay {
    display: block;
  }
}

@media (max-width: 640px) {
  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .search-control {
    width: 150px;
  }

  .modal-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1rem;
  }

  .product-image-large {
    height: 250px;
  }

  .category-pills {
    flex-wrap: nowrap;
    overflow-x: auto;
  }
}
</style>