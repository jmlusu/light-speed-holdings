import { defineConfig, type Plugin } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

/* Dev-only enquiry stub: lets local/demo mailers succeed with HTTP 201 without
   hitting the live worker (128:8787). configureServer runs only in `vite dev`,
   never in `vite build`/preview — so this is production-gated by construction. */
const devEnquiryStub = (): Plugin => ({
  name: 'dev-enquiry-stub',
  apply: 'serve',
  configureServer(server) {
    server.middlewares.use('/api/enquiry', (req, res, next) => {
      if (req.method !== 'POST') return next();
      res.statusCode = 201;
      res.setHeader('Content-Type', 'application/json');
      res.end(
        JSON.stringify({
          ok: true,
          id: 'dev-stub-' + Date.now(),
          note: 'Dev-only stub — no email dispatched'
        })
      );
    });
  }
});

export default defineConfig({
  plugins: [react(), tailwindcss(), devEnquiryStub()],
  define: {
    __TURNSTILE_SITE_KEY__: JSON.stringify(
      process.env.TURNSTILE_SITE_KEY ?? process.env.VITE_TURNSTILE_SITE_KEY ?? ''
    )
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: true,
    proxy: {
      '/api': 'http://127.0.0.1:8787'
    }
  }
});
