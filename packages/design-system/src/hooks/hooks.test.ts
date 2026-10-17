import { describe, it, expect, vi } from 'vitest';
import { useTheme } from './useTheme';
import { useMediaQuery } from './useMediaQuery';
import { useReducedMotion, getMotionProps } from './useReducedMotion';
import { renderHook, act } from '@testing-library/react';

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock matchMedia
const matchMediaMock = vi.fn();
Object.defineProperty(window, 'matchMedia', { value: matchMediaMock });

describe('useTheme', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
    document.documentElement.classList.remove('dark');
  });

  it('returns dark theme by default', () => {
    const { result } = renderHook(() => useTheme());
    expect(result.current[0]).toBe('dark');
  });

  it('reads from localStorage', () => {
    localStorageMock.getItem.mockReturnValue('light');
    const { result } = renderHook(() => useTheme());
    expect(result.current[0]).toBe('light');
  });

  it('toggles theme', () => {
    const { result } = renderHook(() => useTheme());
    act(() => {
      result.current[1](); // toggleTheme
    });
    expect(result.current[0]).toBe('light');
  });

  it('sets explicit theme', () => {
    const { result } = renderHook(() => useTheme());
    act(() => {
      result.current[2]('light'); // setThemeExplicit
    });
    expect(result.current[0]).toBe('light');
  });
});

describe('useMediaQuery', () => {
  let mediaQueryList: MediaQueryList;

  beforeEach(() => {
    mediaQueryList = {
      matches: false,
      media: '',
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
      dispatchEvent: vi.fn(),
    } as unknown as MediaQueryList;
    matchMediaMock.mockReturnValue(mediaQueryList);
  });

  it('returns matches value', () => {
    mediaQueryList.matches = true;
    const { result } = renderHook(() => useMediaQuery('(min-width: 640px)'));
    expect(result.current).toBe(true);
  });

  it('adds event listener', () => {
    renderHook(() => useMediaQuery('(min-width: 640px)'));
    expect(mediaQueryList.addEventListener).toHaveBeenCalled();
  });
});

describe('useReducedMotion', () => {
  let mediaQueryList: MediaQueryList;

  beforeEach(() => {
    mediaQueryList = {
      matches: false,
      media: '',
      onchange: null,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn(),
      dispatchEvent: vi.fn(),
    } as unknown as MediaQueryList;
    matchMediaMock.mockReturnValue(mediaQueryList);
  });

  it('returns reduced motion preference', () => {
    mediaQueryList.matches = true;
    const { result } = renderHook(() => useReducedMotion());
    expect(result.current).toBe(true);
  });

  it('getMotionProps returns reduced motion styles', () => {
    const props = getMotionProps(true);
    expect(props.style?.animationDuration).toBe('0.01ms');
    expect(props.style?.transitionDuration).toBe('0.01ms');
  });

  it('getMotionProps returns empty for normal motion', () => {
    const props = getMotionProps(false);
    expect(props).toEqual({});
  });
});
