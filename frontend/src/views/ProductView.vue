<template>
  <v-container fluid class="products-container">
    <v-row>
      <!-- Left Sidebar (Matches Dashboard) -->
      <v-col cols="2" class="left-nav-bar">
        <v-list dark>
          <v-list-item link to="/dashboard">
            <v-icon class="nav-icon">mdi-view-dashboard</v-icon>
            <v-list-item-title>Dashboard</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/products" active-class="active-link">
            <v-icon class="nav-icon">mdi-package-variant</v-icon>
            <v-list-item-title>Products</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/logout">
            <v-icon class="nav-icon">mdi-logout</v-icon>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-col>

      <!-- Main Content -->
      <v-col cols="10">
        <v-container>
          <h1 class="text-h4 font-weight-bold mb-4">Product Management</h1>

          <!-- Add Product Button -->
          <v-btn color="primary" dark @click="openAddDialog">+ Add Product</v-btn>

          <!-- Product Grid -->
          <v-row>
            <v-col v-for="product in products" :key="product.id" cols="12" sm="6" md="4" lg="3">
              <v-hover v-slot:default="{ isHovering }">
                <v-card
                  class="product-card"
                  :elevation="isHovering ? 12 : 4"
                  :class="{ 'hover-effect': isHovering }"
                >
                  <v-img :src="product.image || 'https://via.placeholder.com/150'" height="150px" contain></v-img>
                  <v-card-title>{{ product.name }}</v-card-title>
                  <v-card-subtitle class="text-primary text-bold">${{ product.price }}</v-card-subtitle>
                  <v-card-text>
                    <v-chip :color="product.stock > 0 ? 'green' : 'red'">
                      {{ product.stock > 0 ? `${product.stock} In Stock` : "Out of Stock" }}
                    </v-chip>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn color="blue" text @click="editProduct(product)">Edit</v-btn>
                    <v-btn color="red" text @click="deleteProduct(product.id)">Delete</v-btn>
                  </v-card-actions>
                </v-card>
              </v-hover>
            </v-col>
          </v-row>
        </v-container>
      </v-col>
    </v-row>

    <!-- Add/Edit Product Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ editingProduct ? 'Edit Product' : 'Add Product' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.name" label="Product Name"></v-text-field>
          <v-text-field v-model="form.price" label="Price" type="number"></v-text-field>
          <v-text-field v-model="form.stock" label="Stock" type="number"></v-text-field>
          <v-text-field v-model="form.image" label="Image URL"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn color="red" text @click="dialog = false">Cancel</v-btn>
          <v-btn color="green" text @click="saveProduct">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      products: [],
      dialog: false,
      editingProduct: null,
      form: { name: '', price: '', stock: '', image: '' },
    };
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/products');
        this.products = await response.json();
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },
    openAddDialog() {
      this.editingProduct = null;
      this.form = { name: '', price: '', stock: '', image: '' };
      this.dialog = true;
    },
    editProduct(product) {
      this.editingProduct = product;
      this.form = { ...product };
      this.dialog = true;
    },
    async saveProduct() {
      try {
        const method = this.editingProduct ? "PUT" : "POST";
        const url = this.editingProduct ? `http://127.0.0.1:5000/api/products/${this.editingProduct.id}` : "http://127.0.0.1:5000/api/products";
        await fetch(url, {
          method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.form),
        });
        this.dialog = false;
        this.fetchProducts();
      } catch (error) {
        console.error("Error saving product:", error);
      }
    },
    async deleteProduct(id) {
      try {
        await fetch(`http://127.0.0.1:5000/api/products/${id}`, { method: "DELETE" });
        this.fetchProducts();
      } catch (error) {
        console.error("Error deleting product:", error);
      }
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
/* Fix: Make Left Sidebar Fully Black */
.left-nav-bar {
  background-color: #121212 !important;
  color: white;
  min-height: 100vh;
  padding-top: 20px;
  padding-left: 10px;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

/* Fix: Ensure Sidebar Text & Icons Are White */
.nav-icon {
  color: white !important;
}

.v-list-item {
  color: white !important;
}

/* Product Cards */
.product-card {
  background: #232323;
  color: white;
  border-radius: 12px;
  transition: 0.3s;
  text-align: center;
}

.product-card:hover {
  transform: scale(1.05);
  box-shadow: 0px 5px 15px rgba(255, 255, 255, 0.2);
}

/* Hover Effect */
.hover-effect {
  background: linear-gradient(to right, #4a90e2, #9013fe);
  color: white;
}

/* Button Styling */
.v-btn {
  text-transform: none;
  font-weight: bold;
}

/* Fix: Background of the Page */
.products-container {
  background: linear-gradient(to bottom, #1e1e1e, #121212);
  color: white;
  min-height: 100vh;
  padding: 20px;
}
</style>
