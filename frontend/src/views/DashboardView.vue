<template>
  <v-app>
    <!-- Sidebar Navigation -->
    <v-navigation-drawer app permanent>
      <v-list>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link to="/products">
    <v-list-item-icon><v-icon>mdi-package-variant</v-icon></v-list-item-icon>
    <v-list-item-title>Products</v-list-item-title>
  </v-list-item>

  <v-list-item link to="/categories">
    <v-list-item-icon><v-icon>mdi-shape</v-icon></v-list-item-icon>
    <v-list-item-title>Categories</v-list-item-title>
  </v-list-item>

  <v-list-item link to="/orders">
    <v-list-item-icon><v-icon>mdi-cart</v-icon></v-list-item-icon>
    <v-list-item-title>Orders</v-list-item-title>
  </v-list-item>

  <v-list-item link to="/suppliers">
    <v-list-item-icon><v-icon>mdi-truck</v-icon></v-list-item-icon>
    <v-list-item-title>Suppliers</v-list-item-title>
  </v-list-item>

  <v-list-item link to="/inventory">
    <v-list-item-icon><v-icon>mdi-warehouse</v-icon></v-list-item-icon>
    <v-list-item-title>Inventory</v-list-item-title>
  </v-list-item>

  <v-list-item link to="/returns">
    <v-list-item-icon><v-icon>mdi-backup-restore</v-icon></v-list-item-icon>
    <v-list-item-title>Returns</v-list-item-title>
  </v-list-item>

  <v-list-item link to="/reports">
    <v-list-item-icon><v-icon>mdi-chart-box</v-icon></v-list-item-icon>
    <v-list-item-title>Reports</v-list-item-title>
  </v-list-item>
        <v-divider class="my-2"></v-divider>

  <v-list-item link to="/logout">
    <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
    <v-list-item-title>Logout</v-list-item-title>
  </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container fluid>
        <!-- Cards Row -->
        <v-row class="mt-4" dense>
          <v-col v-for="(card, index) in cards" :key="index" cols="12" md="3">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                class="pa-4 card-style"
                elevation="12"
                v-bind="props"
                :style="{ background: isHovering ? card.hoverGradient : card.gradient }"
              >
                <v-icon size="36" class="mb-2" color="white">{{ card.icon }}</v-icon>
                <div class="text-h5 font-weight-bold text-white">{{ card.value }}</div>
                <div class="text-caption text-white">{{ card.title }}</div>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>

        <!-- Sales Overview & Recent Orders Side-by-Side -->
        <v-row class="mt-6" dense>
          <!-- Sales Overview -->
          <v-col cols="12" md="6">
            <v-card class="pa-4 h-100" elevation="10">
              <v-card-title class="font-weight-bold">Sales Overview</v-card-title>
              <v-card-text>
                <v-skeleton-loader
                  type="image"
                  class="elevation-2 chart-placeholder"
                ></v-skeleton-loader>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Recent Orders -->
          <v-col cols="12" md="6">
            <v-card class="pa-4 h-100" elevation="10">
              <v-card-title class="font-weight-bold">Recent Orders</v-card-title>
              <v-card-text>
                <v-data-table
                  :headers="orderHeaders"
                  :items="recentOrders"
                  class="elevation-1"
                  dense
                  hide-default-footer
                >
                  <template v-slot:[`item.status`]="{ item }">
                    <v-chip
                      :color="item.status === 'Completed' ? 'green' : 'orange'"
                      dark
                      small
                    >
                      {{ item.status }}
                    </v-chip>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from "vue";

const cards = ref([
  {
    title: "Total Sales",
    value: "$12,400",
    icon: "mdi-cash-register",
    gradient: "linear-gradient(to right, #00b09b, #96c93d)",
    hoverGradient: "linear-gradient(to right, #96c93d, #00b09b)",
  },
  {
    title: "Total Products",
    value: "124",
    icon: "mdi-package-variant",
    gradient: "linear-gradient(to right, #2193b0, #6dd5ed)",
    hoverGradient: "linear-gradient(to right, #6dd5ed, #2193b0)",
  },
  {
    title: "Total Orders",
    value: "342",
    icon: "mdi-cart",
    gradient: "linear-gradient(to right, #ee0979, #ff6a00)",
    hoverGradient: "linear-gradient(to right, #ff6a00, #ee0979)",
  },
  {
    title: "Total Revenue",
    value: "$25,100",
    icon: "mdi-currency-usd",
    gradient: "linear-gradient(to right, #8e2de2, #4a00e0)",
    hoverGradient: "linear-gradient(to right, #4a00e0, #8e2de2)",
  },
]);

const orderHeaders = [
  { text: "Order ID", value: "id" },
  { text: "Customer", value: "customer" },
  { text: "Date", value: "date" },
  { text: "Total", value: "total" },
  { text: "Status", value: "status" },
];

const recentOrders = [
  { id: 1001, customer: "Ali Khan", date: "2025-04-10", total: "$250.00", status: "Completed" },
  { id: 1002, customer: "Sara Noor", date: "2025-04-09", total: "$180.00", status: "Pending" },
  { id: 1003, customer: "Hamza Ahmed", date: "2025-04-08", total: "$99.00", status: "Completed" },
];
</script>

<style scoped>
.card-style {
  border-radius: 12px;
  transition: 0.3s ease;
  cursor: pointer;
}
.card-style:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}
.chart-placeholder {
  height: 250px;
  border-radius: 12px;
  background: linear-gradient(to right, #f4f4f4, #e0e0e0);
}
</style>
