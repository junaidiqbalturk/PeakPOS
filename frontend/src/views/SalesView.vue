<template>
  <div class="pos-app">
    <!-- Left Sidebar Navigation -->
    <div class="sidebar">
      <div class="logo">
        <img style="margin: -83px;width: 191px;margin-left: -35px;margin-top: -71px;"
       src="../assets/peak-pos.png"
       alt="Logo">
      </div>
      <nav>
        <ul>
          <li class="active">
            <span class="icon">
              <i class="fas fa-shopping-cart"></i>
            </span>
            <span class="text">Sales</span>
          </li>
          <li>
            <span class="icon">
              <i class="fas fa-box"></i>
            </span>
            <span class="text">Products</span>
          </li>
          <li>
            <span class="icon">
              <i class="fas fa-chart-line"></i>
            </span>
            <span class="text">Reports</span>
          </li>
          <li>
            <span class="icon">
              <i class="fas fa-cog"></i>
            </span>
            <span class="text">Settings</span>
          </li>
        </ul>
      </nav>
      <div class="user-profile">
        <div class="avatar">
          <i class="fas fa-user"></i>
        </div>
        <div class="user-info">
          <span class="name">Admin User</span>
          <span class="role">Cashier</span>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Top Header -->
      <div class="top-header">
        <div class="search-container">
          <input type="text" v-model="searchTerm" @input="searchProducts" placeholder="Search for products..." />
          <button class="search-button">
            <i class="fas fa-search"></i>
          </button>
        </div>
        <div class="actions">
          <button class="btn-action">
            <i class="fas fa-sync"></i>
          </button>
          <button class="btn-action">
            <i class="fas fa-bell"></i>
            <span class="badge">3</span>
          </button>
        </div>
      </div>

      <!-- Content Grid -->
      <div class="content-grid">
        <!-- Product List -->
        <div class="product-section">
          <h3>Products</h3>
          <div class="product-list">
            <transition-group name="product-fade">
              <div class="product-card" v-for="product in filteredProducts" :key="product.id" @click="addToCart(product)">
                <div class="product-img">
                  <img :src="product.image" :alt="product.name" />
                </div>
                <div class="product-info">
                  <h4>{{ product.name }}</h4>
                  <p class="price">${{ product.price.toFixed(2) }}</p>
                  <p class="stock">In stock: {{ product.stock }}</p>
                </div>
                <div class="product-add">
                  <button class="btn-add">
                    <i class="fas fa-plus"></i>
                  </button>
                </div>
              </div>
            </transition-group>
          </div>
        </div>

        <!-- Cart Section -->
        <div class="cart-section">
          <h3>Cart</h3>
          <div class="cart-items">
            <transition-group name="cart-item">
              <div class="cart-item" v-for="(item, index) in cart" :key="item.id">
                <div class="item-info">
                  <h4>{{ item.name }}</h4>
                  <p>${{ item.price.toFixed(2) }}</p>
                </div>
                <div class="item-quantity">
                  <button class="btn-quantity" @click="decreaseQuantity(index)">
                    <i class="fas fa-minus"></i>
                  </button>
                  <span class="quantity">{{ item.quantity }}</span>
                  <button class="btn-quantity" @click="increaseQuantity(index)">
                    <i class="fas fa-plus"></i>
                  </button>
                </div>
                <div class="item-subtotal">
                  ${{ (item.price * item.quantity).toFixed(2) }}
                </div>
                <button class="btn-remove" @click="removeItem(index)">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </transition-group>
          </div>

          <!-- Cart Summary -->
          <div class="cart-summary">
            <div class="summary-item">
              <span>Subtotal</span>
              <span>${{ calculateSubtotal().toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span>Tax (7%)</span>
              <span>${{ calculateTax().toFixed(2) }}</span>
            </div>
            <div class="summary-item discount">
              <span>Discount</span>
              <div class="discount-input">
                <input type="number" v-model.number="discount" placeholder="0" min="0" max="100" />
                <span>%</span>
              </div>
            </div>
            <div class="summary-total">
              <span>Total</span>
              <span>${{ calculateTotal().toFixed(2) }}</span>
            </div>
            <button class="btn-checkout" @click="placeOrder">
              Place Order
              <i class="fas fa-arrow-right"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'POSSalesPage',
  data() {
    return {
      searchTerm: '',
      products: [],
      cart: [],
      discount: 0,
      filteredProducts: [],
    };
  },
  mounted() {
    this.loadProducts();
  },
  methods: {
    async loadProducts() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/products");
        this.products = response.data;
        this.filteredProducts = [...this.products];
      } catch (error) {
        console.error("Failed to load products:", error);
      }
    },
    searchProducts() {
      if (!this.searchTerm) {
        this.filteredProducts = [...this.products];
        return;
      }
      const term = this.searchTerm.toLowerCase();
      this.filteredProducts = this.products.filter(product =>
        product.name.toLowerCase().includes(term)
      );
    },
    addToCart(product) {
      const existingItem = this.cart.find(item => item.id === product.id);
      if (existingItem) {
        this.increaseQuantity(this.cart.indexOf(existingItem));
      } else {
        this.cart.push({ ...product, quantity: 1 });
      }
    },
    increaseQuantity(index) {
      const product = this.products.find(p => p.id === this.cart[index].id);
      if (this.cart[index].quantity < product.stock) {
        this.cart[index].quantity++;
      }
    },
    decreaseQuantity(index) {
      if (this.cart[index].quantity > 1) {
        this.cart[index].quantity--;
      } else {
        this.removeItem(index);
      }
    },
    removeItem(index) {
      this.cart.splice(index, 1);
    },
    calculateSubtotal() {
      return this.cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    },
    calculateTax() {
      return this.calculateSubtotal() * 0.07;
    },
    calculateTotal() {
      const subtotal = this.calculateSubtotal();
      const tax = this.calculateTax();
      const discountAmount = subtotal * (this.discount / 100);
      return subtotal + tax - discountAmount;
    },
async placeOrder() {
  if (this.cart.length === 0) {
    alert('Please add items to your cart first.');
    return;
  }

  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please login first.");
    return;
  }

  const orderPayload = {
    items: this.cart.map(item => ({
      product_id: item.id,
      quantity: item.quantity
    }))
  };

  try {
    await axios.post(
      "http://127.0.0.1:5000/api/orders",
      orderPayload,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json"
        }
      }
    );

    alert("✅ Order placed successfully!");
    this.cart = [];
    this.discount = 0;
  } catch (error) {
    console.error("Failed to place order", error);
    alert("❌ Failed to place order.");
  }
}


  },
};
</script>


<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

.pos-app {
  display: flex;
  height: 100vh;
  background-color: #f5f5f5;
}

/* Sidebar Styles */
.sidebar {
  width: 240px;
  background-color: #1976d2;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.logo {
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
}

.logo h2 {
  font-weight: 500;
  font-size: 20px;
}

nav ul {
  list-style: none;
}

nav ul li {
  padding: 12px 20px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

nav ul li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

nav ul li.active {
  background-color: rgba(255, 255, 255, 0.2);
  border-left: 4px solid white;
}

nav ul li .icon {
  width: 24px;
  margin-right: 10px;
  text-align: center;
}

.user-profile {
  margin-top: auto;
  padding: 20px;
  display: flex;
  align-items: center;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.avatar {
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-info .name {
  font-weight: 500;
  font-size: 14px;
}

.user-info .role {
  font-size: 12px;
  opacity: 0.7;
}

/* Main Content Styles */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.search-container {
  display: flex;
  width: 400px;
  position: relative;
}

.search-container input {
  width: 100%;
  padding: 10px 40px 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.search-container input:focus {
  border-color: #1976d2;
}

.search-button {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #777;
  cursor: pointer;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn-action {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f5f5f5;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: background-color 0.3s;
}

.btn-action:hover {
  background-color: #e0e0e0;
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #f44336;
  color: white;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Content Grid */
.content-grid {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.product-section {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.product-section h3 {
  margin-bottom: 20px;
  color: #333;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.product-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  position: relative;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.product-img {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f9f9f9;
}

.product-img img {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
}

.product-info {
  padding: 15px;
}

.product-info h4 {
  font-weight: 500;
  margin-bottom: 5px;
  color: #333;
}

.price {
  font-weight: 700;
  color: #1976d2;
  margin-bottom: 5px;
}

.stock {
  font-size: 12px;
  color: #777;
}

.product-add {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.btn-add {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #1976d2;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-add:hover {
  background-color: #1565c0;
}

/* Cart Section */
.cart-section {
  width: 380px;
  background-color: white;
  border-left: 1px solid #ddd;
  display: flex;
  flex-direction: column;
}

.cart-section h3 {
  padding: 20px;
  border-bottom: 1px solid #ddd;
  margin: 0;
  color: #333;
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.cart-item {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  position: relative;
}

.item-info {
  flex: 1;
}

.item-info h4 {
  font-weight: 500;
  font-size: 14px;
  margin-bottom: 5px;
  color: #333;
}

.item-info p {
  font-size: 13px;
  color: #777;
}

.item-quantity {
  display: flex;
  align-items: center;
  margin: 0 15px;
}

.btn-quantity {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #f5f5f5;
  border: none;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-quantity:hover {
  background-color: #e0e0e0;
}

.quantity {
  margin: 0 10px;
  font-weight: 500;
}

.item-subtotal {
  font-weight: 500;
  color: #1976d2;
  width: 60px;
  text-align: right;
}

.btn-remove {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  color: #f44336;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s;
}

.cart-item:hover .btn-remove {
  opacity: 1;
}

/* Cart Summary */
.cart-summary {
  padding: 20px;
  border-top: 1px solid #ddd;
  background-color: #f9f9f9;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.discount-input {
  display: flex;
  align-items: center;
}

.discount-input input {
  width: 60px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 5px;
  text-align: right;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
  font-weight: 700;
  font-size: 18px;
  color: #333;
}

.btn-checkout {
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-checkout i {
  margin-left: 10px;
}

.btn-checkout:hover {
  background-color: #1565c0;
}

/* Animations */
.product-fade-enter-active, .product-fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.product-fade-enter, .product-fade-leave-to {
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

/* Responsive */
@media screen and (max-width: 1200px) {
  .product-list {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}

@media screen and (max-width: 992px) {
  .sidebar {
    width: 60px;
    overflow: hidden;
  }

  .logo h2, .user-info, nav ul li .text {
    display: none;
  }

  .avatar {
    margin-right: 0;
  }

  .cart-section {
    width: 340px;
  }
}

@media screen and (max-width: 768px) {
  .search-container {
    width: 250px;
  }

  .cart-section {
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    height: 50%;
    z-index: 10;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    transform: translateY(0);
    transition: transform 0.3s;
  }

  .content-grid {
    flex-direction: column;
  }

  .product-section {
    padding-bottom: 50%;
  }
}
</style>