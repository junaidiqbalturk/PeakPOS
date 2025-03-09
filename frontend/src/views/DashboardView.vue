<template>
  <v-app>
    <!-- Left Sidebar -->
    <v-navigation-drawer class="right-navbar" app right width="280" color="#f4f4f4" elevation="10">
  <v-list>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="text-h6 font-weight-bold">
          User Profile
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list-item>
      <v-list-item-icon>
        <v-avatar size="50">
          <v-img src="https://randomuser.me/api/portraits/men/45.jpg"></v-img>
        </v-avatar>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>{{ user ? user.email : "Loading..." }}</v-list-item-title>
        <v-list-item-subtitle>Admin</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list-item link>
      <v-icon left>mdi-account</v-icon>
      <v-list-item-content>My Profile</v-list-item-content>
    </v-list-item>

    <v-list-item link>
      <v-icon left>mdi-cog</v-icon>
      <v-list-item-content>Settings</v-list-item-content>
    </v-list-item>

    <v-list-item link @click="logout">
      <v-icon left color="red">mdi-logout</v-icon>
      <v-list-item-content class="text-red">Logout</v-list-item-content>
    </v-list-item>
  </v-list>
</v-navigation-drawer>


    <!-- Main Content -->
    <v-main class="dashboard-background">
      <v-container fluid>
        <v-row>
          <!-- User Info -->
          <v-col cols="12">
            <h2 class="white--text">Welcome, {{ user ? user.email : "Loading..." }}</h2>
          </v-col>

          <!-- Dashboard Cards -->
          <v-hover>
            <template v-slot:default="{ isHovering, props}">
              <v-col cols="12" md="3">
            <v-card  v-bind="props"
              :color="isHovering ? 'primary' : undefined" class="pa-4 card-style" elevation="24" loading dark>
              <v-icon class="card-icon" size="large" color="#ffb703">mdi-cash</v-icon>
              <div class="text-h5 mt-2">$2,810.00</div>
              <div>Total Revenue</div>
            </v-card>
          </v-col>
            </template>
          </v-hover>
          <v-col cols="12" md="3">
            <v-card class="pa-4 card-style" elevation="24" loading dark>
              <v-icon class="card-icon" size="large" color="#ffb703" >mdi-cart</v-icon>
              <div class="text-h5 mt-2">102</div>
              <div>Total Orders</div>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="pa-4 card-style" elevation="24" loading dark>
              <v-icon class="card-icon" size="large" color="#ffb703">mdi-account-group</v-icon>
              <div class="text-h5 mt-2">1,020</div>
              <div>New Customers</div>
            </v-card>
          </v-col>
          <v-col cols="12" md="3">
            <v-card class="pa-4 card-style" elevation="24" loading dark>
              <v-icon class="card-icon" size="large" color="#ffb703">mdi-eye</v-icon>
              <div class="text-h5 mt-2">81,020</div>
              <div>Visitors Today</div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getUserInfo } from "../services/api"; // Import API function

const user = ref(null);

const fetchUserData = async () => {
  try {
    user.value = await getUserInfo();
  } catch (error) {
    console.error("Failed to fetch user data:", error);
  }
};

onMounted(fetchUserData);
</script>


<style>
.card-style {
  background: linear-gradient(135deg, #023047, #219ebc) !important;
  color: white !important;
  text-align: center;
  border-radius: 15px;
}
.card-icon {
  font-size: 50px;
  margin-bottom: 10px;
}
.card-style:hover {
  transform: translateY(-5px); /* Lift effect */
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.3); /* Hover shadow */
  background: linear-gradient(to bottom right, #219ebc, #219ebc) !important; /* Slightly different hover gradient */
}
.dashboard-background {
  min-height: 100vh;
  background: linear-gradient(45deg, #dad7cd, #a3b18a);
/* Change for desired theme */
  color: black;
  padding: 20px;
}
.right-navbar {
  background: linear-gradient(to bottom, #1e3c72, #2a5298) !important;
  color: white !important;
  padding: 10px;
}
</style>
