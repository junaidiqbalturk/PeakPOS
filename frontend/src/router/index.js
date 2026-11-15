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

  // Aliases & Redirects to prevent dead links (Secured with RBAC metadata)
  { path: "/products", redirect: "/admin/products", meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"] } },
  { path: "/categories", redirect: "/admin/categories", meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"] } },
  { path: "/discounts", redirect: "/admin/settings/discounts", meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"] } },
  { path: "/inventory", redirect: "/admin/products", meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"] } },
  { path: "/enhanced-dashboard", redirect: "/dashboard", meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"] } },
  { path: "/settings", redirect: "/admin/settings", meta: { requiresAuth: true, roles: ["super_admin", "admin"] } },
  { path: "/admin", redirect: "/dashboard", meta: { requiresAuth: true, roles: ["super_admin", "admin", "manager"] } },

  // Catch-all 404 redirect
  { path: "/:pathMatch(.*)*", redirect: "/sales" }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

/**
 * Extracts cryptographically verified role claim from JWT token, with localStorage fallback.
 */
function getUserRole() {
  const token = localStorage.getItem("token");
  if (token) {
    try {
      const parts = token.split(".");
      if (parts.length === 3) {
        const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split("")
            .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
            .join("")
        );
        const payload = JSON.parse(jsonPayload);
        if (payload && payload.role) {
          return String(payload.role).toLowerCase();
        }
      }
    } catch (e) {
      // fallback
    }
  }
  return (localStorage.getItem("role") || "cashier").toLowerCase();
}

// Route Guard for Multi-Tenant Authentication, RBAC & Page Titles
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";
  const role = getUserRole();

  if (to.meta && to.meta.title) {
    document.title = `${to.meta.title} • PeakPOS Enterprise`;
  }

  // 1. Unauthenticated users trying to access protected routes -> Redirect to Login
  if (to.meta.requiresAuth && (!token || !isAuthenticated)) {
    next("/");
    return;
  }

  // 2. Already authenticated users visiting login/signup -> Redirect to home route
  if ((to.path === "/" || to.path === "/signup") && token && isAuthenticated) {
    if (role === "cashier") {
      next("/sales");
    } else {
      next("/dashboard");
    }
    return;
  }

  // 3. RBAC Permission Guard across all matched route records
  const matchedRoute = to.matched.slice().reverse().find((record) => record.meta && record.meta.roles);
  if (matchedRoute) {
    const allowedRoles = matchedRoute.meta.roles;
    if (role === "super_admin" || allowedRoles.includes(role)) {
      next();
    } else {
      console.warn(`[RBAC] Access denied for route "${to.path}" (Role: "${role}", Allowed: ${JSON.stringify(allowedRoles)})`);
      // Cashier is strictly restricted to /sales and /customers
      if (role === "cashier") {
        if (from.path === "/sales") {
          // Prevent redundant navigation if already on /sales
          next(false);
        } else {
          next({ path: "/sales", replace: true });
        }
      } else {
        if (from.path === "/dashboard") {
          next(false);
        } else {
          next({ path: "/dashboard", replace: true });
        }
      }
      return;
    }
  } else {
    next();
  }
});

export default router;
