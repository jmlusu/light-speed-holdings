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
      alias: [
        { find: '@', replacement: path.resolve(__dirname, './src') },
        {
          find: '@lightspeed/design-system/tokens',
          replacement: path.resolve(__dirname, './packages/design-system/src/tokens'),
        },
        {
          find: '@lightspeed/design-system',
          replacement: path.resolve(__dirname, './packages/design-system/src/index.ts'),
        },
        { find: '@lightspeed/data/company', replacement: path.resolve(__dirname, './data/company/registry.ts') },
        { find: '@lightspeed/data/metrics', replacement: path.resolve(__dirname, './data/metrics/registry.ts') },
        { find: '@lightspeed/data/capabilities', replacement: path.resolve(__dirname, './data/capabilities/registry.ts') },
        { find: '@lightspeed/data/solutions', replacement: path.resolve(__dirname, './data/solutions/registry.ts') },
        { find: '@lightspeed/data/use-cases', replacement: path.resolve(__dirname, './data/use-cases/registry.ts') },
        { find: '@lightspeed/data/sectors', replacement: path.resolve(__dirname, './data/sectors/registry.ts') },
        { find: '@lightspeed/data/insights', replacement: path.resolve(__dirname, './data/insights/registry.ts') },
        { find: '@lightspeed/data/faqs', replacement: path.resolve(__dirname, './data/faqs/registry.ts') },
        { find: '@lightspeed/data/claims', replacement: path.resolve(__dirname, './data/claims/registry.ts') },
        { find: '@lightspeed/data/governance', replacement: path.resolve(__dirname, './data/governance/registry.ts') },
        { find: '@lightspeed/data/media', replacement: path.resolve(__dirname, './data/media/registry.ts') },
        { find: '@lightspeed/data/ctas', replacement: path.resolve(__dirname, './data/ctas/registry.ts') },
      ],
    },
    define: {
      __TURNSTILE_SITE_KEY__: JSON.stringify(turnstileSiteKey),
    },
    server: {
      host: '0.0.0.0',
      port: 3000,
      allowedHosts: true,
    },
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            'vendor-react': ['react', 'react-dom', 'react-router-dom'],
            'vendor-ui': ['lucide-react', 'recharts', 'clsx', 'tailwind-merge'],
          },
        },
      },
    },
  };
});
