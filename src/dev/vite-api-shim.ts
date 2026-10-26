// Dev-only API shim. `vite` serves the website but not Vercel functions, so a
// local form submission used to hit 404. This mounts the real handlers from
// `api/` through Vite's SSR pipeline, which means local testing exercises the
// same code that runs in production: validation, rate limit, Turnstile
// siteverify, and the email step (aliased to a recording stub in serve mode).
//
// This file lives under src/ rather than scripts/ on purpose: vite.config.ts
// imports it statically, and .vercelignore strips scripts/ from the upload, so
// an import of a stripped file fails the Vercel build. Nothing here reaches the
// browser bundle: the plugin is `apply: 'serve'` and no app module imports it.
import type { IncomingMessage, ServerResponse } from 'node:http';
import type { Plugin, ViteDevServer } from 'vite';

interface ShimRoute {
  method: 'GET' | 'POST';
  path: string;
  module: string;
  exportName: 'GET' | 'POST';
}

const ROUTES: ShimRoute[] = [
  { method: 'POST', path: '/api/enquiry', module: '/api/enquiry.ts', exportName: 'POST' },
  { method: 'GET', path: '/api/ping', module: '/api/ping.ts', exportName: 'GET' },
];

async function readBody(req: IncomingMessage): Promise<Uint8Array | undefined> {
  if (req.method === 'GET' || req.method === 'HEAD') return undefined;
  const chunks: Buffer[] = [];
  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}

function toHeaders(req: IncomingMessage): Headers {
  const headers = new Headers();
  for (const [key, value] of Object.entries(req.headers)) {
    if (typeof value === 'string') headers.set(key, value);
    else if (Array.isArray(value)) headers.set(key, value.join(','));
  }
  // Vercel always provides a client IP; locally everything shares one bucket.
  if (!headers.has('x-forwarded-for')) headers.set('x-forwarded-for', '127.0.0.1');
  return headers;
}

async function dispatch(server: ViteDevServer, route: ShimRoute, req: IncomingMessage, res: ServerResponse) {
  const mod = (await server.ssrLoadModule(route.module)) as Record<string, unknown>;
  const handler = mod[route.exportName];
  if (typeof handler !== 'function') {
    res.statusCode = 500;
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ error: { code: 'dev_shim_missing_handler', module: route.module } }));
    return;
  }

  const body = await readBody(req);
  const url = `http://${req.headers.host ?? 'localhost'}${req.url ?? route.path}`;
  const request = new Request(url, {
    method: route.method,
    headers: toHeaders(req),
    // Copy into a plain Uint8Array: Node's Buffer is Uint8Array<ArrayBufferLike>,
    // which lib.dom's BodyInit does not accept.
    body: body && body.length > 0 ? new Uint8Array(body) : undefined,
  });

  const response = (await handler(request)) as Response;
  const payload = Buffer.from(await response.arrayBuffer());
  res.statusCode = response.status;
  response.headers.forEach((value, key) => res.setHeader(key, value));
  res.end(payload);

  let detail = '';
  if (payload.length > 0) {
    try {
      const parsed = JSON.parse(payload.toString('utf8')) as { error?: { code?: string; message?: string } };
      detail = parsed.error?.message ?? parsed.error?.code ?? '';
    } catch {
      detail = '';
    }
  }
  console.log(`[dev-api] ${route.method} ${route.path} -> ${response.status}${detail ? ` (${detail})` : ''}`);
}

export function devApiShim(): Plugin {
  return {
    name: 'lightspeed-dev-api-shim',
    apply: 'serve',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const path = (req.url ?? '').split('?')[0];
        const route = ROUTES.find((candidate) => candidate.path === path);
        if (!route) {
          next();
          return;
        }
        if (req.method !== route.method) {
          res.statusCode = 405;
          res.setHeader('Allow', route.method);
          res.end();
          return;
        }
        dispatch(server, route, req, res).catch((error: unknown) => {
          console.error('[dev-api] handler crashed:', error);
          if (!res.headersSent) {
            res.statusCode = 500;
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ error: { code: 'dev_shim_error' } }));
          }
        });
      });
      server.config.logger.info('[dev-api] shim active for /api/enquiry and /api/ping (email is recorded, not sent)');
    },
  };
}
