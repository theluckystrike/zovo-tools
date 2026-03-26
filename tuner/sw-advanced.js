// Advanced Service Worker v4.0 - tuner
// Intelligent caching with network-first, cache-first, and stale-while-revalidate strategies

const CACHE_VERSION = '4.0.1774512394';
const CACHE_PREFIX = 'zovo-tuner';
const STATIC_CACHE = CACHE_PREFIX + '-static-' + CACHE_VERSION;
const DYNAMIC_CACHE = CACHE_PREFIX + '-dynamic-' + CACHE_VERSION;
const IMAGE_CACHE = CACHE_PREFIX + '-images-' + CACHE_VERSION;
const API_CACHE = CACHE_PREFIX + '-api-' + CACHE_VERSION;

// Cache duration in milliseconds
const CACHE_DURATIONS = {
  static: 30 * 24 * 60 * 60 * 1000,    // 30 days
  dynamic: 7 * 24 * 60 * 60 * 1000,    // 7 days
  images: 60 * 24 * 60 * 60 * 1000,    // 60 days
  api: 60 * 60 * 1000                  // 1 hour
};

// Static assets to precache
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/css/main.css',
  '/js/main.js',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// API endpoints to cache
const CACHEABLE_APIS = [
  '/api/calculate',
  '/api/rates',
  '/api/data'
];

// Install event - aggressive precaching
self.addEventListener('install', event => {
  console.log('[SW] Installing service worker for tuner');

  event.waitUntil(
    Promise.all([
      // Cache static assets
      caches.open(STATIC_CACHE).then(cache => {
        console.log('[SW] Precaching static assets');
        return cache.addAll(STATIC_ASSETS.map(url => new Request(url, { cache: 'reload' })));
      }),

      // Initialize other caches
      caches.open(DYNAMIC_CACHE),
      caches.open(IMAGE_CACHE),
      caches.open(API_CACHE)
    ]).then(() => {
      console.log('[SW] Installation complete');
      return self.skipWaiting();
    }).catch(error => {
      console.error('[SW] Installation failed:', error);
    })
  );
});

// Activate event - cleanup old caches
self.addEventListener('activate', event => {
  console.log('[SW] Activating service worker');

  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(name => name.startsWith(CACHE_PREFIX) &&
                           !name.includes(CACHE_VERSION))
            .map(name => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      }),

      // Claim all clients
      self.clients.claim()
    ]).then(() => {
      console.log('[SW] Activation complete');
    })
  );
});

// Fetch event - intelligent caching strategies
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension requests
  if (url.protocol === 'chrome-extension:') {
    return;
  }

  // Route requests to appropriate cache strategies
  if (isStaticAsset(url)) {
    event.respondWith(handleStaticAsset(request));
  } else if (isImage(url)) {
    event.respondWith(handleImage(request));
  } else if (isAPI(url)) {
    event.respondWith(handleAPI(request));
  } else {
    event.respondWith(handleDynamic(request));
  }
});

// Static asset strategy: Cache First with background update
async function handleStaticAsset(request) {
  try {
    const cache = await caches.open(STATIC_CACHE);
    const cachedResponse = await cache.match(request);

    if (cachedResponse && !isExpired(cachedResponse, CACHE_DURATIONS.static)) {
      // Serve from cache and update in background
      updateCache(request, cache);
      return cachedResponse;
    }

    // Fetch from network and cache
    const networkResponse = await fetch(request);
    if (networkResponse.status === 200) {
      await cache.put(request, networkResponse.clone());
    }
    return networkResponse;

  } catch (error) {
    console.error('[SW] Static asset error:', error);
    // Try to serve from cache as fallback
    const cache = await caches.open(STATIC_CACHE);
    return await cache.match(request) || new Response('Offline', { status: 503 });
  }
}

// Image strategy: Cache First with WebP conversion
async function handleImage(request) {
  try {
    const cache = await caches.open(IMAGE_CACHE);
    const cachedResponse = await cache.match(request);

    if (cachedResponse && !isExpired(cachedResponse, CACHE_DURATIONS.images)) {
      return cachedResponse;
    }

    // Try WebP version first if supported
    const supportsWebP = request.headers.get('Accept')?.includes('image/webp');
    if (supportsWebP && !request.url.includes('.webp')) {
      const webpUrl = request.url.replace(/\.(jpg|jpeg|png)$/i, '.webp');
      try {
        const webpResponse = await fetch(webpUrl);
        if (webpResponse.status === 200) {
          await cache.put(request, webpResponse.clone());
          return webpResponse;
        }
      } catch (e) {
        // WebP not available, continue with original
      }
    }

    const networkResponse = await fetch(request);
    if (networkResponse.status === 200) {
      await cache.put(request, networkResponse.clone());
    }
    return networkResponse;

  } catch (error) {
    console.error('[SW] Image error:', error);
    return new Response('Image not available offline', { status: 503 });
  }
}

// API strategy: Network First with Stale While Revalidate
async function handleAPI(request) {
  try {
    const cache = await caches.open(API_CACHE);

    // Try network first
    const networkResponse = await fetch(request, { timeout: 3000 });
    if (networkResponse.status === 200) {
      await cache.put(request, networkResponse.clone());
      return networkResponse;
    }

    // Fall back to cache
    const cachedResponse = await cache.match(request);
    return cachedResponse || new Response('API unavailable', { status: 503 });

  } catch (error) {
    console.error('[SW] API error:', error);
    // Serve from cache
    const cache = await caches.open(API_CACHE);
    const cachedResponse = await cache.match(request);
    return cachedResponse || new Response(
      JSON.stringify({ error: 'Offline', cached: false }),
      { headers: { 'Content-Type': 'application/json' }, status: 503 }
    );
  }
}

// Dynamic content strategy: Stale While Revalidate
async function handleDynamic(request) {
  try {
    const cache = await caches.open(DYNAMIC_CACHE);
    const cachedResponse = await cache.match(request);

    // Serve cached version immediately if available
    if (cachedResponse) {
      // Update cache in background
      fetch(request).then(response => {
        if (response.status === 200) {
          cache.put(request, response);
        }
      }).catch(e => console.log('[SW] Background update failed:', e));

      return cachedResponse;
    }

    // No cache, fetch from network
    const networkResponse = await fetch(request);
    if (networkResponse.status === 200) {
      await cache.put(request, networkResponse.clone());
    }
    return networkResponse;

  } catch (error) {
    console.error('[SW] Dynamic content error:', error);
    return new Response('Content unavailable offline', { status: 503 });
  }
}

// Utility functions
function isStaticAsset(url) {
  return url.pathname.match(/\.(css|js|woff2?|eot|ttf)$/) ||
         url.pathname === '/' ||
         url.pathname.endsWith('.html') ||
         url.pathname.includes('/manifest.json');
}

function isImage(url) {
  return url.pathname.match(/\.(jpg|jpeg|png|gif|webp|svg|ico)$/);
}

function isAPI(url) {
  return CACHEABLE_APIS.some(api => url.pathname.startsWith(api)) ||
         url.pathname.startsWith('/api/');
}

function isExpired(response, maxAge) {
  const dateHeader = response.headers.get('date');
  if (!dateHeader) return true;

  const responseTime = new Date(dateHeader).getTime();
  return (Date.now() - responseTime) > maxAge;
}

async function updateCache(request, cache) {
  try {
    const response = await fetch(request);
    if (response.status === 200) {
      await cache.put(request, response);
    }
  } catch (e) {
    console.log('[SW] Background update failed:', e);
  }
}

// Background sync for analytics and offline data
self.addEventListener('sync', event => {
  if (event.tag === 'analytics-sync') {
    event.waitUntil(syncAnalytics());
  } else if (event.tag === 'calculation-sync') {
    event.waitUntil(syncCalculations());
  }
});

async function syncAnalytics() {
  try {
    const analyticsData = await getStoredData('analytics-queue');
    for (const data of analyticsData) {
      await fetch('/api/analytics', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
      });
    }
    await clearStoredData('analytics-queue');
  } catch (error) {
    console.error('[SW] Analytics sync failed:', error);
  }
}

async function syncCalculations() {
  try {
    const calculations = await getStoredData('calculation-queue');
    for (const calc of calculations) {
      await fetch('/api/calculations', {
        method: 'POST',
        body: JSON.stringify(calc),
        headers: { 'Content-Type': 'application/json' }
      });
    }
    await clearStoredData('calculation-queue');
  } catch (error) {
    console.error('[SW] Calculation sync failed:', error);
  }
}

// IndexedDB utilities for offline storage
async function getStoredData(key) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('ZovoOfflineDB', 1);
    request.onsuccess = () => {
      const db = request.result;
      const transaction = db.transaction(['data'], 'readonly');
      const store = transaction.objectStore('data');
      const getRequest = store.get(key);

      getRequest.onsuccess = () => {
        resolve(getRequest.result?.data || []);
      };
      getRequest.onerror = () => reject(getRequest.error);
    };
    request.onerror = () => reject(request.error);
  });
}

async function clearStoredData(key) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('ZovoOfflineDB', 1);
    request.onsuccess = () => {
      const db = request.result;
      const transaction = db.transaction(['data'], 'readwrite');
      const store = transaction.objectStore('data');
      const deleteRequest = store.delete(key);

      deleteRequest.onsuccess = () => resolve();
      deleteRequest.onerror = () => reject(deleteRequest.error);
    };
    request.onerror = () => reject(request.error);
  });
}

// Push notification handling
self.addEventListener('push', event => {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body,
      icon: '/icons/icon-192x192.png',
      badge: '/icons/badge-72x72.png',
      vibrate: [100, 50, 100],
      data: data.data,
      actions: [
        {
          action: 'open',
          title: 'Open Calculator',
          icon: '/icons/open.png'
        },
        {
          action: 'dismiss',
          title: 'Dismiss',
          icon: '/icons/dismiss.png'
        }
      ]
    };

    event.waitUntil(
      self.registration.showNotification(data.title, options)
    );
  }
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

console.log('[SW] Advanced service worker for tuner loaded successfully');