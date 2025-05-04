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

          <router-link to="/inventory" class="nav-item">
            <div class="nav-indicator"></div>
            <i class="material-icons">inventory_2</i>
            <span class="nav-label">Inventory</span>
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

          <router-link to="/settings" class="nav-item">
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
            <h2>Welcome back, John!</h2>
            <p>Here's what's happening with your business today.</p>
          </div>
          <div class="date-range-picker">
            <div class="date-range-inputs">
              <div class="date-field">
                <label for="start-date">From:</label>
                <input type="date" id="start-date" v-model="dateRange.startDate" @change="fetchSalesSummary">
              </div>
              <div class="date-field">
                <label for="end-date">To:</label>
                <input type="date" id="end-date" v-model="dateRange.endDate" @change="fetchSalesSummary">
              </div>
            </div>
            <div class="date-range-presets">
              <button class="date-preset-btn" @click="setDateRange('week')">Last 7 Days</button>
              <button class="date-preset-btn" @click="setDateRange('month')">Last 30 Days</button>
              <button class="date-preset-btn" @click="setDateRange('quarter')">Last 90 Days</button>
            </div>
          </div>
        </div>

        <!-- Modern Metrics Grid with 3D Cards -->
        <div class="metrics-grid">
          <div class="metric-card sales" :style="{ '--delay': '0.1s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">attach_money</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span class="trend-value">12.5%</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Today's Sales</div>
                <div class="metric-value">
                  <span class="value-prefix">$</span>
                  <span class="value-number">{{ metrics.totalSales.toFixed(2) }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in [40, 70, 45, 90, 50, 60, 75]"
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

          <div class="metric-card orders" :style="{ '--delay': '0.2s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">shopping_bag</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span class="trend-value">8.3%</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Total Orders</div>
                <div class="metric-value">
                  <span class="value-number">{{ metrics.totalOrders }}</span>
                </div>
                <div class="metric-chart">
                  <div class="mini-sparkline">
                    <div class="sparkline-bar" v-for="(value, index) in [60, 45, 55, 80, 65, 75, 50]"
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

          <div class="metric-card products" :style="{ '--delay': '0.3s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">category</i>
                </div>
                <div class="metric-trend positive">
                  <i class="material-icons trend-icon">trending_up</i>
                  <span class="trend-value">5.2%</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Total Products</div>
                <div class="metric-value">
                  <span class="value-number">{{ metrics.totalProduct }}</span>
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

          <div class="metric-card items" :style="{ '--delay': '0.4s' }">
            <div class="metric-card-inner">
              <div class="metric-icon-container">
                <div class="metric-icon">
                  <i class="material-icons">inventory_2</i>
                </div>
                <div class="metric-trend negative">
                  <i class="material-icons trend-icon">trending_down</i>
                  <span class="trend-value">2.1%</span>
                </div>
              </div>
              <div class="metric-content">
                <div class="metric-label">Items Sold</div>
                <div class="metric-value">
                  <span class="value-number">{{ metrics.itemsSold }}</span>
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
          <!-- Sales Overview Chart with improved UI -->
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

          <!-- Enhanced grid layout for secondary charts -->
          <div class="charts-grid">
            <!-- Recent Orders with enhanced UI -->
            <div class="chart-container recent-orders" :style="{ '--delay': '0.6s' }">
              <div class="chart-header">
                <div class="chart-title">
                  <h3>Recent Orders</h3>
                  <p>Latest transactions</p>
                </div>
                <button class="view-all-btn">
                  View All <i class="material-icons">chevron_right</i>
                </button>
              </div>
              <div class="chart-body">
                <div class="orders-list">
                  <div class="order-item" v-for="(order, index) in recentOrders" :key="index">
                    <div class="order-preview">
                      <div class="order-icon" :class="order.status">
                        <i class="material-icons">receipt</i>
                      </div>
                      <div class="order-info">
                        <div class="order-id">#{{ order.id }}</div>
                        <div class="order-customer">{{ order.customer }}</div>
                      </div>
                    </div>
                    <div class="order-details">
                      <div class="order-amount">${{ order.amount }}</div>
                      <div class="order-status" :class="order.status">
                        {{ order.status }}
                      </div>
                    </div>
                  </div>
                  <div class="empty-state" v-if="!recentOrders.length">
                    <i class="material-icons">shopping_cart</i>
                    <p>No recent orders found</p>
                    <button class="empty-action-btn">Create an Order</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Top Products with enhanced UI -->
            <div class="chart-container top-products" :style="{ '--delay': '0.7s' }">
              <div class="chart-header">
                <div class="chart-title">
                  <h3>Top Products</h3>
                  <p>Best performing items</p>
                </div>
                <button class="view-all-btn">
                  View All <i class="material-icons">chevron_right</i>
                </button>
              </div>
              <div class="chart-body">
                <div class="products-list">
                  <div v-if="isLoadingBestSellers" class="loading-products">
                    <div class="loading-spinner"></div>
                    <p>Loading top products...</p>
                  </div>
                  <div v-else-if="topProducts.length === 0" class="empty-state">
                    <i class="material-icons">category</i>
                    <p>No product data available</p>
                    <button class="empty-action-btn" @click="fetchBestSellingProducts">Reload Products</button>
                  </div>
                  <div v-else class="product-item" v-for="(product, index) in topProducts" :key="index">
                    <div class="product-rank">{{ index + 1 }}</div>
                    <div class="product-icon" :style="{ backgroundColor: product.color }">
                      <i class="material-icons">{{ product.icon }}</i>
                    </div>
                    <div class="product-info">
                      <div class="product-name">{{ product.name }}</div>
                      <div class="product-category">{{ product.category }}</div>
                    </div>
                    <div class="product-metrics">
                      <div class="product-sales">
                        <span class="metrics-label">Sales:</span>
                        <span class="metrics-value">{{ product.sales }}</span>
                      </div>
                      <div class="product-revenue">
                        <span class="metrics-label">Revenue:</span>
                        <span class="metrics-value">{{ product.revenue }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Quick Actions Section -->
        <div class="quick-actions-section" :style="{ '--delay': '0.8s' }">
          <div class="section-header">
            <h3>Quick Actions</h3>
            <p>Frequently used operations</p>
          </div>
          <div class="quick-actions-grid">
            <div class="action-card" v-for="(action, index) in quickActions" :key="index"
                 :style="{ '--card-delay': `${index * 0.1}s` }">
              <div class="action-icon" :style="{ backgroundColor: action.color }">
                <i class="material-icons">{{ action.icon }}</i>
              </div>
              <div class="action-name">{{ action.name }}</div>
              <div class="action-hover-effect"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced mobile overlay -->
    <div class="sidebar-overlay" v-if="isSidebarCollapsed === false && isMobileView" @click="toggleSidebar"></div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  name: 'DashboardView',
  data() {
    return {
      salesPeriod: 'week',
      salesChart: null,
      isSidebarCollapsed: window.innerWidth < 1024,
      isMobileView: window.innerWidth < 768,
      isUserMenuOpen: false,
      hasNotifications: true,
      notificationCount: 3,
      isDarkMode: localStorage.getItem('darkMode') === 'true',
      scrolled: false,

      // Date range for reports
      dateRange: {
        startDate: this.getDefaultStartDate(),
        endDate: this.getDefaultEndDate()
      },

      // Loading states
      isLoadingSalesSummary: false,
      isLoadingBestSellers: false,

      // Metrics data
      metrics: {
        totalSales: 0,
        totalOrders: 0,
        totalProduct: 0,
        itemsSold: 0
      },

      recentOrders: [
        { id: '7842', customer: 'Emma Johnson', amount: '245.99', status: 'completed' },
        { id: '7841', customer: 'Michael Chen', amount: '124.50', status: 'processing' },
        { id: '7840', customer: 'Sarah Williams', amount: '86.20', status: 'pending' },
        { id: '7839', customer: 'David Miller', amount: '320.75', status: 'completed' },
        { id: '7838', customer: 'Jessica Lee', amount: '175.30', status: 'processing' }
      ],

      // Top products fetched from the API
      topProducts: [],

      // Fallback icons and colors for products
      productIcons: {
        'Electronics': { icon: 'devices', color: '#4caf50' },
        'Wearables': { icon: 'watch', color: '#2196f3' },
        'Audio': { icon: 'headphones', color: '#ff9800' },
        'Accessories': { icon: 'cable', color: '#9c27b0' },
        'default': { icon: 'shopping_bag', color: '#607d8b' }
      },

      quickActions: [
        { name: 'New Sale', icon: 'add_shopping_cart', color: '#2196f3' },
        { name: 'Add Product', icon: 'add_box', color: '#4caf50' },
        { name: 'New Customer', icon: 'person_add', color: '#ff9800' },
        { name: 'Generate Report', icon: 'assessment', color: '#9c27b0' }
      ],

      currentDate: new Date().toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      })
    };
  },

  mounted() {
    this.createSimpleChart();
    this.loadMetrics();
    this.setupCardHoverEffects();

    // Store initial window width for proper resize handling
    window.initialWidth = window.innerWidth;

    // Set initial responsive states
    this.isMobileView = window.innerWidth < 768;

    // For sidebar state:
    if (window.innerWidth < 1024) {
      // On small screens, always start with collapsed sidebar
      this.isSidebarCollapsed = true;
      // Save this state to localStorage
      localStorage.setItem('sidebarCollapsed', 'true');
    } else {
      // On large screens, check for stored preference
      const storedSidebarState = localStorage.getItem('sidebarCollapsed');
      if (storedSidebarState !== null) {
        this.isSidebarCollapsed = storedSidebarState === 'true';
      } else {
        // Default to expanded if no preference saved
        this.isSidebarCollapsed = false;
        // Save default to localStorage
        localStorage.setItem('sidebarCollapsed', 'false');
      }
    }

    // Add event listeners
    window.addEventListener('resize', this.handleResize);
    document.addEventListener('click', this.handleClickOutside);
    document.addEventListener('keydown', this.handleKeyShortcuts);
    window.addEventListener('scroll', this.handleScroll);
  },

  beforeUnmount() {
    // Clean up the chart to prevent memory leaks
    if (this.salesChart) {
      this.salesChart.destroy();
    }

    window.removeEventListener('resize', this.handleResize);
    document.removeEventListener('click', this.handleClickOutside);
    document.removeEventListener('keydown', this.handleKeyShortcuts);
    window.removeEventListener('scroll', this.handleScroll);
  },

  methods: {
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

    // Fetch sales summary from the report API
    async fetchSalesSummary() {
      this.isLoadingSalesSummary = true;
      try {
        const token = localStorage.getItem("token");
        const config = token ? {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        } : {};

        // Format the URL with the date range parameters
        const url = `http://127.0.0.1:5000/api/sales-summary?start_date=${this.dateRange.startDate}&end_date=${this.dateRange.endDate}`;

        const response = await axios.get(url, config);

        // Update the metrics
        if (response.data && this.salesChart) {
          this.updateChartWithApiData(response.data.daily_data);
          this.metrics.totalSales = response.data.total_revenue || 0;
          this.metrics.totalOrders = response.data.total_orders || 0;
        }
      } catch (error) {
        console.error("Failed to fetch sales summary:", error);
      } finally {
        this.isLoadingSalesSummary = false;
      }
    },

    // Fetch best selling products from the report API
    async fetchBestSellingProducts() {
      this.isLoadingBestSellers = true;
      try {
        const token = localStorage.getItem("token");
        const config = token ? {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        } : {};

        // Get top 5 products
        const url = `http://127.0.0.1:5000/api/best-selling-products?limit=5`;

        const response = await axios.get(url, config);

        if (response.data && Array.isArray(response.data)) {
          // Transform the data to match our UI format
          this.topProducts = response.data.map(product => {
            // Determine an appropriate icon and color based on product category
            const category = product.category || 'default';
            const iconData = this.productIcons[category] || this.productIcons.default;

            return {
              name: product.name,
              category: product.category || 'General',
              sales: product.total_sold ? product.total_sold.toLocaleString() : '0',
              revenue: product.total_revenue ? `$${product.total_revenue.toLocaleString()}` : '$0.00',
              icon: iconData.icon,
              color: iconData.color
            };
          });
        }
      } catch (error) {
        console.error("Failed to fetch best selling products:", error);
      } finally {
        this.isLoadingBestSellers = false;
      }
    },

    // FIXED: Update the chart with API data
    updateChartWithApiData(dailyData) {
      if (!this.salesChart || !dailyData || !Array.isArray(dailyData)) return;

      try {
        // Extract the dates and revenue values
        const labels = dailyData.map(item => {
          // Format date to a more readable format (e.g., "Jan 15")
          const date = new Date(item.date);
          return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });

        const values = dailyData.map(item => item.revenue || 0);

        // Update the chart data
        this.salesChart.data.labels = labels;
        this.salesChart.data.datasets[0].data = values;
        this.salesChart.update();
      } catch (err) {
        console.error('Error updating chart with data:', err);
      }
    },

    // FIXED: This method is used for period changes
    changeSalesPeriod(period) {
      // Store the current period
      this.salesPeriod = period;

      // Set date range based on period
      this.setDateRange(period);

      // Clean up existing chart
      if (this.salesChart) {
        this.salesChart.destroy();
        this.salesChart = null;
      }

      // Wait for next tick to ensure DOM is updated
      this.$nextTick(() => {
        this.createSimpleChart();
        this.fetchSalesSummary();
      });
    },

    // FIXED: Create a simple chart with minimal options
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

        // Create super simple chart
        this.salesChart = new Chart(canvas, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Sales',
              data: values,
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              fill: true
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
      } catch (err) {
        console.error('Chart initialization error:', err);
      }
    },

    // Load all metrics and data
    async loadMetrics() {
      try {
        // Check if user is authenticated
        const token = localStorage.getItem("token");
        if (!token) {
          console.warn("No token found in localStorage. User may need to log in.");
        }

        // Load basic metrics and recent orders
        try {
          const config = token ? {
            headers: {
              Authorization: `Bearer ${token}`,
            }
          } : {};

          const [ordersRes, productsRes] = await Promise.all([
            axios.get("http://127.0.0.1:5000/api/orders", config),
            axios.get("http://127.0.0.1:5000/api/products", config)
          ]);

          // Update inventory metrics
          if (productsRes.data && Array.isArray(productsRes.data)) {
            this.metrics.totalProduct = productsRes.data.length;
            this.metrics.itemsSold = productsRes.data.reduce((sum, p) => sum + (p.stock || 0), 0);
          }

          // Populate recentOrders from latest 5 orders
          if (ordersRes.data && Array.isArray(ordersRes.data)) {
            this.recentOrders = ordersRes.data.slice(0, 5).map(order => ({
              id: order.id,
              customer: order.customer_name || "N/A",
              amount: order.total || "0.00",
              status: order.status || "pending"
            }));
          }
        } catch (error) {
          console.error("Failed to fetch basic metrics:", error);
        }

        // Load data from report APIs
        await Promise.all([
          this.fetchSalesSummary(),
          this.fetchBestSellingProducts()
        ]);

      } catch (error) {
        console.error("Failed to load metrics:", error);
      }
    },

    // Set the date range based on preset periods and fetch updated data
    setDateRange(period) {
      const endDate = new Date();
      let startDate = new Date();

      switch(period) {
        case 'week':
          // Last 7 days
          startDate.setDate(startDate.getDate() - 7);
          break;
        case 'month':
          // Last 30 days
          startDate.setDate(startDate.getDate() - 30);
          break;
        case 'quarter':
          // Last 90 days
          startDate.setDate(startDate.getDate() - 90);
          break;
        case 'day':
          // Last 24 hours
          startDate.setDate(startDate.getDate() - 1);
          break;
        case 'year':
          // Last 365 days
          startDate.setDate(startDate.getDate() - 365);
          break;
      }

      // Format dates for the API
      this.dateRange.startDate = startDate.toISOString().split('T')[0];
      this.dateRange.endDate = endDate.toISOString().split('T')[0];
    },

    // Setup card hover effects
    setupCardHoverEffects() {
      const cards = document.querySelectorAll('.metric-card');

      cards.forEach(card => {
        card.addEventListener('mousemove', this.handleCardMouseMove);
        card.addEventListener('mouseleave', this.handleCardMouseLeave);
      });
    },

    // Handle mouse move over card for 3D effect
    handleCardMouseMove(e) {
      const card = e.currentTarget;
      const cardRect = card.getBoundingClientRect();
      const cardInner = card.querySelector('.metric-card-inner');
      const cardBackdrop = card.querySelector('.metric-card-backdrop');
      const cardGlow = card.querySelector('.metric-card-glow');

      if (!cardInner || !cardBackdrop || !cardGlow) return;

      // Calculate mouse position relative to card
      const x = e.clientX - cardRect.left;
      const y = e.clientY - cardRect.top;

      // Calculate rotation values based on mouse position
      const rotateY = (x / cardRect.width - 0.5) * 10;
      const rotateX = (y / cardRect.height - 0.5) * -10;

      // Apply transformations
      cardInner.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;

      // Update backdrop and glow effects
      cardBackdrop.style.opacity = '1';
      cardGlow.style.opacity = '1';
      cardGlow.style.left = `${x}px`;
      cardGlow.style.top = `${y}px`;
    },

    // Handle mouse leave event for cards
    handleCardMouseLeave(e) {
      const card = e.currentTarget;
      const cardInner = card.querySelector('.metric-card-inner');
      const cardBackdrop = card.querySelector('.metric-card-backdrop');
      const cardGlow = card.querySelector('.metric-card-glow');

      if (!cardInner || !cardBackdrop || !cardGlow) return;

      // Reset transformations
      cardInner.style.transform = 'rotateX(0deg) rotateY(0deg)';

      // Hide effects
      cardBackdrop.style.opacity = '0';
      cardGlow.style.opacity = '0';
    },

    // Toggle sidebar visibility
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
      localStorage.setItem('sidebarCollapsed', this.isSidebarCollapsed.toString());
    },

    // Handle window resize
    handleResize() {
      this.isMobileView = window.innerWidth < 768;

      // Responsive sidebar behavior
      if (window.innerWidth < 1024) {
        this.isSidebarCollapsed = true;
      }

      // Responsive chart adjustment
      if (this.salesChart) {
        this.salesChart.resize();
      }
    },

    // Handle scroll event
    handleScroll() {
      this.scrolled = window.scrollY > 10;
    },

    // Handle click outside user menu
    handleClickOutside(e) {
      const userProfile = document.querySelector('.user-profile');
      const mobileAvatar = document.querySelector('.mobile-avatar');

      if (userProfile && mobileAvatar && !userProfile.contains(e.target) && !mobileAvatar.contains(e.target)) {
        this.isUserMenuOpen = false;
      }
    },

    // Handle keyboard shortcuts
    handleKeyShortcuts(e) {
      // Toggle sidebar with Shift + S
      if (e.shiftKey && e.key.toLowerCase() === 's') {
        this.toggleSidebar();
      }
      // Toggle dark mode with Shift + D
      if (e.shiftKey && e.key.toLowerCase() === 'd') {
        this.isDarkMode = !this.isDarkMode;
        localStorage.setItem('darkMode', this.isDarkMode.toString());
      }
    },
    
// Add the new periodLabel method
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
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

html, body {
  height: 100%;
  width: 100%;
}

body {
  background-color: var(--bg-color);
  color: var(--text-primary);
}

button, input {
  font-family: inherit;
}

a {
  text-decoration: none;
  color: inherit;
}

/* Dashboard App Container */
.dashboard-app {
  min-height: 100vh;
  position: relative;
  background-color: var(--bg-color);
  color: var(--text-primary);
  display: flex;
  transition: background-color var(--transition-base);
}

/* Sidebar Styling */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background-color: var(--sidebar-bg);
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  transition: width var(--transition-base),
              transform var(--transition-base),
              background-color var(--transition-base);
  overflow: hidden;
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
}

.sidebar-header {
  height: 80px;
  padding: 0 var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
}

.brand {
  display: flex;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-500);
  background: var(--primary-50);
  border-radius: var(--radius-md);
  margin-right: var(--spacing-md);
  transition: all var(--transition-base);
}

.dark-mode .logo-icon {
  background: var(--primary-900);
}

.logo {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
}

.logo span {
  color: var(--primary-500);
}

.toggle-btn {
  border: none;
  background: none;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--radius-full);
  transition: all var(--transition-fast);
}

.toggle-btn:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
}

.dark-mode .toggle-btn:hover {
  background-color: var(--neutral-800);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-lg) 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: 0 var(--spacing-sm);
}

.nav-item {
  position: relative;
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  color: var(--text-secondary);
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  overflow: hidden;
}

.nav-item i {
  font-size: 20px;
  margin-right: var(--spacing-md);
  transition: all var(--transition-fast);
}

.nav-label {
  white-space: nowrap;
  opacity: 1;
  transition: opacity var(--transition-fast);
}

.sidebar.collapsed .nav-label {
  opacity: 0;
  width: 0;
  height: 0;
  visibility: hidden;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: var(--spacing-md);
}

.sidebar.collapsed .nav-item i {
  margin-right: 0;
}

.nav-indicator {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: transparent;
  border-radius: 0 4px 4px 0;
  transition: transform var(--transition-fast), background-color var(--transition-fast);
  transform: scaleY(0);
}

.nav-item.active .nav-indicator {
  background-color: var(--primary-500);
  transform: scaleY(1);
}

.nav-item:hover {
  background-color: var(--neutral-100);
  color: var(--primary-600);
}

.dark-mode .nav-item:hover {
  background-color: var(--neutral-800);
}

.nav-item.active {
  background-color: var(--primary-50);
  color: var(--primary-600);
  font-weight: 600;
}

.dark-mode .nav-item.active {
  background-color: var(--primary-900);
  color: var(--primary-300);
}

.sidebar.collapsed .nav-menu {
  align-items: center;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: var(--spacing-md);
}

.sidebar.collapsed .nav-item i {
  margin-right: 0;
  font-size: 22px;
}

/* Add tooltips for mini sidebar */
.tooltip {
  position: absolute;
  left: calc(var(--sidebar-collapsed-width) + 5px);
  background-color: var(--card-bg);
  color: var(--text-primary);
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 14px;
  box-shadow: var(--shadow-md);
  pointer-events: none;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.2s ease;
  z-index: 1200;
  white-space: nowrap; /* Prevent label wrap */
}

.nav-item:hover .tooltip,
.user-profile:hover .tooltip {
  opacity: 1;
  transform: translateX(0);
}

/* Add fade-in animation for sidebar overlay */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.sidebar-footer {
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-md) var(--spacing-lg);
  position: relative;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  border-radius: var(--radius-lg);
  padding: var(--spacing-sm);
  transition: background-color var(--transition-fast);
}

.user-profile:hover {
  background-color: var(--neutral-100);
}

.dark-mode .user-profile:hover {
  background-color: var(--neutral-800);
}

.avatar-wrapper {
  position: relative;
  margin-right: var(--spacing-md);
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-full);
  background-color: var(--primary-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
}

.avatar.small {
  width: 34px;
  height: 34px;
  font-size: 14px;
}

.status-indicator {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: var(--radius-full);
  border: 2px solid var(--sidebar-bg);
  bottom: 0;
  right: 0;
}

.status-indicator.online {
  background-color: var(--success-color);
}

.user-info {
  flex: 1;
  white-space: nowrap;
  opacity: 1;
  transition: opacity var(--transition-fast);
}

.sidebar.collapsed .user-info {
  opacity: 0;
  width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.user-role {
  font-size: 12px;
  color: var(--text-secondary);
}

.user-menu-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 1;
  transition: opacity var(--transition-fast), transform var(--transition-fast);
}

.user-menu-toggle i {
  font-size: 20px;
  color: var(--text-secondary);
}

.sidebar.collapsed .user-menu-toggle {
  opacity: 0;
  width: 0;
}

.user-dropdown {
  position: absolute;
  bottom: 100%;
  left: var(--spacing-lg);
  width: calc(var(--sidebar-width) - (var(--spacing-lg) * 2));
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  margin-bottom: var(--spacing-sm);
  overflow: hidden;
  z-index: 1010;
  animation: slideUp 0.2s var(--transition-base);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: 14px;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
  cursor: pointer;
}

.dropdown-item i {
  font-size: 18px;
  margin-right: var(--spacing-md);
  color: var(--text-secondary);
}

.dropdown-item:hover {
  background-color: var(--neutral-100);
  color: var(--text-primary);
}

.dark-mode .dropdown-item:hover {
  background-color: var(--neutral-800);
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

/* Main Content Area */
.main-content {
  margin-left: var(--sidebar-width);
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: margin-left var(--transition-base);
  min-height: 100vh;
}

.main-content.sidebar-collapsed {
  margin-left: var(--sidebar-collapsed-width);
}

/* Top Header */
.top-header {
  height: var(--top-header-height);
  background-color: var(--header-bg);
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  position: sticky;
  top: 0;
  z-index: 900;
  transition: all var(--transition-base);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-lg);
}

.header-shadow {
  box-shadow: var(--shadow-md);
}

.header-left {
  display: flex;
  align-items: center;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--text-secondary);
  margin-right: var(--spacing-md);
  width: 38px;
  height: 38px;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.mobile-toggle:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
}

.dark-mode .mobile-toggle:hover {
  background-color: var(--neutral-800);
}

.page-info {
  display: flex;
  flex-direction: column;
}

.page-title {
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.breadcrumb {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.breadcrumb i {
  font-size: 16px;
  margin: 0 var(--spacing-xs);
}

.breadcrumb .current {
  color: var(--primary-500);
}

.header-middle {
  flex: 1;
  display: flex;
  justify-content: center;
  max-width: 500px;
}

.search-container {
  position: relative;
  background-color: var(--neutral-100);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  padding: 0 var(--spacing-md);
  width: 100%;
  transition: all var(--transition-fast);
}

.dark-mode .search-container {
  background-color: var(--neutral-800);
}

.search-container:focus-within {
  background-color: var(--card-bg);
  box-shadow: 0 0 0 2px var(--primary-400);
}

.search-container i {
  color: var(--text-secondary);
  margin-right: var(--spacing-sm);
}

.search-input {
  border: none;
  background: transparent;
  height: 40px;
  padding: var(--spacing-sm) 0;
  outline: none;
  width: 100%;
  color: var(--text-primary);
  font-size: 14px;
}

.search-shortcut {
  position: absolute;
  right: var(--spacing-lg);
  background-color: var(--neutral-200);
  color: var(--text-secondary);
  font-size: 12px;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  pointer-events: none;
}

.dark-mode .search-shortcut {
  background-color: var(--neutral-700);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-left: auto;
}

.date-display {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: var(--text-secondary);
}

.date-display i {
  margin-right: var(--spacing-sm);
  font-size: 18px;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.action-btn {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
}

.action-btn:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
}

.dark-mode .action-btn:hover {
  background-color: var(--neutral-800);
}

.action-btn.theme-btn {
  color: var(--warning-color);
}

.notification-btn {
  color: var(--text-secondary);
}

.has-notifications::after {
  content: '';
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background-color: var(--danger-color);
  border-radius: var(--radius-full);
  box-shadow: 0 0 0 2px var(--header-bg);
}

.badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 18px;
  height: 18px;
  border-radius: var(--radius-full);
  background-color: var(--danger-color);
  color: white;
  font-size: 10px;
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

/* Dashboard Content */
.dashboard-content {
  padding: var(--spacing-xl);
  flex: 1;
  overflow-y: auto;
}

/* Dashboard Summary */
.dashboard-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.welcome-message h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
}

.welcome-message p {
  color: var(--text-secondary);
  font-size: 15px;
}

.date-range-picker {
  display: flex;
  flex-direction: column;
  background-color: var(--card-bg);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.date-range-inputs {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
}

.date-field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.date-field label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.date-field input {
  padding: var(--spacing-xs) var(--spacing-sm);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background-color: var(--bg-color);
  color: var(--text-primary);
  font-size: 0.9rem;
}

.date-range-presets {
  display: flex;
  gap: var(--spacing-sm);
}

.date-preset-btn {
  padding: var(--spacing-xs) var(--spacing-sm);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background-color: var(--neutral-100);
  color: var(--text-secondary);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.date-preset-btn:hover {
  background-color: var(--primary-50);
  color: var(--primary-600);
  border-color: var(--primary-200);
}

.dark-mode .date-preset-btn {
  background-color: var(--neutral-800);
}

.dark-mode .date-preset-btn:hover {
  background-color: var(--primary-900);
  color: var(--primary-300);
}

/* Modern Metrics Grid with 3D Effects */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

.metric-card {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  position: relative;
  overflow: hidden;
  transition: all 0.5s cubic-bezier(0.215, 0.61, 0.355, 1);
  animation: fadeInUp 0.7s cubic-bezier(0.23, 1, 0.32, 1) both;
  animation-delay: var(--delay, 0s);
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
  height: 180px;
  perspective: 1000px;
  transform-style: preserve-3d;
}

.metric-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-sm);
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transform-style: preserve-3d;
  z-index: 1;
  box-sizing: border-box;
}

.dark-mode .metric-card-inner {
  background-color: var(--neutral-800);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.metric-card:hover .metric-card-inner {
  transform: translateY(-8px) rotateX(2deg) rotateY(2deg);
  box-shadow: var(--shadow-lg), 0 15px 30px rgba(0, 0, 0, 0.1);
}

.dark-mode .metric-card:hover .metric-card-inner {
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

.metric-card-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0) 70%
  );
  transition: opacity 0.3s ease;
  z-index: 0;
  pointer-events: none;
}

.dark-mode .metric-card-backdrop {
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgba(255, 255, 255, 0.07) 0%,
    rgba(255, 255, 255, 0) 70%
  );
}

.metric-card:hover .metric-card-backdrop {
  opacity: 1;
}

.metric-card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle at center,
    rgba(255, 255, 255, 0.5) 0%,
    rgba(255, 255, 255, 0) 70%
  );
  opacity: 0;
  transform: scale(0.7);
  z-index: -1;
  transition: transform 0.5s ease, opacity 0.5s ease;
  pointer-events: none;
}

.dark-mode .metric-card-glow {
  background: radial-gradient(
    circle at center,
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0) 70%
  );
}

.metric-card:hover .metric-card-glow {
  opacity: 0.2;
  transform: scale(1);
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  transition: all var(--transition-fast);
  z-index: 2;
}

.metric-card.sales::before {
  background: linear-gradient(to bottom, var(--primary-400), var(--primary-600));
}

.metric-card.orders::before {
  background: linear-gradient(to bottom, #ba68c8, #7b1fa2);
}

.metric-card.products::before {
  background: linear-gradient(to bottom, #66bb6a, #2e7d32);
}

.metric-card.items::before {
  background: linear-gradient(to bottom, #ffa726, #ef6c00);
}

.metric-icon-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  width: 100%;
}

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.metric-card.sales .metric-icon {
  background-color: var(--info-light);
  color: var(--info-color);
}

.metric-card.orders .metric-icon {
  background-color: var(--warning-light);
  color: var(--warning-color);
}

.metric-card.products .metric-icon {
  background-color: var(--success-light);
  color: var(--success-color);
}

.metric-card.items .metric-icon {
  background-color: var(--purple-light);
  color: var(--purple-color);
}

.metric-icon i {
  font-size: 28px;
}

.metric-trend {
  display: flex;
  align-items: center;
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.metric-trend.positive {
  background-color: var(--success-light);
  color: var(--success-color);
}

.metric-trend.negative {
  background-color: var(--danger-light);
  color: var(--danger-color);
}

.metric-trend i {
  font-size: 14px;
  margin-right: 2px;
}

.metric-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.metric-value {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  display: flex;
  align-items: center;
}

.value-prefix {
  font-weight: 600;
  font-size: 16px;
  margin-right: 2px;
  opacity: 0.9;
}

.value-number {
  font-size: 22px;
  font-weight: 700;
}

.metric-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.metric-chart {
  margin-top: auto;
}

.mini-sparkline {
  display: flex;
  align-items: flex-end;
  height: 30px;
  gap: 3px;
}

.sparkline-bar {
  flex: 1;
  background-color: var(--primary-100);
  border-radius: 2px;
  min-width: 4px;
  transition: height 0.3s ease;
}

.metric-card.sales .sparkline-bar {
  background-color: var(--info-light);
}

.metric-card.orders .sparkline-bar {
  background-color: var(--warning-light);
}

.metric-card.products .sparkline-bar {
  background-color: var(--success-light);
}

.metric-card.items .sparkline-bar {
  background-color: var(--purple-light);
}

/* Charts Section */
.charts-section {
  margin-bottom: var(--spacing-2xl);
}

.chart-container {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition-base);
  animation: fadeInUp 0.6s var(--transition-base) both;
  animation-delay: var(--delay, 0s);
}

.chart-container:hover {
  box-shadow: var(--shadow-md);
}

.sales-overview {
  margin-bottom: var(--spacing-xl);
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.chart-title h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.chart-title p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
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
  background-color: var(--neutral-800);
}

.period-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.period-btn:hover {
  color: var(--primary-500);
}

.period-btn.active {
  background-color: var(--primary-500);
  color: white;
}

.chart-option-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.chart-option-btn:hover {
  background-color: var(--neutral-100);
  color: var(--primary-500);
}

.dark-mode .chart-option-btn:hover {
  background-color: var(--neutral-800);
}

.chart-body {
  padding: var(--spacing-lg);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-xl);
}

/* Recent Orders */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: var(--spacing-md);
}

.order-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.order-preview {
  display: flex;
  align-items: center;
}

.order-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background-color: var(--primary-50);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
}

.order-icon.completed {
  background-color: var(--success-light);
  color: var(--success-color);
}

.order-icon.pending {
  background-color: var(--warning-light);
  color: var(--warning-color);
}

.order-icon.processing {
  background-color: var(--info-light);
  color: var(--info-color);
}

.order-info {
  display: flex;
  flex-direction: column;
}

.order-id {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.order-customer {
  color: var(--text-secondary);
  font-size: 13px;
}

.order-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.order-amount {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 15px;
}

.order-status {
  padding: 4px 8px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.order-status.completed {
  background-color: var(--success-light);
  color: var(--success-color);
}

.order-status.pending {
  background-color: var(--warning-light);
  color: var(--warning-color);
}

.order-status.processing {
  background-color: var(--info-light);
  color: var(--info-color);
}

.view-all-btn {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: var(--primary-500);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color var(--transition-fast);
  gap: var(--spacing-xs);
}

.view-all-btn:hover {
  color: var(--primary-600);
}

.view-all-btn i {
  font-size: 18px;
}

/* Top Products */
.products-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.product-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  border-bottom: 1px solid var(--border-color);
  background-color: var(--bg-color);
  transition: all var(--transition-fast);
}

.product-item:hover {
  background-color: var(--neutral-100);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.dark-mode .product-item:hover {
  background-color: var(--neutral-800);
}

.product-item:last-child {
  border-bottom: none;
}

.product-rank {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  background-color: var(--neutral-100);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 13px;
  color: var(--text-secondary);
}

.dark-mode .product-rank {
  background-color: var(--neutral-800);
}

.product-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
  margin-bottom: 2px;
}

.product-category {
  color: var(--text-secondary);
  font-size: 13px;
}

.product-metrics {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.product-sales, .product-revenue {
  display: flex;
  align-items: center;
  gap: 4px;
}

.metrics-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.metrics-value {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.product-revenue .metrics-value {
  color: var(--success-color);
}

/* Loading state for products */
.loading-products {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl) 0;
  color: var(--text-secondary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--neutral-200);
  border-top-color: var(--primary-500);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-md);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty state styling */
.empty-state {
  padding: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  text-align: center;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.empty-state p {
  margin-bottom: var(--spacing-lg);
}

.empty-action-btn {
  margin-top: var(--spacing-md);
  border: none;
  background-color: var(--primary-500);
  color: white;
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-weight: 500;
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.empty-action-btn:hover {
  background-color: var(--primary-600);
}

/* Quick Actions Section */
.quick-actions-section {
  margin-bottom: var(--spacing-xl);
  animation: fadeInUp 0.6s var(--transition-base) both;
  animation-delay: var(--delay, 0s);
}

.section-header {
  margin-bottom: var(--spacing-lg);
}

.section-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--text-primary);
}

.section-header p {
  font-size: 14px;
  color: var(--text-secondary);
  margin: 0;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-lg);
}

.action-card {
  background-color: var(--card-bg);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
  animation: fadeInUp 0.7s cubic-bezier(0.23, 1, 0.32, 1) both;
  animation-delay: calc(var(--delay, 0s) + var(--card-delay, 0s));
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.action-hover-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0) 70%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
  pointer-events: none;
}

.dark-mode .action-hover-effect {
  background: radial-gradient(
    circle at var(--x, 50%) var(--y, 50%),
    rgba(255, 255, 255, 0.05) 0%,
    rgba(255, 255, 255, 0) 70%
  );
}

.action-card:hover .action-hover-effect {
  opacity: 1;
}

.action-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: var(--spacing-md);
  transition: transform var(--transition-base);
}

.action-card:hover .action-icon {
  transform: scale(1.1);
}

.action-icon i {
  font-size: 32px;
}

.action-name {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 15px;
  text-align: center;
  position: relative;
  z-index: 1;
}

/* Sidebar Overlay */
.sidebar-overlay {
  display: none;
  opacity: 0;
}

/* Mobile Responsiveness */
@media (max-width: 1200px) {
  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 1024px) {
  .sidebar {
    transform: translateX(-100%);
    box-shadow: var(--shadow-lg);
    z-index: 1200; /* Ensure sidebar stays above all content */
  }

  .sidebar.mobile-open {
    transform: translateX(0);
    width: var(--sidebar-width);
  }

  .sidebar.collapsed {
    transform: translateX(-100%); /* Hide when collapsed on mobile */
  }

  .main-content, .main-content.sidebar-collapsed {
    margin-left: 0;
  }

  .mobile-toggle {
    display: flex;
  }

  .header-middle {
    justify-content: flex-start;
  }

  /* We already have a sidebar-overlay class defined earlier */
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }

  .top-header {
    padding: 0 var(--spacing-md);
  }

  .header-middle {
    display: none;
  }

  .header-right {
    gap: var(--spacing-xs);
  }

  .date-display {
    display: none;
  }

  .dashboard-summary {
    flex-direction: column;
    align-items: flex-start;
  }

  .welcome-message {
    margin-bottom: var(--spacing-md);
  }

  .dashboard-content {
    padding: var(--spacing-md);
  }

  .help-btn {
    display: none;
  }

  .mobile-avatar {
    display: block;
  }

  .user-dropdown {
    position: fixed;
    top: calc(var(--top-header-height) - 10px);
    right: var(--spacing-md);
    left: auto;
    width: 240px;
  }
}

@media (max-width: 576px) {
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