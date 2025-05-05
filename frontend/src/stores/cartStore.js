import { defineStore } from 'pinia';
import axios from 'axios';

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    selectedDiscountId: null,
    discounts: []
  }),

  getters: {
    cartCount: (state) => state.items.length,

    itemCount: (state) => {
      return state.items.reduce((total, item) => total + item.quantity, 0);
    },

    subtotal: (state) => {
      return state.items.reduce((total, item) => {
        return total + (item.price * item.quantity);
      }, 0);
    },

    tax() {
      return this.subtotal * 0.07; // 7% tax rate
    },

    selectedDiscount: (state) => {
      if (!state.selectedDiscountId) return null;
      return state.discounts.find(d => d.id === state.selectedDiscountId);
    },

    discountAmount() {
      if (!this.selectedDiscount) return 0;

      if (this.selectedDiscount.discount_type === 'percentage') {
        return this.subtotal * (this.selectedDiscount.value / 100);
      } else if (this.selectedDiscount.discount_type === 'fixed') {
        return Math.min(this.selectedDiscount.value, this.subtotal);
      }

      return 0;
    },

    total() {
      return this.subtotal + this.tax - this.discountAmount;
    }
  },

  actions: {
    // Add a product to the cart
    addItem(product, quantity = 1) {
      const existingItem = this.items.find(item => item.id === product.id);

      if (existingItem) {
        // Increase quantity of existing item
        existingItem.quantity += quantity;
      } else {
        // Add new item
        this.items.push({
          id: product.id,
          name: product.name,
          price: product.price,
          image: product.image || '/placeholder.jpg',
          quantity,
          stock: product.stock
        });
      }

      this.saveToLocalStorage();
    },

    // Remove an item from the cart
    removeItem(index) {
      this.items.splice(index, 1);
      this.saveToLocalStorage();
    },

    // Update quantity of an item
    updateQuantity(index, newQuantity) {
      if (index >= 0 && index < this.items.length) {
        this.items[index].quantity = newQuantity;
        this.saveToLocalStorage();
      }
    },

    // Increase quantity of an item
    increaseQuantity(index) {
      if (index >= 0 && index < this.items.length) {
        const item = this.items[index];
        if (item.quantity < item.stock) {
          item.quantity++;
          this.saveToLocalStorage();
        }
      }
    },

    // Decrease quantity of an item
    decreaseQuantity(index) {
      if (index >= 0 && index < this.items.length) {
        if (this.items[index].quantity > 1) {
          this.items[index].quantity--;
          this.saveToLocalStorage();
        }
      }
    },

    // Clear the cart
    clearCart() {
      this.items = [];
      this.selectedDiscountId = null;
      this.saveToLocalStorage();
    },

    // Set a discount
    setDiscount(discountId) {
      this.selectedDiscountId = discountId;
      this.saveToLocalStorage();
    },

    // Load available discounts
    async loadDiscounts() {
      try {
        const response = await axios.get('/api/discounts');
        if (response.data) {
          this.discounts = response.data;
        }
      } catch (error) {
        console.error('Error loading discounts:', error);
      }
    },

    // Save cart to localStorage
    saveToLocalStorage() {
      localStorage.setItem('peak_pos_cart', JSON.stringify({
        items: this.items,
        selectedDiscountId: this.selectedDiscountId
      }));
    },

    // Load cart from localStorage
    loadFromLocalStorage() {
      const savedCart = localStorage.getItem('peak_pos_cart');
      if (savedCart) {
        try {
          const parsed = JSON.parse(savedCart);
          this.items = parsed.items || [];
          this.selectedDiscountId = parsed.selectedDiscountId;
        } catch (e) {
          console.error('Error parsing saved cart:', e);
          // If there's an error, clear the invalid data
          localStorage.removeItem('peak_pos_cart');
        }
      }
    },

    // Checkout process
    async checkout() {
      try {
        // Get the authentication token
        const token = localStorage.getItem('token');

        if (!token) {
          return { success: false, error: 'Authentication required' };
        }

        // Call your checkout endpoint
        const response = await axios.post('/api/checkout', {
          cart: this.items,
          discount_id: this.selectedDiscountId
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        // If successful, clear the cart
        if (response.data) {
          this.clearCart();
          return {
            success: true,
            order: response.data
          };
        }
      } catch (error) {
        console.error('Checkout error:', error);
        return {
          success: false,
          error: error.response?.data?.error || 'Error processing checkout'
        };
      }
    }
  }
});