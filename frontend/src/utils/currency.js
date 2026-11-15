// frontend/src/utils/currency.js

export function getCurrencySymbol() {
  return localStorage.getItem('currency_symbol') || 'Rs.';
}

export function getCurrencyCode() {
  return localStorage.getItem('currency_code') || 'PKR';
}

export function setStoreCurrency(code, symbol) {
  if (code) localStorage.setItem('currency_code', code);
  if (symbol) localStorage.setItem('currency_symbol', symbol);
  window.dispatchEvent(new CustomEvent('currency-changed', {
    detail: { code, symbol }
  }));
}

export function formatPrice(amount, symbol = null) {
  const val = Number(amount) || 0;
  const currSym = symbol !== null ? symbol : getCurrencySymbol();
  return `${currSym} ${val.toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })}`;
}

export default {
  getCurrencySymbol,
  getCurrencyCode,
  setStoreCurrency,
  formatPrice
};
