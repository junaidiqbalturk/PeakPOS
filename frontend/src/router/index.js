import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import DashboardView from "../views/DashboardView.vue";
import SalesView from "@/views/SalesView.vue";

const routes = [
  { path: "/", name: "Login", component: LoginView },
  { path: "/signup", name: "Signup", component: SignupView },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardView,
    meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"], title: "Executive Dashboard" },
  },
  {
    path: "/sales",
    name: "Sales",
    component: SalesView,
    meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager", "cashier"], title: "Point of Sale Counter" },
  },
  {
    path: "/reports",
    name: "Reports",
    component: () => import("../views/ReportsView.vue"),
    meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"], title: "Reports & Analytics" },
  },
  {
    path: "/customers",
    name: "Customers",
    component: () => import("../views/CustomerView.vue"),
    meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager", "cashier"], title: "Customer Ledger" },
  },
  {
    path: "/admin/products",
    name: "products-management",
    component: () => import("../views/ProductManagement.vue"),
    meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"], title: "Product Catalog" },
  },
  {
    path: "/admin/categories",
    name: "category-management",
    component: () => import("../views/CategoryManagement.vue"),
    meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"], title: "Category Management" },
  },
  {
    path: "/admin/settings",
    name: "Settings",
    component: () => import("../views/Settings.vue"),
    meta: { requiresAuth: true, roles: ["super_admin", "admin"], title: "Settings & Thermal Receipts" },
  },
  {
    path: "/admin/settings/discounts",
    name: "discount-management",
    component: () => import("../views/DiscountManagement.vue"),
    meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"], title: "Discounts & Promotions" },
  },

  // Aliases & Redirects to prevent dead links
  { path: "/products", redirect: "/admin/products" },
  { path: "/categories", redirect: "/admin/categories" },
  { path: "/discounts", redirect: "/admin/settings/discounts" },
  { path: "/inventory", redirect: "/admin/products" },
  { path: "/enhanced-dashboard", redirect: "/dashboard" },
  { path: "/settings", redirect: "/admin/settings" },
  { path: "/admin", redirect: "/dashboard" },

  // Catch-all 404 redirect
  { path: "/:pathMatch(.*)*", redirect: "/dashboard" }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Route Guard for Multi-Tenant Authentication, RBAC & Page Titles
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = (localStorage.getItem("role") || "cashier").toLowerCase();
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

  if (to.meta && to.meta.title) {
    document.title = `${to.meta.title} • PeakPOS Enterprise`;
  }

  if (to.meta.requiresAuth && (!token || !isAuthenticated)) {
    next("/");
    return;
  }

  // RBAC Permission Guard
  if (to.meta.roles && Array.isArray(to.meta.roles)) {
    if (role === "super_admin" || to.meta.roles.includes(role)) {
      next();
    } else {
      // Cashier redirected to sales register; others to sales if dashboard restricted
      if (role === "cashier") {
        next("/sales");
      } else {
        next("/dashboard");
      }
    }
  } else {
    next();
  }
});

export default router;
