import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import DashboardView from "../views/DashboardView.vue";
import AdminView from "../views/AdminView.vue";
import ProductView from "@/views/ProductView.vue";
import SalesView from "@/views/SalesView.vue";

const routes = [
  { path: "/", component: LoginView },
  { path: "/signup", component: SignupView },
  {
    path: "/dashboard",
    component: DashboardView,
    meta: { requiresAuth: true }, // Protect this route
  },
  {
    path: "/admin",
    component: AdminView,
    meta: { requiresAuth: true, requiresAdmin: true },
  },

  { path: "/products", component: ProductView, meta: { requiresAuth: true } },
  { path: "/sales", component: SalesView, meta: { requiresAuth: true } },
  {
    path: '/admin/products',
    name: 'products-management',
    component: () => import('../views/ProductManagement.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Route Guard for Authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  const role = localStorage.getItem("role");
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

  if (to.meta.requiresAuth && (!token || !isAuthenticated)) {
    next("/"); // Redirect to login if not authenticated
  } else if (to.meta.requiresAdmin && role !== "admin") {
    next("/dashboard"); // Redirect non-admins to dashboard
  } else {
    next();
  }
});


export default router;
