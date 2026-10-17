import { describe, it, expect } from 'vitest';
import { cn } from '../utils/cn';
import { formatters } from '../utils/formatters';

describe('cn utility', () => {
  it('joins class names', () => {
    expect(cn('a', 'b', 'c')).toBe('a b c');
  });

  it('handles conditional classes', () => {
    expect(cn('base', true && 'conditional')).toBe('base conditional');
    expect(cn('base', false && 'conditional')).toBe('base');
  });

  it('merges tailwind classes', () => {
    expect(cn('p-4', 'p-2')).toBe('p-2');
  });
});

describe('formatters', () => {
  it('formats numbers', () => {
    expect(formatters.number(1000)).toBe('1,000');
    expect(formatters.number(1000000)).toBe('1,000,000');
  });

  it('formats currency MWK', () => {
    expect(formatters.currencyMWK(1000)).toBe('MWK 1,000');
  });

  it('formats currency USD', () => {
    expect(formatters.currencyUSD(1000)).toBe('$1,000');
    expect(formatters.currencyUSD(1000.5)).toBe('$1,001');
  });

  it('formats percentages', () => {
    expect(formatters.percentage(50)).toBe('50.0%');
    expect(formatters.percentage(33.33, 2)).toBe('33.33%');
  });

  it('formats dates', () => {
    const result = formatters.date('2026-01-15');
    expect(result).toContain('15');
    expect(result).toContain('Jan');
    expect(result).toContain('2026');
  });

  it('truncates text', () => {
    expect(formatters.truncate('hello world', 8)).toBe('hello...');
    expect(formatters.truncate('hi', 10)).toBe('hi');
  });

  it('formats file sizes', () => {
    expect(formatters.fileSize(0)).toBe('0 B');
    expect(formatters.fileSize(1024)).toBe('1 KB');
    expect(formatters.fileSize(1024 * 1024)).toBe('1 MB');
  });

  it('formats metrics', () => {
    expect(formatters.metric(42.5, 'ms')).toBe('42.5 ms');
    expect(formatters.metric(100, '%', 0)).toBe('100 %');
  });
});
