<template>
  <v-app>
    <!-- Left Sidebar -->
    <v-navigation-drawer app permanent dark color="#1E1E1E">
      <v-list dense>
        <v-list-item-title class="text-h6 white--text pl-4">PeakPOS</v-list-item-title>
        <v-divider></v-divider>
        <v-list-item link>
          <v-icon left>mdi-home</v-icon>
          <v-list-item-content>Home</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-icon left>mdi-chart-bar</v-icon>
          <v-list-item-content>Sales</v-list-item-content>
        </v-list-item>
        <v-list-group>
          <template v-slot:activator>
            <v-icon left>mdi-tshirt-crew</v-icon>
            <v-list-item-content>Products</v-list-item-content>
          </template>
          <v-list-item link>
            <v-list-item-content>Show All</v-list-item-content>
          </v-list-item>
          <v-list-item link>
            <v-list-item-content>T-Shirts</v-list-item-content>
          </v-list-item>
        </v-list-group>
        <v-list-item link>
          <v-icon left>mdi-file-chart</v-icon>
          <v-list-item-content>Reports</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-icon left>mdi-account-group</v-icon>
          <v-list-item-content>Customers</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-icon left>mdi-cog</v-icon>
          <v-list-item-content>Settings</v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-icon left>mdi-logout</v-icon>
          <v-list-item-content>Log Out</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main Content -->
    <v-main>
      <v-container fluid>
        <v-row>
          <!-- User Info -->
          <v-col cols="12">
            <h2 class="white--text">Welcome, {{ username }}</h2>
          </v-col>

          <!-- Dashboard Cards -->
          <v-col cols="12" md="3">
            <v-card class="pa-4 card-style" elevation="25" dark>
              <v-icon class="card-icon" large>mdi-cash</v-icon>
              <div class="text-h5 mt-2">$2,810.00</div>
              <div>Total Revenue</div>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="pa-4 card-style" elevation="25" dark>
              <v-icon class="card-icon" large>mdi-cart</v-icon>
              <div class="text-h5 mt-2">102</div>
              <div>Total Orders</div>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="pa-4 card-style" elevation="25" dark>
              <v-icon class="card-icon" large>mdi-account-group</v-icon>
              <div class="text-h5 mt-2">1,020</div>
              <div>New Customers</div>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="pa-4 card-style" elevation="25" dark>
              <v-icon class="card-icon" large>mdi-eye</v-icon>
              <div class="text-h5 mt-2">81,020</div>
              <div>Visitors Today</div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "DashboardView",
  data() {
    return {
      username: "TestUser", // Replace this with actual user data
    };
  },
};
</script>

<style>
.card-style {
  background: linear-gradient(135deg, #42a5f5, #478ed1);
  color: white;
  text-align: center;
  border-radius: 15px;
}
.card-icon {
  font-size: 50px;
  margin-bottom: 10px;
}
</style>
