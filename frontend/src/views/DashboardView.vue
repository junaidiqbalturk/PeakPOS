<template>
  <div class="app-container">
    <!-- Left Navigation Sidebar -->
    <div class="sidebar">
      <div class="logo-container">
        <h2 class="logo">Peak<span>POS</span></h2>
      </div>
      <nav class="nav-menu">
        <router-link to="/" class="nav-item active">
          <i class="material-icons">dashboard</i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/sales" class="nav-item">
          <i class="material-icons">shopping_cart</i>
          <span>Sales</span>
        </router-link>
        <router-link to="/inventory" class="nav-item">
          <i class="material-icons">inventory</i>
          <span>Inventory</span>
        </router-link>
        <router-link to="/customers" class="nav-item">
          <i class="material-icons">people</i>
          <span>Customers</span>
        </router-link>
        <router-link to="/reports" class="nav-item">
          <i class="material-icons">bar_chart</i>
          <span>Reports</span>
        </router-link>
        <router-link to="/settings" class="nav-item">
          <i class="material-icons">settings</i>
          <span>Settings</span>
        </router-link>
      </nav>
      <div class="user-profile">
        <div class="avatar">JS</div>
        <div class="user-info">
          <span class="user-name">John Smith</span>
          <span class="user-role">Admin</span>
        </div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="main-content">
      <header class="top-bar">
        <div class="search-container">
          <i class="material-icons">search</i>
          <input type="text" placeholder="Search..." class="search-input" />
        </div>
        <div class="action-icons">
          <i class="material-icons">notifications</i>
          <i class="material-icons">help_outline</i>
        </div>
      </header>

      <div class="dashboard-content">
        <h1 class="page-title">Dashboard</h1>

        <!-- Metrics Cards -->
        <transition-group name="fade" tag="div" class="metrics-container">
          <div class="metric-card" key="sales">
            <div class="metric-icon sales">
              <i class="material-icons">attach_money</i>
            </div>
            <div class="metric-details">
              <h3>Today's Sales</h3>
              <p class="metric-value">${{ metrics.totalSales.toLocaleString() }}</p>
              <p class="metric-change positive">+12.5% <span>vs yesterday</span></p>
            </div>
          </div>

          <div class="metric-card" key="orders">
            <div class="metric-icon orders">
              <i class="material-icons">shopping_bag</i>
            </div>
            <div class="metric-details">
              <h3>Total Orders</h3>
              <p class="metric-value">{{ metrics.totalOrders }}</p>
              <p class="metric-change positive">+8.3% <span>vs yesterday</span></p>
            </div>
          </div>

          <div class="metric-card" key="customers">
            <div class="metric-icon customers">
              <i class="material-icons">person</i>
            </div>
            <div class="metric-details">
              <h3>Total Products</h3>
              <p class="metric-value">{{ metrics.totalOrders }}</p>
              <p class="metric-change positive">+5.2% <span>vs yesterday</span></p>
            </div>
          </div>

          <div class="metric-card" key="items">
            <div class="metric-icon items">
              <i class="material-icons">inventory_2</i>
            </div>
            <div class="metric-details">
              <h3>Items Sold</h3>
              <p class="metric-value">{{ metrics.itemsSold }}</p>
              <p class="metric-change negative">-2.1% <span>vs yesterday</span></p>
            </div>
          </div>
        </transition-group>

        <!-- Charts Section -->
        <div class="charts-container">
          <!-- Sales Overview Chart -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>Sales Overview</h3>
              <div class="chart-actions">
                <select v-model="salesPeriod" class="period-select">
                  <option value="day">Today</option>
                  <option value="week">This Week</option>
                  <option value="month">This Month</option>
                </select>
              </div>
            </div>
            <div class="chart-body">
              <canvas id="sales-chart" ref="salesChart"></canvas>
            </div>
          </div>

          <!-- Recent Orders Chart -->
          <div class="chart-card">
            <div class="chart-header">
              <h3>Recent Orders</h3>
              <button class="view-all-btn">View All</button>
            </div>
            <div class="chart-body orders-list">
              <div class="order-item" v-for="(order, index) in recentOrders" :key="index">
                <div class="order-info">
                  <p class="order-id">#{{ order.id }}</p>
                  <p class="order-customer">{{ order.customer }}</p>
                </div>
                <div class="order-details">
                  <p class="order-amount">${{ order.amount }}</p>
                  <span class="order-status" :class="order.status">{{ order.status }}</span>
                </div>
              </div>
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
  name: 'DashboardView',
  data() {
    return {
      salesPeriod: 'week',
      salesChart: null,
      metrics: {
        totalSales: 0,
        totalOrders: 0,
        totalProduct: 0,
        itemsSold: 0,
      },
      recentOrders: []
    };
  },
  mounted() {
    this.initSalesChart();
    this.loadMetrics();
  },
  methods: {
    async loadMetrics() {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          console.warn("No token found in localStorage.");
          return;
        }

        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };

        const [salesRes, ordersRes, productsRes] = await Promise.all([
          axios.get("http://127.0.0.1:5000/api/sales-summary", config),
          axios.get("http://127.0.0.1:5000/api/orders", config),
          axios.get("http://127.0.0.1:5000/api/products") // Assuming this is public
        ]);

        this.metrics.totalSales = salesRes.data.total_revenue || 0;
        this.metrics.totalOrders = ordersRes.data.length;
        this.metrics.totalProduct = productsRes.data.length;
        this.metrics.itemsSold = productsRes.data.reduce((sum, p) => sum + (p.stock || 0), 0);

        // Populate recentOrders from latest 5 orders (you can sort/filter on backend if needed)
        this.recentOrders = ordersRes.data.slice(0, 5).map(order => ({
          id: order.id,
          customer: order.customer_name || "N/A",  // Adapt to your backend schema
          amount: order.total || "0.00",
          status: order.status || "pending"
        }));
      } catch (error) {
        console.error("Failed to fetch dashboard metrics", error);
      }
    },

    initSalesChart() {
      const ctx = this.$refs.salesChart.getContext('2d');
      this.salesChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
          datasets: [{
            label: 'Sales',
            data: [200, 400, 300, 600, 500, 750],
            backgroundColor: 'rgba(33, 150, 243, 0.1)',
            borderColor: '#2196f3',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#2196f3'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: context => `$${context.parsed.y.toFixed(2)}`
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { callback: val => `$${val}` }
            }
          }
        }
      });
    }
  }
};
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

/* App Container */
.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: #f5f7fa;
}

/* Sidebar Navigation */
.sidebar {
  width: 260px;
  height: 100%;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
  z-index: 10;
  transition: all 0.3s ease;
}

.logo-container {
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.logo {
  font-size: 22px;
  font-weight: 700;
  color: #333;
}

.logo span {
  color: #2196f3;
}

.nav-menu {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 8px;
  color: #5f6368;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: #f5f7fa;
  color: #2196f3;
}

.nav-item.active {
  background-color: #e3f2fd;
  color: #2196f3;
  font-weight: 500;
}

.nav-item i {
  margin-right: 12px;
  font-size: 20px;
}

.user-profile {
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #2196f3;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
  font-size: 14px;
}

.user-role {
  color: #5f6368;
  font-size: 12px;
}

/* Main Content Area */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-bar {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background-color: #ffffff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  z-index: 5;
}

.search-container {
  display: flex;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 8px 16px;
  width: 300px;
}

.search-container i {
  color: #5f6368;
  margin-right: 8px;
}

.search-input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  width: 100%;
}

.action-icons {
  display: flex;
  align-items: center;
}

.action-icons i {
  margin-left: 16px;
  color: #5f6368;
  cursor: pointer;
  font-size: 20px;
}

.dashboard-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 24px;
}

/* Metrics Cards */
.metrics-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 24px;
  margin-bottom: 24px;
}

.metric-card {
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.metric-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.metric-icon i {
  font-size: 24px;
  color: white;
}

.metric-icon.sales {
  background-color: #2196f3;
}

.metric-icon.orders {
  background-color: #ff9800;
}

.metric-icon.customers {
  background-color: #4caf50;
}

.metric-icon.items {
  background-color: #9c27b0;
}

.metric-details h3 {
  font-size: 14px;
  font-weight: 500;
  color: #5f6368;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.metric-change {
  font-size: 13px;
  font-weight: 500;
}

.metric-change span {
  font-weight: 400;
  color: #5f6368;
}

.metric-change.positive {
  color: #4caf50;
}

.metric-change.negative {
  color: #f44336;
}

/* Charts Container */
.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 24px;
}

.chart-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.chart-header {
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f0f0f0;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.period-select {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
  background-color: white;
  font-size: 13px;
  outline: none;
  cursor: pointer;
}

.view-all-btn {
  padding: 6px 12px;
  font-size: 13px;
  color: #2196f3;
  background-color: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.view-all-btn:hover {
  background-color: #e3f2fd;
}

.chart-body {
  padding: 16px 20px;
  height: 300px;
}

/* Recent Orders List */
.orders-list {
  height: 300px;
  padding: 0;
  overflow-y: auto;
}

.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.order-id {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  margin-bottom: 4px;
}

.order-customer {
  font-size: 13px;
  color: #5f6368;
}

.order-amount {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  text-align: right;
  margin-bottom: 4px;
}

.order-status {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
}

.order-status.completed {
  background-color: #e8f5e9;
  color: #4caf50;
}

.order-status.processing {
  background-color: #e3f2fd;
  color: #2196f3;
}

.order-status.pending {
  background-color: #fff3e0;
  color: #ff9800;
}

/* Animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Responsive */
@media screen and (max-width: 1200px) {
  .metrics-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (max-width: 992px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
}

@media screen and (max-width: 768px) {
  .sidebar {
    width: 80px;
  }

  .logo {
    font-size: 18px;
    text-align: center;
  }

  .logo span {
    display: none;
  }

  .nav-item span {
    display: none;
  }

  .nav-item i {
    margin-right: 0;
  }

  .user-info {
    display: none;
  }

  .avatar {
    margin-right: 0;
    margin: 0 auto;
  }
}

@media screen and (max-width: 576px) {
  .metrics-container {
    grid-template-columns: 1fr;
  }

  .search-container {
    width: 200px;
  }
}
</style>