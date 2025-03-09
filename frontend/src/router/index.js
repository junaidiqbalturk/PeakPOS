import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import DashboardView from "../views/DashboardView.vue";

const routes = [
  { path: "/", component: LoginView },
  { path: "/signup", component: SignupView },
  {
    path: "/dashboard",
    component: DashboardView,
    meta: { requiresAuth: true }, // Protect this route
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Route Guard for Authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

  if (to.meta.requiresAuth && (!token || !isAuthenticated)) {
    next("/"); // Redirect to login if not authenticated
  } else {
    next();
  }
});


export default router;
