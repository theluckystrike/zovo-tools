const CACHE_NAME = 'gear-calc-v1.0.1';
const STATIC_CACHE = 'static-gear-v1.0.1';
const RUNTIME_CACHE = 'runtime-gear-v1.0.1';
const DYNAMIC_CACHE = 'dynamic-gear-v1.0.1';

// Critical resources for immediate caching
const CRITICAL_URLS = [
  './',
  './index.html',
  './manifest.json'
];

// Font resources
const FONT_URLS = [
  'https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2',
  'https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuOKfAZ9hiA.woff2'
];

// Performance configuration
const PERF_CONFIG = {
  maxCacheAge: 86400000, // 24 hours
  staleWhileRevalidate: 3600000, // 1 hour
  maxEntries: 100,
  purgeInterval: 604800000 // 7 days
};

self.addEventListener('install', event => {
  console.log('[SW] Installing gear ratio calculator service worker v1.0.1');
  event.waitUntil(
    Promise.all([
      caches.open(STATIC_CACHE).then(cache => {
        console.log('[SW] Caching critical resources');
        return cache.addAll(CRITICAL_URLS);
      }),
      caches.open(RUNTIME_CACHE).then(cache => {
        console.log('[SW] Pre-caching fonts');
        return cache.addAll(FONT_URLS.filter(url => url));
      })
    ]).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  console.log('[SW] Activating gear ratio calculator service worker v1.0.1');
  event.waitUntil(
    Promise.all([
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE &&
                cacheName !== RUNTIME_CACHE &&
                cacheName !== DYNAMIC_CACHE) {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      self.clients.claim()
    ])
  );
});

self.addEventListener('fetch', event => {
  const {request} = event;
  const url = new URL(request.url);

  if (request.method !== 'GET') return;
  if (!url.protocol.startsWith('http')) return;

  // Handle different resource types
  if (url.pathname.endsWith('.html') || url.pathname === '/' || url.pathname.endsWith('/')) {
    event.respondWith(staleWhileRevalidateStrategy(request, STATIC_CACHE));
  } else if (url.pathname.endsWith('.css') || url.pathname.endsWith('.js')) {
    event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
  } else if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(cacheFirstStrategy(request, RUNTIME_CACHE, 31536000000));
  } else if (url.pathname.match(/\.(png|jpg|jpeg|webp|svg|ico|gif)$/)) {
    event.respondWith(cacheFirstStrategy(request, DYNAMIC_CACHE));
  } else if (url.hostname === 'quickchart.io' || url.hostname === 'www.youtube.com') {
    event.respondWith(networkFirstStrategy(request, DYNAMIC_CACHE));
  } else {
    event.respondWith(networkFirstStrategy(request, RUNTIME_CACHE));
  }
});

async function staleWhileRevalidateStrategy(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);

  const fetchPromise = fetch(request).then(response => {
    if (response && response.status === 200) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(error => {
    console.log('[SW] Network failed, serving cached version:', error);
    return cachedResponse;
  });

  return cachedResponse || fetchPromise;
}

async function cacheFirstStrategy(request, cacheName, maxAge = PERF_CONFIG.maxCacheAge) {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);

  if (cachedResponse) {
    const cachedDate = new Date(cachedResponse.headers.get('date') || Date.now());
    if (Date.now() - cachedDate.getTime() < maxAge) {
      return cachedResponse;
    }
  }

  try {
    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.status === 200) {
      await cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed, serving stale cache:', error);
    return cachedResponse || new Response('Offline', {
      status: 408,
      statusText: 'Request Timeout - Offline'
    });
  }
}

async function networkFirstStrategy(request, cacheName) {
  const cache = await caches.open(cacheName);

  try {
    const networkResponse = await fetch(request);
    if (networkResponse && networkResponse.status === 200) {
      await cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed, trying cache:', error);
    const cachedResponse = await cache.match(request);
    return cachedResponse || new Response('Offline', {
      status: 408,
      statusText: 'Request Timeout - Offline'
    });
  }
}

// Background sync
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(performBackgroundSync());
  }
});

async function performBackgroundSync() {
  try {
    console.log('[SW] Performing background sync for gear ratio calculator');
    const cache = await caches.open(STATIC_CACHE);
    await Promise.allSettled(
      CRITICAL_URLS.map(url => fetch(url).then(response => {
        if (response && response.status === 200) {
          return cache.put(url, response);
        }
      }))
    );
  } catch (error) {
    console.log('[SW] Background sync failed:', error);
  }
}

console.log('[SW] Gear ratio calculator service worker v1.0.1 loaded successfully');