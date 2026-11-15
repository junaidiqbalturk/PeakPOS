/**
 * PeakPOS ESC/POS Silent Hardware Printing & Peripheral Driver
 * Supports WebUSB, WebSerial, and raw ESC/POS command sequences.
 * Direct thermal printing & Cash Drawer Kick without browser print dialog.
 */

class EscPosDriver {
  constructor() {
    this.usbDevice = null;
    this.serialPort = null;
    this.serialWriter = null;
    this.connectionType = localStorage.getItem('peakpos_printer_type') || null; // 'usb', 'serial', or null
    this.audioCtx = null;
  }

  // Audio feedback using Web Audio API (No external sound files required)
  getAudioContext() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.audioCtx = new AudioContext();
      }
    }
    return this.audioCtx;
  }

  playBeep(freq = 1200, duration = 0.08, type = 'sine') {
    try {
      const ctx = this.getAudioContext();
      if (!ctx) return;
      if (ctx.state === 'suspended') ctx.resume();

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      gain.gain.setValueAtTime(0.15, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + duration);
    } catch {
      // Audio autoplay policy fallback
    }
  }

  playScanSuccess() {
    this.playBeep(1400, 0.09, 'sine');
  }

  playErrorBuzz() {
    this.playBeep(320, 0.22, 'sawtooth');
  }

  playDrawerKickSound() {
    this.playBeep(800, 0.15, 'square');
  }

  // Check hardware API availability
  isWebUsbSupported() {
    return !!(navigator && navigator.usb);
  }

  isWebSerialSupported() {
    return !!(navigator && navigator.serial);
  }

  getPrinterStatus() {
    if (this.usbDevice && this.usbDevice.opened) {
      return { connected: true, type: 'usb', name: this.usbDevice.productName || 'USB Thermal Printer' };
    }
    if (this.serialPort && this.serialPort.readable) {
      return { connected: true, type: 'serial', name: 'Serial / COM POS Printer' };
    }
    const saved = localStorage.getItem('peakpos_printer_name');
    if (saved) {
      return { connected: false, type: this.connectionType, name: `${saved} (Paired)` };
    }
    return { connected: false, type: null, name: 'Standard Browser Print (No Direct USB)' };
  }

  /**
   * Pair WebUSB Printer
   */
  async pairUsbPrinter() {
    if (!this.isWebUsbSupported()) {
      throw new Error('WebUSB is not supported in this browser. Please use Google Chrome or Microsoft Edge.');
    }

    try {
      // Request device with printer class or generic USB
      const device = await navigator.usb.requestDevice({
        filters: [{ classCode: 7 }] // 7 = USB Printer Class
      }).catch(async () => {
        // Fallback to all devices if device descriptor doesn't advertise classCode 7
        return await navigator.usb.requestDevice({ filters: [] });
      });

      if (!device) throw new Error('No device selected.');

      await device.open();
      if (device.configuration === null) {
        await device.selectConfiguration(1);
      }
      await device.claimInterface(0);

      this.usbDevice = device;
      this.connectionType = 'usb';
      localStorage.setItem('peakpos_printer_type', 'usb');
      localStorage.setItem('peakpos_printer_name', device.productName || 'USB Thermal Printer');

      this.playScanSuccess();
      return { success: true, name: device.productName || 'USB Thermal Printer' };
    } catch (err) {
      console.warn('WebUSB pairing canceled or failed:', err);
      throw err;
    }
  }

  /**
   * Pair WebSerial Printer (COM Port)
   */
  async pairSerialPrinter(baudRate = 9600) {
    if (!this.isWebSerialSupported()) {
      throw new Error('WebSerial is not supported in this browser. Please use Google Chrome or Microsoft Edge.');
    }

    try {
      const port = await navigator.serial.requestPort();
      await port.open({ baudRate: Number(baudRate) || 9600 });
      this.serialPort = port;
      this.serialWriter = port.writable.getWriter();
      this.connectionType = 'serial';
      localStorage.setItem('peakpos_printer_type', 'serial');
      localStorage.setItem('peakpos_printer_name', `COM Port (${baudRate} baud)`);

      this.playScanSuccess();
      return { success: true, name: `COM Port (${baudRate} baud)` };
    } catch (err) {
      console.warn('WebSerial pairing canceled or failed:', err);
      throw err;
    }
  }

  disconnectPrinter() {
    if (this.usbDevice && this.usbDevice.opened) {
      this.usbDevice.close().catch(() => {});
    }
    if (this.serialWriter) {
      this.serialWriter.releaseLock();
      this.serialWriter = null;
    }
    if (this.serialPort) {
      this.serialPort.close().catch(() => {});
      this.serialPort = null;
    }
    this.usbDevice = null;
    this.connectionType = null;
    localStorage.removeItem('peakpos_printer_type');
    localStorage.removeItem('peakpos_printer_name');
  }

  /**
   * Generate raw ESC/POS Byte Buffer
   */
  buildEscPosCommands(receiptData, settings = {}, options = { kickDrawer: true, cutPaper: true }) {
    const bytes = [];
    const textEncoder = new TextEncoder();

    const pushBytes = (...arr) => bytes.push(...arr);
    const pushString = (str) => {
      const encoded = textEncoder.encode(str);
      for (let i = 0; i < encoded.length; i++) {
        bytes.push(encoded[i]);
      }
    };
    const pushLine = (str = '') => {
      pushString(str + '\n');
    };

    // 1. Initialize Printer (ESC @)
    pushBytes(0x1B, 0x40);

    // 2. Kick Cash Drawer if requested (ESC p 0 25 250)
    if (options.kickDrawer) {
      pushBytes(0x1B, 0x70, 0x00, 0x19, 0xFA);
    }

    // 3. Center Align (ESC a 1)
    pushBytes(0x1B, 0x61, 0x01);

    // Double Height & Width for Store Title (ESC ! 0x30)
    pushBytes(0x1B, 0x21, 0x30);
    const storeName = (settings.business_name || 'PEAKPOS STORE').toUpperCase();
    pushLine(storeName);

    // Normal Text Mode (ESC ! 0x00)
    pushBytes(0x1B, 0x21, 0x00);

    // Header Text (Address, phone, etc.)
    if (settings.header_text) {
      const headerLines = settings.header_text.split('\n');
      headerLines.forEach(l => pushLine(l.trim()));
    }

    const colWidth = (settings.paper_width === '58' ? 32 : 42);
    const divider = '-'.repeat(colWidth);
    pushLine(divider);

    // Left Align for Metadata (ESC a 0)
    pushBytes(0x1B, 0x61, 0x00);
    const dateStr = receiptData.date || new Date().toLocaleDateString();
    const timeStr = receiptData.time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const invoiceStr = receiptData.invoiceNo || `#PK-${Math.floor(1000 + Math.random() * 9000)}`;
    const cashierStr = receiptData.cashier || 'Admin';

    pushLine(`Inv #: ${invoiceStr}  Date: ${dateStr}`);
    pushLine(`Time : ${timeStr}  Cashier: ${cashierStr}`);
    if (receiptData.customer && receiptData.customer.name) {
      pushLine(`Cust : ${receiptData.customer.name} (${receiptData.customer.phone || 'General'})`);
    }
    pushLine(divider);

    // Table Header
    // Column format: Name (18 chars), Qty (4 chars), Price (8 chars), Total (10 chars)
    if (colWidth >= 40) {
      pushLine('Item Description         Qty   Price     Total');
    } else {
      pushLine('Item Description    Qty  Price   Total');
    }
    pushLine(divider);

    // Line Items
    const items = receiptData.items || [];
    items.forEach(item => {
      const name = (item.name || item.product_name || 'Item').substring(0, 18);
      const qty = String(item.quantity || 1).padStart(3, ' ');
      const price = `$${Number(item.price || item.unit_price || 0).toFixed(2)}`.padStart(7, ' ');
      const total = `$${(Number(item.quantity || 1) * Number(item.price || 0)).toFixed(2)}`.padStart(8, ' ');

      const paddedName = name.padEnd(18, ' ');
      pushLine(`${paddedName} ${qty} ${price} ${total}`);
    });

    pushLine(divider);

    // Totals Section (Right Align)
    pushBytes(0x1B, 0x61, 0x02);
    const subtotal = Number(receiptData.subtotal || 0).toFixed(2);
    const tax = Number(receiptData.tax || 0).toFixed(2);
    const total = Number(receiptData.total || 0).toFixed(2);
    const tendered = Number(receiptData.tendered || receiptData.total || 0).toFixed(2);
    const change = Number(receiptData.change || 0).toFixed(2);

    pushLine(`Subtotal: $${subtotal}`);
    pushLine(`Tax: $${tax}`);

    // Bold Total (ESC E 1)
    pushBytes(0x1B, 0x45, 0x01);
    pushBytes(0x1B, 0x21, 0x20); // Double height
    pushLine(`TOTAL DUE: $${total}`);
    pushBytes(0x1B, 0x45, 0x00);
    pushBytes(0x1B, 0x21, 0x00); // Normal text

    pushLine(`Paid (${receiptData.paymentMethod || 'Cash'}): $${tendered}`);
    if (Number(change) > 0) {
      pushLine(`Change Due: $${change}`);
    }

    pushLine(divider);

    // Center Align Footer (ESC a 1)
    pushBytes(0x1B, 0x61, 0x01);
    if (settings.footer_text) {
      pushLine(settings.footer_text);
    }
    if (settings.legal_text) {
      pushLine(settings.legal_text);
    }
    pushLine('*** PeakPOS Intelligent POS ***');

    // Feed lines before cut (ESC d 4)
    pushBytes(0x1B, 0x64, 0x04);

    // Cut Paper (GS V 66 0)
    if (options.cutPaper) {
      pushBytes(0x1D, 0x56, 0x42, 0x00);
    }

    return new Uint8Array(bytes);
  }

  /**
   * Silently Print Receipt
   * Sends raw ESC/POS bytes directly to WebUSB / WebSerial endpoint if connected;
   * otherwise falls back to standard window.print().
   */
  async printReceiptSilently(receiptData, settings = {}) {
    const rawData = this.buildEscPosCommands(receiptData, settings, { kickDrawer: true, cutPaper: true });

    // 1. Try WebUSB if device is open
    if (this.usbDevice && this.usbDevice.opened) {
      try {
        // Endpoint 1 is standard bulk OUT for thermal printers
        await this.usbDevice.transferOut(1, rawData);
        this.playScanSuccess();
        return { success: true, mode: 'silent_usb' };
      } catch (err) {
        console.warn('USB transfer failed, falling back to serial/standard:', err);
      }
    }

    // 2. Try WebSerial if open
    if (this.serialWriter) {
      try {
        await this.serialWriter.write(rawData);
        this.playScanSuccess();
        return { success: true, mode: 'silent_serial' };
      } catch (err) {
        console.warn('Serial write failed, falling back to standard print:', err);
      }
    }

    // 3. Fallback: Browser Print
    window.print();
    return { success: true, mode: 'browser_print_fallback' };
  }

  /**
   * Pop / Kick Cash Drawer Directly
   */
  async kickCashDrawer() {
    this.playDrawerKickSound();
    const kickBytes = new Uint8Array([0x1B, 0x70, 0x00, 0x19, 0xFA]); // Standard ESC/POS pulse

    if (this.usbDevice && this.usbDevice.opened) {
      try {
        await this.usbDevice.transferOut(1, kickBytes);
        return true;
      } catch (err) {
        console.warn('USB cash drawer kick failed:', err);
      }
    }
    if (this.serialWriter) {
      try {
        await this.serialWriter.write(kickBytes);
        return true;
      } catch (err) {
        console.warn('Serial cash drawer kick failed:', err);
      }
    }
    return false;
  }
}

export const escpos = new EscPosDriver();
export default escpos;
