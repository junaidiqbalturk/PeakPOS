<template>
  <AppLayout page-title="Settings & Thermal Receipts">
    <div class="settings-studio">
      <!-- Top Action Toolbar -->
      <div class="settings-toolbar">
        <div class="toolbar-left">
          <h2>Store Configuration & Thermal Receipt Studio</h2>
          <p>Customize store identity, tax rates, currency, and design your 80mm/58mm thermal receipts with live preview</p>
        </div>
        <div class="toolbar-right">
          <button class="btn-print-test" @click="printTestReceipt">
            <i class="material-icons">print</i>
            <span>Test Print Receipt</span>
          </button>
          <button class="btn-save-primary" @click="saveReceiptSettings" :disabled="receiptSaving">
            <i class="material-icons" :class="{ 'spin': receiptSaving }">{{ receiptSaving ? 'sync' : 'save' }}</i>
            <span>{{ receiptSaving ? 'Saving...' : 'Save Settings' }}</span>
          </button>
        </div>
      </div>

      <!-- Preserved 3D Metric Cards with Hover Effects and Glow -->
      <div class="metrics-grid">
        <!-- Receipt Active Status -->
        <div class="metric-card sales">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">receipt</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Receipt Engine</span>
              <div class="metric-value">Active</div>
              <span class="metric-sub">{{ paperWidth }}mm Thermal Mode</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Store Logo Status -->
        <div class="metric-card products">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">image</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Store Branding</span>
              <div class="metric-value">{{ receiptSettings.logo_filename ? 'Logo Set' : 'Text Only' }}</div>
              <span class="metric-sub">{{ receiptSettings.business_name || 'PeakPOS Store' }}</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Default Tax Rate -->
        <div class="metric-card orders">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">percent</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Tax Rate</span>
              <div class="metric-value">{{ taxRate }}%</div>
              <span class="metric-sub">Standard Sales Tax</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>

        <!-- Currency Profile -->
        <div class="metric-card items">
          <div class="metric-card-inner">
            <div class="metric-icon-container">
              <div class="metric-icon">
                <i class="material-icons">attach_money</i>
              </div>
            </div>
            <div class="metric-content">
              <span class="metric-label">Currency Symbol</span>
              <div class="metric-value">{{ currencySymbol }} (USD)</div>
              <span class="metric-sub">Standard Tender Code</span>
            </div>
            <div class="metric-card-backdrop"></div>
            <div class="metric-card-glow"></div>
          </div>
        </div>
      </div>

      <!-- Studio Split View: Configuration Form vs Live Receipt Canvas -->
      <div class="studio-split-grid">
        <!-- Left: Configuration Form Card -->
        <div class="config-card">
          <div class="card-section-title">
            <i class="material-icons">store</i>
            <h3>1. Store Identity & Thermal Header</h3>
          </div>

          <div class="form-body">
            <div class="form-group">
              <label>Business / Store Display Name *</label>
              <input
                type="text"
                v-model="receiptSettings.business_name"
                placeholder="e.g. PeakPOS Pharmacy & Supermarket"
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label>Receipt Header Message (Address / Phone / Tax ID)</label>
              <textarea
                v-model="receiptSettings.header_text"
                rows="3"
                placeholder="123 Commercial Boulevard, Suite 400&#10;Phone: (555) 019-2834&#10;Tax ID: 84-2938102"
                class="form-control"
              ></textarea>
            </div>

            <!-- Logo Upload Strip -->
            <div class="logo-upload-box">
              <div class="logo-preview-area" v-if="receiptSettings.logo_filename">
                <img :src="getLogoUrl(receiptSettings.logo_filename)" alt="Store Logo" class="thumb-logo" />
                <button type="button" class="btn-remove-logo" @click="removeLogo" title="Remove logo">
                  <i class="material-icons">delete</i>
                </button>
              </div>
              <div class="logo-meta">
                <strong>Thermal Receipt Logo (Monochrome / PNG)</strong>
                <p>Upload a high-contrast black & white logo (max 2MB) for thermal printing.</p>
                <div class="logo-actions">
                  <input
                    type="file"
                    ref="logoInput"
                    accept="image/*"
                    @change="handleLogoUpload"
                    style="display: none;"
                  />
                  <button type="button" class="btn-upload-file" @click="$refs.logoInput.click()">
                    <i class="material-icons">cloud_upload</i>
                    <span>{{ receiptSettings.logo_filename ? 'Replace Logo' : 'Upload Receipt Logo' }}</span>
                  </button>
                </div>
              </div>
            </div>

            <div class="card-section-title mt-4">
              <i class="material-icons">chat</i>
              <h3>2. Receipt Footer & Legal Policies</h3>
            </div>

            <div class="form-group">
              <label>Thank You Note / Customer Message</label>
              <input
                type="text"
                v-model="receiptSettings.footer_text"
                placeholder="Thank you for shopping with us! Please come again."
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label>Legal & Return Policy Disclaimer</label>
              <textarea
                v-model="receiptSettings.legal_text"
                rows="2"
                placeholder="All items returnable within 7 days with original receipt. Medicines/Perishables excluded."
                class="form-control"
              ></textarea>
            </div>

            <div class="card-section-title mt-4">
              <i class="material-icons">tune</i>
              <h3>3. Hardware & POS Printing Preferences</h3>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label>Paper Roll Size</label>
                <select v-model="paperWidth" class="form-control">
                  <option value="80">80mm Standard (Counter POS)</option>
                  <option value="58">58mm Compact (Mobile / Handheld)</option>
                </select>
              </div>
              <div class="form-group">
                <label>Sales Tax Rate (%)</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  v-model.number="taxRate"
                  class="form-control"
                />
              </div>
            </div>

            <!-- Direct Hardware Peripheral Strip -->
            <div class="hardware-peripheral-box mt-3">
              <div class="hardware-status-row">
                <div class="status-indicator-wrap">
                  <span class="status-pulse-dot" :class="{ connected: printerStatus.connected }"></span>
                  <div>
                    <strong>{{ printerStatus.name }}</strong>
                    <small>{{ printerStatus.connected ? 'Silent Direct ESC/POS Hardware Ready' : 'Standard Browser Print Preview Active' }}</small>
                  </div>
                </div>
                <button
                  type="button"
                  class="btn-kick-drawer"
                  @click="testCashDrawer"
                  title="Pulse Cash Drawer Kick (ESC p 0 25 250)"
                >
                  <i class="material-icons">point_of_sale</i>
                  <span>Test Drawer Kick</span>
                </button>
              </div>

              <div class="hardware-actions-row">
                <button
                  type="button"
                  class="btn-hardware-connect usb"
                  @click="pairUsbPrinter"
                  title="Pair USB Thermal Printer (WebUSB - No print preview popup)"
                >
                  <i class="material-icons">usb</i>
                  <span>Pair USB Printer (WebUSB)</span>
                </button>
                <button
                  type="button"
                  class="btn-hardware-connect serial"
                  @click="pairSerialPrinter"
                  title="Pair Serial / COM Printer (WebSerial)"
                >
                  <i class="material-icons">settings_input_composite</i>
                  <span>Pair COM Port</span>
                </button>
                <button
                  v-if="printerStatus.type"
                  type="button"
                  class="btn-hardware-disconnect"
                  @click="disconnectPrinter"
                  title="Disconnect direct printer"
                >
                  Disconnect
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Live Photorealistic Thermal Receipt Canvas -->
        <div class="canvas-panel">
          <div class="canvas-header">
            <div class="canvas-title">
              <i class="material-icons">visibility</i>
              <span>Live Thermal Receipt Canvas (WYSIWYG)</span>
            </div>
            <div class="paper-badge">{{ paperWidth }}mm Width</div>
          </div>

          <div class="receipt-viewport">
            <div class="thermal-paper" :class="'paper-' + paperWidth">
              <!-- Jagged Top Tear Effect -->
              <div class="jagged-tear top"></div>

              <!-- Logo Section -->
              <div class="thermal-logo-wrap" v-if="receiptSettings.logo_filename">
                <img :src="getLogoUrl(receiptSettings.logo_filename)" alt="Receipt Logo" class="thermal-logo-img" />
              </div>

              <!-- Store Name -->
              <h2 class="thermal-store-name">
                {{ receiptSettings.business_name || 'PEAKPOS ENTERPRISE STORE' }}
              </h2>

              <!-- Header Info -->
              <div class="thermal-header-text" v-if="receiptSettings.header_text">
                {{ receiptSettings.header_text }}
              </div>

              <div class="thermal-divider"></div>

              <!-- Metadata Strip -->
              <div class="thermal-meta-grid">
                <div><span>Date:</span> <strong>{{ mockReceipt.date }}</strong></div>
                <div><span>Time:</span> <strong>{{ mockReceipt.time }}</strong></div>
                <div><span>Cashier:</span> <strong>Admin</strong></div>
                <div><span>Invoice #:</span> <strong>#PK-10842</strong></div>
              </div>

              <div class="thermal-divider"></div>

              <!-- Itemized Table -->
              <table class="thermal-items-table">
                <thead>
                  <tr>
                    <th class="text-left">Item Description</th>
                    <th class="text-center">Qty</th>
                    <th class="text-right">Price</th>
                    <th class="text-right">Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in mockReceipt.items" :key="item.name">
                    <td class="text-left">{{ item.name }}</td>
                    <td class="text-center">{{ item.qty }}</td>
                    <td class="text-right">${{ item.price.toFixed(2) }}</td>
                    <td class="text-right font-bold">${{ (item.qty * item.price).toFixed(2) }}</td>
                  </tr>
                </tbody>
              </table>

              <div class="thermal-divider dashed"></div>

              <!-- Calculation Totals -->
              <div class="thermal-totals-wrap">
                <div class="thermal-row">
                  <span>Subtotal:</span>
                  <span>${{ mockSubtotal.toFixed(2) }}</span>
                </div>
                <div class="thermal-row">
                  <span>Sales Tax ({{ taxRate }}%):</span>
                  <span>${{ mockTax.toFixed(2) }}</span>
                </div>
                <div class="thermal-row thermal-grand-total">
                  <span>TOTAL DUE:</span>
                  <strong>${{ mockTotal.toFixed(2) }}</strong>
                </div>
                <div class="thermal-row">
                  <span>Cash Tendered:</span>
                  <span>$50.00</span>
                </div>
                <div class="thermal-row font-bold">
                  <span>Change Due:</span>
                  <span>${{ Math.max(0, 50.0 - mockTotal).toFixed(2) }}</span>
                </div>
              </div>

              <div class="thermal-divider"></div>

              <!-- Footer Message -->
              <div class="thermal-footer-msg" v-if="receiptSettings.footer_text">
                {{ receiptSettings.footer_text }}
              </div>

              <!-- Legal Disclaimer -->
              <div class="thermal-legal-text" v-if="receiptSettings.legal_text">
                {{ receiptSettings.legal_text }}
              </div>

              <!-- Simulated Barcode -->
              <div class="thermal-barcode-wrap">
                <div class="simulated-barcode"></div>
                <span class="barcode-num">*PK-10842-2026*</span>
              </div>

              <!-- Jagged Bottom Tear Effect -->
              <div class="jagged-tear bottom"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Toast Feedback Popup -->
      <transition name="fade">
        <div v-if="toast.show" class="toast-popup" :class="toast.type">
          <i class="material-icons">{{ toast.type === 'success' ? 'check_circle' : 'error' }}</i>
          <span>{{ toast.message }}</span>
        </div>
      </transition>
    </div>
  </AppLayout>
</template>

<script>
import AppLayout from '@/components/layout/AppLayout.vue';
import escpos from '@/services/escpos';
import '@/assets/cards.css';

export default {
  name: 'SettingsView',
  components: {
    AppLayout
  },
  data() {
    return {
      receiptSaving: false,
      paperWidth: '80',
      taxRate: 7.0,
      currencySymbol: '$',
      printerStatus: escpos.getPrinterStatus(),
      receiptSettings: {
        business_name: 'PeakPOS Retail & Pharmacy',
        header_text: '100 Innovation Boulevard, Suite 500\nPhone: (555) 019-2834\nTax Registration: #TX-902184',
        footer_text: 'Thank you for shopping with PeakPOS! Please retain this slip for returns.',
        legal_text: 'Goods once sold can be returned within 7 days in original packing. Medicines and perishables are non-returnable.',
        logo_filename: null
      },
      mockReceipt: {
        date: new Date().toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' }),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        items: [
          { name: 'Amoxicillin 500mg Caps', qty: 2, price: 12.50 },
          { name: 'Organic Mineral Water 1L', qty: 1, price: 2.75 },
          { name: 'Vitamin C 1000mg Tabs', qty: 1, price: 8.90 }
        ]
      },
      toast: {
        show: false,
        message: '',
        type: 'success'
      }
    };
  },
  computed: {
    mockSubtotal() {
      return this.mockReceipt.items.reduce((sum, item) => sum + (item.qty * item.price), 0);
    },
    mockTax() {
      return (this.mockSubtotal * this.taxRate) / 100;
    },
    mockTotal() {
      return this.mockSubtotal + this.mockTax;
    }
  },
  created() {
    const role = (localStorage.getItem("role") || "").toLowerCase();
    if (role === "cashier" || role === "manager") {
      this.$router.replace("/sales");
    }
  },
  mounted() {
    this.fetchReceiptSettings();
  },
  methods: {
    async fetchReceiptSettings() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/receipt-settings');
        if (response.ok) {
          const data = await response.json();
          this.receiptSettings = {
            business_name: data.business_name || this.receiptSettings.business_name,
            header_text: data.header_text || this.receiptSettings.header_text,
            footer_text: data.footer_text || this.receiptSettings.footer_text,
            legal_text: data.legal_text || this.receiptSettings.legal_text,
            logo_filename: data.logo_filename || null
          };
        }
      } catch (err) {
        console.error('Error fetching receipt settings:', err);
      }
    },
    async saveReceiptSettings() {
      this.receiptSaving = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/receipt-settings', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.receiptSettings)
        });
        if (response.ok) {
          this.showToast('Thermal receipt settings saved successfully!', 'success');
        } else {
          this.showToast('Failed to save receipt settings', 'error');
        }
      } catch (err) {
        console.error('Error saving settings:', err);
        this.showToast('Network error while saving settings', 'error');
      } finally {
        this.receiptSaving = false;
      }
    },
    async handleLogoUpload(e) {
      const file = e.target.files[0];
      if (!file) return;

      if (!file.type.startsWith('image/')) {
        this.showToast('Please select a valid image file', 'error');
        return;
      }

      const formData = new FormData();
      formData.append('file', file);
      formData.append('logo', file);

      try {
        const response = await fetch('http://127.0.0.1:5000/api/receipt-settings/logo', {
          method: 'POST',
          body: formData
        });
        if (response.ok) {
          const data = await response.json();
          this.receiptSettings.logo_filename = data.filename;
          this.showToast('Receipt logo uploaded successfully!', 'success');
        } else {
          this.showToast('Failed to upload logo', 'error');
        }
      } catch (err) {
        console.error('Error uploading logo:', err);
        this.showToast('Network error uploading logo', 'error');
      }
    },
    removeLogo() {
      this.receiptSettings.logo_filename = null;
      this.showToast('Logo removed. Save settings to apply.', 'success');
    },
    getLogoUrl(filename) {
      if (!filename) return null;
      return `http://127.0.0.1:5000/static/receipt_logos/${filename}`;
    },
    async pairUsbPrinter() {
      try {
        const res = await escpos.pairUsbPrinter();
        this.printerStatus = escpos.getPrinterStatus();
        this.showToast(`Paired with USB Printer: ${res.name}`, 'success');
      } catch (err) {
        this.showToast(err.message || 'USB pairing failed', 'error');
      }
    },
    async pairSerialPrinter() {
      try {
        const res = await escpos.pairSerialPrinter(9600);
        this.printerStatus = escpos.getPrinterStatus();
        this.showToast(`Paired with Serial Printer: ${res.name}`, 'success');
      } catch (err) {
        this.showToast(err.message || 'Serial pairing failed', 'error');
      }
    },
    disconnectPrinter() {
      escpos.disconnectPrinter();
      this.printerStatus = escpos.getPrinterStatus();
      this.showToast('Direct hardware printer disconnected.', 'success');
    },
    async testCashDrawer() {
      const kicked = await escpos.kickCashDrawer();
      if (kicked) {
        this.showToast('Cash drawer kick pulse sent!', 'success');
      } else {
        this.showToast('Drawer kicked (Audio pulse feedback). Pair USB printer for physical kick.', 'success');
      }
    },
    async printTestReceipt() {
      const receiptData = {
        date: this.mockReceipt.date,
        time: this.mockReceipt.time,
        invoiceNo: '#PK-10842',
        cashier: 'Admin',
        items: this.mockReceipt.items,
        subtotal: this.mockSubtotal,
        tax: this.mockTax,
        total: this.mockTotal,
        tendered: 50.00,
        change: Math.max(0, 50.00 - this.mockTotal),
        paymentMethod: 'Cash'
      };
      const settings = {
        ...this.receiptSettings,
        paper_width: this.paperWidth
      };
      const res = await escpos.printReceiptSilently(receiptData, settings);
      if (res.mode === 'silent_usb' || res.mode === 'silent_serial') {
        this.showToast('Printed silently to direct thermal printer without dialog!', 'success');
      } else {
        this.showToast('Opened print preview. Pair USB printer in settings for silent printing.', 'success');
      }
    },
    showToast(msg, type = 'success') {
      this.toast.message = msg;
      this.toast.type = type;
      this.toast.show = true;
      setTimeout(() => {
        this.toast.show = false;
      }, 3500);
    }
  }
};
</script>

<style scoped>
.settings-studio {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Toolbar */
.settings-toolbar {
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

.dark-theme .settings-toolbar {
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

.btn-print-test {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #334155;
  padding: 9px 16px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.dark-theme .btn-print-test {
  background: #0f172a;
  border-color: #334155;
  color: #e2e8f0;
}

.btn-print-test:hover {
  background: #e2e8f0;
}

.btn-save-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #4338ca 0%, #3730a3 100%);
  color: white;
  padding: 9px 20px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 800;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(67, 56, 202, 0.3);
  transition: transform 0.15s;
}

.btn-save-primary:hover:not(:disabled) {
  transform: translateY(-1px);
}

.btn-save-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Split View Grid */
.studio-split-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 24px;
}

@media (max-width: 1080px) {
  .studio-split-grid {
    grid-template-columns: 1fr;
  }
}

/* Left: Configuration Form Card */
.config-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  padding: 24px;
  box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05);
}

.dark-theme .config-card {
  background: #1e293b;
  border-color: #334155;
}

.card-section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.card-section-title i {
  color: #4338ca;
  font-size: 1.4rem;
}

.card-section-title h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .card-section-title h3 {
  color: #f8fafc;
}

.mt-4 {
  margin-top: 24px;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #475569;
}

.dark-theme .form-group label {
  color: #94a3b8;
}

.form-control {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 0.88rem;
  outline: none;
  background: #ffffff;
  color: #0f172a;
  transition: border-color 0.2s;
  font-family: inherit;
}

.dark-theme .form-control {
  background: #0f172a;
  border-color: #334155;
  color: #f8fafc;
}

.form-control:focus {
  border-color: #6366f1;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* Logo Upload Strip */
.logo-upload-box {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 12px;
}

.dark-theme .logo-upload-box {
  background: #0f172a;
  border-color: #334155;
}

.logo-preview-area {
  position: relative;
  width: 70px;
  height: 70px;
  border-radius: 10px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  flex-shrink: 0;
}

.thumb-logo {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.btn-remove-logo {
  position: absolute;
  top: -6px;
  right: -6px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #ef4444;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.75rem;
}

.logo-meta {
  flex: 1;
}

.logo-meta strong {
  display: block;
  font-size: 0.85rem;
  color: #0f172a;
}

.dark-theme .logo-meta strong {
  color: #f8fafc;
}

.logo-meta p {
  margin: 3px 0 8px 0;
  font-size: 0.75rem;
  color: #64748b;
}

.btn-upload-file {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #4338ca;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
}

.dark-theme .btn-upload-file {
  background: #1e293b;
  border-color: #334155;
  color: #818cf8;
}

/* Hardware Peripheral Direct Printing Box */
.hardware-peripheral-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dark-theme .hardware-peripheral-box {
  background: #0f172a;
  border-color: #334155;
}

.hardware-status-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.status-indicator-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-pulse-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #94a3b8;
  border: 2px solid #ffffff;
}

.status-pulse-dot.connected {
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
}

.status-indicator-wrap strong {
  display: block;
  font-size: 0.88rem;
  color: #0f172a;
}

.dark-theme .status-indicator-wrap strong {
  color: #f8fafc;
}

.status-indicator-wrap small {
  font-size: 0.72rem;
  color: #64748b;
}

.btn-kick-drawer {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #0f172a;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.dark-theme .btn-kick-drawer {
  background: #1e293b;
  border-color: #334155;
  color: #f8fafc;
}

.btn-kick-drawer:hover {
  background: #eef2ff;
  border-color: #6366f1;
  color: #4338ca;
}

.hardware-actions-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-hardware-connect {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.btn-hardware-connect.usb {
  background: #eef2ff;
  border-color: #c7d2fe;
  color: #4338ca;
}

.btn-hardware-connect.usb:hover {
  background: #4338ca;
  color: #ffffff;
}

.btn-hardware-connect.serial {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #334155;
}

.dark-theme .btn-hardware-connect.serial {
  background: #1e293b;
  border-color: #334155;
  color: #e2e8f0;
}

.btn-hardware-disconnect {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #fee2e2;
  background: #fef2f2;
  color: #ef4444;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
}

/* Right: Canvas Panel */
.canvas-panel {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  padding: 20px;
  box-shadow: 0 4px 20px -2px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
}

.dark-theme .canvas-panel {
  background: #1e293b;
  border-color: #334155;
}

.canvas-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 14px;
  border-bottom: 1px solid #f1f5f9;
}

.dark-theme .canvas-header {
  border-bottom-color: #334155;
}

.canvas-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
  font-weight: 800;
  color: #0f172a;
}

.dark-theme .canvas-title {
  color: #f8fafc;
}

.canvas-title i {
  color: #10b981;
}

.paper-badge {
  font-size: 0.72rem;
  font-weight: 800;
  background: #f1f5f9;
  color: #4338ca;
  padding: 3px 8px;
  border-radius: 6px;
}

.receipt-viewport {
  flex: 1;
  background: #e2e8f0;
  border-radius: 12px;
  padding: 30px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  overflow-y: auto;
  margin-top: 14px;
}

.dark-theme .receipt-viewport {
  background: #0b0f19;
}

/* Photorealistic Thermal Receipt Paper */
.thermal-paper {
  background: #ffffff;
  color: #111827;
  font-family: 'Courier New', Courier, monospace;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  padding: 26px 20px;
  position: relative;
  transition: width 0.3s ease;
}

.paper-80 {
  width: 320px;
}

.paper-58 {
  width: 250px;
}

/* Top & Bottom jagged paper tear */
.jagged-tear {
  position: absolute;
  left: 0;
  right: 0;
  height: 8px;
  background: radial-gradient(circle, transparent, transparent 50%, #ffffff 50%, #ffffff 100%);
  background-size: 12px 12px;
}

.jagged-tear.top {
  top: -6px;
  transform: rotate(180deg);
}

.jagged-tear.bottom {
  bottom: -6px;
}

.thermal-logo-wrap {
  text-align: center;
  margin-bottom: 10px;
}

.thermal-logo-img {
  max-width: 90px;
  max-height: 50px;
  filter: grayscale(100%) contrast(150%);
}

.thermal-store-name {
  font-size: 1.05rem;
  font-weight: 900;
  text-align: center;
  margin: 0 0 6px 0;
  letter-spacing: 0.5px;
}

.thermal-header-text {
  font-size: 0.72rem;
  text-align: center;
  white-space: pre-line;
  line-height: 1.3;
  color: #374151;
}

.thermal-divider {
  border-top: 1px solid #111827;
  margin: 10px 0;
}

.thermal-divider.dashed {
  border-top-style: dashed;
}

.thermal-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  font-size: 0.68rem;
  gap: 3px;
  color: #1f2937;
}

.thermal-items-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.68rem;
}

.thermal-items-table th {
  padding: 4px 0;
  font-weight: 800;
  border-bottom: 1px dashed #111827;
}

.thermal-items-table td {
  padding: 4px 0;
}

.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.font-bold { font-weight: 900; }

.thermal-totals-wrap {
  font-size: 0.72rem;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.thermal-row {
  display: flex;
  justify-content: space-between;
}

.thermal-grand-total {
  font-size: 0.95rem;
  border-top: 1px solid #111827;
  border-bottom: 1px solid #111827;
  padding: 4px 0;
  margin: 4px 0;
}

.thermal-footer-msg {
  font-size: 0.68rem;
  text-align: center;
  font-weight: 700;
  margin-top: 8px;
}

.thermal-legal-text {
  font-size: 0.6rem;
  text-align: center;
  margin-top: 6px;
  color: #4b5563;
  line-height: 1.2;
}

.thermal-barcode-wrap {
  margin-top: 12px;
  text-align: center;
}

.simulated-barcode {
  height: 28px;
  background: repeating-linear-gradient(
    90deg,
    #111827 0,
    #111827 2px,
    transparent 2px,
    transparent 4px,
    #111827 4px,
    #111827 7px,
    transparent 7px,
    transparent 9px
  );
  margin-bottom: 4px;
}

.barcode-num {
  font-size: 0.65rem;
  letter-spacing: 2px;
}

/* Toast */
.toast-popup {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  z-index: 2000;
}

.toast-popup.success {
  background: #10b981;
}

.toast-popup.error {
  background: #ef4444;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Print Styles */
@media print {
  body * {
    visibility: hidden;
  }
  .thermal-paper, .thermal-paper * {
    visibility: visible;
  }
  .thermal-paper {
    position: absolute;
    left: 0;
    top: 0;
    width: 100% !important;
    box-shadow: none;
    padding: 0;
  }
}
</style>
