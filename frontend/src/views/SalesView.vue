<template>
  <div class="pos-layout" :class="{ 'mode-counter': posMode === 'counter', 'mode-visual': posMode === 'visual' }">
    <!-- Top Enterprise Navigation Header (Unified & Clean) -->
    <header class="pos-header">
      <div class="header-left">
        <div class="brand-container">
          <img src="../assets/logo-pp.png" alt="PeakPOS Logo" class="brand-logo" />
          <div class="brand-meta">
            <h1 class="brand-name">Peak<span>POS</span></h1>
            <span class="register-pill">
              <span class="pulse-dot"></span>
              {{ posMode === 'counter' ? 'High-Speed POS Counter' : 'Touch POS Terminal' }}
            </span>
          </div>
        </div>

        <!-- Mode Toggle: Visual vs High-Speed Counter -->
        <div class="mode-selector">
          <button
            class="mode-btn"
            :class="{ active: posMode === 'counter' }"
            @click="setPosMode('counter')"
            title="Split-Pane High-Speed Counter [F9]"
          >
            <i class="material-icons">flash_on</i>
            <span>Register [F9]</span>
          </button>
          <button
            class="mode-btn"
            :class="{ active: posMode === 'visual' }"
            @click="setPosMode('visual')"
            title="Touch Visual Catalog Mode"
          >
            <i class="material-icons">grid_view</i>
            <span>Touch Catalog</span>
          </button>
        </div>

        <!-- Navigation Links -->
        <nav class="header-nav">
          <router-link to="/dashboard" class="nav-pill" title="Dashboard">
            <i class="material-icons">dashboard</i>
            <span>Dashboard</span>
          </router-link>
          <router-link to="/admin/products" class="nav-pill" title="Products">
            <i class="material-icons">inventory_2</i>
            <span>Products</span>
          </router-link>
          <router-link to="/admin/settings" class="nav-pill" title="Settings">
            <i class="material-icons">settings</i>
            <span>Settings</span>
          </router-link>
        </nav>
      </div>

      <div class="header-right">
        <!-- Quick Action Shortcuts -->
        <div class="shortcuts-legend">
          <span class="sc-tag" title="Search / Scan Focus"><kbd>F1</kbd> Scan</span>
          <span class="sc-tag" title="Park / Hold Current Sale" @click="parkCurrentBill"><kbd>F2</kbd> Park</span>
          <span class="sc-tag" title="Recall Held Sales" :class="{ 'has-held': heldBillsCount > 0 }" @click="openHeldBillsModal">
            <kbd>F3</kbd> Held ({{ heldBillsCount }})
          </span>
          <span class="sc-tag" title="Pay and Print" @click="openPaymentModal"><kbd>F12</kbd> Pay</span>
          <span class="sc-tag lock-tag" @click="isTerminalLocked = true" title="Quick Lock Terminal & Switch Cashier [Ctrl+L]"><kbd>Ctrl+L</kbd> Lock</span>
        </div>

        <!-- Live Clock -->
        <div class="clock-widget">
          <span class="clock-time">{{ currentTime }}</span>
          <span class="clock-date">{{ currentDate }}</span>
        </div>

        <!-- Cashier Avatar Badge with Quick Lock on click -->
        <div class="cashier-badge" @click="isTerminalLocked = true" title="Quick Lock Terminal & Switch Cashier [Ctrl+L]">
          <div class="cashier-avatar">
            <i class="material-icons">badge</i>
          </div>
          <div class="cashier-info">
            <span class="cashier-name">{{ cashierName }}</span>
            <span class="cashier-role">{{ cashierRole }}</span>
          </div>
          <i class="material-icons lock-status-ico">lock_outline</i>
        </div>

        <!-- Mobile Cart Button -->
        <button class="mobile-cart-btn" @click="toggleMobileCart" :class="{ 'has-items': cart.length > 0 }">
          <i class="material-icons">shopping_bag</i>
          <span class="badge" v-if="cartTotalItems > 0">{{ cartTotalItems }}</span>
        </button>
      </div>
    </header>

    <!-- ==================== MODE 1: MODERN SPLIT-PANE HYBRID (Square / Shopify POS) ==================== -->
    <main v-if="posMode === 'counter'" class="split-register-layout">
      <!-- LEFT PANE (62%): High-Speed Working Area & Barcode Center -->
      <section class="register-left-pane">
        <!-- Top Utility Bar: Integrated Customer Pill & Search -->
        <div class="register-top-bar">
          <!-- Customer Selection Chip with Popover Toggle -->
          <div class="customer-picker-pill" :class="{ 'has-customer': customer.name }">
            <i class="material-icons">person</i>
            <div class="cust-pill-text">
              <span class="cust-name-label">{{ customer.name || 'Walk-in Customer' }}</span>
              <span class="cust-phone-label" v-if="customer.phone">{{ customer.phone }}</span>
            </div>
            <button class="btn-edit-customer" @click="customerPopoverOpen = !customerPopoverOpen" title="Edit Customer Details">
              <i class="material-icons">{{ customerPopoverOpen ? 'expand_less' : 'edit' }}</i>
            </button>
          </div>

          <!-- Customer Edit Popover -->
          <div v-if="customerPopoverOpen" class="customer-popover-card">
            <div class="popover-header">
              <span>Customer / Loyalty Profile</span>
              <button @click="customerPopoverOpen = false" class="popover-close"><i class="material-icons">close</i></button>
            </div>
            <div class="popover-body">
              <div class="popover-input-group">
                <label>Customer Name</label>
                <input type="text" v-model="customer.name" placeholder="Walk-in Customer" class="popover-input" />
              </div>
              <div class="popover-input-group">
                <label>Mobile Number (Loyalty / Ledger)</label>
                <input type="tel" v-model="customer.phone" placeholder="e.g. +1 555 0192" class="popover-input" />
              </div>
              <div class="popover-input-group">
                <label>Prescriber / Doctor (Optional)</label>
                <input type="text" v-model="customer.doctor" placeholder="Dr. Name" class="popover-input" />
              </div>
              <button class="btn-popover-save" @click="customerPopoverOpen = false">Done</button>
            </div>
          </div>

          <!-- Line Stats & Quick Actions -->
          <div class="register-quick-stats">
            <div class="stat-bubble">
              <i class="material-icons">shopping_bag</i>
              <span><strong>{{ cart.length }}</strong> Items (<strong>{{ cartTotalItems }}</strong> Units)</span>
            </div>
            <button class="btn-clean-cart" v-if="cart.length > 0" @click="clearCart" title="Clear Bill [F4]">
              <i class="material-icons">delete_sweep</i> Clear
            </button>
          </div>
        </div>

        <!-- Prominent Hero Barcode & Search Input -->
        <div class="hero-search-container">
          <div class="hero-search-box">
            <i class="material-icons hero-scan-ico">qr_code_scanner</i>
            <input
              ref="barcodeInput"
              type="text"
              v-model="searchTerm"
              @keydown.enter.prevent="handleBarcodeOrEnterSearch"
              placeholder="Scan Barcode or Type Product / Formula / Salt Name and Press [Enter]..."
              class="hero-search-input"
              autofocus
            />
            <span class="f1-badge"><kbd>F1</kbd></span>
            <button v-if="searchTerm" @click="clearSearch" class="hero-clear-btn">
              <i class="material-icons">close</i>
            </button>
          </div>

          <!-- Quick Category / Filter Chips Bar -->
          <div class="quick-filter-chips">
            <button
              class="filter-chip"
              :class="{ active: activeCategory === 'all' }"
              @click="filterByCategory('all')"
            >
              <i class="material-icons">apps</i> All
            </button>
            <button
              class="filter-chip"
              :class="{ active: activeCategory === 'popular' }"
              @click="filterByCategory('popular')"
            >
              <i class="material-icons">trending_up</i> Top Sellers
            </button>
            <button
              class="filter-chip"
              :class="{ active: activeCategory === 'sale' }"
              @click="filterByCategory('sale')"
            >
              <i class="material-icons">local_offer</i> On Sale
            </button>
            <button
              v-for="cat in categories.slice(0, 5)"
              :key="cat.id"
              class="filter-chip"
              :class="{ active: activeCategory === String(cat.id) }"
              @click="filterByCategory(String(cat.id))"
            >
              {{ cat.name }}
            </button>
          </div>
        </div>

        <!-- Live Instant Search Dropdown (When typing) -->
        <div v-if="searchTerm && !exactMatchFound" class="instant-search-dropdown-split">
          <div class="dropdown-header">
            <span>Matches for "{{ searchTerm }}" (Click or Press Enter to Add)</span>
            <button @click="clearSearch" class="dropdown-close"><i class="material-icons">close</i></button>
          </div>
          <div class="dropdown-list">
            <div
              v-for="p in filteredProducts.slice(0, 8)"
              :key="p.id"
              class="dropdown-item"
              :class="{ 'item-oos': p.stock <= 0 }"
              @click="addAndClear(p)"
            >
              <div class="item-main">
                <span class="item-name">{{ p.name }}</span>
                <span class="item-cat">{{ getCategoryName(p.category_id) }} &bull; SKU #{{ p.id }}</span>
              </div>
              <div class="item-right">
                <span class="item-stock" :class="getStockClass(p)">{{ p.stock }} in stock</span>
                <span class="item-price">${{ p.price.toFixed(2) }}</span>
                <button class="btn-dropdown-add" :disabled="p.stock <= 0">Add</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Spacious Modern Cart Table Area -->
        <div class="split-table-wrapper">
          <table class="split-cart-table">
            <thead>
              <tr>
                <th style="width: 44px;">#</th>
                <th>Item & Details</th>
                <th style="width: 110px;">Stock</th>
                <th style="width: 110px;">Unit Price</th>
                <th style="width: 140px;">Quantity</th>
                <th style="width: 120px; text-align: right;">Total</th>
                <th style="width: 44px;"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="cart.length === 0" class="split-table-empty">
                <td colspan="7">
                  <div class="empty-register-art">
                    <div class="art-icon-ring">
                      <i class="material-icons">barcode_reader</i>
                    </div>
                    <h3>Ready for Next Customer</h3>
                    <p>Scan barcode gun or start typing in the search box above <kbd>[F1]</kbd>.</p>
                    <div class="ready-tips">
                      <span><kbd>Enter</kbd> Add item</span>
                      <span><kbd>F2</kbd> Park</span>
                      <span><kbd>F12</kbd> Instant Pay</span>
                      <span><kbd>Ctrl+L</kbd> Cashier Switch</span>
                    </div>
                  </div>
                </td>
              </tr>

              <tr v-for="(item, idx) in cart" :key="item.id" class="split-item-row">
                <td class="col-idx">{{ idx + 1 }}</td>
                <td class="col-item-details">
                  <div class="item-title-block">
                    <span class="item-name-text">{{ item.name }}</span>
                    <div class="item-subtags">
                      <span class="subtag-sku">SKU: {{ item.barcode || ('#' + item.id) }}</span>
                      <span class="subtag-category">{{ getCategoryName(item.category_id) }}</span>
                      <span class="subtag-desc" v-if="item.description">{{ item.description }}</span>
                    </div>
                  </div>
                </td>
                <td class="col-stock">
                  <span class="stock-pill-badge" :class="getStockClass(item)">
                    {{ item.stock }} in stock
                  </span>
                </td>
                <td class="col-price">
                  <div class="price-input-box">
                    <span class="curr-sign">$</span>
                    <input
                      type="number"
                      step="0.01"
                      v-model.number="item.price"
                      class="table-price-input"
                      @change="saveCartToStorage"
                    />
                  </div>
                </td>
                <td class="col-qty">
                  <div class="stepper-box">
                    <button class="step-btn" @click="decreaseQuantity(idx)" :disabled="item.quantity <= 1">
                      <i class="material-icons">remove</i>
                    </button>
                    <input
                      type="number"
                      min="1"
                      :max="item.stock"
                      v-model.number="item.quantity"
                      class="step-input"
                      @change="validateItemQuantity(item)"
                    />
                    <button class="step-btn" @click="increaseQuantity(idx)" :disabled="item.quantity >= item.stock">
                      <i class="material-icons">add</i>
                    </button>
                  </div>
                </td>
                <td class="col-line-total">
                  <span class="item-total-amount">${{ (item.price * item.quantity).toFixed(2) }}</span>
                </td>
                <td class="col-del">
                  <button class="btn-del-row" @click="removeFromCart(idx)" title="Remove item">
                    <i class="material-icons">close</i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- RIGHT PANE (38%): Fixed Action & Tender Summary Slip -->
      <aside class="register-right-pane">
        <div class="order-slip-card">
          <!-- Order Slip Header -->
          <div class="slip-header">
            <div class="slip-title-meta">
              <i class="material-icons">receipt_long</i>
              <h3>Active Sale Ticket</h3>
            </div>
            <div class="slip-actions-top">
              <button
                class="btn-slip-action"
                :disabled="cart.length === 0"
                @click="parkCurrentBill"
                title="Hold / Park Bill (F2)"
              >
                <i class="material-icons">pause</i> Park [F2]
              </button>
              <button
                class="btn-slip-action"
                :class="{ 'has-held-badge': heldBillsCount > 0 }"
                @click="openHeldBillsModal"
                title="Recall Parked Bills (F3)"
              >
                <i class="material-icons">history</i> Held ({{ heldBillsCount }})
              </button>
            </div>
          </div>

          <!-- Customer Loyalty Info Card inside Ticket -->
          <div class="slip-customer-badge">
            <div class="cust-avatar-ring">
              <i class="material-icons">person</i>
            </div>
            <div class="cust-meta-block">
              <span class="cust-lead-name">{{ customer.name || 'Walk-in Customer' }}</span>
              <span class="cust-lead-sub">
                {{ customer.phone ? ('📞 ' + customer.phone) : 'Standard Tier &bull; No Loyalty Account' }}
              </span>
            </div>
            <button class="btn-swap-cust" @click="customerPopoverOpen = !customerPopoverOpen">
              Change
            </button>
          </div>

          <!-- Financial Calculation Breakdown -->
          <div class="slip-breakdown">
            <div class="breakdown-row">
              <span class="row-label">Subtotal</span>
              <span class="row-value">${{ calculateSubtotal().toFixed(2) }}</span>
            </div>

            <!-- Discount Selector -->
            <div class="breakdown-row discount-row">
              <div class="row-label-with-icon">
                <i class="material-icons">local_offer</i>
                <span>Discount</span>
              </div>
              <div class="discount-control">
                <select v-model="selectedDiscount" class="slip-discount-select">
                  <option :value="null">None (0%)</option>
                  <option v-for="d in discounts" :key="d.id" :value="d.id">
                    {{ d.name }} ({{ d.discount_type === 'percentage' ? d.value + '%' : '$' + d.value }})
                  </option>
                </select>
                <span class="discount-deduct-val" v-if="selectedDiscount">
                  -${{ calculateDiscountAmount().toFixed(2) }}
                </span>
              </div>
            </div>

            <div class="breakdown-row">
              <span class="row-label">Estimated Tax (7%)</span>
              <span class="row-value">${{ calculateTax().toFixed(2) }}</span>
            </div>

            <div class="slip-divider"></div>

            <!-- Hero Net Total Due -->
            <div class="breakdown-hero-total">
              <div class="hero-total-label">
                <span>Total Amount Due</span>
                <span class="items-summary-note">{{ cart.length }} items &bull; {{ cartTotalItems }} units</span>
              </div>
              <div class="hero-total-price">
                <span class="hero-curr">$</span>
                <span class="hero-val">{{ calculateTotal().toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <!-- Quick Cash Preset 1-Click Buttons -->
          <div class="quick-cash-presets">
            <span class="preset-label">1-Click Cash Presets</span>
            <div class="preset-buttons-grid">
              <button
                class="btn-cash-preset exact"
                :disabled="cart.length === 0"
                @click="oneClickCashPay('exact')"
              >
                Exact Cash
              </button>
              <button
                class="btn-cash-preset"
                :disabled="cart.length === 0"
                @click="oneClickCashPay(10)"
              >
                $10
              </button>
              <button
                class="btn-cash-preset"
                :disabled="cart.length === 0"
                @click="oneClickCashPay(20)"
              >
                $20
              </button>
              <button
                class="btn-cash-preset"
                :disabled="cart.length === 0"
                @click="oneClickCashPay(50)"
              >
                $50
              </button>
              <button
                class="btn-cash-preset"
                :disabled="cart.length === 0"
                @click="oneClickCashPay(100)"
              >
                $100
              </button>
              <button
                class="btn-cash-preset card-preset"
                :disabled="cart.length === 0"
                @click="oneClickCardPay"
              >
                <i class="material-icons">credit_card</i> Card
              </button>
            </div>
          </div>

          <!-- Massive Primary Pay Button -->
          <div class="slip-pay-action">
            <button
              class="btn-massive-pay"
              :disabled="cart.length === 0 || processingOrder"
              @click="openPaymentModal"
            >
              <div class="pay-btn-content">
                <i class="material-icons">payments</i>
                <span>PAY &bull; [F12]</span>
              </div>
              <span class="pay-btn-amount">${{ calculateTotal().toFixed(2) }}</span>
            </button>
          </div>

          <!-- Quick Utility Bar at Bottom of Slip -->
          <div class="slip-bottom-bar">
            <button class="bottom-util-btn" @click="printLastReceipt" title="Reprint Last Thermal Receipt">
              <i class="material-icons">receipt</i> Reprint Last
            </button>
            <button class="bottom-util-btn" @click="openDrawerKick" title="Open Cash Drawer">
              <i class="material-icons">point_of_sale</i> Kick Drawer
            </button>
            <button class="bottom-util-btn danger" :disabled="cart.length === 0" @click="clearCart" title="Void Current Bill">
              <i class="material-icons">delete_sweep</i> Void [F4]
            </button>
          </div>
        </div>
      </aside>
    </main>

    <!-- ==================== MODE 2: TOUCH / VISUAL CATALOG MODE ==================== -->
    <div v-else class="pos-main">
      <!-- Catalog Section -->
      <section class="catalog-section">
        <!-- Control Bar -->
        <div class="catalog-toolbar">
          <div class="search-box">
            <i class="material-icons search-ico">search</i>
            <input
              ref="visualSearchInput"
              type="text"
              v-model="searchTerm"
              placeholder="Search products by name, formula, category..."
              class="search-input"
            />
            <button v-if="searchTerm" @click="clearSearch" class="search-clear-btn">
              <i class="material-icons">close</i>
            </button>
          </div>

          <div class="toolbar-actions">
            <div class="view-switch">
              <button
                class="view-toggle-btn"
                :class="{ active: viewMode === 'grid' }"
                @click="viewMode = 'grid'"
                title="Grid View"
              >
                <i class="material-icons">grid_view</i>
              </button>
              <button
                class="view-toggle-btn"
                :class="{ active: viewMode === 'list' }"
                @click="viewMode = 'list'"
                title="List View"
              >
                <i class="material-icons">view_list</i>
              </button>
            </div>

            <button class="refresh-catalog-btn" @click="fetchProducts" title="Reload products">
              <i class="material-icons" :class="{ 'spin': loading }">refresh</i>
            </button>
          </div>
        </div>

        <!-- Category Horizontal Strip -->
        <div class="category-strip">
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'all' }"
            @click="filterByCategory('all')"
          >
            <i class="material-icons">apps</i>
            <span>All Items</span>
            <span class="chip-count">{{ products.length }}</span>
          </button>
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'popular' }"
            @click="filterByCategory('popular')"
          >
            <i class="material-icons">trending_up</i>
            <span>Popular</span>
          </button>
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'new' }"
            @click="filterByCategory('new')"
          >
            <i class="material-icons">bolt</i>
            <span>New</span>
          </button>
          <button
            class="category-chip"
            :class="{ active: activeCategory === 'sale' }"
            @click="filterByCategory('sale')"
          >
            <i class="material-icons">local_offer</i>
            <span>On Sale</span>
          </button>

          <button
            v-for="cat in categories"
            :key="cat.id"
            class="category-chip"
            :class="{ active: activeCategory === String(cat.id) }"
            @click="filterByCategory(String(cat.id))"
          >
            <i class="material-icons">folder_open</i>
            <span>{{ cat.name }}</span>
          </button>
        </div>

        <!-- Catalog Scroll Area -->
        <div class="catalog-scroll-area">
          <div v-if="loading" class="state-container">
            <div class="pos-spinner"></div>
            <p class="state-title">Loading Catalog...</p>
          </div>

          <div v-else-if="filteredProducts.length === 0" class="state-container empty-state">
            <div class="empty-icon-wrap">
              <i class="material-icons">inventory_2</i>
            </div>
            <h3 class="state-title">No products found</h3>
            <p class="state-desc">Try clearing your search query or choosing another category filter.</p>
            <button class="btn-reset-filter" @click="resetFilters">
              <i class="material-icons">refresh</i> Reset Filters
            </button>
          </div>

          <!-- Grid Cards Mode -->
          <div v-else-if="viewMode === 'grid'" class="product-grid">
            <div
              v-for="product in filteredProducts"
              :key="product.id"
              class="pos-card"
              :class="{ 'is-out-of-stock': product.stock <= 0 }"
              @click="handleCardClick(product)"
            >
              <div class="card-image-box">
                <img :src="getProductImageUrl(product)" :alt="product.name" loading="lazy" @error="handleImageError" />
                <div class="card-badges">
                  <span class="badge sale" v-if="isOnSale(product)">SALE</span>
                  <span class="badge new" v-else-if="isNewProduct(product)">NEW</span>
                  <span class="badge oos" v-if="product.stock <= 0">Out of Stock</span>
                  <span class="badge low-stock" v-else-if="product.stock < 10">Low ({{ product.stock }})</span>
                </div>
              </div>

              <div class="card-content">
                <span class="card-category">{{ getCategoryName(product.category_id) }}</span>
                <h3 class="card-title" :title="product.name">{{ product.name }}</h3>

                <div class="card-footer">
                  <div class="price-stack">
                    <span class="currency-symbol">$</span>
                    <span class="price-value">{{ product.price.toFixed(2) }}</span>
                  </div>

                  <button
                    class="btn-add-cart"
                    :disabled="product.stock <= 0"
                    @click.stop="addToCart(product)"
                    title="Add to order"
                  >
                    <i class="material-icons">add</i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- List Table Mode -->
          <div v-else class="product-table-wrapper">
            <table class="product-table">
              <thead>
                <tr>
                  <th class="th-item">Product</th>
                  <th class="th-cat">Category</th>
                  <th class="th-stock">Stock Level</th>
                  <th class="th-price">Price</th>
                  <th class="th-action">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="product in filteredProducts"
                  :key="product.id"
                  class="table-row"
                  :class="{ 'row-oos': product.stock <= 0 }"
                  @click="showProductQuickView(product)"
                >
                  <td class="td-item">
                    <img :src="getProductImageUrl(product)" :alt="product.name" class="row-thumb" @error="handleImageError" />
                    <div class="row-meta">
                      <span class="row-title">{{ product.name }}</span>
                      <span class="row-sku">ID #{{ product.id }}</span>
                    </div>
                  </td>
                  <td class="td-cat"><span class="cat-tag">{{ getCategoryName(product.category_id) }}</span></td>
                  <td class="td-stock">
                    <span class="stock-pill" :class="getStockClass(product)">
                      <i class="material-icons">{{ getStockIcon(product) }}</i>
                      {{ product.stock }} in stock
                    </span>
                  </td>
                  <td class="td-price">${{ product.price.toFixed(2) }}</td>
                  <td class="td-action">
                    <button class="btn-table-add" :disabled="product.stock <= 0" @click.stop="addToCart(product)">
                      <i class="material-icons">add_shopping_cart</i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- Cart Register Sidebar -->
      <aside class="pos-cart" :class="{ 'mobile-open': isMobileCartVisible }">
        <div class="cart-card">
          <div class="cart-top">
            <div class="cart-title-wrap">
              <div class="cart-icon-bubble">
                <i class="material-icons">receipt_long</i>
              </div>
              <div>
                <h2 class="cart-heading">Current Sale</h2>
                <span class="cart-subheading">{{ cart.length }} line items &bull; {{ cartTotalItems }} units</span>
              </div>
            </div>

            <div class="cart-top-actions">
              <button class="btn-cart-clear" v-if="cart.length > 0" @click="clearCart" title="Empty Cart">
                <i class="material-icons">delete_sweep</i>
                <span>Clear</span>
              </button>
              <button class="btn-close-mobile-cart" @click="toggleMobileCart">
                <i class="material-icons">close</i>
              </button>
            </div>
          </div>

          <!-- Cart Body Items -->
          <div class="cart-body">
            <div v-if="cart.length === 0" class="cart-empty-state">
              <div class="cart-empty-icon">
                <i class="material-icons">shopping_cart</i>
              </div>
              <h4>No Items in Cart</h4>
              <p>Select products from the catalog to build your order.</p>
            </div>

            <div v-else class="cart-items-list">
              <div v-for="(item, index) in cart" :key="item.id" class="cart-row">
                <div class="cart-item-thumb">
                  <img :src="getProductImageUrl(item)" :alt="item.name" @error="handleImageError" />
                </div>

                <div class="cart-item-details">
                  <div class="cart-item-main">
                    <h4 class="cart-item-name" :title="item.name">{{ item.name }}</h4>
                    <span class="cart-item-unit-price">${{ item.price.toFixed(2) }} ea</span>
                  </div>

                  <div class="cart-item-subline">
                    <div class="qty-stepper">
                      <button class="qty-btn" @click.stop="decreaseQuantity(index)" :disabled="item.quantity <= 1">
                        <i class="material-icons">remove</i>
                      </button>
                      <span class="qty-value">{{ item.quantity }}</span>
                      <button class="qty-btn" @click.stop="increaseQuantity(index)" :disabled="item.quantity >= item.stock">
                        <i class="material-icons">add</i>
                      </button>
                    </div>

                    <div class="cart-item-total">
                      ${{ (item.price * item.quantity).toFixed(2) }}
                    </div>

                    <button class="btn-item-del" @click.stop="removeFromCart(index)" title="Remove item">
                      <i class="material-icons">close</i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Financial Summary -->
          <div class="cart-footer">
            <div class="summary-breakdown">
              <div class="calc-row">
                <span class="calc-label">Subtotal</span>
                <span class="calc-val">${{ calculateSubtotal().toFixed(2) }}</span>
              </div>

              <div class="calc-row discount-selection-row">
                <div class="discount-lead">
                  <i class="material-icons">local_offer</i>
                  <span>Discount</span>
                </div>
                <div class="discount-inputs">
                  <select v-model="selectedDiscount" class="pos-select-discount">
                    <option :value="null">No Discount</option>
                    <option v-for="d in discounts" :key="d.id" :value="d.id">
                      {{ d.name }} ({{ d.discount_type === 'percentage' ? d.value + '%' : '$' + d.value }})
                    </option>
                  </select>
                  <span class="discount-deduction" v-if="selectedDiscount">
                    -${{ calculateDiscountAmount().toFixed(2) }}
                  </span>
                </div>
              </div>

              <div class="calc-row">
                <span class="calc-label">Tax (7%)</span>
                <span class="calc-val">${{ calculateTax().toFixed(2) }}</span>
              </div>

              <div class="calc-divider"></div>

              <div class="calc-row grand-total-row">
                <span class="grand-total-label">Total Due</span>
                <span class="grand-total-val">${{ calculateTotal().toFixed(2) }}</span>
              </div>
            </div>

            <!-- Complete Purchase Action Button -->
            <button
              class="btn-checkout-primary"
              :disabled="cart.length === 0 || processingOrder"
              @click="openPaymentModal"
            >
              <i class="material-icons">payments</i>
              <span>Charge ${{ calculateTotal().toFixed(2) }} &bull; [F12]</span>
            </button>
          </div>
        </div>
      </aside>

      <!-- Mobile Backdrop Overlay -->
      <div class="mobile-backdrop" v-if="isMobileCartVisible" @click="toggleMobileCart"></div>
    </div>

    <!-- ==================== PAYMENT & CASH CALCULATOR MODAL ==================== -->
    <transition name="fade-modal">
      <div class="modal-overlay" v-if="paymentModal.show" @click="closePaymentModal">
        <div class="payment-dialog" @click.stop>
          <div class="payment-modal-header">
            <div class="pay-title-box">
              <i class="material-icons">point_of_sale</i>
              <h3>Process Payment &bull; Bill Checkout</h3>
            </div>
            <button class="btn-modal-x" @click="closePaymentModal"><i class="material-icons">close</i></button>
          </div>

          <div class="payment-modal-body">
            <!-- Left: Tender Method & Calculation -->
            <div class="pay-left-col">
              <label class="pay-section-label">Select Payment Method</label>
              <div class="tender-tabs">
                <button
                  class="tender-btn"
                  :class="{ active: paymentModal.method === 'cash' }"
                  @click="setPaymentMethod('cash')"
                >
                  <i class="material-icons">payments</i>
                  <span>Cash</span>
                </button>
                <button
                  class="tender-btn"
                  :class="{ active: paymentModal.method === 'card' }"
                  @click="setPaymentMethod('card')"
                >
                  <i class="material-icons">credit_card</i>
                  <span>Card / POS</span>
                </button>
                <button
                  class="tender-btn"
                  :class="{ active: paymentModal.method === 'wallet' }"
                  @click="setPaymentMethod('wallet')"
                >
                  <i class="material-icons">account_balance_wallet</i>
                  <span>Mobile Wallet</span>
                </button>
                <button
                  class="tender-btn"
                  :class="{ active: paymentModal.method === 'credit' }"
                  @click="setPaymentMethod('credit')"
                >
                  <i class="material-icons">menu_book</i>
                  <span>Customer Ledger</span>
                </button>
              </div>

              <!-- Cash Tendered & Change Return Cockpit -->
              <div class="cash-calc-container" v-if="paymentModal.method === 'cash'">
                <label class="pay-section-label">Cash Received From Customer</label>
                <div class="tendered-input-wrapper">
                  <span class="tendered-curr">$</span>
                  <input
                    ref="tenderedInput"
                    type="number"
                    step="0.01"
                    v-model.number="paymentModal.tendered"
                    @input="calculateChange"
                    placeholder="0.00"
                    class="tendered-input"
                  />
                </div>

                <!-- Fast Denomination Presets -->
                <div class="denom-presets">
                  <button class="denom-btn" @click="setExactTendered">Exact Amount</button>
                  <button class="denom-btn" @click="addTendered(10)">+$10</button>
                  <button class="denom-btn" @click="addTendered(20)">+$20</button>
                  <button class="denom-btn" @click="addTendered(50)">+$50</button>
                  <button class="denom-btn" @click="addTendered(100)">+$100</button>
                </div>
              </div>

              <div class="customer-receipt-note" v-if="customer.name || customer.phone">
                <i class="material-icons">person</i>
                <span>Customer: <strong>{{ customer.name || 'Walk-in' }}</strong> &bull; {{ customer.phone || 'No phone' }}</span>
              </div>
            </div>

            <!-- Right: Grand Total & Change Due Display -->
            <div class="pay-right-col">
              <div class="bill-summary-ticket">
                <div class="ticket-row-sm">
                  <span>Subtotal</span>
                  <span>${{ calculateSubtotal().toFixed(2) }}</span>
                </div>
                <div class="ticket-row-sm" v-if="selectedDiscount">
                  <span>Discount</span>
                  <span class="disc-text">-${{ calculateDiscountAmount().toFixed(2) }}</span>
                </div>
                <div class="ticket-row-sm">
                  <span>Tax (7%)</span>
                  <span>${{ calculateTax().toFixed(2) }}</span>
                </div>

                <div class="ticket-hero-total">
                  <span class="hero-lbl">Net Amount Due</span>
                  <span class="hero-amt">${{ calculateTotal().toFixed(2) }}</span>
                </div>

                <!-- Change Due Box -->
                <div class="change-due-box" v-if="paymentModal.method === 'cash'">
                  <span class="change-lbl">Change to Return</span>
                  <span class="change-amt" :class="{ 'change-positive': paymentModal.change >= 0, 'change-insufficient': paymentModal.change < 0 }">
                    ${{ Math.max(0, paymentModal.change).toFixed(2) }}
                  </span>
                  <span class="underpaid-warning" v-if="paymentModal.change < 0">
                    Remaining to collect: ${{ Math.abs(paymentModal.change).toFixed(2) }}
                  </span>
                </div>
              </div>

              <!-- Complete Transaction Button -->
              <button
                class="btn-finalize-pay"
                :disabled="processingOrder || (paymentModal.method === 'cash' && paymentModal.tendered < calculateTotal())"
                @click="proceedToCheckout"
              >
                <i class="material-icons" :class="{ 'spin': processingOrder }">
                  {{ processingOrder ? 'autorenew' : 'print' }}
                </i>
                <span>{{ processingOrder ? 'Recording Sale...' : 'Finalize & Print [Enter]' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- ==================== HELD / PARKED BILLS DRAWER MODAL ==================== -->
    <transition name="fade-modal">
      <div class="modal-overlay" v-if="heldBillsModal" @click="heldBillsModal = false">
        <div class="held-bills-dialog" @click.stop>
          <div class="held-header">
            <div class="held-title-box">
              <i class="material-icons">history</i>
              <h3>Parked Sales Register ({{ heldBillsCount }})</h3>
            </div>
            <button class="btn-modal-x" @click="heldBillsModal = false"><i class="material-icons">close</i></button>
          </div>

          <div class="held-body">
            <div v-if="heldBillsCount === 0" class="held-empty">
              <i class="material-icons">inbox</i>
              <p>No parked bills currently on hold.</p>
            </div>

            <div v-else class="held-list">
              <div v-for="(bill, index) in (heldBills || [])" :key="bill.id" class="held-card">
                <div class="held-card-header">
                  <div class="held-card-meta">
                    <span class="held-badge">Bill #{{ index + 1 }}</span>
                    <span class="held-time">{{ bill.timestamp }}</span>
                  </div>
                  <span class="held-total">${{ bill.total.toFixed(2) }}</span>
                </div>

                <div class="held-card-customer">
                  <i class="material-icons">person</i>
                  <span>{{ bill.customer.name || 'Walk-in' }} ({{ bill.customer.phone || 'No phone' }})</span>
                </div>

                <div class="held-card-items-preview">
                  <span v-for="it in bill.items.slice(0, 4)" :key="it.id" class="held-item-pill">
                    {{ it.name }} &times; {{ it.quantity }}
                  </span>
                  <span v-if="bill.items.length > 4" class="held-more">+{{ bill.items.length - 4 }} more</span>
                </div>

                <div class="held-card-actions">
                  <button class="btn-recall-this" @click="recallBill(index)">
                    <i class="material-icons">restore</i>
                    <span>Resume Sale</span>
                  </button>
                  <button class="btn-discard-held" @click="discardHeldBill(index)" title="Discard this held bill">
                    <i class="material-icons">delete_outline</i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Product Quick View Modal (Visual Mode) -->
    <transition name="fade-modal">
      <div class="modal-overlay" v-if="quickViewProduct" @click="closeQuickView">
        <div class="modal-dialog" @click.stop>
          <button class="modal-close-icon" @click="closeQuickView"><i class="material-icons">close</i></button>

          <div class="modal-body-split">
            <div class="modal-img-col">
              <img :src="getProductImageUrl(quickViewProduct)" :alt="quickViewProduct.name" @error="handleImageError" />
              <div class="modal-stock-badge" :class="getStockClass(quickViewProduct)">
                <i class="material-icons">{{ getStockIcon(quickViewProduct) }}</i>
                <span>{{ getStockLabel(quickViewProduct) }} ({{ quickViewProduct.stock }} in stock)</span>
              </div>
            </div>

            <div class="modal-info-col">
              <span class="modal-category">{{ getCategoryName(quickViewProduct.category_id) }}</span>
              <h2 class="modal-title">{{ quickViewProduct.name }}</h2>
              <p class="modal-price">${{ quickViewProduct.price.toFixed(2) }}</p>

              <div class="modal-desc" v-if="quickViewProduct.description">{{ quickViewProduct.description }}</div>

              <div class="modal-action-box">
                <div class="modal-qty-control">
                  <span class="qty-prompt">Quantity:</span>
                  <div class="qty-stepper modal-stepper">
                    <button class="qty-btn" @click="decreaseModalQuantity" :disabled="modalQuantity <= 1">
                      <i class="material-icons">remove</i>
                    </button>
                    <span class="qty-value">{{ modalQuantity }}</span>
                    <button class="qty-btn" @click="increaseModalQuantity" :disabled="modalQuantity >= quickViewProduct.stock">
                      <i class="material-icons">add</i>
                    </button>
                  </div>
                </div>

                <button class="btn-modal-add-cart" :disabled="quickViewProduct.stock <= 0" @click="addFromModal">
                  <i class="material-icons">add_shopping_cart</i>
                  <span>Add {{ modalQuantity }} to Order</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Order Complete / Receipt Confirmation Modal -->
    <transition name="fade-modal">
      <div class="modal-overlay" v-if="showOrderComplete" @click="closeOrderComplete">
        <div class="order-success-dialog" @click.stop>
          <div class="success-top-badge">
            <div class="check-ring"><i class="material-icons">done</i></div>
            <h2>Transaction Completed!</h2>
            <p>Invoice #{{ orderSummary.order_id || '---' }} generated successfully.</p>
          </div>

          <div class="receipt-preview-ticket">
            <div class="ticket-header">
              <h3>PeakPOS Store</h3>
              <p>Receipt #{{ orderSummary.order_id }} &bull; {{ currentDate }}</p>
              <p v-if="customer.name">Customer: {{ customer.name }} ({{ customer.phone || 'N/A' }})</p>
            </div>

            <div class="ticket-items">
              <div v-for="item in orderSummary.items" :key="item.id" class="ticket-row">
                <span class="ticket-item-title">{{ item.name }} &times; {{ item.quantity }}</span>
                <span class="ticket-item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>

            <div class="ticket-totals">
              <div class="ticket-calc-row"><span>Subtotal:</span><span>${{ orderSummary.subtotal.toFixed(2) }}</span></div>
              <div class="ticket-calc-row"><span>Tax (7%):</span><span>${{ orderSummary.tax.toFixed(2) }}</span></div>
              <div class="ticket-calc-row" v-if="orderSummary.discount > 0">
                <span>Discount:</span><span>-${{ orderSummary.discount.toFixed(2) }}</span>
              </div>
              <div class="ticket-calc-row ticket-grand-total"><span>Total Paid:</span><span>${{ orderSummary.total.toFixed(2) }}</span></div>
              <div class="ticket-calc-row" v-if="paymentModal.method === 'cash'">
                <span>Cash Tendered:</span><span>${{ paymentModal.tendered.toFixed(2) }}</span>
              </div>
              <div class="ticket-calc-row" v-if="paymentModal.method === 'cash'">
                <span>Change Returned:</span><span>${{ Math.max(0, paymentModal.change).toFixed(2) }}</span>
              </div>
            </div>
          </div>

          <div class="success-actions">
            <button class="btn-thermal-print" @click="printReceipt">
              <i class="material-icons">receipt</i>
              <span>Print Thermal Receipt</span>
            </button>
            <button class="btn-new-order" @click="closeOrderComplete">
              <i class="material-icons">add_shopping_cart</i>
              <span>New Sale [F1]</span>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modern Toast Notification -->
    <transition name="toast-slide">
      <div v-if="toast.show" class="pos-toast" :class="toast.type">
        <i class="material-icons toast-ico">{{ toast.icon }}</i>
        <div class="toast-body">
          <h5 class="toast-heading">{{ toast.title }}</h5>
          <p class="toast-msg">{{ toast.message }}</p>
        </div>
        <button class="toast-dismiss" @click="toast.show = false"><i class="material-icons">close</i></button>
      </div>
    </transition>

    <!-- Fast Cashier PIN Switch / Terminal Lock Overlay -->
    <PinLockModal
      :is-open="isTerminalLocked"
      @unlock="onCashierUnlocked"
      @close="isTerminalLocked = false"
    />
  </div>
</template>

<script>
import PinLockModal from '@/components/common/PinLockModal.vue';
import escpos from '@/services/escpos';

export default {
  name: 'SalesView',
  components: {
    PinLockModal
  },
  data() {
    return {
      // Background USB Barcode Scanner Interceptor State
      scannerBuffer: '',
      lastKeystrokeTime: 0,
      isTerminalLocked: false,

      // POS Display Mode: 'counter' (high-speed data grid) vs 'visual' (touch cards)
      posMode: localStorage.getItem('posMode') || 'counter',

      // Products & Categories Data
      products: [],
      categories: [],
      loading: true,
      searchTerm: '',
      exactMatchFound: false,
      viewMode: localStorage.getItem('salesViewMode') || 'grid',
      activeCategory: 'all',

      // Cart & Line Items
      cart: [],
      isMobileCartVisible: false,
      selectedDiscount: null,
      discounts: [],
      discountLoading: false,
      processingOrder: false,

      // Customer & Prescriber Information
      customer: {
        name: '',
        phone: '',
        doctor: ''
      },
      customerPopoverOpen: false,

      // Held / Parked Bills Register
      heldBills: [],
      heldBillsModal: false,

      // Payment Tender & Change Calculator
      paymentModal: {
        show: false,
        method: 'cash',
        tendered: 0,
        change: 0
      },

      // Modals State
      quickViewProduct: null,
      modalQuantity: 1,
      showOrderComplete: false,
      orderSummary: {
        items: [],
        subtotal: 0,
        tax: 0,
        discount: 0,
        total: 0,
        order_id: null
      },

      // Cashier and Time state
      cashierName: localStorage.getItem('username') || 'Cashier',
      cashierRole: localStorage.getItem('role') || 'Staff',
      currentTime: '',
      currentDate: '',
      clockInterval: null,

      // Toast State
      toast: {
        show: false,
        type: 'success',
        title: '',
        message: '',
        icon: 'check_circle',
        timeout: null
      }
    };
  },
  computed: {
    heldBillsCount() {
      return Array.isArray(this.heldBills) ? this.heldBills.length : 0;
    },
    cartTotalItems() {
      return this.cart.reduce((sum, item) => sum + item.quantity, 0);
    },
    filteredProducts() {
      let result = [...this.products];

      if (this.searchTerm) {
        const query = this.searchTerm.toLowerCase().trim();
        result = result.filter(product => {
          const nameMatch = product.name && product.name.toLowerCase().includes(query);
          const descMatch = product.description && product.description.toLowerCase().includes(query);
          const catMatch = this.getCategoryName(product.category_id).toLowerCase().includes(query);
          const idMatch = String(product.id) === query;
          return nameMatch || descMatch || catMatch || idMatch;
        });
      }

      if (this.activeCategory !== 'all') {
        switch (this.activeCategory) {
          case 'popular':
            result = result.filter(p => p.sales_count && p.sales_count > 5);
            result.sort((a, b) => (b.sales_count || 0) - (a.sales_count || 0));
            break;
          case 'new':
            result = result.filter(p => this.isNewProduct(p));
            break;
          case 'sale':
            result = result.filter(p => this.isOnSale(p));
            break;
          default:
            if (!isNaN(parseInt(this.activeCategory))) {
              result = result.filter(p => p.category_id === parseInt(this.activeCategory));
            }
        }
      }

      return result;
    }
  },
  methods: {
    setPosMode(mode) {
      this.posMode = mode;
      localStorage.setItem('posMode', mode);
      this.$nextTick(() => {
        if (mode === 'counter' && this.$refs.barcodeInput) {
          this.$refs.barcodeInput.focus();
        }
      });
    },

    togglePosMode() {
      this.setPosMode(this.posMode === 'counter' ? 'visual' : 'counter');
    },

    updateClock() {
      const now = new Date();
      this.currentTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      this.currentDate = now.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
    },

    getProductImageUrl(product) {
      if (!product) return this.getPlaceholderImage();
      const imagePath = product.image_url || product.image;
      if (!imagePath) return this.getPlaceholderImage();
      if (/^https?:\/\//.test(imagePath)) return imagePath;

      const backendBase = 'http://127.0.0.1:5000';
      const cleanPath = imagePath.replace(/^\/+|\/+$/g, '');
      let finalPath;

      if (cleanPath.startsWith('static/')) {
        finalPath = cleanPath;
      } else if (cleanPath.startsWith('product_images/')) {
        finalPath = `static/${cleanPath}`;
      } else {
        finalPath = `static/product_images/${cleanPath}`;
      }

      return `${backendBase}/${finalPath}`;
    },

    handleImageError(e) {
      e.target.src = this.getPlaceholderImage();
    },

    getPlaceholderImage() {
      return 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlMmU4ZjAiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1zaXplPSIyMCIgZm9udC13ZWlnaHQ9IjYwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZvbnQtZmFtaWx5PSJzeXN0ZW0tdWksIHNhbnMtc2VyaWYiIGZpbGw9IiM5NGEzYjgiPlBlYWtQT1M8L3RleHQ+PC9zdmc+';
    },

    isNewProduct(product) {
      if (!product || !product.created_at) return false;
      const createdDate = new Date(product.created_at);
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return createdDate > thirtyDaysAgo;
    },

    isOnSale(product) {
      return !!(product.on_sale || product.discount_price);
    },

    getStockClass(product) {
      if (product.stock <= 0) return 'out-of-stock';
      if (product.stock < 10) return 'low-stock';
      return 'in-stock';
    },

    getStockIcon(product) {
      if (product.stock <= 0) return 'block';
      if (product.stock < 10) return 'warning';
      return 'check_circle';
    },

    getStockLabel(product) {
      if (product.stock <= 0) return 'Out of Stock';
      if (product.stock < 10) return 'Low Stock';
      return 'In Stock';
    },

    getCategoryName(categoryId) {
      const cat = this.categories.find(c => c.id === categoryId);
      return cat ? cat.name : 'General';
    },

    handleCardClick(product) {
      if (product.stock > 0) {
        this.addToCart(product);
      } else {
        this.showProductQuickView(product);
      }
    },

    // Rapid Barcode & Search Enter Action
    handleBarcodeOrEnterSearch() {
      const query = this.searchTerm.trim();
      if (!query) return;

      // Check for exact ID / Barcode match first
      const exactMatch = this.products.find(p => String(p.id) === query || (p.barcode && p.barcode === query));
      if (exactMatch) {
        this.addToCart(exactMatch);
        this.searchTerm = '';
        return;
      }

      // If exactly one match in filtered list, add it
      if (this.filteredProducts.length === 1) {
        this.addToCart(this.filteredProducts[0]);
        this.searchTerm = '';
        return;
      }

      // Otherwise if matches exist, add first available
      if (this.filteredProducts.length > 0) {
        const available = this.filteredProducts.find(p => p.stock > 0);
        if (available) {
          this.addToCart(available);
          this.searchTerm = '';
        }
      }
    },

    addAndClear(product) {
      this.addToCart(product);
      this.searchTerm = '';
      if (this.$refs.barcodeInput) {
        this.$refs.barcodeInput.focus();
      }
    },

    async fetchProducts() {
      this.loading = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/products');
        if (response.ok) {
          this.products = await response.json();
          this.restoreCartFromStorage();
        } else {
          this.showToast('Error', 'Failed to load products.', 'error');
        }
      } catch (error) {
        this.showToast('Network Error', 'Cannot connect to server.', 'error');
      } finally {
        this.loading = false;
      }
    },

    async fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/categories');
        if (response.ok) {
          this.categories = await response.json();
        }
      } catch (err) {
        console.error('Error fetching categories:', err);
      }
    },

    async fetchDiscounts() {
      this.discountLoading = true;
      try {
        const response = await fetch('http://127.0.0.1:5000/api/discounts');
        if (response.ok) {
          this.discounts = await response.json();
        }
      } catch (err) {
        console.error('Error fetching discounts:', err);
      } finally {
        this.discountLoading = false;
      }
    },

    searchProducts() {},

    clearSearch() {
      this.searchTerm = '';
    },

    filterByCategory(category) {
      this.activeCategory = category;
    },

    resetFilters() {
      this.searchTerm = '';
      this.activeCategory = 'all';
    },

    addToCart(product) {
      if (product.stock <= 0) {
        this.showToast('Out of Stock', `${product.name} is currently out of stock.`, 'warning');
        return;
      }

      const existingIndex = this.cart.findIndex(item => item.id === product.id);
      if (existingIndex >= 0) {
        if (this.cart[existingIndex].quantity < product.stock) {
          this.cart[existingIndex].quantity++;
          this.showToast('Updated', `Quantity increased for ${product.name}`, 'success');
        } else {
          this.showToast('Stock Limit', `Maximum available stock (${product.stock}) reached.`, 'warning');
        }
      } else {
        this.cart.push({ ...product, quantity: 1 });
        this.showToast('Added', `${product.name} added to bill`, 'success');
      }
      this.saveCartToStorage();
    },

    removeFromCart(index) {
      const removed = this.cart[index];
      this.cart.splice(index, 1);
      this.saveCartToStorage();
      if (removed) {
        this.showToast('Removed', `${removed.name} removed from bill.`, 'info');
      }
    },

    increaseQuantity(index) {
      const item = this.cart[index];
      if (item && item.quantity < item.stock) {
        item.quantity++;
        this.saveCartToStorage();
      }
    },

    decreaseQuantity(index) {
      const item = this.cart[index];
      if (item && item.quantity > 1) {
        item.quantity--;
        this.saveCartToStorage();
      }
    },

    validateItemQuantity(item) {
      if (!item.quantity || item.quantity < 1) item.quantity = 1;
      if (item.quantity > item.stock) {
        item.quantity = item.stock;
        this.showToast('Stock Limit', `Adjusted to maximum available (${item.stock}).`, 'warning');
      }
      this.saveCartToStorage();
    },

    clearCart() {
      if (!this.cart.length) return;
      this.cart = [];
      localStorage.removeItem('peak_pos_cart');
      this.showToast('Cart Cleared', 'Active register cleared.', 'info');
    },

    saveCartToStorage() {
      localStorage.setItem('peak_pos_cart', JSON.stringify(this.cart));
    },

    restoreCartFromStorage() {
      const saved = localStorage.getItem('peak_pos_cart');
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          this.cart = parsed.filter(item => {
            const current = this.products.find(p => p.id === item.id);
            if (!current) return false;
            item.price = current.price;
            item.stock = current.stock;
            if (item.quantity > current.stock) {
              item.quantity = Math.max(1, current.stock);
            }
            return true;
          });
          if (parsed.length !== this.cart.length) {
            this.saveCartToStorage();
          }
        } catch (e) {
          localStorage.removeItem('peak_pos_cart');
        }
      }
    },

    toggleMobileCart() {
      this.isMobileCartVisible = !this.isMobileCartVisible;
    },

    calculateSubtotal() {
      return this.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    },

    calculateTax() {
      return this.calculateSubtotal() * 0.07;
    },

    calculateDiscountAmount() {
      if (!this.selectedDiscount) return 0;
      const discount = this.discounts.find(d => d.id === this.selectedDiscount);
      if (!discount) return 0;
      const sub = this.calculateSubtotal();
      if (discount.discount_type === 'percentage') {
        return sub * (discount.value / 100);
      }
      return Math.min(sub, discount.value);
    },

    calculateTotal() {
      const total = this.calculateSubtotal() + this.calculateTax() - this.calculateDiscountAmount();
      return Math.max(0, total);
    },

    // 1-Click Fast Tender Presets for Right Pane
    oneClickCashPay(amount) {
      if (this.cart.length === 0) return;
      const total = this.calculateTotal();
      this.paymentModal.method = 'cash';
      if (amount === 'exact') {
        this.paymentModal.tendered = parseFloat(total.toFixed(2));
      } else {
        this.paymentModal.tendered = parseFloat(amount.toFixed(2));
      }
      this.calculateChange();
      this.paymentModal.show = true;
    },

    oneClickCardPay() {
      if (this.cart.length === 0) return;
      this.paymentModal.method = 'card';
      this.paymentModal.tendered = this.calculateTotal();
      this.paymentModal.change = 0;
      this.paymentModal.show = true;
    },

    async printLastReceipt() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/receipts', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          const receipts = await response.json();
          if (receipts && receipts.length > 0) {
            const latest = receipts[0];
            this.orderSummary = {
              order_id: latest.order_id || latest.receipt_id,
              items: latest.snapshot?.items || [],
              subtotal: latest.snapshot?.subtotal || 0,
              tax: latest.snapshot?.tax || 0,
              discount: latest.snapshot?.discount || 0,
              total: latest.snapshot?.total || 0
            };
            this.printReceipt();
            this.showToast('Reprinting', `Reprinting receipt #${latest.receipt_id}`, 'info');
          } else {
            this.showToast('No Receipts', 'No prior transactions found to reprint.', 'warning');
          }
        }
      } catch (e) {
        this.showToast('Reprint Error', 'Could not fetch prior receipt.', 'error');
      }
    },

    async openDrawerKick() {
      const res = await escpos.kickCashDrawer();
      if (res.success) {
        this.showToast('Drawer Open', 'Cash drawer pulse signal sent.', 'success');
      } else {
        this.showToast('Drawer Signal', 'Simulated cash drawer trigger.', 'info');
      }
    },

    // ==================== BILL PARKING / HOLDING SYSTEM ====================
    parkCurrentBill() {
      if (this.cart.length === 0) return;

      const newHeld = {
        id: Date.now(),
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        items: [...this.cart],
        customer: { ...this.customer },
        discountId: this.selectedDiscount,
        total: this.calculateTotal()
      };

      this.heldBills.unshift(newHeld);
      localStorage.setItem('peak_held_bills', JSON.stringify(this.heldBills));

      // Reset active cart and customer
      this.cart = [];
      this.customer = { name: '', phone: '', doctor: '' };
      this.selectedDiscount = null;
      localStorage.removeItem('peak_pos_cart');

      this.showToast('Bill Parked [F2]', `Saved to held queue. New bill ready.`, 'info');
    },

    openHeldBillsModal() {
      this.heldBillsModal = true;
    },

    recallBill(index) {
      const bill = this.heldBills[index];
      if (!bill) return;

      // If active cart has items, warn or auto-park
      if (this.cart.length > 0) {
        this.parkCurrentBill();
      }

      this.cart = [...bill.items];
      this.customer = { ...bill.customer };
      this.selectedDiscount = bill.discountId;
      this.saveCartToStorage();

      this.heldBills.splice(index, 1);
      localStorage.setItem('peak_held_bills', JSON.stringify(this.heldBills));

      this.heldBillsModal = false;
      this.showToast('Sale Resumed', `Restored bill with ${this.cart.length} items.`, 'success');
    },

    discardHeldBill(index) {
      this.heldBills.splice(index, 1);
      localStorage.setItem('peak_held_bills', JSON.stringify(this.heldBills));
      this.showToast('Discarded', 'Held bill removed.', 'info');
    },

    restoreHeldBillsFromStorage() {
      try {
        const saved = localStorage.getItem('peak_held_bills');
        if (saved) {
          const parsed = JSON.parse(saved);
          if (Array.isArray(parsed)) {
            this.heldBills = parsed;
            return;
          }
        }
      } catch (e) {
        console.error('Error restoring held bills:', e);
      }
      this.heldBills = [];
    },

    // ==================== PAYMENT MODAL & CASH CALCULATOR ====================
    openPaymentModal() {
      if (this.cart.length === 0) return;
      this.paymentModal.show = true;
      this.paymentModal.method = 'cash';
      this.paymentModal.tendered = Math.ceil(this.calculateTotal());
      this.calculateChange();

      this.$nextTick(() => {
        if (this.$refs.tenderedInput) {
          this.$refs.tenderedInput.focus();
          this.$refs.tenderedInput.select();
        }
      });
    },

    closePaymentModal() {
      this.paymentModal.show = false;
    },

    setPaymentMethod(method) {
      this.paymentModal.method = method;
      if (method !== 'cash') {
        this.paymentModal.tendered = this.calculateTotal();
        this.paymentModal.change = 0;
      } else {
        this.calculateChange();
      }
    },

    setExactTendered() {
      this.paymentModal.tendered = parseFloat(this.calculateTotal().toFixed(2));
      this.calculateChange();
    },

    addTendered(amount) {
      const current = parseFloat(this.paymentModal.tendered || 0);
      this.paymentModal.tendered = parseFloat((current + amount).toFixed(2));
      this.calculateChange();
    },

    calculateChange() {
      const tendered = parseFloat(this.paymentModal.tendered || 0);
      const total = this.calculateTotal();
      this.paymentModal.change = parseFloat((tendered - total).toFixed(2));
    },

    // Checkout Finalization
    async proceedToCheckout() {
      if (this.cart.length === 0 || this.processingOrder) return;
      this.processingOrder = true;

      try {
        const orderData = {
          cart: this.cart.map(c => ({
            id: c.id,
            quantity: c.quantity,
            price: c.price
          })),
          discount_id: this.selectedDiscount,
          subtotal: this.calculateSubtotal(),
          tax: this.calculateTax(),
          total: this.calculateTotal()
        };

        const response = await fetch('http://127.0.0.1:5000/api/checkout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(orderData)
        });

        if (!response.ok) {
          throw new Error('Failed to process order');
        }

        const orderResponse = await response.json();
        const orderId = orderResponse.order_id || orderResponse.order?.id;

        this.orderSummary = {
          items: [...this.cart],
          subtotal: this.calculateSubtotal(),
          tax: this.calculateTax(),
          discount: this.calculateDiscountAmount(),
          total: this.calculateTotal(),
          order_id: orderId
        };

        // Create snapshot receipt
        const receiptPayload = {
          order_id: this.orderSummary.order_id,
          snapshot: {
            items: this.cart.map(item => ({
              id: item.id,
              name: item.name,
              price: item.price,
              quantity: item.quantity
            })),
            customer: this.customer,
            subtotal: this.orderSummary.subtotal,
            tax: this.orderSummary.tax,
            discount: this.orderSummary.discount,
            total: this.orderSummary.total
          }
        };

        try {
          await fetch('http://127.0.0.1:5000/api/receipts', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(receiptPayload)
          });
        } catch (err) {
          console.error('Receipt generation error:', err);
        }

        this.closePaymentModal();
        this.showOrderComplete = true;
        this.cart = [];
        this.customer = { name: '', phone: '', doctor: '' };
        localStorage.removeItem('peak_pos_cart');
      } catch (error) {
        console.error('Checkout error:', error);
        this.showToast('Checkout Failed', 'Failed to complete transaction.', 'error');
      } finally {
        this.processingOrder = false;
      }
    },

    async printReceipt() {
      if (!this.orderSummary || !this.orderSummary.order_id) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/receipts/${this.orderSummary.order_id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (!response.ok) throw new Error('Failed to fetch receipt');
        const receipt = await response.json();

        // Check if direct silent hardware thermal printer is paired
        const printerStatus = escpos.getPrinterStatus();
        if (printerStatus.connected) {
          const receiptData = {
            date: new Date(receipt.created_at || Date.now()).toLocaleDateString(),
            time: new Date(receipt.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            invoiceNo: `#PK-${receipt.receipt_id}`,
            cashier: this.cashierName || 'Admin',
            items: receipt.snapshot.items,
            subtotal: receipt.snapshot.subtotal,
            tax: receipt.snapshot.tax,
            total: receipt.snapshot.total,
            tendered: this.paymentModal.tendered || receipt.snapshot.total,
            change: this.paymentModal.change || 0,
            paymentMethod: this.paymentModal.method || 'Cash',
            customer: receipt.snapshot.customer
          };
          const res = await escpos.printReceiptSilently(receiptData, { business_name: 'PeakPOS Retail & Pharmacy' });
          if (res.mode === 'silent_usb' || res.mode === 'silent_serial') {
            this.showToast('Silent Print', 'Receipt printed directly to thermal printer & cash drawer kicked!', 'success');
            return;
          }
        }

        const receiptHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Receipt #${receipt.receipt_id} - PeakPOS</title>
  <style>
    body {
      font-family: 'Courier New', monospace;
      padding: 18px;
      max-width: 320px;
      margin: 0 auto;
      color: #111;
      font-size: 13px;
    }
    .head { text-align: center; border-bottom: 1px dashed #444; padding-bottom: 10px; margin-bottom: 10px; }
    .head h2 { margin: 0; font-size: 18px; text-transform: uppercase; letter-spacing: 1px; }
    .meta { font-size: 11px; margin-top: 5px; color: #555; }
    .items { width: 100%; border-bottom: 1px dashed #444; padding-bottom: 8px; margin-bottom: 8px; }
    .item-line { display: flex; justify-content: space-between; margin-bottom: 4px; }
    .totals-line { display: flex; justify-content: space-between; margin-bottom: 4px; }
    .grand { font-weight: bold; font-size: 15px; border-top: 1px solid #111; padding-top: 6px; margin-top: 6px; }
    .foot { text-align: center; margin-top: 15px; font-size: 11px; color: #555; }
    @media print { body { padding: 0; } }
  </style>
</head>
<body>
  <div class="head">
    <h2>PeakPOS Store</h2>
    <div class="meta">
      <div>Order #${receipt.receipt_id}</div>
      <div>Date: ${new Date(receipt.created_at || Date.now()).toLocaleString()}</div>
      ${receipt.snapshot.customer?.name ? `<div>Customer: ${receipt.snapshot.customer.name}</div>` : ''}
    </div>
  </div>
  <div class="items">
    ${receipt.snapshot.items.map(it => `
      <div class="item-line">
        <span>${it.name} &times; ${it.quantity}</span>
        <span>$${(it.price * it.quantity).toFixed(2)}</span>
      </div>
    `).join('')}
  </div>
  <div>
    <div class="totals-line"><span>Subtotal:</span><span>$${receipt.snapshot.subtotal.toFixed(2)}</span></div>
    <div class="totals-line"><span>Tax (7%):</span><span>$${receipt.snapshot.tax.toFixed(2)}</span></div>
    ${receipt.snapshot.discount > 0 ? `<div class="totals-line"><span>Discount:</span><span>-$${receipt.snapshot.discount.toFixed(2)}</span></div>` : ''}
    <div class="totals-line grand"><span>Total:</span><span>$${receipt.snapshot.total.toFixed(2)}</span></div>
  </div>
  <div class="foot">
    <p>Thank you for your purchase!</p>
    <p>PeakPOS &bull; www.peakpos.com</p>
  </div>
</body>
</html>`;

        const win = window.open('', '_blank');
        win.document.open();
        win.document.write(receiptHtml);
        win.document.close();
        win.onload = () => {
          setTimeout(() => {
            win.focus();
            win.print();
          }, 300);
        };
      } catch (err) {
        console.error('Print receipt error:', err);
      }
    },

    closeOrderComplete() {
      this.showOrderComplete = false;
      this.selectedDiscount = null;
    },

    showProductQuickView(product) {
      this.quickViewProduct = product;
      this.modalQuantity = 1;
    },

    closeQuickView() {
      this.quickViewProduct = null;
    },

    increaseModalQuantity() {
      if (this.quickViewProduct && this.modalQuantity < this.quickViewProduct.stock) {
        this.modalQuantity++;
      }
    },

    decreaseModalQuantity() {
      if (this.modalQuantity > 1) {
        this.modalQuantity--;
      }
    },

    addFromModal() {
      if (!this.quickViewProduct || this.quickViewProduct.stock <= 0) return;
      this.addToCart(this.quickViewProduct);
      this.closeQuickView();
    },

    // Keyboard Shortcuts & Background USB Barcode Scanner Handler
    handleGlobalKeydown(e) {
      if (this.isTerminalLocked) return;

      // Ctrl+L: Lock Terminal & Switch Cashier
      if ((e.ctrlKey || e.metaKey) && (e.key === 'l' || e.key === 'L')) {
        e.preventDefault();
        this.isTerminalLocked = true;
        return;
      }

      // Background USB Laser / CCD Barcode Gun Interceptor
      // Hardware barcode scanners stream characters rapidly (< 50ms interval) terminated by Enter
      const now = Date.now();
      const diff = now - this.lastKeystrokeTime;
      this.lastKeystrokeTime = now;

      if (e.key === 'Enter') {
        if (this.scannerBuffer.length >= 3 && diff < 80) {
          e.preventDefault();
          e.stopPropagation();
          const scannedCode = this.scannerBuffer.trim();
          this.scannerBuffer = '';
          this.processBackgroundBarcodeScan(scannedCode);
          return;
        }
        this.scannerBuffer = '';
      } else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        if (diff < 60 || this.scannerBuffer.length === 0) {
          this.scannerBuffer += e.key;
        } else {
          this.scannerBuffer = e.key;
        }
      } else if (e.key !== 'Shift') {
        this.scannerBuffer = '';
      }

      // Don't intercept if typing in standard textareas
      if (e.target.tagName === 'TEXTAREA') return;

      if (e.key === 'F1') {
        e.preventDefault();
        if (this.posMode === 'counter' && this.$refs.barcodeInput) {
          this.$refs.barcodeInput.focus();
          this.$refs.barcodeInput.select();
        } else if (this.$refs.visualSearchInput) {
          this.$refs.visualSearchInput.focus();
        }
      } else if (e.key === 'F2') {
        e.preventDefault();
        this.parkCurrentBill();
      } else if (e.key === 'F3') {
        e.preventDefault();
        this.openHeldBillsModal();
      } else if (e.key === 'F4') {
        e.preventDefault();
        this.clearCart();
      } else if (e.key === 'F9') {
        e.preventDefault();
        this.togglePosMode();
      } else if (e.key === 'F12') {
        e.preventDefault();
        if (this.cart.length > 0 && !this.processingOrder) {
          if (!this.paymentModal.show) {
            this.openPaymentModal();
          } else {
            this.proceedToCheckout();
          }
        }
      } else if (e.key === 'Escape') {
        if (this.paymentModal.show) this.closePaymentModal();
        if (this.heldBillsModal) this.heldBillsModal = false;
        if (this.quickViewProduct) this.closeQuickView();
        if (this.showOrderComplete) this.closeOrderComplete();
      }
    },

    processBackgroundBarcodeScan(barcode) {
      const code = String(barcode).trim().toLowerCase();
      const product = this.products.find(p => {
        const pBarcode = String(p.barcode || '').toLowerCase();
        const pSku = String(p.sku || '').toLowerCase();
        const pId = String(p.id);
        const pName = String(p.name || '').toLowerCase();
        return pBarcode === code || pSku === code || pId === code || pName === code;
      });

      if (product) {
        this.addToCart(product);
        escpos.playScanSuccess();
        this.showToast('Item Scanned', `${product.name} added to cart`, 'success');
        if (this.$refs.barcodeInput) this.counterSearchTerm = '';
      } else {
        escpos.playErrorBuzz();
        this.showToast('Barcode Not Found', `No product matching "${barcode}"`, 'error');
      }
    },

    onCashierUnlocked(cashier) {
      this.cashierName = cashier.name;
      this.cashierRole = cashier.role;
      this.isTerminalLocked = false;
      this.showToast('Shift Active', `Logged in as ${cashier.name}`, 'info');
    },

    showToast(title, message, type = 'success') {
      if (this.toast.timeout) clearTimeout(this.toast.timeout);
      let icon = 'check_circle';
      if (type === 'error') icon = 'error_outline';
      else if (type === 'warning') icon = 'warning_amber';
      else if (type === 'info') icon = 'info_outline';

      this.toast = {
        show: true,
        type,
        title,
        message,
        icon,
        timeout: setTimeout(() => {
          this.toast.show = false;
        }, 3200)
      };
    }
  },
  created() {
    this.$watch('viewMode', newMode => {
      localStorage.setItem('salesViewMode', newMode);
    });
    this.fetchProducts();
    this.fetchCategories();
    this.fetchDiscounts();
    this.restoreHeldBillsFromStorage();
    this.updateClock();
    this.clockInterval = setInterval(this.updateClock, 1000);
  },
  mounted() {
    window.addEventListener('keydown', this.handleGlobalKeydown);
  },
  beforeUnmount() {
    if (this.clockInterval) clearInterval(this.clockInterval);
    window.removeEventListener('keydown', this.handleGlobalKeydown);
  }
};
</script>

<style scoped>
/* ==========================================================================
   PeakPOS High-Speed Hybrid POS Layout
   ========================================================================== */

.pos-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  background-color: #f1f5f9;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #0f172a;
  overflow: hidden;
}

/* --------------------------------------------------------------------------
   Header Bar
   -------------------------------------------------------------------------- */
.pos-header {
  height: 60px;
  background: #ffffff;
  border-bottom: 1px solid #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  flex-shrink: 0;
  z-index: 25;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.brand-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-logo {
  height: 38px;
  width: auto;
  max-width: 44px;
  object-fit: contain;
}

.brand-meta {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.03em;
  line-height: 1;
  margin: 0;
}

.brand-name span { color: #4f46e5; }

.register-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.68rem;
  font-weight: 700;
  color: #059669;
  letter-spacing: 0.02em;
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
}

/* Mode Switcher Tabs in Header */
.mode-selector {
  display: flex;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 2px;
}

.mode-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: #64748b;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.mode-btn i { font-size: 1rem; }

.mode-btn.active {
  background: #1e293b;
  color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
  text-decoration: none;
}

.nav-pill:hover { background: #f1f5f9; color: #0f172a; }

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* Shortcuts Legend */
.shortcuts-legend {
  display: flex;
  align-items: center;
  gap: 6px;
}

.sc-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 700;
  color: #475569;
  cursor: default;
}

.sc-tag kbd {
  background: #1e293b;
  color: #fff;
  border-radius: 4px;
  padding: 1px 5px;
  font-size: 0.68rem;
  font-family: inherit;
}

.sc-tag.has-held {
  background: #eef2ff;
  border-color: #818cf8;
  color: #4338ca;
  cursor: pointer;
}

.clock-widget {
  display: flex;
  flex-direction: column;
  text-align: right;
  line-height: 1.15;
}

.clock-time {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1e293b;
  font-variant-numeric: tabular-nums;
}

.clock-date {
  font-size: 0.7rem;
  color: #64748b;
  font-weight: 500;
}

.cashier-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 3px 10px 3px 4px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.2s;
}

.cashier-badge:hover {
  background: #eef2ff;
  border-color: #6366f1;
}

.lock-status-ico {
  font-size: 1rem;
  color: #64748b;
  margin-left: 2px;
}

.sc-tag.lock-tag {
  background: #fef2f2;
  color: #ef4444;
  border: 1px solid #fecaca;
  cursor: pointer;
  transition: all 0.2s;
}

.sc-tag.lock-tag:hover {
  background: #ef4444;
  color: white;
}

.cashier-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #e0e7ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cashier-avatar i { font-size: 1rem; }

.cashier-info { display: flex; flex-direction: column; }
.cashier-name { font-size: 0.8rem; font-weight: 700; color: #0f172a; line-height: 1.1; }
.cashier-role { font-size: 0.65rem; color: #64748b; text-transform: capitalize; }

.mobile-cart-btn {
  display: none;
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #4f46e5;
  color: #fff;
  border: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.mobile-cart-btn .badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ef4444;
  color: #fff;
  font-size: 0.68rem;
  font-weight: 800;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* --------------------------------------------------------------------------
   Sub-Header: Customer & Prescriber Strip
   -------------------------------------------------------------------------- */
.customer-strip {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 6px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-shrink: 0;
}

.customer-fields {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon i {
  position: absolute;
  left: 10px;
  color: #94a3b8;
  font-size: 1.05rem;
  pointer-events: none;
}

.strip-input {
  height: 34px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0 10px 0 32px;
  font-size: 0.82rem;
  color: #0f172a;
  min-width: 200px;
  outline: none;
}

.strip-input:focus {
  border-color: #4f46e5;
  background: #ffffff;
}

.strip-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-park-bill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fde68a;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-park-bill:hover:not(:disabled) {
  background: #fde68a;
}

.btn-park-bill:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-recall-bill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-recall-bill.btn-recall-active {
  background: #eef2ff;
  border-color: #a5b4fc;
  color: #4338ca;
}

/* --------------------------------------------------------------------------
   MODE 1: MODERN SPLIT-PANE HYBRID (Square & Shopify POS Pro)
   -------------------------------------------------------------------------- */
.split-register-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
  background: #f1f5f9;
  position: relative;
}

/* LEFT PANE (62%): High-Speed Working Area */
.register-left-pane {
  flex: 62;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-right: 1px solid #cbd5e1;
  overflow: hidden;
  position: relative;
}

/* Top Utility Bar */
.register-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 18px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  position: relative;
}

.customer-picker-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  padding: 4px 10px;
  border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.customer-picker-pill.has-customer {
  background: #eef2ff;
  border-color: #818cf8;
}

.customer-picker-pill i {
  color: #4f46e5;
  font-size: 1.15rem;
}

.cust-pill-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.cust-name-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #0f172a;
}

.cust-phone-label {
  font-size: 0.68rem;
  color: #64748b;
}

.btn-edit-customer {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #64748b;
  display: flex;
  align-items: center;
  padding: 2px;
}

.btn-edit-customer:hover {
  color: #4f46e5;
}

/* Customer Popover */
.customer-popover-card {
  position: absolute;
  top: 50px;
  left: 18px;
  width: 320px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
  z-index: 40;
  overflow: hidden;
}

.popover-header {
  padding: 10px 14px;
  background: #f1f5f9;
  font-size: 0.8rem;
  font-weight: 700;
  color: #334155;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popover-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
}

.popover-body {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.popover-input-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.popover-input-group label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
}

.popover-input {
  height: 34px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0 10px;
  font-size: 0.84rem;
  outline: none;
}

.popover-input:focus {
  border-color: #4f46e5;
}

.btn-popover-save {
  margin-top: 6px;
  height: 36px;
  background: #4f46e5;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
}

.register-quick-stats {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stat-bubble {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #475569;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
}

.stat-bubble i {
  font-size: 1rem;
  color: #4f46e5;
}

.btn-clean-cart {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
}

/* Hero Search & Category Bar */
.hero-search-container {
  padding: 12px 18px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.hero-search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.hero-scan-ico {
  position: absolute;
  left: 14px;
  color: #4f46e5;
  font-size: 1.4rem;
  pointer-events: none;
}

.hero-search-input {
  width: 100%;
  height: 48px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  padding: 0 80px 0 48px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #0f172a;
  outline: none;
  transition: all 0.2s;
}

.hero-search-input:focus {
  background: #ffffff;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.f1-badge {
  position: absolute;
  right: 40px;
  color: #94a3b8;
  font-size: 0.7rem;
  font-weight: 700;
  pointer-events: none;
}

.f1-badge kbd {
  background: #e2e8f0;
  color: #475569;
  padding: 2px 6px;
  border-radius: 4px;
}

.hero-clear-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
}

.quick-filter-chips {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 2px;
}

.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 12px;
  border-radius: 20px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #475569;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s;
}

.filter-chip:hover {
  background: #eef2ff;
  border-color: #a5b4fc;
  color: #4338ca;
}

.filter-chip.active {
  background: #1e293b;
  border-color: #1e293b;
  color: #ffffff;
}

.filter-chip i {
  font-size: 0.95rem;
}

/* Instant Search Dropdown */
.instant-search-dropdown-split {
  position: absolute;
  top: 130px;
  left: 18px;
  right: 18px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.2);
  z-index: 35;
  overflow: hidden;
}

/* Spacious Modern Cart Table */
.split-table-wrapper {
  flex: 1;
  overflow-y: auto;
  background: #ffffff;
}

.split-cart-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.split-cart-table thead {
  position: sticky;
  top: 0;
  background: #f8fafc;
  color: #475569;
  z-index: 5;
  border-bottom: 2px solid #e2e8f0;
}

.split-cart-table th {
  padding: 12px 14px;
  font-size: 0.74rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.split-item-row {
  border-bottom: 1px solid #e2e8f0;
  transition: background 0.15s;
}

.split-item-row:hover {
  background: #f8fafc;
}

.split-cart-table td {
  padding: 12px 14px;
  vertical-align: middle;
}

.col-idx {
  font-size: 0.8rem;
  font-weight: 700;
  color: #94a3b8;
}

.item-title-block {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.item-name-text {
  font-size: 0.92rem;
  font-weight: 700;
  color: #0f172a;
}

.item-subtags {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.subtag-sku {
  font-size: 0.72rem;
  font-family: monospace;
  background: #f1f5f9;
  padding: 1px 6px;
  border-radius: 4px;
  color: #475569;
}

.subtag-category {
  font-size: 0.72rem;
  font-weight: 600;
  color: #4f46e5;
  background: #eef2ff;
  padding: 1px 6px;
  border-radius: 4px;
}

.subtag-desc {
  font-size: 0.72rem;
  color: #64748b;
}

.stock-pill-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 12px;
  display: inline-block;
  background: #dcfce7;
  color: #166534;
}

.stock-pill-badge.low-stock {
  background: #fef3c7;
  color: #92400e;
}

.stock-pill-badge.out-of-stock {
  background: #fee2e2;
  color: #991b1b;
}

.price-input-box {
  display: flex;
  align-items: center;
  gap: 2px;
}

.curr-sign {
  font-size: 0.8rem;
  font-weight: 700;
  color: #64748b;
}

.table-price-input {
  width: 76px;
  height: 32px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0 6px;
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
}

.table-price-input:focus {
  border-color: #4f46e5;
  background: #ffffff;
}

.stepper-box {
  display: inline-flex;
  align-items: center;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  overflow: hidden;
}

.step-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #ffffff;
  color: #334155;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}

.step-btn:hover:not(:disabled) {
  background: #e2e8f0;
}

.step-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.step-btn i {
  font-size: 1rem;
}

.step-input {
  width: 44px;
  height: 32px;
  border: none;
  background: transparent;
  text-align: center;
  font-weight: 800;
  font-size: 0.9rem;
  color: #0f172a;
  outline: none;
}

.item-total-amount {
  font-size: 1rem;
  font-weight: 800;
  color: #0f172a;
  display: block;
  text-align: right;
}

.btn-del-row {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}

.btn-del-row:hover {
  color: #ef4444;
}

/* Empty Art State */
.split-table-empty {
  height: 360px;
  text-align: center;
}

.empty-register-art {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.art-icon-ring {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #eef2ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.art-icon-ring i {
  font-size: 3rem;
}

.empty-register-art h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 6px 0;
}

.empty-register-art p {
  font-size: 0.88rem;
  color: #64748b;
  margin: 0 0 16px 0;
}

.empty-register-art kbd {
  background: #1e293b;
  color: #ffffff;
  padding: 2px 6px;
  border-radius: 4px;
}

.ready-tips {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 0.78rem;
  color: #64748b;
}

.ready-tips kbd {
  background: #e2e8f0;
  color: #334155;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 700;
}

/* ==========================================================================
   RIGHT PANE (38%): Fixed Action & Tender Summary Slip
   ========================================================================== */
.register-right-pane {
  flex: 38;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  overflow-y: auto;
  padding: 16px;
}

.order-slip-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.slip-header {
  padding: 14px 18px;
  background: #1e293b;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.slip-title-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.slip-title-meta i {
  color: #818cf8;
  font-size: 1.3rem;
}

.slip-title-meta h3 {
  font-size: 0.95rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.01em;
}

.slip-actions-top {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-slip-action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 6px;
  background: #334155;
  color: #f1f5f9;
  border: 1px solid #475569;
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-slip-action:hover:not(:disabled) {
  background: #475569;
}

.btn-slip-action.has-held-badge {
  background: #4f46e5;
  border-color: #6366f1;
}

.btn-slip-action:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Customer Card inside Slip */
.slip-customer-badge {
  padding: 12px 18px;
  background: #f8fafc;
  border-bottom: 1px dashed #cbd5e1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.cust-avatar-ring {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #e0e7ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cust-meta-block {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.cust-lead-name {
  font-size: 0.88rem;
  font-weight: 800;
  color: #0f172a;
}

.cust-lead-sub {
  font-size: 0.72rem;
  color: #64748b;
}

.btn-swap-cust {
  padding: 4px 10px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.74rem;
  font-weight: 700;
  color: #4f46e5;
  cursor: pointer;
}

/* Slip Breakdown */
.slip-breakdown {
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.breakdown-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.85rem;
}

.row-label {
  color: #64748b;
  font-weight: 600;
}

.row-value {
  color: #1e293b;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}

.discount-row {
  background: #f8fafc;
  padding: 6px 10px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.row-label-with-icon {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
  color: #334155;
}

.row-label-with-icon i {
  color: #4f46e5;
  font-size: 1rem;
}

.discount-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.slip-discount-select {
  border: 1px solid #cbd5e1;
  background: #ffffff;
  border-radius: 4px;
  padding: 3px 6px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #4f46e5;
  outline: none;
}

.discount-deduct-val {
  font-size: 0.85rem;
  font-weight: 800;
  color: #ef4444;
}

.slip-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 4px 0;
}

/* Hero Grand Total */
.breakdown-hero-total {
  padding: 14px;
  background: #f1f5f9;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hero-total-label {
  display: flex;
  flex-direction: column;
}

.hero-total-label span:first-child {
  font-size: 0.8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #4f46e5;
}

.items-summary-note {
  font-size: 0.72rem;
  color: #64748b;
}

.hero-total-price {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.hero-curr {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0f172a;
}

.hero-val {
  font-size: 2.1rem;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.03em;
  line-height: 1;
}

/* Quick Cash Presets */
.quick-cash-presets {
  padding: 12px 18px;
  border-top: 1px dashed #cbd5e1;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.preset-label {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #64748b;
  letter-spacing: 0.05em;
}

.preset-buttons-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.btn-cash-preset {
  height: 38px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 800;
  color: #1e293b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  transition: all 0.15s;
}

.btn-cash-preset:hover:not(:disabled) {
  background: #eef2ff;
  border-color: #818cf8;
  color: #4338ca;
}

.btn-cash-preset.exact {
  background: #ecfdf5;
  border-color: #a7f3d0;
  color: #065f46;
}

.btn-cash-preset.exact:hover:not(:disabled) {
  background: #d1fae5;
}

.btn-cash-preset.card-preset {
  background: #f1f5f9;
  color: #475569;
}

.btn-cash-preset.card-preset i {
  font-size: 1rem;
}

.btn-cash-preset:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Massive Primary Pay Button */
.slip-pay-action {
  padding: 14px 18px;
  background: #ffffff;
}

.btn-massive-pay {
  width: 100%;
  height: 58px;
  border-radius: 12px;
  background: #10b981;
  color: #ffffff;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
  transition: all 0.15s ease;
}

.btn-massive-pay:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
}

.btn-massive-pay:disabled {
  background: #cbd5e1;
  color: #94a3b8;
  cursor: not-allowed;
  box-shadow: none;
}

.pay-btn-content {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.15rem;
  font-weight: 900;
  letter-spacing: 0.02em;
}

.pay-btn-content i {
  font-size: 1.5rem;
}

.pay-btn-amount {
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: -0.02em;
}

/* Slip Bottom Utility Bar */
.slip-bottom-bar {
  padding: 10px 18px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.bottom-util-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: transparent;
  border: none;
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
}

.bottom-util-btn:hover:not(:disabled) {
  background: #e2e8f0;
  color: #0f172a;
}

.bottom-util-btn.danger {
  color: #ef4444;
}

.bottom-util-btn.danger:hover:not(:disabled) {
  background: #fee2e2;
}

.bottom-util-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* --------------------------------------------------------------------------
   MODE 2: TOUCH / VISUAL CATALOG MODE STYLING
   -------------------------------------------------------------------------- */
.pos-main {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
}

.catalog-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f8fafc;
  padding: 16px 20px 20px 24px;
}

.catalog-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 12px;
}

.search-box {
  flex: 1;
  max-width: 520px;
  position: relative;
  display: flex;
  align-items: center;
}

.search-ico {
  position: absolute;
  left: 14px;
  color: #94a3b8;
  font-size: 1.25rem;
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 42px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0 38px 0 42px;
  font-size: 0.88rem;
  color: #0f172a;
  outline: none;
}

.search-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12);
}

.search-clear-btn {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
}

.toolbar-actions { display: flex; align-items: center; gap: 8px; }

.view-switch {
  display: flex;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 2px;
}

.view-toggle-btn {
  width: 34px;
  height: 34px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.view-toggle-btn.active { background: #4f46e5; color: #ffffff; }

.refresh-catalog-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

/* Category Strip */
.category-strip {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 12px;
  scrollbar-width: none;
  flex-shrink: 0;
}

.category-strip::-webkit-scrollbar { display: none; }

.category-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  font-size: 0.82rem;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  white-space: nowrap;
}

.category-chip i { font-size: 1rem; }
.chip-count {
  font-size: 0.7rem;
  padding: 1px 6px;
  border-radius: 9999px;
  background: #f1f5f9;
  color: #64748b;
}

.category-chip.active {
  background: #1e293b;
  color: #ffffff;
  border-color: #1e293b;
}

.category-chip.active .chip-count {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

/* Catalog Scroll Container */
.catalog-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding-right: 4px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  padding-bottom: 24px;
}

.pos-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.pos-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px -3px rgba(0, 0, 0, 0.08);
}

.pos-card.is-out-of-stock { opacity: 0.65; }

.card-image-box {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #f1f5f9;
}

.card-image-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-badges {
  position: absolute;
  top: 8px;
  left: 8px;
  right: 8px;
  display: flex;
  justify-content: space-between;
  pointer-events: none;
}

.badge {
  font-size: 0.65rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
}

.badge.sale { background: #ef4444; color: #fff; }
.badge.new { background: #3b82f6; color: #fff; }
.badge.low-stock { background: #f59e0b; color: #fff; }
.badge.oos { background: #64748b; color: #fff; }

.card-content {
  padding: 10px 12px 12px 12px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-category {
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
}

.card-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.25;
  margin: 2px 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  height: 2.5em;
}

.card-footer {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 6px;
  border-top: 1px dashed #f1f5f9;
}

.price-stack { display: flex; align-items: baseline; }
.currency-symbol { font-size: 0.8rem; font-weight: 800; color: #4f46e5; }
.price-value { font-size: 1.1rem; font-weight: 800; color: #0f172a; }

.btn-add-cart {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #eef2ff;
  color: #4f46e5;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-add-cart:hover:not(:disabled) { background: #4f46e5; color: #fff; }

/* Table View in Visual Mode */
.product-table-wrapper {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  overflow: hidden;
}

.product-table { width: 100%; border-collapse: collapse; text-align: left; }
.product-table th {
  background: #f8fafc;
  padding: 10px 14px;
  font-size: 0.75rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  border-bottom: 1px solid #cbd5e1;
}

.product-table td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
.td-item { display: flex; align-items: center; gap: 10px; }
.row-thumb { width: 40px; height: 40px; border-radius: 6px; object-fit: cover; }
.row-title { font-weight: 700; font-size: 0.88rem; color: #0f172a; display: block; }
.row-sku { font-size: 0.7rem; color: #94a3b8; }
.cat-tag { font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; background: #f1f5f9; font-weight: 600; }
.stock-pill { display: inline-flex; align-items: center; gap: 3px; font-size: 0.75rem; font-weight: 600; }
.stock-pill.in-stock { color: #059669; }
.stock-pill.low-stock { color: #d97706; }
.stock-pill.out-of-stock { color: #dc2626; }
.td-price { font-size: 0.95rem; font-weight: 800; }
.btn-table-add { width: 34px; height: 34px; border-radius: 6px; background: #4f46e5; color: #fff; border: none; cursor: pointer; }

/* Visual Mode Cart Sidebar */
.pos-cart {
  width: 380px;
  flex-shrink: 0;
  background: #ffffff;
  border-left: 1px solid #cbd5e1;
  display: flex;
  flex-direction: column;
}

.cart-card { display: flex; flex-direction: column; height: 100%; }

.cart-top {
  padding: 14px 18px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.cart-title-wrap { display: flex; align-items: center; gap: 10px; }
.cart-icon-bubble {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #eef2ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-heading { font-size: 1rem; font-weight: 800; margin: 0; }
.cart-subheading { font-size: 0.72rem; color: #64748b; }
.cart-top-actions { display: flex; align-items: center; gap: 6px; }

.btn-cart-clear {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 4px 8px;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 5px;
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
}

.btn-close-mobile-cart { display: none; background: none; border: none; }

.cart-body { flex: 1; overflow-y: auto; padding: 12px 14px; }
.cart-empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #94a3b8;
  padding: 20px;
}

.cart-empty-icon {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.cart-empty-icon i { font-size: 1.8rem; color: #94a3b8; }
.cart-items-list { display: flex; flex-direction: column; gap: 8px; }

.cart-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.cart-item-thumb {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  overflow: hidden;
  background: #e2e8f0;
  flex-shrink: 0;
}

.cart-item-thumb img { width: 100%; height: 100%; object-fit: cover; }
.cart-item-details { flex: 1; min-width: 0; }
.cart-item-main { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
.cart-item-name { font-size: 0.82rem; font-weight: 700; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cart-item-unit-price { font-size: 0.7rem; color: #64748b; }
.cart-item-subline { display: flex; align-items: center; justify-content: space-between; }
.qty-stepper { display: inline-flex; align-items: center; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 5px; }
.qty-btn { width: 22px; height: 22px; background: none; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.qty-value { padding: 0 4px; font-size: 0.78rem; font-weight: 700; min-width: 18px; text-align: center; }
.cart-item-total { font-size: 0.88rem; font-weight: 800; }
.btn-item-del { background: none; border: none; color: #94a3b8; cursor: pointer; }
.btn-item-del:hover { color: #ef4444; }

.cart-footer { border-top: 1px solid #e2e8f0; padding: 14px 18px 18px 18px; background: #ffffff; }
.summary-breakdown { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }
.calc-row { display: flex; justify-content: space-between; font-size: 0.82rem; color: #64748b; }
.calc-val { font-weight: 700; color: #1e293b; }
.discount-selection-row { padding: 2px 0; }
.discount-lead { display: flex; align-items: center; gap: 4px; color: #4f46e5; font-weight: 600; }
.pos-select-discount { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 2px 6px; font-size: 0.75rem; }
.discount-deduction { color: #dc2626; font-weight: 700; font-size: 0.82rem; }
.calc-divider { height: 1px; background: #f1f5f9; margin: 4px 0; }
.grand-total-row { margin-top: 2px; }
.grand-total-label { font-size: 1rem; font-weight: 800; color: #0f172a; }
.grand-total-val { font-size: 1.35rem; font-weight: 900; color: #0f172a; }

.btn-checkout-primary {
  width: 100%;
  height: 48px;
  border-radius: 10px;
  background: #4f46e5;
  color: #ffffff;
  border: none;
  font-size: 0.95rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
}

.btn-checkout-primary:disabled { background: #cbd5e1; color: #94a3b8; cursor: not-allowed; box-shadow: none; }

/* --------------------------------------------------------------------------
   PAYMENT & CASH CALCULATOR MODAL STYLING
   -------------------------------------------------------------------------- */
.payment-dialog {
  background: #ffffff;
  border-radius: 16px;
  max-width: 780px;
  width: 100%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.payment-modal-header {
  padding: 14px 20px;
  background: #1e293b;
  color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pay-title-box { display: flex; align-items: center; gap: 8px; }
.pay-title-box h3 { font-size: 1.05rem; font-weight: 800; margin: 0; }
.btn-modal-x { background: none; border: none; color: #94a3b8; cursor: pointer; }
.btn-modal-x:hover { color: #fff; }

.payment-modal-body {
  display: flex;
  min-height: 380px;
}

.pay-left-col {
  width: 55%;
  padding: 24px;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.pay-section-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 8px;
  display: block;
}

.tender-tabs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.tender-btn {
  height: 48px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #334155;
  font-weight: 700;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 12px;
  cursor: pointer;
}

.tender-btn i { font-size: 1.25rem; color: #64748b; }

.tender-btn.active {
  background: #eef2ff;
  border-color: #4f46e5;
  color: #4f46e5;
}

.tender-btn.active i { color: #4f46e5; }

.cash-calc-container { margin-bottom: 16px; }

.tendered-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.tendered-curr {
  position: absolute;
  left: 14px;
  font-size: 1.4rem;
  font-weight: 800;
  color: #4f46e5;
}

.tendered-input {
  width: 100%;
  height: 52px;
  background: #f8fafc;
  border: 2px solid #cbd5e1;
  border-radius: 8px;
  padding: 0 14px 0 38px;
  font-size: 1.5rem;
  font-weight: 900;
  color: #0f172a;
  outline: none;
}

.tendered-input:focus {
  border-color: #4f46e5;
  background: #ffffff;
}

.denom-presets {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.denom-btn {
  padding: 6px 12px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 700;
  color: #334155;
  cursor: pointer;
}

.denom-btn:hover { background: #f1f5f9; }

.customer-receipt-note {
  margin-top: auto;
  padding: 8px 12px;
  background: #f1f5f9;
  border-radius: 6px;
  font-size: 0.78rem;
  color: #475569;
  display: flex;
  align-items: center;
  gap: 6px;
}

.pay-right-col {
  width: 45%;
  background: #f8fafc;
  padding: 24px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.bill-summary-ticket {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
}

.ticket-row-sm {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  color: #64748b;
  margin-bottom: 6px;
}

.disc-text { color: #dc2626; font-weight: 700; }

.ticket-hero-total {
  border-top: 1px dashed #cbd5e1;
  padding-top: 10px;
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.hero-lbl { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; }
.hero-amt { font-size: 1.8rem; font-weight: 900; color: #0f172a; line-height: 1.1; }

.change-due-box {
  margin-top: 16px;
  padding: 12px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.change-lbl { font-size: 0.75rem; font-weight: 700; color: #475569; text-transform: uppercase; }

.change-amt {
  font-size: 1.7rem;
  font-weight: 900;
  line-height: 1.1;
  margin: 4px 0 2px 0;
}

.change-positive { color: #059669; }
.change-insufficient { color: #dc2626; }
.underpaid-warning { font-size: 0.72rem; color: #dc2626; font-weight: 700; }

.btn-finalize-pay {
  width: 100%;
  height: 52px;
  border-radius: 10px;
  background: #059669;
  color: #ffffff;
  border: none;
  font-size: 1.05rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.35);
  margin-top: 16px;
}

.btn-finalize-pay:disabled {
  background: #cbd5e1;
  color: #94a3b8;
  cursor: not-allowed;
  box-shadow: none;
}

/* --------------------------------------------------------------------------
   HELD BILLS MODAL STYLING
   -------------------------------------------------------------------------- */
.held-bills-dialog {
  background: #ffffff;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.held-header {
  padding: 14px 20px;
  background: #1e293b;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.held-title-box { display: flex; align-items: center; gap: 8px; }
.held-title-box h3 { margin: 0; font-size: 1.05rem; font-weight: 800; }

.held-body { padding: 18px; overflow-y: auto; flex: 1; }
.held-empty { text-align: center; padding: 40px; color: #94a3b8; }
.held-empty i { font-size: 3rem; margin-bottom: 8px; }

.held-list { display: flex; flex-direction: column; gap: 12px; }

.held-card {
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 12px 14px;
  background: #f8fafc;
}

.held-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.held-card-meta { display: flex; align-items: center; gap: 8px; }
.held-badge { font-size: 0.75rem; font-weight: 800; background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 4px; }
.held-time { font-size: 0.75rem; color: #64748b; }
.held-total { font-size: 1.1rem; font-weight: 900; color: #0f172a; }

.held-card-customer { font-size: 0.8rem; color: #475569; display: flex; align-items: center; gap: 4px; margin-bottom: 8px; }
.held-card-customer i { font-size: 0.95rem; }

.held-card-items-preview { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px; }
.held-item-pill { font-size: 0.72rem; padding: 2px 6px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; }
.held-more { font-size: 0.72rem; color: #64748b; padding: 2px; }

.held-card-actions { display: flex; justify-content: flex-end; gap: 8px; }
.btn-recall-this {
  padding: 6px 14px;
  border-radius: 6px;
  background: #4f46e5;
  color: #fff;
  border: none;
  font-size: 0.82rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.btn-discard-held {
  padding: 6px 8px;
  background: #fee2e2;
  color: #dc2626;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* Modals & Overlays */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 16px;
}

.modal-dialog {
  background: #ffffff;
  border-radius: 16px;
  max-width: 650px;
  width: 100%;
  position: relative;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-close-icon {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body-split { display: flex; min-height: 320px; }
.modal-img-col {
  width: 45%;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border-right: 1px solid #f1f5f9;
}

.modal-img-col img { max-width: 100%; max-height: 180px; object-fit: contain; }
.modal-stock-badge { margin-top: 12px; font-size: 0.72rem; font-weight: 700; padding: 4px 8px; border-radius: 9999px; }
.modal-stock-badge.in-stock { background: #dcfce7; color: #166534; }
.modal-stock-badge.low-stock { background: #fef3c7; color: #92400e; }
.modal-stock-badge.out-of-stock { background: #fee2e2; color: #991b1b; }

.modal-info-col { width: 55%; padding: 28px 24px; display: flex; flex-direction: column; }
.modal-category { font-size: 0.72rem; font-weight: 700; color: #4f46e5; text-transform: uppercase; }
.modal-title { font-size: 1.2rem; font-weight: 800; color: #0f172a; margin: 2px 0 6px 0; }
.modal-price { font-size: 1.4rem; font-weight: 900; color: #0f172a; margin-bottom: 10px; }
.modal-desc { font-size: 0.82rem; color: #64748b; line-height: 1.4; margin-bottom: 16px; flex: 1; }
.modal-action-box { margin-top: auto; display: flex; flex-direction: column; gap: 10px; }
.modal-qty-control { display: flex; align-items: center; justify-content: space-between; }
.qty-prompt { font-size: 0.82rem; font-weight: 700; }
.modal-stepper { padding: 2px; }
.modal-stepper .qty-btn { width: 28px; height: 28px; }
.btn-modal-add-cart {
  width: 100%;
  height: 44px;
  border-radius: 8px;
  background: #4f46e5;
  color: #fff;
  border: none;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
}

/* Order Success Dialog */
.order-success-dialog {
  background: #ffffff;
  border-radius: 16px;
  max-width: 440px;
  width: 100%;
  padding: 24px;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.check-ring {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: #dcfce7;
  color: #16a34a;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.check-ring i { font-size: 2rem; }
.success-top-badge h2 { font-size: 1.25rem; font-weight: 800; margin: 0 0 4px 0; }
.success-top-badge p { font-size: 0.8rem; color: #64748b; margin: 0 0 14px 0; }

.receipt-preview-ticket {
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 16px;
  text-align: left;
}

.ticket-header { border-bottom: 1px dashed #cbd5e1; padding-bottom: 6px; margin-bottom: 6px; text-align: center; }
.ticket-header h3 { font-size: 0.92rem; font-weight: 800; margin: 0; }
.ticket-header p { font-size: 0.72rem; color: #64748b; margin: 0; }

.ticket-items { max-height: 120px; overflow-y: auto; border-bottom: 1px dashed #cbd5e1; padding-bottom: 6px; margin-bottom: 6px; }
.ticket-row { display: flex; justify-content: space-between; font-size: 0.76rem; margin-bottom: 2px; }
.ticket-totals { display: flex; flex-direction: column; gap: 2px; font-size: 0.76rem; }
.ticket-calc-row { display: flex; justify-content: space-between; color: #64748b; }
.ticket-grand-total { font-size: 0.9rem; font-weight: 800; color: #0f172a; border-top: 1px solid #cbd5e1; padding-top: 4px; margin-top: 2px; }

.success-actions { display: flex; gap: 8px; }
.btn-thermal-print {
  flex: 1;
  height: 44px;
  border-radius: 8px;
  background: #1e293b;
  color: #fff;
  border: none;
  font-weight: 700;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
}

.btn-new-order {
  flex: 1;
  height: 44px;
  border-radius: 8px;
  background: #4f46e5;
  color: #fff;
  border: none;
  font-weight: 700;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
}

/* Toast */
.pos-toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #ffffff;
  border-radius: 10px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
  border: 1px solid #cbd5e1;
  z-index: 100;
  max-width: 340px;
}

.pos-toast.success { border-left: 4px solid #10b981; }
.pos-toast.warning { border-left: 4px solid #f59e0b; }
.pos-toast.error   { border-left: 4px solid #ef4444; }
.pos-toast.info    { border-left: 4px solid #3b82f6; }

.toast-body { flex: 1; }
.toast-heading { font-size: 0.82rem; font-weight: 700; margin: 0; color: #0f172a; }
.toast-msg { font-size: 0.75rem; color: #64748b; margin: 1px 0 0 0; }
.toast-dismiss { background: none; border: none; color: #94a3b8; cursor: pointer; }

/* Responsive adjustments */
@media (max-width: 1024px) {
  .header-nav { display: none; }
  .mobile-cart-btn { display: flex; }
  .pos-cart {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: 380px;
    max-width: 90vw;
    z-index: 40;
    transform: translateX(100%);
    transition: transform 0.25s ease;
    box-shadow: -10px 0 25px rgba(0, 0, 0, 0.15);
  }
  .pos-cart.mobile-open { transform: translateX(0); }
  .btn-close-mobile-cart { display: flex; }
  .mobile-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    z-index: 35;
  }
}

@media (max-width: 768px) {
  .shortcuts-legend { display: none; }
  .payment-modal-body { flex-direction: column; }
  .pay-left-col, .pay-right-col { width: 100%; border-right: none; }
  .pay-left-col { border-bottom: 1px solid #e2e8f0; }
}
</style>
