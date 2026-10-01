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

export function useTurnstile(action: string, onToken: (token: string) => void) {
  const [container, setContainer] = useState<HTMLDivElement | null>(null);
  const containerRef = useCallback((node: HTMLDivElement | null) => {
    setContainer(node);
  }, []);
  const siteKey = (__TURNSTILE_SITE_KEY__ || import.meta.env.VITE_TURNSTILE_SITE_KEY) as
    | string
    | undefined;

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
