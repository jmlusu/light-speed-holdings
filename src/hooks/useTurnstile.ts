import { useCallback, useEffect, useState } from 'react';

const SCRIPT_SRC = 'https://challenges.cloudflare.com/turnstile/v0/api.js';

declare global {
  interface Window {
    turnstile?: {
      render: (container: HTMLElement, options: Record<string, unknown>) => string;
      reset: (widgetId?: string) => void;
    };
  }
}

let scriptLoaded = false;

// Mirrors vite.config.ts: reject malformed values (e.g. pasted env blocks that
// embed TURNSTILE_SECRET_KEY) so a bad .env line can never reach the widget.
const SITE_KEY_RE = /^[0-9a-zA-Z._-]{10,120}$/;

export function useTurnstile(action: string, onToken: (token: string) => void) {
  const [container, setContainer] = useState<HTMLDivElement | null>(null);
  const containerRef = useCallback((node: HTMLDivElement | null) => {
    setContainer(node);
  }, []);
  // Single source: vite.config.ts loadEnv -> pattern-checked define.
  // (No import.meta.env fallback: VITE_ vars are inlined as-is, which is how
  // a malformed .env value reached the bundle before.)
  const rawSiteKey = String(__TURNSTILE_SITE_KEY__ || '');
  const siteKey: string | undefined = SITE_KEY_RE.test(rawSiteKey) ? rawSiteKey : undefined;

  const reset = useCallback(() => {
    window.turnstile?.reset();
    onToken('');
  }, [onToken]);

  useEffect(() => {
    if (!siteKey || !container) return;

    const render = () => {
      if (typeof window.turnstile?.render !== 'function') return;
      window.turnstile.render(container, {
        sitekey: siteKey,
        action,
        callback: (token: string) => onToken(token)
      });
    };

    if (!scriptLoaded) {
      scriptLoaded = true;
      const script = document.createElement('script');
      script.src = SCRIPT_SRC;
      script.async = true;
      script.defer = true;
      script.onload = render;
      document.head.appendChild(script);
    } else {
      render();
    }

    return () => {
      window.turnstile?.reset();
    };
  }, [siteKey, onToken, action, container]);

  return { containerRef, siteKey, reset };
}
