import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

// Cloudflare site keys are public, but we refuse anything that is not a bare
// key: values containing '=', whitespace, or pasted env blocks (which can
// embed TURNSTILE_SECRET_KEY) must never be baked into the client bundle.
const TURNSTILE_SITE_KEY_RE = /^[0-9a-zA-Z._-]{10,120}$/;

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const rawSiteKey = env.VITE_TURNSTILE_SITE_KEY ?? '';
  const turnstileSiteKey = TURNSTILE_SITE_KEY_RE.test(rawSiteKey) ? rawSiteKey : '';

  return {
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    define: {
      __TURNSTILE_SITE_KEY__: JSON.stringify(turnstileSiteKey),
    },
    server: {
      host: '0.0.0.0',
      port: 3000,
      allowedHosts: true,
    },
  };
});
