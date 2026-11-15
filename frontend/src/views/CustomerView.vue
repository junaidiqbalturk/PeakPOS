<template>
  <AppLayout page-title="Customer Ledger & Accounts">
    <div class="customers-container">
      <!-- Toolbar -->
      <div class="customers-toolbar">
        <div class="toolbar-left">
          <h2>Customer Directory & Receivables</h2>
          <p>Manage customer profiles, credit ledgers, loyalty tiers, and prescriber records</p>
        </div>
        <div class="toolbar-right">
          <div class="search-input-wrap">
            <i class="material-icons">search</i>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search by name, phone, or prescriber..."
              class="customer-search-input"
            />
            <button v-if="searchQuery" @click="searchQuery = ''" class="btn-clear-search">&times;</button>
          </div>
          <button class="btn-add-customer" @click="openAddCustomerModal">
            <i class="material-icons">person_add</i>
            <span>New Customer</span>
          </button>
        </div>
      </div>

      <!-- Preserved 3D Metric Cards with Hover Effects and Glow -->
      <div class="metrics-grid">
        <!-- Active Customers Card -->
        <div class="metric-card sales">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">groups</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Active Customers</span>
              <div class="metric-value">{{ filteredCustomers.length }}</div>
              <span class="metric-sub">Registered store profiles</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Ledger Receivables Card -->
        <div class="metric-card alerts">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">account_balance_wallet</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Ledger Receivables</span>
              <div class="metric-value">${{ formatMoney(totalReceivables) }}</div>
              <span class="metric-sub">Pending credit balances</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Total Customer Spend -->
        <div class="metric-card orders">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">paid</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Total Purchases</span>
              <div class="metric-value">${{ formatMoney(totalPurchases) }}</div>
              <span class="metric-sub">Lifetime customer spend</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- VIP Members -->
        <div class="metric-card products">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">star</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">VIP / Gold Tier</span>
              <div class="metric-value">{{ vipCount }}</div>
              <span class="metric-sub">Loyalty club members</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>
      </div>

      <!-- Main Customers Table Card -->
      <div class="customer-table-card">
        <div class="table-header-strip">
          <div class="strip-left">
            <h3>Registered Account Directory</h3>
            <span class="count-pill">{{ filteredCustomers.length }} records</span>
          </div>
          <div class="strip-right">
            <div class="filter-pills">
              <button
                class="filter-pill"
                :class="{ active: activeFilter === 'all' }"
                @click="activeFilter = 'all'"
              >
                All
              </button>
              <button
                class="filter-pill"
                :class="{ active: activeFilter === 'due' }"
                @click="activeFilter = 'due'"
              >
                Has Balance Due
              </button>
              <button
                class="filter-pill"
                :class="{ active: activeFilter === 'vip' }"
                @click="activeFilter = 'vip'"
              >
                VIP Members
              </button>
            </div>
          </div>
        </div>

        <div class="table-responsive">
          <table class="customer-table">
            <thead>
              <tr>
                <th>Customer</th>
                <th>Phone / Contact</th>
                <th>Doctor / Prescriber</th>
                <th>Loyalty Tier</th>
                <th class="text-right">Total Purchases</th>
                <th class="text-right">Ledger Balance</th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredCustomers.length === 0">
                <td colspan="7" class="empty-table-cell">
                  <i class="material-icons">search_off</i>
                  <p>No customers match your search criteria.</p>
                </td>
              </tr>
              <tr v-for="c in filteredCustomers" :key="c.id">
                <td>
                  <div class="customer-profile-cell">
                    <div class="avatar-sm">{{ getInitials(c.name) }}</div>
                    <div>
                      <strong class="cust-name">{{ c.name }}</strong>
                      <span class="cust-email">{{ c.email || 'No email registered' }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="phone-cell">
                    <i class="material-icons phone-icon">call</i>
                    <span>{{ c.phone || 'N/A' }}</span>
                  </div>
                </td>
                <td>
                  <span class="doctor-badge" v-if="c.doctor">
                    <i class="material-icons">medical_services</i>
                    {{ c.doctor }}
                  </span>
                  <span v-else class="text-muted">—</span>
                </td>
                <td>
                  <span class="loyalty-badge" :class="'tier-' + c.tier.toLowerCase()">
                    {{ c.tier }}
                  </span>
                </td>
                <td class="text-right font-bold">${{ formatMoney(c.totalPurchases) }}</td>
                <td class="text-right">
                  <span
                    class="balance-pill"
                    :class="{ 'has-debt': c.balance > 0, 'zero-debt': c.balance <= 0 }"
                  >
                    ${{ formatMoney(c.balance) }}
                  </span>
                </td>
                <td class="text-center">
                  <div class="action-buttons-group">
                    <button
                      class="btn-icon-action"
                      title="Settle / Adjust Ledger"
                      @click="openLedgerModal(c)"
                    >
                      <i class="material-icons">receipt</i>
                    </button>
                    <button
                      class="btn-icon-action"
                      title="Edit Customer"
                      @click="editCustomer(c)"
                    >
                      <i class="material-icons">edit</i>
                    </button>
                    <button
                      class="btn-icon-action text-danger"
                      title="Delete Customer"
                      @click="deleteCustomer(c.id)"
                    >
                      <i class="material-icons">delete_outline</i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Add/Edit Customer Modal -->
      <div v-if="showCustomerModal" class="pos-modal-overlay" @click.self="showCustomerModal = false">
        <div class="pos-modal-dialog">
          <header class="dialog-header">
            <div class="dialog-title-group">
              <i class="material-icons">person</i>
              <h3>{{ editingCustomer.id ? 'Edit Customer' : 'Create New Customer' }}</h3>
            </div>
            <button class="dialog-close-btn" @click="showCustomerModal = false">
              <i class="material-icons">close</i>
            </button>
          </header>

          <form @submit.prevent="saveCustomer" class="dialog-form">
            <div class="form-row">
              <div class="form-group">
                <label>Full Name *</label>
                <input type="text" v-model="customerForm.name" required placeholder="e.g. John Doe" />
              </div>
              <div class="form-group">
                <label>Phone Number *</label>
                <input type="tel" v-model="customerForm.phone" required placeholder="e.g. +1 555-0192" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Email Address</label>
                <input type="email" v-model="customerForm.email" placeholder="john@example.com" />
              </div>
              <div class="form-group">
                <label>Doctor / Prescriber (Optional)</label>
                <input type="text" v-model="customerForm.doctor" placeholder="e.g. Dr. Robert Vance" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Loyalty Tier</label>
                <select v-model="customerForm.tier">
                  <option value="Bronze">Bronze (Standard)</option>
                  <option value="Silver">Silver (5% Off)</option>
                  <option value="Gold">Gold (VIP 10% Off)</option>
                </select>
              </div>
              <div class="form-group">
                <label>Initial Ledger Credit ($)</label>
                <input type="number" step="0.01" v-model.number="customerForm.balance" placeholder="0.00" />
              </div>
            </div>

            <div class="dialog-footer">
              <button type="button" class="btn-cancel" @click="showCustomerModal = false">Cancel</button>
              <button type="submit" class="btn-primary-action">Save Customer</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Ledger Payment Modal -->
      <div v-if="showLedgerModal" class="pos-modal-overlay" @click.self="showLedgerModal = false">
        <div class="pos-modal-dialog ledger-dialog">
          <header class="dialog-header">
            <div class="dialog-title-group">
              <i class="material-icons">receipt_long</i>
              <div>
                <h3>Customer Ledger Settlement</h3>
                <p>{{ activeLedgerCustomer ? activeLedgerCustomer.name : '' }}</p>
              </div>
            </div>
            <button class="dialog-close-btn" @click="showLedgerModal = false">
              <i class="material-icons">close</i>
            </button>
          </header>

          <div class="ledger-modal-body">
            <div class="ledger-balance-box">
              <span>Current Outstanding Balance</span>
              <strong class="balance-display">${{ formatMoney(activeLedgerCustomer ? activeLedgerCustomer.balance : 0) }}</strong>
            </div>

            <div class="form-group">
              <label>Payment / Credit Adjustment Amount ($)</label>
              <input
                type="number"
                step="0.01"
                v-model.number="ledgerPaymentAmount"
                class="ledger-amt-input"
                placeholder="0.00"
              />
            </div>

            <div class="quick-adjust-buttons">
              <button
                type="button"
                class="btn-chip"
                @click="ledgerPaymentAmount = activeLedgerCustomer ? activeLedgerCustomer.balance : 0"
              >
                Clear Full Balance
              </button>
              <button type="button" class="btn-chip" @click="ledgerPaymentAmount = 20">+$20</button>
              <button type="button" class="btn-chip" @click="ledgerPaymentAmount = 50">+$50</button>
            </div>
          </div>

          <div class="dialog-footer">
            <button type="button" class="btn-cancel" @click="showLedgerModal = false">Cancel</button>
            <button type="button" class="btn-primary-action" @click="applyLedgerPayment">Post Payment</button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout.vue';
import '@/assets/cards.css';

const DEFAULT_CUSTOMERS = [
  { id: 1, name: 'Walk-in Customer', phone: 'General POS', email: '', doctor: '', tier: 'Bronze', balance: 0.00, totalPurchases: 450.25 },
  { id: 2, name: 'Sarah Jenkins', phone: '+1 (555) 234-5678', email: 'sarah.j@gmail.com', doctor: 'Dr. Michael Chen', tier: 'Gold', balance: 145.50, totalPurchases: 1850.00 },
  { id: 3, name: 'David Miller', phone: '+1 (555) 876-5432', email: 'miller.d@outlook.com', doctor: 'Dr. Sarah Vance', tier: 'Silver', balance: 0.00, totalPurchases: 890.75 },
  { id: 4, name: 'Emily Watson', phone: '+1 (555) 345-6789', email: 'emily.w@yahoo.com', doctor: 'Dr. Robert Vance', tier: 'Bronze', balance: 42.00, totalPurchases: 320.10 },
  { id: 5, name: 'James Peterson', phone: '+1 (555) 654-9870', email: 'j.peterson@tech.co', doctor: '', tier: 'Gold', balance: 0.00, totalPurchases: 2450.60 }
];

export default {
  name: 'CustomerView',
  components: {
    AppLayout
  },
  data() {
    return {
      customers: [],
      searchQuery: '',
      activeFilter: 'all',
      showCustomerModal: false,
      showLedgerModal: false,
      editingCustomer: {},
      customerForm: {
        name: '',
        phone: '',
        email: '',
        doctor: '',
        tier: 'Bronze',
        balance: 0
      },
      activeLedgerCustomer: null,
      ledgerPaymentAmount: 0
    };
  },
  computed: {
    filteredCustomers() {
      return this.customers.filter(c => {
        const matchesSearch =
          c.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          (c.phone && c.phone.includes(this.searchQuery)) ||
          (c.doctor && c.doctor.toLowerCase().includes(this.searchQuery.toLowerCase()));

        if (!matchesSearch) return false;

        if (this.activeFilter === 'due') {
          return c.balance > 0;
        }
        if (this.activeFilter === 'vip') {
          return c.tier === 'Gold';
        }
        return true;
      });
    },
    totalReceivables() {
      return this.customers.reduce((sum, c) => sum + (Number(c.balance) || 0), 0);
    },
    totalPurchases() {
      return this.customers.reduce((sum, c) => sum + (Number(c.totalPurchases) || 0), 0);
    },
    vipCount() {
      return this.customers.filter(c => c.tier === 'Gold').length;
    }
  },
  mounted() {
    this.loadCustomers();
  },
  methods: {
    loadCustomers() {
      const stored = localStorage.getItem('peakpos_customers');
      if (stored) {
        try {
          this.customers = JSON.parse(stored);
        } catch {
          this.customers = DEFAULT_CUSTOMERS;
        }
      } else {
        this.customers = DEFAULT_CUSTOMERS;
        localStorage.setItem('peakpos_customers', JSON.stringify(DEFAULT_CUSTOMERS));
      }
    },
    saveToStorage() {
      localStorage.setItem('peakpos_customers', JSON.stringify(this.customers));
    },
    getInitials(name) {
      if (!name) return 'CU';
      const parts = name.trim().split(' ');
      if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
      return name.substring(0, 2).toUpperCase();
    },
    formatMoney(val) {
      const num = Number(val) || 0;
      return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
    openAddCustomerModal() {
      this.editingCustomer = {};
      this.customerForm = {
        name: '',
        phone: '',
        email: '',
        doctor: '',
        tier: 'Bronze',
        balance: 0
      };
      this.showCustomerModal = true;
    },
    editCustomer(cust) {
      this.editingCustomer = { ...cust };
      this.customerForm = { ...cust };
      this.showCustomerModal = true;
    },
    deleteCustomer(id) {
      if (confirm('Are you sure you want to remove this customer record?')) {
        this.customers = this.customers.filter(c => c.id !== id);
        this.saveToStorage();
      }
    },
    saveCustomer() {
      if (this.editingCustomer.id) {
        const index = this.customers.findIndex(c => c.id === this.editingCustomer.id);
        if (index !== -1) {
          this.customers[index] = {
            ...this.customers[index],
            ...this.customerForm
          };
        }
      } else {
        const newCust = {
          id: Date.now(),
          ...this.customerForm,
          totalPurchases: 0
        };
        this.customers.unshift(newCust);
      }
      this.saveToStorage();
      this.showCustomerModal = false;
    },
    openLedgerModal(cust) {
      this.activeLedgerCustomer = cust;
      this.ledgerPaymentAmount = 0;
      this.showLedgerModal = true;
    },
    applyLedgerPayment() {
      if (!this.activeLedgerCustomer || this.ledgerPaymentAmount <= 0) return;
      this.activeLedgerCustomer.balance = Math.max(0, this.activeLedgerCustomer.balance - this.ledgerPaymentAmount);
      this.saveToStorage();
      this.showLedgerModal = false;
    }
  }
};
</script>

<style scoped>
.customers-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Toolbar */
.customers-toolbar {
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

.dark-theme .customers-toolbar {
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
  gap: 12px;
}

.search-input-wrap {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 6px 12px;
  gap: 8px;
  min-width: 300px;
}

.dark-theme .search-input-wrap {
  background: #0f172a;
  border-color: #334155;
}

.search-input-wrap i {
  color: #94a3b8;
  font-size: 1.2rem;
}

.customer-search-input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.85rem;
  color: #1e293b;
  width: 100%;
}

.dark-theme .customer-search-input {
  color: #f8fafc;
}

.btn-clear-search {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #94a3b8;
  cursor: pointer;
}

.btn-add-customer {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #4338ca 0%, #3730a3 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 800;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(67, 56, 202, 0.3);
  transition: transform 0.15s;
}

.btn-add-customer:hover {
  transform: translateY(-1px);
}

/* Table Card */
.customer-table-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05);
  overflow: hidden;
}

.dark-theme .customer-table-card {
  background: #1e293b;
  border-color: #334155;
}

.table-header-strip {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 22px;
  border-bottom: 1px solid #f1f5f9;
}

.dark-theme .table-header-strip {
  border-bottom-color: #334155;
}

.strip-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.strip-left h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .strip-left h3 {
  color: #f8fafc;
}

.count-pill {
  font-size: 0.72rem;
  font-weight: 700;
  background: #f1f5f9;
  color: #64748b;
  padding: 2px 8px;
  border-radius: 6px;
}

.dark-theme .count-pill {
  background: #334155;
  color: #94a3b8;
}

.filter-pills {
  display: flex;
  gap: 6px;
}

.filter-pill {
  background: #f1f5f9;
  border: none;
  padding: 5px 12px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.dark-theme .filter-pill {
  background: #0f172a;
  color: #94a3b8;
}

.filter-pill.active {
  background: #4338ca;
  color: white;
}

/* Table */
.table-responsive {
  overflow-x: auto;
}

.customer-table {
  width: 100%;
  border-collapse: collapse;
}

.customer-table th {
  text-align: left;
  font-size: 0.72rem;
  font-weight: 800;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 12px 18px;
  border-bottom: 2px solid #e2e8f0;
}

.dark-theme .customer-table th {
  border-bottom-color: #334155;
  color: #94a3b8;
}

.customer-table td {
  padding: 14px 18px;
  font-size: 0.88rem;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
}

.dark-theme .customer-table td {
  border-bottom-color: #334155;
  color: #f1f5f9;
}

.customer-profile-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-sm {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.8rem;
}

.cust-name {
  display: block;
  font-size: 0.88rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .cust-name {
  color: #f8fafc;
}

.cust-email {
  display: block;
  font-size: 0.72rem;
  color: #64748b;
}

.phone-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
  color: #475569;
}

.dark-theme .phone-cell {
  color: #cbd5e1;
}

.phone-icon {
  font-size: 1rem;
  color: #94a3b8;
}

.doctor-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  background: #f0fdf4;
  color: #15803d;
  padding: 3px 8px;
  border-radius: 6px;
}

.loyalty-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 8px;
}

.tier-gold {
  background: #fef3c7;
  color: #b45309;
}

.tier-silver {
  background: #f1f5f9;
  color: #475569;
}

.tier-bronze {
  background: #ffedd5;
  color: #9a3412;
}

.balance-pill {
  font-size: 0.85rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 8px;
}

.balance-pill.has-debt {
  background: #fee2e2;
  color: #b91c1c;
}

.balance-pill.zero-debt {
  background: #dcfce7;
  color: #15803d;
}

.action-buttons-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-icon-action {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background: #ffffff;
  color: #475569;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
}

.dark-theme .btn-icon-action {
  background: #0f172a;
  border-color: #334155;
  color: #cbd5e1;
}

.btn-icon-action:hover {
  background: #f1f5f9;
  color: #4338ca;
}

.text-danger:hover {
  color: #ef4444;
  border-color: #fca5a5;
}

/* Modals */
.pos-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.pos-modal-dialog {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 580px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  overflow: hidden;
}

.dark-theme .pos-modal-dialog {
  background: #1e293b;
  border: 1px solid #334155;
}

.dialog-header {
  padding: 18px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e2e8f0;
}

.dark-theme .dialog-header {
  border-bottom-color: #334155;
}

.dialog-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.dialog-title-group i {
  font-size: 1.6rem;
  color: #4338ca;
}

.dialog-title-group h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .dialog-title-group h3 {
  color: #f8fafc;
}

.dialog-close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 1.2rem;
}

.dialog-form {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #475569;
}

.dark-theme .form-group label {
  color: #94a3b8;
}

.form-group input, .form-group select {
  padding: 9px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.85rem;
  outline: none;
  background: #ffffff;
  color: #0f172a;
}

.dark-theme .form-group input, .dark-theme .form-group select {
  background: #0f172a;
  border-color: #334155;
  color: #f8fafc;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 24px;
  border-top: 1px solid #e2e8f0;
}

.dark-theme .dialog-footer {
  border-top-color: #334155;
}

.btn-cancel {
  padding: 8px 16px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #475569;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

.btn-primary-action {
  padding: 8px 20px;
  background: #4338ca;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 800;
  cursor: pointer;
}

/* Ledger Modal */
.ledger-modal-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ledger-balance-box {
  background: #fef2f2;
  border: 1px solid #fecaca;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.ledger-balance-box span {
  font-size: 0.78rem;
  color: #991b1b;
  font-weight: 700;
}

.balance-display {
  font-size: 1.8rem;
  font-weight: 900;
  color: #b91c1c;
}

.ledger-amt-input {
  font-size: 1.25rem !important;
  font-weight: 800;
  text-align: center;
}

.quick-adjust-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.btn-chip {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #4338ca;
  cursor: pointer;
}
</style>
