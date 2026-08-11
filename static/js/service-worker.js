/* ============================================================
   Service Worker — CEO Dashboard (Offline Support)
   Strategy: Cache-first for static assets, network-first for API
   ============================================================ */

const CACHE_NAME = "dashboard-v1";
const STATIC_ASSETS = [
  "/",
  "/index.html",
  "/mobile.html",
  "/css/style.css",
  "/css/mobile.css",
  "/js/app.js",
  "/js/mobile.js",
];

const API_CACHE_NAME = "api-v1";
const API_CACHE_TTL = 30 * 1000; // 30 seconds for KPI data

// ── Install ─────────────────────────────────────────────────

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("[SW] Pre-caching static assets");
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// ── Activate ────────────────────────────────────────────────

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME && name !== API_CACHE_NAME)
          .map((name) => {
            console.log("[SW] Deleting old cache:", name);
            return caches.delete(name);
          })
      );
    })
  );
  self.clients.claim();
});

// ── Fetch Strategy ──────────────────────────────────────────

self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API requests: network-first with cache fallback
  if (url.pathname.startsWith("/api/")) {
    event.respondWith(networkFirstWithCache(request, API_CACHE_NAME, API_CACHE_TTL));
    return;
  }

  // Static assets: cache-first
  event.respondWith(cacheFirst(request, CACHE_NAME));
});

// ── Cache-First Strategy (static assets) ────────────────────

async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Return offline fallback if available
    const offlineFallback = await caches.match("/");
    return offlineFallback || new Response("Offline", { status: 503 });
  }
}

// ── Network-First Strategy (API) ────────────────────────────

async function networkFirstWithCache(request, cacheName, ttl) {
  try {
    const response = await fetch(request);

    if (response.ok) {
      // Cache successful API responses
      const cache = await caches.open(cacheName);
      const cloned = response.clone();
      // Store with timestamp for TTL check
      const responseWithMeta = new Response(await cloned.blob(), {
        status: cloned.status,
        statusText: cloned.statusText,
        headers: cloned.headers,
      });
      cache.put(request, responseWithMeta);
    }

    return response;
  } catch (error) {
    // Network failed, try cache
    const cached = await caches.match(request);
    if (cached) {
      // Add header to indicate stale data
      const staleResponse = new Response(await cached.blob(), {
        status: cached.status,
        statusText: cached.statusText,
        headers: {
          ...Object.fromEntries(cached.headers.entries()),
          "X-From-Cache": "true",
          "X-Cache-Time": new Date().toISOString(),
        },
      });
      return staleResponse;
    }

    // No cache, no network
    return new Response(
      JSON.stringify({
        error: "offline",
        message: "No network connection and no cached data available",
      }),
      {
        status: 503,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}

// ── Background Sync ─────────────────────────────────────────

self.addEventListener("sync", (event) => {
  if (event.tag === "sync-pending-actions") {
    event.waitUntil(syncPendingActions());
  }
});

async function syncPendingActions() {
  // Open IndexedDB to get pending actions
  const db = await openDB();
  const tx = db.transaction("pending-actions", "readwrite");
  const store = tx.objectStore("pending-actions");
  const request = store.getAll();

  return new Promise((resolve, reject) => {
    request.onsuccess = async () => {
      const actions = request.result;
      if (actions.length === 0) {
        resolve();
        return;
      }

      try {
        const response = await fetch("/api/mobile/sync", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            last_sync_at: localStorage.getItem("last_sync_at") || null,
            pending_actions: actions.map((a) => ({
              client_id: a.id,
              type: a.type,
              target_id: a.target_id,
              queued_at: a.queued_at,
            })),
          }),
        });

        if (response.ok) {
          const result = await response.json();
          // Clear synced actions
          const clearTx = db.transaction("pending-actions", "readwrite");
          clearTx.objectStore("pending-actions").clear();
          localStorage.setItem("last_sync_at", result.synced_at);

          // Notify all clients of sync completion
          const clients = await self.clients.matchAll();
          clients.forEach((client) => {
            client.postMessage({
              type: "SYNC_COMPLETE",
              payload: result,
            });
          });
        }
      } catch (error) {
        console.error("[SW] Sync failed:", error);
      }

      resolve();
    };
    request.onerror = reject;
  });
}

// ── IndexedDB Helper ────────────────────────────────────────

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open("DashboardOffline", 1);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains("pending-actions")) {
        db.createObjectStore("pending-actions", {
          keyPath: "id",
          autoIncrement: true,
        });
      }
      if (!db.objectStoreNames.contains("cache")) {
        db.createObjectStore("cache", { keyPath: "key" });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

// ── Push Notification Handling ──────────────────────────────

self.addEventListener("push", (event) => {
  const data = event.data?.json() || {};

  const options = {
    body: data.notification?.body || "",
    icon: "/icons/icon-192.png",
    badge: "/icons/badge-72.png",
    data: data.data || {},
    tag: data.data?.type || "general",
    renotify: true,
    requireInteraction: data.data?.category === "urgent",
    actions: getActionsForType(data.data?.type),
  };

  event.waitUntil(
    self.registration.showNotification(
      data.notification?.title || "AI Company Builder",
      options
    )
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();

  const url = event.notification.data?.action_url || "/";
  const action = event.action;

  if (action === "approve" && event.notification.data?.request_id) {
    event.waitUntil(
      fetch(`/api/approvals/${event.notification.data.request_id}/approve`, {
        method: "POST",
      }).then(() => self.clients.openWindow(url))
    );
  } else if (action === "reject" && event.notification.data?.request_id) {
    event.waitUntil(
      fetch(`/api/approvals/${event.notification.data.request_id}/reject`, {
        method: "POST",
      }).then(() => self.clients.openWindow(url))
    );
  } else {
    event.waitUntil(self.clients.openWindow(url));
  }
});

function getActionsForType(type) {
  switch (type) {
    case "approval_needed":
      return [
        { action: "approve", title: "Approve" },
        { action: "reject", title: "Reject" },
      ];
    case "escalation":
      return [{ action: "view", title: "View" }];
    default:
      return [];
  }
}
