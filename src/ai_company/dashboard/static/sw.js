/* ═══════════════════════════════════════════════════════════════
   J.A.R.V.I.S. Control Plane — Service Worker
   Offline-first caching, background sync for queued actions.
   Issue #41 — Wire offline-first PWA into served dashboard.
   ═══════════════════════════════════════════════════════════════ */

const CACHE_VERSION = 'jarvis-v1';
const CACHE_STATIC = `${CACHE_VERSION}-static`;
const CACHE_API    = `${CACHE_VERSION}-api`;
const CACHE_HTML   = `${CACHE_VERSION}-html`;

/* ── App shell: precache on install ─────────────────────────── */
const PRECACHE_URLS = [
  '/',
  '/agents',
  '/tasks',
  '/kpis',
  '/costs',
  '/escalations',
  '/command-center',
  '/mission-control',
  '/finance',
  '/onboarding',
  '/org-chart',
  '/static/css/control-plane-theme.css',
  '/static/css/style.css',
  '/static/css/command-bar.css',
  '/static/js/app.js',
  '/static/js/command-bar-service.js',
  '/static/js/command-bar.js',
  '/static/manifest.json',
];

/* ── URL classification helpers ─────────────────────────────── */

/** Static assets: CSS, JS, images, fonts, SVGs */
function isStaticAsset(url) {
  return /\.(css|js|woff2?|ttf|eot|svg|png|jpg|gif|ico)(\?|$)/.test(url.pathname)
    || url.pathname.startsWith('/static/icons/');
}

/** API calls */
function isApiCall(url) {
  return url.pathname.startsWith('/api/');
}

/** HTML navigation requests */
function isNavigation(request) {
  return request.mode === 'navigate';
}

/* ═══ INSTALL ══════════════════════════════════════════════════ */

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_STATIC)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

/* ═══ ACTIVATE ═════════════════════════════════════════════════ */

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(
        names
          .filter((name) => !name.startsWith(CACHE_VERSION))
          .map((name) => caches.delete(name))
      )
    ).then(() => self.clients.claim())
  );
});

/* ═══ FETCH ════════════════════════════════════════════════════ */

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET for caching strategies (POST/PUT/PATCH/DELETE go
  // straight to network — the offline-sync module handles queuing).
  if (request.method !== 'GET') return;

  // Skip cross-origin (CDN scripts, etc.)
  if (url.origin !== self.location.origin) return;

  // ── API calls: network-first with short-lived cache fallback ─
  if (isApiCall(url)) {
    event.respondWith(networkFirst(request, CACHE_API, 60));
    return;
  }

  // ── HTML pages: stale-while-revalidate ──────────────────────
  if (isNavigation(request)) {
    event.respondWith(staleWhileRevalidate(request, CACHE_HTML, 300));
    return;
  }

  // ── Static assets: cache-first ──────────────────────────────
  if (isStaticAsset(url)) {
    event.respondWith(cacheFirst(request, CACHE_STATIC));
    return;
  }

  // ── Everything else: network-first ──────────────────────────
  event.respondWith(networkFirst(request, CACHE_API, 60));
});

/* ═══ BACKGROUND SYNC ══════════════════════════════════════════ */

self.addEventListener('sync', (event) => {
  if (event.tag === 'jarvis-offline-queue') {
    event.waitUntil(replayQueuedActions());
  }
});

/**
 * Replay all queued offline actions from IndexedDB.
 * Each entry has: { id, url, method, headers, body, timestamp }
 */
async function replayQueuedActions() {
  const db = await openQueueDB();
  const tx = db.transaction('actions', 'readwrite');
  const store = tx.objectStore('actions');
  const all = await idbRequest(store.getAll());

  const results = [];
  for (const action of all) {
    try {
      const res = await fetch(action.url, {
        method: action.method,
        headers: action.headers,
        body: action.body,
      });
      if (res.ok) {
        store.delete(action.id);
        results.push({ id: action.id, status: 'replayed' });
      } else {
        results.push({ id: action.id, status: 'failed', http: res.status });
      }
    } catch (_e) {
      // Still offline — leave in queue for next sync attempt.
      results.push({ id: action.id, status: 'pending' });
    }
  }

  await idbRequest(tx.done);

  // Notify all open clients of the sync result.
  const clients = await self.clients.matchAll();
  for (const client of clients) {
    client.postMessage({
      type: 'SYNC_COMPLETE',
      results,
    });
  }
}

/* ═══ CACHE STRATEGIES ════════════════════════════════════════ */

/** Cache-first: serve from cache, fall back to network + cache. */
async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;

  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(cacheName);
    cache.put(request, response.clone());
  }
  return response;
}

/** Network-first: try network, fall back to cache (optionally stale). */
async function networkFirst(request, cacheName, maxAgeSeconds) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch (_e) {
    const cached = await caches.match(request);
    if (cached) return cached;
    // Return a basic offline page for navigation requests.
    if (request.mode === 'navigate') {
      return new Response(offlineHTML(), {
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
        status: 503,
      });
    }
    return new Response('{"error":"offline"}', {
      status: 503,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}

/** Stale-while-revalidate: serve cache immediately, update in background. */
async function staleWhileRevalidate(request, cacheName, maxAgeSeconds) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);

  const networkPromise = fetch(request).then((response) => {
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(() => cached);

  return cached || networkPromise;
}

/* ═══ INDEXEDDB HELPERS ════════════════════════════════════════ */

function openQueueDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('jarvis-offline-queue', 1);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains('actions')) {
        db.createObjectStore('actions', { keyPath: 'id', autoIncrement: true });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function idbRequest(request) {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

/* ═══ OFFLINE FALLBACK HTML ════════════════════════════════════ */

function offlineHTML() {
  return `<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>J.A.R.V.I.S. — Offline</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #070b14; color: #e2e8f0;
      font-family: system-ui, -apple-system, sans-serif;
      display: flex; align-items: center; justify-content: center;
      min-height: 100vh; text-align: center;
    }
    .container { max-width: 400px; padding: 2rem; }
    h1 { font-size: 1.5rem; margin-bottom: 0.5rem; color: #22d3ee; }
    p { color: #94a3b8; font-size: 0.875rem; line-height: 1.6; }
    .icon { font-size: 3rem; margin-bottom: 1rem; }
  </style>
</head>
<body>
  <div class="container">
    <div class="icon">⚡</div>
    <h1>J.A.R.V.I.S. Offline</h1>
    <p>You are currently offline. Cached data is available.
       Queued actions will sync when connectivity is restored.</p>
  </div>
</body>
</html>`;
}
