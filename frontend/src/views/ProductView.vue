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



  </v-app>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getUserInfo } from "../services/api"; // Import API function
import { useRouter } from "vue-router";

const user = ref(null);

const fetchUserData = async () => {
  try {
    user.value = await getUserInfo();
  } catch (error) {
    console.error("Failed to fetch user data:", error);
  }
};

onMounted(fetchUserData);



const router = useRouter();

const logout = () => {
  localStorage.removeItem("token"); // Clear stored JWT token
  router.push("/"); // Redirect to login page
};
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
