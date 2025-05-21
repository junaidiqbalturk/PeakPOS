<template>
  <div class="dashboard-app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Sidebar - Left Navigation -->
    <div class="sidebar" :class="{ 'collapsed': isSidebarCollapsed, 'mobile-open': !isSidebarCollapsed && isMobileView }">
      <div class="sidebar-header">
        <div class="brand">
          <div class="logo-container">
            <div class="logo-icon">
              <i class="material-icons">storefront</i>
            </div>
            <div class="logo">Peak<span>POS</span></div>
          </div>
        </div>
        <button class="toggle-btn" @click="toggleSidebar">
          <i class="material-icons">{{ isSidebarCollapsed ? 'menu_open' : 'menu' }}</i>
        </button>
      </div>
      <div class="sidebar-content">
        <nav class="nav-menu">
          <router-link to="/enhanced-dashboard" class="nav-item active">
            <div class="nav-indicator"></div>
            <i class="material-icons">dashboard</i>
            <span class="nav-label">Dashboard</span>
            <span class="tooltip" v-if="isSidebarCollapsed">Dashboard</span>
          </router-link>

          <router-link to="/sales" class="nav-item">
            <div class="nav-indicator"></div>
            <i class="material-icons">point_of_sale</i>
            <span class="nav-label">Sales</span>
            <span class="tooltip" v-if="isSidebarCollapsed">Sales</span>
          </router-link>

          <router-link to="/admin/categories" class="nav-item">
            <div class="nav-indicator"></div>
            <i class="material-icons">category</i>
            <span class="nav-label">Category Management</span>
            <span class="tooltip" v-if="isSidebarCollapsed">Inventory</span>
          </router-link>
          <router-link to="/admin/products" class="nav-item">
            <div class="nav-indicator"></div>
            <i class="material-icons">inventory</i>
            <span class="nav-label">Products Managements</span>
            <span class="tooltip" v-if="isSidebarCollapsed">Inventory</span>
          </router-link>

          <router-link to="/customers" class="nav-item">
            <div class="nav-indicator"></div>
            <i class="material-icons">people</i>
            <span class="nav-label">Customers</span>
            <span class="tooltip" v-if="isSidebarCollapsed">Customers</span>
          </router-link>

          <router-link to="/reports" class="nav-item">
            <div class="nav-indicator"></div>
            <i class="material-icons">bar_chart</i>
            <span class="nav-label">Reports</span>
            <span class="tooltip" v-if="isSidebarCollapsed">Reports</span>
          </router-link>

          <router-link to="admin/settings" class="nav-item">
            <div class="nav-indicator"></div>
            <i class="material-icons">settings</i>
            <span class="nav-label">Settings</span>
            <span class="tooltip" v-if="isSidebarCollapsed">Settings</span>
          </router-link>
        </nav>
      </div>
      <div class="sidebar-footer">
        <div class="user-profile" @click="isUserMenuOpen = !isUserMenuOpen">
          <div class="avatar-wrapper">
            <div class="avatar">JD</div>
            <div class="status-indicator online"></div>
          </div>
          <div class="user-info">
            <div class="user-name">John Doe</div>
            <div class="user-role">Administrator</div>
          </div>
          <div class="user-menu-toggle">
            <i class="material-icons">{{ isUserMenuOpen ? 'keyboard_arrow_down' : 'keyboard_arrow_up' }}</i>
          </div>
          <span class="tooltip" v-if="isSidebarCollapsed">User Profile</span>
        </div>

        <!-- User Dropdown Menu -->
        <div class="user-dropdown" v-if="isUserMenuOpen">
          <div class="dropdown-item">
            <i class="material-icons">person</i>
            <span>My Profile</span>
          </div>
          <div class="dropdown-item">
            <i class="material-icons">settings</i>
            <span>Account Settings</span>
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item logout">
            <i class="material-icons">logout</i>
            <span>Logout</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- Top Header -->
      <div class="top-header" :class="{ 'header-shadow': scrolled }">
        <div class="header-left">
          <button class="mobile-toggle" @click="toggleSidebar">
            <i class="material-icons">menu</i>
          </button>
          <div class="page-info">
            <h1 class="page-title">Dashboard</h1>
            <div class="breadcrumb">
              <span>Home</span>
              <i class="material-icons">navigate_next</i>
              <span class="current">Dashboard</span>
            </div>
          </div>
        </div>

        <div class="header-middle">
          <div class="search-container">
            <i class="material-icons">search</i>
            <input type="text" class="search-input" placeholder="Search...">
            <div class="search-shortcut">/</div>
          </div>
        </div>

        <div class="header-right">
          <div class="date-display">
            <i class="material-icons">today</i>
            <span>{{ currentDate }}</span>
          </div>

          <div class="action-buttons">
            <button class="action-btn theme-btn" @click="isDarkMode = !isDarkMode">
              <i class="material-icons">{{ isDarkMode ? 'light_mode' : 'dark_mode' }}</i>
            </button>

            <button class="action-btn notification-btn" :class="{ 'has-notifications': hasNotifications }">
              <i class="material-icons">notifications</i>
              <span class="badge" v-if="notificationCount">{{ notificationCount }}</span>
            </button>

            <button class="action-btn help-btn">
              <i class="material-icons">help_outline</i>
            </button>
          </div>

          <div class="mobile-avatar" @click="isUserMenuOpen = !isUserMenuOpen">
            <div class="avatar small">JD</div>
          </div>
        </div>
      </div>

      <!-- Dashboard Content -->
      <div class="dashboard-content">
        <!-- Dashboard Summary -->
        <div class="dashboard-summary">
          <div class="welcome-message">
            <h2>Welcome back, {{ currentUser.name }}!</h2>
            <p>Here's what's happening with your business today.</p>
          </div>
          <div class="date-range-picker">
            <div class="date-range-inputs">
              <div class="date-field">
                <label for="start-date">From:</label>
                <input type="date" id="start-date" v-model="dateRange.startDate" @change="fetchAllDashboardData">
              </div>
              <div class="date-field">
                <label for="end-date">To:</label>
                <input type="date" id="end-date" v-model="dateRange.endDate" @change="fetchAllDashboardData">
              </div>
            </div>
            <div class="date-range-presets">
              <button class="date-preset-btn" @click="setDateRange('week')">Last 7 Days</button>
              <button class="date-preset-btn" @click="setDateRange('month')">Last 30 Days</button>
              <button class="date-preset-btn" @click="setDateRange('quarter')">Last 90 Days</button>
            </div>
          </div>
        </div>

        <!-- Modern Metrics Grid with 3D Cards (Updated with real data) -->
        <div class="metrics-grid">
          <!-- Sales Metric Card (Updated with real data from sales-summary) -->
          <div class="metric-card sales" :style="{ '--delay': '0.1s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">attach_money</i>
                </div>
                <div class="metric-trend" :class="salesTrend.direction">
                  <i class="material-icons trend-icon">{{ salesTrend.direction === 'positive' ? 'trending_up' : 'trending_down' }}</i>
                  <span class="trend-value">{{ salesTrend.value }}%</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Total Sales</div>
                <div class="metric-value">
                  <span class="value-prefix">$</span>
                  <span class="value-number">{{ formatCurrency(metrics.totalSales) }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in salesSparklineData"
                         :key="index"
                         :style="{ height: `${calculateSparklineHeight(value, maxSalesValue)}%`, animationDelay: `${index * 0.1}s` }"></div>
                  </div>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>

          <!-- Orders Metric Card (Updated with real data from sales-summary) -->
          <div class="metric-card orders" :style="{ '--delay': '0.2s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">shopping_bag</i>
                </div>
                <div class="metric-trend" :class="ordersTrend.direction">
                  <i class="material-icons trend-icon">{{ ordersTrend.direction === 'positive' ? 'trending_up' : 'trending_down' }}</i>
                  <span class="trend-value">{{ ordersTrend.value }}%</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Total Orders</div>
                <div class="metric-value">
                  <span class="value-number">{{ metrics.totalOrders }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in ordersSparklineData"
                         :key="index"
                         :style="{ height: `${calculateSparklineHeight(value, maxOrdersValue)}%`, animationDelay: `${index * 0.1}s` }"></div>
                  </div>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>

          <!-- Products Metric Card (Updated with real data from inventory-status) -->
          <div class="metric-card products" :style="{ '--delay': '0.3s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">category</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">inventory</i>
                  <span class="trend-value">{{ inventoryStats.total_stock || 0 }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Total Products</div>
                <div class="metric-value">
                  <span class="value-number">{{ inventoryStats.total_products || metrics.totalProduct }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in [50, 60, 70, 65, 80, 75, 90]"
                         :key="index"
                         :style="{ height: `${value}%`, animationDelay: `${index * 0.1}s` }"></div>
                  </div>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>

          <!-- Low Stock Items Card (Updated with real data from inventory-status) -->
          <div class="metric-card items" :style="{ '--delay': '0.4s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon warning">
                  <i class="material-icons">warning</i>
                </div>
                <div class="metric-trend negative">
                  <i class="material-icons trend-icon">trending_down</i>
                  <span class="trend-value">{{ inventoryStats.low_stock_count || 0 }}</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Low Stock Items</div>
                <div class="metric-value">
                  <span class="value-number">{{ inventoryStats.low_stock_count || 0 }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in [80, 70, 60, 50, 55, 45, 60]"
                         :key="index"
                         :style="{ height: `${value}%`, animationDelay: `${index * 0.1}s` }"></div>
                  </div>
                </div>
              </div>

              <!-- Interactive hover effect elements -->
              <div class="metric-card-backdrop"></div>
              <div class="metric-card-glow"></div>
            </div>
          </div>
        </div>

        <!-- Enhanced Charts Section -->
        <div class="charts-section">
          <!-- Sales Overview Chart with improved UI and real data -->
          <div class="chart-container sales-overview" :style="{ '--delay': '0.5s' }">
            <div class="chart-header">
              <div class="chart-title">
                <h3>Sales Overview</h3>
                <p>Total revenue over time</p>
              </div>
              <div class="chart-controls">
                <div class="time-filter">
                  <button
                    v-for="period in ['day', 'week', 'month', 'year']"
                    :key="period"
                    :class="{ active: salesPeriod === period }"
                    @click="changeSalesPeriod(period)"
                    class="period-btn"
                  >
                    {{ periodLabel(period) }}
                  </button>
                </div>
                <button class="chart-option-btn">
                  <i class="material-icons">more_vert</i>
                </button>
              </div>
            </div>
            <div class="chart-body">
              <canvas id="sales-chart" ref="salesChart"></canvas>
            </div>
          </div>

          <!-- New Section: Best Selling Products from best-selling-products API -->
          <div class="chart-container top-products" :style="{ '--delay': '0.6s' }">
            <div class="chart-header">
              <div class="chart-title">
                <h3>Best Selling Products</h3>
                <p>Top products by sales volume</p>
              </div>
              <button class="view-all-btn">View All Products</button>
            </div>
            <div class="top-products-grid">
              <div v-if="topProducts.length === 0" class="no-data-message">
                <i class="material-icons">info</i>
                <p>No product sales data available</p>
              </div>
              <div class="product-card" v-for="(product, index) in topProducts" :key="index">
                <div class="product-rank">{{ index + 1 }}</div>
                <div class="product-details">
                  <div class="product-name">{{ product.name }}</div>
                  <div class="product-category">{{ product.category }}</div>
                </div>
                <div class="product-stats">
                  <div class="product-stat">
                    <span class="stat-label">Sold</span>
                    <span class="stat-value">{{ product.total_sold }}</span>
                  </div>
                  <div class="product-stat">
                    <span class="stat-label">Revenue</span>
                    <span class="stat-value">${{ formatCurrency(product.total_revenue) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Low Stock Items Table from inventory-status API -->
        <div class="low-stock-section" :style="{ '--delay': '0.7s' }">
          <div class="section-header">
            <div class="section-title">
              <h3>Low Stock Alert</h3>
              <p>Items that need attention</p>
            </div>
            <button class="action-btn">
              <i class="material-icons">add_shopping_cart</i>
              <span>Order Stock</span>
            </button>
          </div>

          <div class="data-table-wrapper">
            <table class="data-table low-stock-table" v-if="lowStockItems.length > 0">
              <thead>
                <tr>
                  <th>Product Name</th>
                  <th>Category</th>
                  <th>Current Stock</th>
                  <th>Price</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in lowStockItems" :key="index">
                  <td>{{ item.name }}</td>
                  <td>{{ item.category }}</td>
                  <td>
                    <span class="stock-badge" :class="getStockLevelClass(item.quantity)">
                      {{ item.quantity }}
                    </span>
                  </td>
                  <td>${{ formatCurrency(item.price) }}</td>
                  <td>
                    <button class="table-action-btn restock-btn">
                      <i class="material-icons">add_circle</i>
                      <span>Restock</span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-else class="no-data-message">
              <i class="material-icons">check_circle</i>
              <p>No low stock items found</p>
            </div>
          </div>
        </div>

        <!-- Recent Orders Table (Existing implementation) -->
        <div class="recent-orders-section" :style="{ '--delay': '0.8s' }">
          <div class="section-header">
            <div class="section-title">
              <h3>Recent Orders</h3>
              <p>Latest transactions</p>
            </div>
            <button class="view-all-btn">View All Orders</button>
          </div>

          <div class="data-table-wrapper">
            <table class="data-table orders-table" v-if="recentOrders.length > 0">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Product Name</th>
                  <th>Amount</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(order, index) in recentOrders" :key="index">
                  <td>#{{ order.id }}</td>
                  <td>{{ order.customer }}</td>
                  <td>${{ formatCurrency(order.amount) }}</td>
                  <td>
                    <span class="status-badge" :class="order.status">{{ order.status }}</span>
                  </td>
                  <td>
                    <button class="table-action-btn">
                      <i class="material-icons">visibility</i>
                      <span>View</span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-else class="no-data-message">
              <i class="material-icons">info</i>
              <p>No recent orders found</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  data() {
    return {
      // Dark mode settings
      isDarkMode: false,

      // Sidebar states
      isSidebarCollapsed: false,
      isMobileView: false,
      isUserMenuOpen: false,

      // Header states
      scrolled: false,

      // Chart related
      salesChart: null,
      salesPeriod: 'week',

      // Date ranges
      dateRange: {
        startDate: this.getDefaultStartDate(),
        endDate: this.getDefaultEndDate()
      },

      // Metrics - updated from API
      metrics: {
        totalSales: 0,
        totalOrders: 0,
        totalProduct: 0,
        itemsSold: 0
      },

      // Sales trends (calculated from real data)
      salesTrend: {
        direction: 'positive',
        value: 0
      },
      ordersTrend: {
        direction: 'positive',
        value: 0
      },
      //get User info
      currentUser:{
        name: "John",
        role: "Administrator"
      },

      // Data for mini-charts (sparklines)
      salesSparklineData: [],
      ordersSparklineData: [],
      maxSalesValue: 1,
      maxOrdersValue: 1,

      // Data from API endpoints
      dailySalesData: [],
      topProducts: [],
      lowStockItems: [],
      inventoryStats: {
        total_products: 0,
        total_stock: 0,
        avg_price: 0,
        low_stock_count: 0
      },

      // Recent orders
      recentOrders: [],
      isLoadingData: false
    };
  },

  computed: {
    currentDate() {
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
      return new Date().toLocaleDateString('en-US', options);
    },

    hasNotifications() {
      return this.notificationCount > 0;
    },

    notificationCount() {
      // Sample notification count
      return 3;
    }
  },

  mounted() {
    // Initialize charts and load data
    this.fetchCurrentUser();
    this.$nextTick(() => {
      if (this.$refs.salesChart) {
        this.createSimpleChart();
      }
      this.fetchAllDashboardData();
      this.setupCardHoverEffects();
    });

    // Set initial responsive states
    window.initialWidth = window.innerWidth;
    this.isMobileView = window.innerWidth < 768;

    // For sidebar state
    if (window.innerWidth < 1024) {
      this.isSidebarCollapsed = true;
      localStorage.setItem('sidebarCollapsed', 'true');
    } else {
      const storedSidebarState = localStorage.getItem('sidebarCollapsed');
      if (storedSidebarState !== null) {
        this.isSidebarCollapsed = storedSidebarState === 'true';
      } else {
        this.isSidebarCollapsed = false;
        localStorage.setItem('sidebarCollapsed', 'false');
      }
    }

    // Load dark mode preference
    const darkModeSetting = localStorage.getItem('darkMode');
    if (darkModeSetting !== null) {
      this.isDarkMode = darkModeSetting === 'true';
    }

    // Add event listeners
    window.addEventListener('resize', this.handleResize);
    document.addEventListener('click', this.handleClickOutside);
    document.addEventListener('keydown', this.handleKeyShortcuts);
    window.addEventListener('scroll', this.handleScroll);
  },

  beforeUnmount() {
    // Clean up
    if (this.salesChart) {
      this.salesChart.destroy();
    }

    window.removeEventListener('resize', this.handleResize);
    document.removeEventListener('click', this.handleClickOutside);
    document.removeEventListener('keydown', this.handleKeyShortcuts);
    window.removeEventListener('scroll', this.handleScroll);
  },

  methods: {
    async fetchCurrentUser() {
    try {
      // Get the token (assuming you use JWT authentication)
      const token = localStorage.getItem("token");

      // Set up request headers
      const config = token ? {
        headers: {
          Authorization: `Bearer ${token}`
        }
      } : {};

      // Make the API call to your user endpoint
      const response = await axios.get("http://localhost:5000/api/auth/user/me", config);

      // Update the user data if the request was successful
      if (response.data) {
        // Update based on your API's response structure
        // Adjust the property names to match your actual API response
        this.currentUser = {
          name: response.data.username || response.data.name || "Guest",
          role: response.data.role || "User"
        };
      }
    } catch (error) {
      console.error("Failed to fetch user data:", error);
      // Keep the default values if the request fails
    }
  },
    // Method to get default start date (7 days ago)
    getDefaultStartDate() {
      const date = new Date();
      date.setDate(date.getDate() - 7);
      return date.toISOString().split('T')[0]; // Format as YYYY-MM-DD
    },

    // Method to get default end date (today)
    getDefaultEndDate() {
      return new Date().toISOString().split('T')[0]; // Format as YYYY-MM-DD
    },

    // Format currency with commas and correct decimal places
    formatCurrency(value) {
      if (value === undefined || value === null) return '0.00';
      return parseFloat(value).toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    },

    // Calculate sparkline bar height with proper bounds checking
    calculateSparklineHeight(value, maxValue) {
      if (!value || !maxValue || maxValue <= 0) return 0;
      // Ensure minimum height of 10% and maximum of 100%
      return Math.max(10, Math.min(100, (value / maxValue) * 100));
    },

    // Get appropriate CSS class for stock level indicator
    getStockLevelClass(quantity) {
      if (quantity <= 5) return 'critical';
      if (quantity <= 10) return 'warning';
      return 'normal';
    },

    // Method to fetch all dashboard data
    async fetchAllDashboardData() {
      this.isLoadingData = true;

      try {
        // Fetch data from all reporting endpoints in parallel
        await Promise.all([
          this.fetchSalesSummary(),
          this.fetchBestSellingProducts(),
          this.fetchInventoryStatus(),
          this.loadMetrics() // Also load regular metrics as fallback
        ]);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        this.isLoadingData = false;
      }
    },

    // Fetch sales summary from the report API
    async fetchSalesSummary() {
      try {
        const token = localStorage.getItem("token");
        const config = token ? {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        } : {};

        const response = await axios.get("http://localhost:5000/api/sales-summary", {
          ...config,
          params: {
            start_date: this.dateRange.startDate,
            end_date: this.dateRange.endDate
          }
        });

        if (response.data) {
          // Update metrics from API data
          this.metrics.totalSales = response.data.total_revenue || 0;
          this.metrics.totalOrders = response.data.total_orders || 0;

          // Process daily data
          if (response.data.daily_data && response.data.daily_data.length > 0) {
            this.dailySalesData = response.data.daily_data;

            // Update sparkline data for mini-charts
            this.salesSparklineData = this.dailySalesData.map(day => day.revenue);
            this.ordersSparklineData = this.dailySalesData.map(day => day.orders);

            // Calculate max values for scaling
            this.maxSalesValue = Math.max(...this.salesSparklineData, 1);
            this.maxOrdersValue = Math.max(...this.ordersSparklineData, 1);

            // Update chart with real data
            this.updateSalesChartWithRealData(this.dailySalesData);

            // Calculate trend indicators
            this.calculateTrends(this.dailySalesData);
          }
        }
      } catch (error) {
        console.error("Failed to fetch sales summary:", error);
      }
    },

    // Calculate trend indicators from daily data
    calculateTrends(dailyData) {
      if (!dailyData || dailyData.length < 4) {
        // Not enough data for meaningful trend
        return;
      }

      // Calculate sales trend (using last 3 days vs previous 3 days)
      const recentSales = dailyData.slice(-3).reduce((sum, day) => sum + day.revenue, 0);
      const prevSales = dailyData.slice(-6, -3).reduce((sum, day) => sum + day.revenue, 0);

      if (prevSales > 0) {
        const salesTrendPercent = ((recentSales - prevSales) / prevSales) * 100;
        this.salesTrend.value = Math.abs(salesTrendPercent).toFixed(1);
        this.salesTrend.direction = salesTrendPercent >= 0 ? 'positive' : 'negative';
      }

      // Calculate orders trend
      const recentOrders = dailyData.slice(-3).reduce((sum, day) => sum + day.orders, 0);
      const prevOrders = dailyData.slice(-6, -3).reduce((sum, day) => sum + day.orders, 0);

      if (prevOrders > 0) {
        const ordersTrendPercent = ((recentOrders - prevOrders) / prevOrders) * 100;
        this.ordersTrend.value = Math.abs(ordersTrendPercent).toFixed(1);
        this.ordersTrend.direction = ordersTrendPercent >= 0 ? 'positive' : 'negative';
      }
    },

    // Fetch best selling products
    async fetchBestSellingProducts() {
      try {
        const token = localStorage.getItem("token");
        const config = token ? {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        } : {};

        const response = await axios.get("http://localhost:5000/api/best-selling-products", {
          ...config,
          params: {
            limit: 5 // Get top 5 products
          }
        });

        if (response.data && Array.isArray(response.data)) {
          this.topProducts = response.data;
        }
      } catch (error) {
        console.error("Failed to fetch best selling products:", error);
        this.topProducts = [];
      }
    },

    // Fetch inventory status
    async fetchInventoryStatus() {
      try {
        const token = localStorage.getItem("token");
        const config = token ? {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        } : {};

        const response = await axios.get("http://localhost:5000/api/inventory-status", {
          ...config,
          params: {
            threshold: 10 // Set low stock threshold
          }
        });

        if (response.data) {
          // Update inventory statistics
          this.inventoryStats = response.data.inventory_stats || {
            total_products: 0,
            total_stock: 0,
            avg_price: 0,
            low_stock_count: 0
          };

          // Update low stock items list
          this.lowStockItems = response.data.low_stock_products || [];
        }
      } catch (error) {
        console.error("Failed to fetch inventory status:", error);
        this.inventoryStats = {
          total_products: 0,
          total_stock: 0,
          avg_price: 0,
          low_stock_count: 0
        };
        this.lowStockItems = [];
      }
    },

    // Load regular metrics data for fallback
    async loadMetrics() {
      try {
        // Check if user is authenticated
        const token = localStorage.getItem("token");
        const config = token ? {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        } : {};

        try {
          const [productsRes, ordersRes] = await Promise.all([
            axios.get("http://localhost:5000/api/products", config),
            axios.get("http://localhost:5000/api/admin/orders", config)
          ]);

          // Update metrics as fallback
          if (productsRes.data && Array.isArray(productsRes.data)) {
            // Only set if not already set by inventory status
            if (!this.inventoryStats.total_products) {
              this.metrics.totalProduct = productsRes.data.length;
            }
          }

          const products = productsRes.data;

this.recentOrders = ordersRes.data.slice(0, 5).map(order => {
  const firstItem = order.items[0];  // assuming at least one item per order
  const product = firstItem
    ? products.find(p => p.id === firstItem.product_id)
    : null;

  return {
    id: order.order_id || Math.floor(Math.random() * 10000),
    customer: product ? product.name : 'Unknown Product',
    amount: order.total_price || 0,
    status: order.status || 'completed'
  };
});
        } catch (apiError) {
          console.error("API Error:", apiError);
        }
      } catch (err) {
        console.error("Error loading metrics:", err);
      }
    },

    // Setup hover effects for metric cards
    setupCardHoverEffects() {
      this.$nextTick(() => {
        document.querySelectorAll('.metric-card-inner').forEach(card => {
          card.addEventListener('mouseenter', function() {
            this.querySelector('.metric-card-backdrop').style.opacity = 1;
            this.querySelector('.metric-card-glow').style.opacity = 0.8;
          });

          card.addEventListener('mouseleave', function() {
            this.querySelector('.metric-card-backdrop').style.opacity = 0;
            this.querySelector('.metric-card-glow').style.opacity = 0;
          });

          card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            this.querySelector('.metric-card-glow').style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 60%)`;
          });
        });
      });
    },

    // Handle scroll events
    handleScroll() {
      this.scrolled = window.scrollY > 10;
    },

    // Change sales period and update chart
    changeSalesPeriod(period) {
      // Store the current period
      this.salesPeriod = period;

      // Clean up existing chart
      if (this.salesChart) {
        this.salesChart.destroy();
        this.salesChart = null;
      }

      // Wait for next tick to ensure DOM is updated
      this.$nextTick(() => {
        this.createSimpleChart();

        // If we have real data, update the chart
        if (this.dailySalesData && this.dailySalesData.length > 0) {
          this.updateSalesChartWithRealData(this.dailySalesData);
        }
      });
    },

    // FIXED: Chart rendering method that avoids errors
    createSimpleChart() {
      try {
        // Get the canvas element
        const canvas = this.$refs.salesChart;
        if (!canvas) return;

        // Create basic chart data based on period
        let labels = [];
        let values = [];

        switch(this.salesPeriod) {
          case 'day':
            labels = ['9AM', '12PM', '3PM', '6PM', '9PM'];
            values = [750, 1200, 980, 1120, 1300];
            break;
          case 'month':
            labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
            values = [22000, 19500, 23400, 25100];
            break;
          case 'year':
            labels = ['Jan', 'Mar', 'May', 'Jul', 'Sep', 'Nov'];
            values = [65000, 73000, 75000, 86000, 81000, 110000];
            break;
          case 'week':
          default:
            labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
            values = [4200, 3800, 4100, 4500, 5200, 6100, 5800];
            break;
        }

        // Create very minimal chart with NO fill to avoid clip errors
        this.salesChart = new Chart(canvas, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Sales',
              data: values,
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              fill: false, // IMPORTANT: Set fill to false to avoid the clip error
              tension: 0.1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            events: [], // Disable events to prevent the first error
            animation: { duration: 0 }, // Disable animations
            plugins: {
              legend: { display: false }
            }
          }
        });
      } catch (err) {
        console.error('Chart initialization error:', err);
      }
    },

    // Update sales chart with real data
    updateSalesChartWithRealData(dailyData) {
      if (!this.salesChart || !dailyData || dailyData.length === 0) return;

      try {
        // Extract and format data according to selected period
        let labels = [];
        let values = [];

        switch (this.salesPeriod) {
          case 'day':
          {
            // For day view, use hours (if available) or just one day's data
            if (dailyData[0].hourly_data) {
              const hours = dailyData[0].hourly_data;
              labels = hours.map(hour => `${hour.hour}:00`);
              values = hours.map(hour => hour.revenue);
            } else {
              // Get the most recent day
              const day = dailyData[dailyData.length - 1];
              labels = [new Date(day.date).toLocaleDateString()];
              values = [day.revenue];
            }
          }
            break;

          case 'week':
          {
            const weekData = dailyData.slice(-7);// Last 7 days
            labels = weekData.map(day => {
              const date = new Date(day.date);
              return date.toLocaleDateString('en-US', { weekday: 'short' });
            });
            values = weekData.map(day => day.revenue);
          }
            break;

          case 'month':
          {
            // Group by week
            const monthData = this.groupDataByWeek(dailyData);
            labels = monthData.map(week => week.label);
            values = monthData.map(week => week.revenue);
          }
            break;

          case 'year':
          {
            // Group by month
            const yearData = this.groupDataByMonth(dailyData);
            labels = yearData.map(month => month.label);
            values = yearData.map(month => month.revenue);
          }
            break;

          default:
            // Default to showing all days
            labels = dailyData.map(day => {
              const date = new Date(day.date);
              return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            });
            values = dailyData.map(day => day.revenue);
        }

        // Update chart data
        this.salesChart.data.labels = labels;
        this.salesChart.data.datasets[0].data = values;

        // Update chart options for better interactivity
        this.salesChart.options = {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.7)',
              titleColor: '#fff',
              bodyColor: '#fff',
              displayColors: false,
              callbacks: {
                label: function(context) {
                  return `$${context.raw.toFixed(2)}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              }
            },
            y: {
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              },
              ticks: {
                callback: function(value) {
                  return '$' + value;
                }
              }
            }
          }
        };

        // Update chart
        this.salesChart.update();
      } catch (error) {
        console.error('Error updating chart with real data:', error);
      }
    },

    // Helper methods for data aggregation
    groupDataByWeek(dailyData) {
      // Group by week
      const weeks = [];
      const numWeeks = 4; // Show last 4 weeks

      for (let i = 0; i < numWeeks; i++) {
        const startIndex = dailyData.length - ((i + 1) * 7);
        const endIndex = dailyData.length - (i * 7);

        // Make sure we have data for this week
        if (startIndex >= 0) {
          const weekData = dailyData.slice(Math.max(0, startIndex), endIndex);
          const weekSum = weekData.reduce((sum, day) => sum + day.revenue, 0);

          weeks.unshift({
            label: `Week ${numWeeks - i}`,
            revenue: weekSum
          });
        }
      }

      return weeks;
    },

    groupDataByMonth(dailyData) {
      // Group by month
      const monthsMap = {};

      dailyData.forEach(day => {
        const date = new Date(day.date);
        const monthKey = `${date.getFullYear()}-${date.getMonth() + 1}`;
        const monthLabel = date.toLocaleDateString('en-US', { month: 'short' });

        if (!monthsMap[monthKey]) {
          monthsMap[monthKey] = {
            label: monthLabel,
            revenue: 0
          };
        }

        monthsMap[monthKey].revenue += day.revenue;
      });

      // Convert to array and sort chronologically
      return Object.values(monthsMap);
    },

    // Set date range based on period
    setDateRange(period) {
      const today = new Date();
      const endDate = new Date(today);
      let startDate = new Date(today);

      switch(period) {
        case 'day':
          // Just today
          break;
        case 'week':
          // Last 7 days
          startDate.setDate(today.getDate() - 7);
          break;
        case 'month':
          // Last 30 days
          startDate.setDate(today.getDate() - 30);
          break;
        case 'quarter':
          // Last 90 days
          startDate.setDate(today.getDate() - 90);
          break;
        case 'year':
          // Last 365 days
          startDate.setDate(today.getDate() - 365);
          break;
        default:
          // Default to week
          startDate.setDate(today.getDate() - 7);
      }

      this.dateRange.startDate = startDate.toISOString().split('T')[0];
      this.dateRange.endDate = endDate.toISOString().split('T')[0];

      // Fetch new data with updated date range
      this.fetchAllDashboardData();
    },

    // Toggle sidebar open/closed
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
      localStorage.setItem('sidebarCollapsed', this.isSidebarCollapsed);
    },

    // Handle window resize
    handleResize() {
      this.isMobileView = window.innerWidth < 768;

      // On small screens, always collapse sidebar
      if (window.innerWidth < 1024) {
        this.isSidebarCollapsed = true;
      }
    },

    // Handle clicks outside the user menu
    handleClickOutside(e) {
      const userMenu = document.querySelector('.user-profile');
      const userDropdown = document.querySelector('.user-dropdown');

      if (userMenu && !userMenu.contains(e.target) &&
          userDropdown && !userDropdown.contains(e.target) &&
          this.isUserMenuOpen) {
        this.isUserMenuOpen = false;
      }
    },

    // Handle keyboard shortcuts
    handleKeyShortcuts(e) {
      // '/' key to focus search
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        document.querySelector('.search-input').focus();
      }
    },

    // Period label formatter
    periodLabel(period) {
      // Convert period to a properly formatted label
      switch(period) {
        case 'day':
          return 'Today';
        case 'week':
          return 'This Week';
        case 'month':
          return 'This Month';
        case 'quarter':
          return 'This Quarter';
        case 'year':
          return 'This Year';
        default:
          return period.charAt(0).toUpperCase() + period.slice(1);
      }
    }
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

/* Root Variables - Light Theme */
:root {
  /* Primary Colors */
  --primary-50: #e3f2fd;
  --primary-100: #bbdefb;
  --primary-200: #90caf9;
  --primary-300: #64b5f6;
  --primary-400: #42a5f5;
  --primary-500: #2196f3;
  --primary-600: #1e88e5;
  --primary-700: #1976d2;
  --primary-800: #1565c0;
  --primary-900: #0d47a1;

  /* Accent Colors */
  --success-color: #4caf50;
  --success-light: #e8f5e9;
  --warning-color: #ff9800;
  --warning-light: #fff3e0;
  --danger-color: #f44336;
  --danger-light: #ffebee;
  --info-color: #2196f3;
  --info-light: #e3f2fd;
  --purple-color: #9c27b0;
  --purple-light: #f3e5f5;

  /* Neutral Colors */
  --neutral-50: #fafafa;
  --neutral-100: #f5f5f5;
  --neutral-200: #eeeeee;
  --neutral-300: #e0e0e0;
  --neutral-400: #bdbdbd;
  --neutral-500: #9e9e9e;
  --neutral-600: #757575;
  --neutral-700: #616161;
  --neutral-800: #424242;
  --neutral-900: #212121;

  /* Layout Colors */
  --bg-color: #f8f9fa;
  --card-bg: #ffffff;
  --sidebar-bg: #ffffff;
  --header-bg: #ffffff;

  /* Text Colors */
  --text-primary: #263238;
  --text-secondary: #546e7a;
  --text-disabled: #9e9e9e;
  --text-hint: #78909c;

  /* Border & Shadow */
  --border-color: #e0e0e0;
  --divider-color: #eeeeee;
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.04), 0 2px 4px rgba(0,0,0,0.06);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.04), 0 4px 6px rgba(0,0,0,0.06);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.04), 0 10px 10px rgba(0,0,0,0.06);

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Sizing & Layout */
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 80px;
  --top-header-height: 70px;
  --mobile-breakpoint: 768px;
  --tablet-breakpoint: 1024px;

  /* Motion & Transitions */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --spacing-3xl: 64px;
}

/* Dark Theme Variables */
.dark-mode {
  --bg-color: #121212;
  --card-bg: #1e1e1e;
  --sidebar-bg: #1e1e1e;
  --header-bg: #1e1e1e;

  --text-primary: #e0e0e0;
  --text-secondary: #9e9e9e;
  --text-disabled: #616161;
  --text-hint: #757575;

  --border-color: #333333;
  --divider-color: #2c2c2c;

  --shadow-sm: 0 2px 4px rgba(0,0,0,0.2), 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.2), 0 2px 4px rgba(0,0,0,0.3);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.2), 0 4px 6px rgba(0,0,0,0.3);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.2), 0 10px 10px rgba(0,0,0,0.3);
}

/* Base Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Layout & Container Styles */
.dashboard-app {
  display: flex;
  background-color: var(--bg-color);
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

.main-content {
  flex: 1;
  padding: var(--spacing-lg);
  padding-top: calc(var(--spacing-lg) + var(--top-header-height));
  transition: margin-left var(--transition-base);
  margin-left: var(--sidebar-width);
  width: calc(100% - var(--sidebar-width));
}

.main-content.sidebar-collapsed {
  margin-left: var(--sidebar-collapsed-width);
  width: calc(100% - var(--sidebar-collapsed-width));
}

.dashboard-content {
  padding-bottom: var(--spacing-lg);
  overflow-x: hidden;
}

/* Sidebar Styles */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: var(--sidebar-width);
  background-color: var(--sidebar-bg);
  box-shadow: var(--shadow-md);
  z-index: 100;
  display: flex;
  flex-direction: column;
  transition:
    width var(--transition-base),
    transform var(--transition-base);
  overflow: hidden;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg);
  height: var(--top-header-height);
  border-bottom: 1px solid var(--border-color);
}

.brand {
  display: flex;
  align-items: center;
  overflow: hidden;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary-500);
  color: white;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  margin-right: var(--spacing-md);
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  white-space: nowrap;
  color: var(--text-primary);
}

.logo span {
  color: var(--primary-500);
}

.toggle-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
}

.toggle-btn:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
}

.dark-mode .toggle-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md) 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.nav-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  color: var(--text-secondary);
  text-decoration: none;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
}

.nav-item i {
  margin-right: var(--spacing-md);
}

.nav-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 0;
  background-color: var(--primary-500);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  transition: height var(--transition-fast);
}

.nav-item:hover {
  background-color: var(--neutral-100);
  color: var(--text-primary);
}

.dark-mode .nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.nav-item.active {
  color: var(--primary-500);
  font-weight: 500;
}

.nav-item.active .nav-indicator {
  height: 20px;
}

.collapsed .nav-label {
  display: none;
}

.tooltip {
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%);
  background-color: var(--neutral-800);
  color: white;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  transition: opacity var(--transition-fast), transform var(--transition-fast);
  transform-origin: left center;
  margin-left: var(--spacing-md);
  z-index: 10;
}

.sidebar.collapsed .nav-item:hover .tooltip {
  opacity: 1;
  transform: translateY(-50%) scale(1);
}

.sidebar-footer {
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  position: relative;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: var(--spacing-sm) 0;
  border-radius: var(--radius-md);
  position: relative;
}

.avatar-wrapper {
  position: relative;
  margin-right: var(--spacing-md);
}

.avatar {
  width: 40px;
  height: 40px;
  background-color: var(--primary-100);
  color: var(--primary-600);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.status-indicator {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid var(--sidebar-bg);
}

.status-indicator.online {
  background-color: var(--success-color);
}

.user-info {
  flex: 1;
  overflow: hidden;
}

.user-name {
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.75rem;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-menu-toggle {
  display: flex;
  align-items: center;
}

.collapsed .user-info,
.collapsed .user-menu-toggle {
  display: none;
}

.user-dropdown {
  position: absolute;
  bottom: 100%;
  left: var(--spacing-lg);
  right: var(--spacing-lg);
  background-color: var(--card-bg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  margin-bottom: var(--spacing-xs);
  overflow: hidden;
  z-index: 10;
}

.collapsed .user-dropdown {
  left: 100%;
  bottom: auto;
  top: 0;
  width: 200px;
  margin-bottom: 0;
  margin-left: var(--spacing-md);
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  color: var(--text-primary);
  cursor: pointer;
}

.dropdown-item i {
  margin-right: var(--spacing-md);
  color: var(--text-secondary);
}

.dropdown-item:hover {
  background-color: var(--neutral-100);
}

.dark-mode .dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.dropdown-item.logout {
  color: var(--danger-color);
}

.dropdown-item.logout i {
  color: var(--danger-color);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: var(--spacing-xs) 0;
}

/* Header Styles */
.top-header {
  position: fixed;
  top: 0;
  right: 0;
  left: var(--sidebar-width);
  height: var(--top-header-height);
  background-color: var(--header-bg);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  transition:
    left var(--transition-base),
    box-shadow var(--transition-fast);
}

.header-shadow {
  box-shadow: var(--shadow-sm);
}

.main-content.sidebar-collapsed + .top-header {
  left: var(--sidebar-collapsed-width);
}

.header-left, .header-middle, .header-right {
  display: flex;
  align-items: center;
}

.mobile-toggle {
  display: none;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  margin-right: var(--spacing-md);
}

.page-info {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.breadcrumb {
  display: flex;
  align-items: center;
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.breadcrumb i {
  font-size: 16px;
  margin: 0 var(--spacing-xs);
}

.breadcrumb .current {
  color: var(--primary-500);
}

.search-container {
  position: relative;
  width: 300px;
  margin: 0 var(--spacing-lg);
}

.search-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-lg);
  padding-left: 36px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  background-color: var(--neutral-50);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: all var(--transition-fast);
}

.dark-mode .search-input {
  background-color: rgba(255, 255, 255, 0.05);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-300);
  background-color: var(--card-bg);
  box-shadow: 0 0 0 3px var(--primary-100);
}

.dark-mode .search-input:focus {
  background-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.3);
}

.search-container i {
  position: absolute;
  top: 50%;
  left: var(--spacing-sm);
  transform: translateY(-50%);
  color: var(--text-secondary);
  pointer-events: none;
}

.search-shortcut {
  position: absolute;
  top: 50%;
  right: var(--spacing-sm);
  transform: translateY(-50%);
  height: 22px;
  width: 22px;
  background-color: var(--neutral-200);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  pointer-events: none;
}

.dark-mode .search-shortcut {
  background-color: rgba(255, 255, 255, 0.1);
}

.date-display {
  display: flex;
  align-items: center;
  margin-right: var(--spacing-lg);
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.date-display i {
  margin-right: var(--spacing-xs);
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.action-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background-color: transparent;
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
}

.dark-mode .action-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.notification-btn.has-notifications::after {
  content: '';
  position: absolute;
  top: 10px;
  right: 10px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--danger-color);
}

.badge {
  position: absolute;
  top: 5px;
  right: 5px;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  background-color: var(--danger-color);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 var(--spacing-xs);
}

.mobile-avatar {
  display: none;
  cursor: pointer;
}

.avatar.small {
  width: 32px;
  height: 32px;
  font-size: 0.75rem;
}

/* Dashboard Summary Section */
.dashboard-summary {
  margin-bottom: var(--spacing-xl);
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-lg);
}

.welcome-message {
  flex: 1;
  min-width: 250px;
}

.welcome-message h2 {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
}

.welcome-message p {
  color: var(--text-secondary);
}

.date-range-picker {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  min-width: 300px;
}

.date-range-inputs {
  display: flex;
  gap: var(--spacing-md);
}

.date-field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.date-field label {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.date-field input {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background-color: var(--card-bg);
  color: var(--text-primary);
}

.date-field input:focus {
  outline: none;
  border-color: var(--primary-300);
  box-shadow: 0 0 0 3px var(--primary-100);
}

.dark-mode .date-field input:focus {
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.3);
}

.date-range-presets {
  display: flex;
  gap: var(--spacing-sm);
}

.date-preset-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background-color: var(--card-bg);
  color: var(--text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.date-preset-btn:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
  border-color: var(--primary-300);
}

.dark-mode .date-preset-btn:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

/* Metrics Grid */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.metric-card {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  --card-bg-from: var(--primary-50);
  --card-bg-to: var(--primary-100);
  animation: fadeIn 0.5s ease forwards;
  animation-delay: var(--delay, 0s);
  transform: translateY(20px);
  opacity: 0;
}

.metric-card.sales {
  --card-bg-from: var(--info-light);
  --card-bg-to: var(--primary-100);
}

.metric-card.orders {
  --card-bg-from: var(--purple-light);
  --card-bg-to: #e1d4f9;
}

.metric-card.products {
  --card-bg-from: var(--success-light);
  --card-bg-to: #d7f9d1;
}

.metric-card.items {
  --card-bg-from: var(--warning-light);
  --card-bg-to: #ffecce;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.metric-card-inner {
  position: relative;
  display: flex;
  padding: var(--spacing-lg);
  z-index: 1;
  overflow: hidden;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.3s ease;
}

.metric-card-inner:hover {
  transform: perspective(1000px) rotateX(5deg) rotateY(5deg);
}

.metric-card-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--card-bg-from) 0%, var(--card-bg-to) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.metric-card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.8), rgba(255,255,255,0) 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
  pointer-events: none;
}

.metric-icon-container {
  margin-right: var(--spacing-lg);
}

.metric-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-lg);
  background-color: var(--primary-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--spacing-md);
}

.metric-icon.warning {
  background-color: var(--warning-color);
}

.sales .metric-icon {
  background-color: var(--info-color);
}

.orders .metric-icon {
  background-color: var(--purple-color);
}

.products .metric-icon {
  background-color: var(--success-color);
}

.items .metric-icon {
  background-color: var(--warning-color);
}

.metric-trend {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
}

.metric-trend.positive {
  color: var(--success-color);
}

.metric-trend.negative {
  color: var(--danger-color);
}

.trend-icon {
  font-size: 16px;
  margin-right: var(--spacing-xs);
}

.metric-content {
  flex: 1;
}

.metric-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-bottom: var(--spacing-xs);
}

.metric-value {
  color: var(--text-primary);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  display: flex;
  align-items: baseline;
}

.value-prefix {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-right: 2px;
}

.metric-chart {
  margin-top: var(--spacing-md);
  height: 40px;
}

.mini-sparkline {
  display: flex;
  align-items: flex-end;
  height: 100%;
  gap: 4px;
}

.sparkline-bar {
  flex: 1;
  background-color: var(--primary-400);
  border-radius: 2px 2px 0 0;
  transform: scaleY(0);
  animation: growUp 0.5s ease forwards;
  animation-delay: calc(var(--delay, 0s) + 0.2s);
  transform-origin: bottom;
}

@keyframes growUp {
  0% {
    transform: scaleY(0);
  }
  100% {
    transform: scaleY(1);
  }
}

.sales .sparkline-bar {
  background-color: var(--info-color);
}

.orders .sparkline-bar {
  background-color: var(--purple-color);
}

.products .sparkline-bar {
  background-color: var(--success-color);
}

.items .sparkline-bar {
  background-color: var(--warning-color);
}

/* Charts Section */
.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.chart-container {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
  animation: fadeIn 0.5s ease forwards;
  animation-delay: var(--delay, 0s);
  transform: translateY(20px);
  opacity: 0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.chart-title h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
}

.chart-title p {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.time-filter {
  display: flex;
  background-color: var(--neutral-100);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.dark-mode .time-filter {
  background-color: rgba(255, 255, 255, 0.05);
}

.period-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.period-btn:hover {
  color: var(--text-primary);
}

.period-btn.active {
  background-color: var(--primary-500);
  color: white;
}

.chart-option-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background-color: transparent;
  border: none;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.chart-option-btn:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
}

.dark-mode .chart-option-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.chart-body {
  position: relative;
  height: 300px;
}

/* New Best-Selling Products Styles */
.top-products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.product-card {
  position: relative;
  background-color: var(--neutral-50);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.dark-mode .product-card {
  background-color: rgba(255, 255, 255, 0.05);
}

.product-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.product-rank {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: var(--primary-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  z-index: 1;
}

.product-details {
  margin-left: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.product-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.product-category {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.product-stats {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
}

.product-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xs);
}

.stat-value {
  font-weight: 600;
  color: var(--text-primary);
}

/* Low Stock and Recent Orders Sections */
.low-stock-section,
.recent-orders-section {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  animation: fadeIn 0.5s ease forwards;
  animation-delay: var(--delay, 0s);
  transform: translateY(20px);
  opacity: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.section-title h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
}

.section-title p {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.view-all-btn,
.action-btn {
  display: flex;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: transparent;
  border: 1px solid var(--primary-500);
  color: var(--primary-500);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.view-all-btn:hover,
.action-btn:hover {
  background-color: var(--primary-500);
  color: white;
}

.action-btn i {
  margin-right: var(--spacing-xs);
}

.data-table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: var(--spacing-md);
  text-align: left;
}

.data-table th {
  background-color: var(--neutral-50);
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.875rem;
  white-space: nowrap;
  border-bottom: 1px solid var(--border-color);
}

.dark-mode .data-table th {
  background-color: rgba(255, 255, 255, 0.05);
}

.data-table td {
  border-bottom: 1px solid var(--border-color);
}

.data-table tbody tr:hover {
  background-color: var(--neutral-50);
}

.dark-mode .data-table tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.stock-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.875rem;
}

.stock-badge.critical {
  background-color: var(--danger-light);
  color: var(--danger-color);
}

.stock-badge.warning {
  background-color: var(--warning-light);
  color: var(--warning-color);
}

.stock-badge.normal {
  background-color: var(--success-light);
  color: var(--success-color);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-full);
  font-weight: 500;
  font-size: 0.875rem;
  text-transform: capitalize;
}

.status-badge.completed {
  background-color: var(--success-light);
  color: var(--success-color);
}

.status-badge.pending {
  background-color: var(--warning-light);
  color: var(--warning-color);
}

.status-badge.processing {
  background-color: var(--info-light);
  color: var(--info-color);
}

.status-badge.cancelled {
  background-color: var(--danger-light);
  color: var(--danger-color);
}

.table-action-btn {
  display: inline-flex;
  align-items: center;
  padding: var(--spacing-xs) var(--spacing-sm);
  background-color: transparent;
  border: none;
  color: var(--primary-500);
  font-size: 0.875rem;
  cursor: pointer;
  border-radius: var(--radius-sm);
}

.table-action-btn:hover {
  background-color: var(--primary-50);
}

.dark-mode .table-action-btn:hover {
  background-color: rgba(33, 150, 243, 0.1);
}

.table-action-btn i {
  margin-right: var(--spacing-xs);
  font-size: 16px;
}

.restock-btn {
  color: var(--success-color);
}

.restock-btn:hover {
  background-color: var(--success-light);
}

/* No Data Messages */
.no-data-message {
  padding: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  text-align: center;
}

.no-data-message i {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    z-index: 200;
  }

  .sidebar.mobile-open {
    transform: translateX(0);
  }

  .main-content {
    margin-left: 0 !important;
    width: 100% !important;
    padding: var(--spacing-md);
    padding-top: calc(var(--spacing-md) + var(--top-header-height));
  }

  .top-header {
    left: 0 !important;
    padding: 0 var(--spacing-md);
  }

  .mobile-toggle {
    display: block;
  }

  .mobile-avatar {
    display: block;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions-grid {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 20px;
  }

  .top-header {
    padding: 0 var(--spacing-md);
  }

  .header-middle {
    display: none;
  }

  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .chart-controls {
    margin-top: var(--spacing-md);
    width: 100%;
    justify-content: space-between;
  }

  .chart-header .view-all-btn {
    margin-top: var(--spacing-md);
    align-self: flex-end;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--neutral-300);
  border-radius: 3px;
}

.dark-mode ::-webkit-scrollbar-thumb {
  background: var(--neutral-700);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--neutral-400);
}

.dark-mode ::-webkit-scrollbar-thumb:hover {
  background: var(--neutral-600);
}
</style>