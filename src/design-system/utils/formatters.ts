/**
 * Formatters Utility
 *
 * Common formatting functions for numbers, dates, currency, etc.
 */

export const formatters = {
  /**
   * Format number with commas
   */
  number: (value: number): string => {
    return value.toLocaleString('en-US');
  },

  /**
   * Format currency (MWK)
   */
  currencyMWK: (value: number): string => {
    return `MWK ${value.toLocaleString('en-US')}`;
  },

  /**
   * Format currency (USD)
   */
  currencyUSD: (value: number): string => {
    return `$${value.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
  },

  /**
   * Format percentage
   */
  percentage: (value: number, decimals = 1): string => {
    return `${value.toFixed(decimals)}%`;
  },

  /**
   * Format date (ISO string to readable)
   */
  date: (isoString: string): string => {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  },

  /**
   * Format date time
   */
  dateTime: (isoString: string): string => {
    const date = new Date(isoString);
    return date.toLocaleString('en-GB', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  },

  /**
   * Format relative time (e.g., "2 hours ago")
   */
  relativeTime: (isoString: string): string => {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return formatters.date(isoString);
  },

  /**
   * Truncate text with ellipsis
   */
  truncate: (text: string, maxLength: number): string => {
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength - 3) + '...';
  },

  /**
   * Format file size
   */
  fileSize: (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
  },

  /**
   * Format metric value with unit
   */
  metric: (value: number, unit: string, decimals = 1): string => {
    return `${value.toFixed(decimals)} ${unit}`;
  },
};
