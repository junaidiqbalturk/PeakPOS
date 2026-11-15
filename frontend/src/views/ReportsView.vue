<template>
  <AppLayout page-title="Reports & Analytics">
    <div class="reports-container">
      <!-- Top Action & Filter Toolbar -->
      <div class="reports-toolbar">
        <div class="toolbar-left">
          <h2>Sales & Performance Insights</h2>
          <p>Real-time revenue, top selling items, and inventory velocity</p>
        </div>
        <div class="toolbar-right">
          <div class="preset-group">
            <button
              v-for="p in presets"
              :key="p.id"
              class="preset-pill"
              :class="{ active: activePreset === p.id }"
              @click="selectPreset(p.id)"
            >
              {{ p.label }}
            </button>
          </div>
          <div class="custom-date-inputs">
            <input type="date" v-model="startDate" @change="fetchReports" class="date-input" />
            <span class="to-text">to</span>
            <input type="date" v-model="endDate" @change="fetchReports" class="date-input" />
          </div>
          <button class="btn-export" @click="exportCSV" title="Export report to CSV">
            <i class="material-icons">file_download</i>
            <span>Export CSV</span>
          </button>
          <button class="btn-refresh" @click="fetchReports" :disabled="loading" title="Refresh data">
            <i class="material-icons" :class="{ 'spin': loading }">refresh</i>
          </button>
        </div>
      </div>

      <!-- Preserved 3D Metric Cards with Hover Effects and Glow -->
      <div class="metrics-grid">
        <!-- Revenue Card -->
        <div class="metric-card sales">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">payments</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Total Revenue</span>
              <div class="metric-value">${{ formatMoney(salesSummary.total_revenue) }}</div>
              <span class="metric-sub">Across {{ salesSummary.total_orders }} transactions</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Orders Card -->
        <div class="metric-card orders">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">receipt_long</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Orders Processed</span>
              <div class="metric-value">{{ salesSummary.total_orders }}</div>
              <span class="metric-sub">Completed customer checkouts</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Average Order Value (AOV) -->
        <div class="metric-card products">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">trending_up</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Avg Order Value</span>
              <div class="metric-value">${{ formatMoney(averageOrderValue) }}</div>
              <span class="metric-sub">Average spend per ticket</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Low Stock Alerts -->
        <div class="metric-card alerts">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">warning_amber</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Low Stock Alerts</span>
              <div class="metric-value">{{ inventoryStats.low_stock_count || 0 }}</div>
              <span class="metric-sub">Items below safety threshold</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>
      </div>

      <!-- Main Analytics Two-Column Section -->
      <div class="reports-split-grid">
        <!-- Daily Revenue Breakdown Card -->
        <div class="report-panel-card">
          <div class="panel-card-header">
            <div class="panel-header-title">
              <i class="material-icons">bar_chart</i>
              <h3>Daily Revenue Breakdown</h3>
            </div>
            <span class="panel-tag">{{ salesSummary.daily_data ? salesSummary.daily_data.length : 0 }} Days Logged</span>
          </div>

          <div class="panel-card-body">
            <div v-if="loading" class="panel-loading">
              <i class="material-icons spin">sync</i>
              <span>Loading daily sales...</span>
            </div>
            <div v-else-if="!salesSummary.daily_data || salesSummary.daily_data.length === 0" class="panel-empty">
              <i class="material-icons">event_busy</i>
              <p>No orders found for the selected period.</p>
            </div>
            <div v-else class="table-responsive">
              <table class="report-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th class="text-center">Orders</th>
                    <th class="text-right">Revenue</th>
                    <th class="text-right">Avg / Order</th>
                    <th>Volume Share</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="d in salesSummary.daily_data" :key="d.date">
                    <td class="font-bold">{{ formatDate(d.date) }}</td>
                    <td class="text-center">
                      <span class="order-badge">{{ d.orders }}</span>
                    </td>
                    <td class="text-right font-bold text-success">${{ formatMoney(d.revenue) }}</td>
                    <td class="text-right">${{ formatMoney(d.orders ? d.revenue / d.orders : 0) }}</td>
                    <td>
                      <div class="progress-bar-wrap">
                        <div
                          class="progress-fill"
                          :style="{ width: calculateShare(d.revenue, salesSummary.total_revenue) + '%' }"
                        ></div>
                        <span class="share-label">{{ calculateShare(d.revenue, salesSummary.total_revenue) }}%</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Best-Selling Products Leaderboard -->
        <div class="report-panel-card">
          <div class="panel-card-header">
            <div class="panel-header-title">
              <i class="material-icons">leaderboard</i>
              <h3>Top Selling Products</h3>
            </div>
            <span class="panel-tag">By Quantity Sold</span>
          </div>

          <div class="panel-card-body">
            <div v-if="loading" class="panel-loading">
              <i class="material-icons spin">sync</i>
              <span>Calculating top sellers...</span>
            </div>
            <div v-else-if="!bestSellers || bestSellers.length === 0" class="panel-empty">
              <i class="material-icons">shopping_bag</i>
              <p>No product sales recorded yet.</p>
            </div>
            <div v-else class="leaderboard-list">
              <div
                v-for="(item, index) in bestSellers"
                :key="item.id"
                class="leaderboard-item"
              >
                <div class="rank-badge" :class="'rank-' + (index + 1)">
                  {{ index + 1 }}
                </div>
                <div class="item-info">
                  <div class="item-title">{{ item.name }}</div>
                  <div class="item-category">{{ item.category || 'Standard Category' }}</div>
                </div>
                <div class="item-stats">
                  <strong class="item-sold">{{ item.total_sold }} units</strong>
                  <span class="item-revenue">${{ formatMoney(item.total_revenue) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Low Stock Reorder Table -->
      <div class="report-panel-card full-width-card" v-if="lowStockProducts.length > 0">
        <div class="panel-card-header alert-header">
          <div class="panel-header-title">
            <i class="material-icons text-warning">notification_important</i>
            <h3>Low Stock Inventory Reorder Watchlist</h3>
          </div>
          <router-link to="/admin/products" class="panel-link">Manage Inventory &rarr;</router-link>
        </div>
        <div class="panel-card-body">
          <table class="report-table">
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Category</th>
                <th class="text-right">Unit Price</th>
                <th class="text-center">Stock Remaining</th>
                <th>Status</th>
                <th class="text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prod in lowStockProducts" :key="prod.id">
                <td class="font-bold">{{ prod.name }}</td>
                <td>{{ prod.category || 'General' }}</td>
                <td class="text-right">${{ formatMoney(prod.price) }}</td>
                <td class="text-center">
                  <span class="stock-pill critical">{{ prod.quantity }} left</span>
                </td>
                <td>
                  <span class="status-warning-badge">Reorder Suggested</span>
                </td>
                <td class="text-right">
                  <router-link to="/admin/products" class="btn-table-action">Restock</router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout.vue';
import api from '@/services/api';
import '@/assets/cards.css';

export default {
  name: 'ReportsView',
  components: {
    AppLayout
  },
  data() {
    return {
      loading: false,
      activePreset: '7days',
      presets: [
        { id: 'today', label: 'Today' },
        { id: '7days', label: 'Last 7 Days' },
        { id: '30days', label: 'Last 30 Days' },
        { id: 'month', label: 'This Month' }
      ],
      startDate: '',
      endDate: '',
      salesSummary: {
        total_revenue: 0,
        total_orders: 0,
        daily_data: []
      },
      bestSellers: [],
      lowStockProducts: [],
      inventoryStats: {}
    };
  },
  computed: {
    averageOrderValue() {
      if (!this.salesSummary.total_orders || this.salesSummary.total_orders === 0) return 0;
      return this.salesSummary.total_revenue / this.salesSummary.total_orders;
    }
  },
  mounted() {
    this.selectPreset('7days');
  },
  methods: {
    selectPreset(presetId) {
      this.activePreset = presetId;
      const today = new Date();
      const end = new Date(today);
      let start = new Date(today);

      if (presetId === 'today') {
        // start is today
      } else if (presetId === '7days') {
        start.setDate(today.getDate() - 7);
      } else if (presetId === '30days') {
        start.setDate(today.getDate() - 30);
      } else if (presetId === 'month') {
        start = new Date(today.getFullYear(), today.getMonth(), 1);
      }

      this.startDate = start.toISOString().split('T')[0];
      this.endDate = end.toISOString().split('T')[0];
      this.fetchReports();
    },
    async fetchReports() {
      this.loading = true;
      try {
        const [summaryRes, bestSellerRes, stockRes] = await Promise.all([
          api.get(`/sales-summary?start_date=${this.startDate}&end_date=${this.endDate}`).catch(() => ({ data: { total_revenue: 0, total_orders: 0, daily_data: [] } })),
          api.get('/best-selling-products?limit=6').catch(() => ({ data: [] })),
          api.get('/inventory-status?threshold=10').catch(() => ({ data: { low_stock_products: [], inventory_stats: {} } }))
        ]);

        this.salesSummary = summaryRes.data || { total_revenue: 0, total_orders: 0, daily_data: [] };
        this.bestSellers = bestSellerRes.data || [];
        this.lowStockProducts = (stockRes.data && stockRes.data.low_stock_products) || [];
        this.inventoryStats = (stockRes.data && stockRes.data.inventory_stats) || {};
      } catch (err) {
        console.error('Error fetching reports:', err);
      } finally {
        this.loading = false;
      }
    },
    formatMoney(val) {
      const num = Number(val) || 0;
      return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },
    calculateShare(part, total) {
      if (!total || total === 0) return 0;
      return Math.round((Number(part) / Number(total)) * 100);
    },
    exportCSV() {
      if (!this.salesSummary.daily_data || this.salesSummary.daily_data.length === 0) {
        alert('No data available to export.');
        return;
      }
      let csv = 'Date,Orders,Revenue,Avg_Order_Value\n';
      this.salesSummary.daily_data.forEach(d => {
        const aov = d.orders ? (d.revenue / d.orders).toFixed(2) : '0.00';
        csv += `${d.date},${d.orders},${d.revenue},${aov}\n`;
      });
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', `PeakPOS_Report_${this.startDate}_to_${this.endDate}.csv`);
      a.click();
    }
  }
};
</script>

<style scoped>
.reports-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Toolbar */
.reports-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  background: #ffffff;
  padding: 18px 24px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

.dark-theme .reports-toolbar {
  background: #1e293b;
  border-color: #334155;
}

.toolbar-left h2 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .toolbar-left h2 {
  color: #f8fafc;
}

.toolbar-left p {
  margin: 4px 0 0 0;
  font-size: 0.85rem;
  color: #64748b;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.preset-group {
  display: flex;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 10px;
}

.dark-theme .preset-group {
  background: #0f172a;
}

.preset-pill {
  border: none;
  background: transparent;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.preset-pill.active {
  background: #ffffff;
  color: #4338ca;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.dark-theme .preset-pill.active {
  background: #334155;
  color: #818cf8;
}

.custom-date-inputs {
  display: flex;
  align-items: center;
  gap: 6px;
}

.date-input {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 0.82rem;
  outline: none;
  background: #ffffff;
  color: #1e293b;
}

.dark-theme .date-input {
  background: #0f172a;
  border-color: #334155;
  color: #f8fafc;
}

.to-text {
  font-size: 0.78rem;
  color: #94a3b8;
  font-weight: 600;
}

.btn-export {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #334155;
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.dark-theme .btn-export {
  background: #0f172a;
  border-color: #334155;
  color: #e2e8f0;
}

.btn-export:hover {
  background: #e2e8f0;
}

.btn-refresh {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #4338ca;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Two-column layout */
.reports-split-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .reports-split-grid {
    grid-template-columns: 1fr;
  }
}

.report-panel-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05);
  overflow: hidden;
}

.dark-theme .report-panel-card {
  background: #1e293b;
  border-color: #334155;
}

.panel-card-header {
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f1f5f9;
}

.dark-theme .panel-card-header {
  border-bottom-color: #334155;
}

.panel-header-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-header-title h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .panel-header-title h3 {
  color: #f8fafc;
}

.panel-tag {
  font-size: 0.72rem;
  font-weight: 700;
  background: #eef2ff;
  color: #4338ca;
  padding: 3px 8px;
  border-radius: 6px;
}

.dark-theme .panel-tag {
  background: rgba(99,102,241,0.2);
  color: #818cf8;
}

.panel-card-body {
  padding: 16px 20px;
}

.panel-loading, .panel-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #94a3b8;
  gap: 10px;
}

/* Tables */
.table-responsive {
  overflow-x: auto;
}

.report-table {
  width: 100%;
  border-collapse: collapse;
}

.report-table th {
  text-align: left;
  font-size: 0.72rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 10px 12px;
  border-bottom: 2px solid #e2e8f0;
}

.dark-theme .report-table th {
  border-bottom-color: #334155;
  color: #94a3b8;
}

.report-table td {
  padding: 12px;
  font-size: 0.85rem;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
}

.dark-theme .report-table td {
  border-bottom-color: #334155;
  color: #f1f5f9;
}

.text-center { text-align: center; }
.text-right { text-align: right; }
.font-bold { font-weight: 700; }
.text-success { color: #10b981; }

.order-badge {
  background: #f1f5f9;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.8rem;
}

.dark-theme .order-badge {
  background: #334155;
}

.progress-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-fill {
  height: 8px;
  background: linear-gradient(90deg, #6366f1, #4338ca);
  border-radius: 4px;
  min-width: 4px;
}

.share-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
}

/* Leaderboard list */
.leaderboard-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.leaderboard-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 14px;
  border-radius: 12px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  transition: transform 0.2s;
}

.dark-theme .leaderboard-item {
  background: #0f172a;
  border-color: #334155;
}

.leaderboard-item:hover {
  transform: translateX(4px);
}

.rank-badge {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #cbd5e1;
  color: #1e293b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
}

.rank-1 { background: #fbbf24; color: #78350f; }
.rank-2 { background: #94a3b8; color: #0f172a; }
.rank-3 { background: #f97316; color: #ffffff; }

.item-info {
  flex: 1;
}

.item-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
}

.dark-theme .item-title {
  color: #f8fafc;
}

.item-category {
  font-size: 0.72rem;
  color: #64748b;
}

.item-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.item-sold {
  font-size: 0.85rem;
  color: #4338ca;
}

.dark-theme .item-sold {
  color: #818cf8;
}

.item-revenue {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

/* Alert Reorder table */
.full-width-card {
  margin-top: 10px;
}

.alert-header {
  background: #fffbeb;
}

.dark-theme .alert-header {
  background: rgba(245, 158, 11, 0.1);
}

.text-warning { color: #f59e0b; }

.panel-link {
  font-size: 0.82rem;
  font-weight: 700;
  color: #4338ca;
  text-decoration: none;
}

.stock-pill.critical {
  background: #fee2e2;
  color: #b91c1c;
  font-weight: 800;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 0.78rem;
}

.status-warning-badge {
  font-size: 0.75rem;
  font-weight: 700;
  background: #fef3c7;
  color: #b45309;
  padding: 3px 8px;
  border-radius: 6px;
}

.btn-table-action {
  display: inline-block;
  padding: 4px 10px;
  background: #4338ca;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.75rem;
  font-weight: 700;
}
</style>
