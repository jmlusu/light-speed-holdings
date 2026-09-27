import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'path';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  define: {
    __TURNSTILE_SITE_KEY__: JSON.stringify(
      process.env.TURNSTILE_SITE_KEY ?? process.env.VITE_TURNSTILE_SITE_KEY ?? ''
    )
  },
  build: {
    rollupOptions: {
      output: {
        // ADR-036: three.js must ship as its own lazy chunk, never in the entry bundle.
        manualChunks(id: string) {
          const normalized = id.split(path.sep).join('/');
          if (normalized.includes('node_modules/three')) return 'three';
          return undefined;
        },
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: true,
  }
});
