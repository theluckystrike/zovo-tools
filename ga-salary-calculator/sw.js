const CACHE_NAME = 'ga-salary-calc-v1.2.1';
const STATIC_CACHE = 'static-v1.2.1';
const RUNTIME_CACHE = 'runtime-v1.2.1';
const DYNAMIC_CACHE = 'dynamic-v1.2.1';

// Critical resources for immediate caching
const CRITICAL_URLS = [
  './',
  './index.html',
  './manifest.json',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
  'https://zovo.one/favicon.ico'
];

// Font and external resources
const FONT_URLS = [
  'https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2',
  'https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuOKfAZ9hiA.woff2'
];

// Advanced performance optimizations
const PERF_CONFIG = {
  imageQuality: 0.85,
  maxCacheAge: 86400000, // 24 hours
  staleWhileRevalidate: 3600000, // 1 hour
  maxEntries: 100,
  purgeInterval: 604800000 // 7 days
};

self.addEventListener('install', event => {
  console.log('[SW] Installing service worker v1.2.1');
  event.waitUntil(
    Promise.all([
      // Cache critical resources immediately
      caches.open(STATIC_CACHE).then(cache => {
        console.log('[SW] Caching critical resources');
        return cache.addAll(CRITICAL_URLS);
      }),
      // Pre-cache fonts for instant loading
      caches.open(RUNTIME_CACHE).then(cache => {
        console.log('[SW] Pre-caching fonts');
        return cache.addAll(FONT_URLS.filter(url => url));
      })
    ]).then(() => {
      // Skip waiting to activate immediately
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', event => {
  console.log('[SW] Activating service worker v1.2.1');
  event.waitUntil(
    Promise.all([
      // Clean up old caches
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
      // Take control of all pages immediately
      self.clients.claim()
    ])
  );
});

self.addEventListener('fetch', event => {
  const {request} = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip chrome-extension and other non-http(s) requests
  if (!url.protocol.startsWith('http')) return;

  // Handle different resource types with specific strategies
  if (url.pathname.endsWith('.html') || url.pathname === '/' || url.pathname.endsWith('/')) {
    event.respondWith(staleWhileRevalidateStrategy(request, STATIC_CACHE));
  } else if (url.pathname.endsWith('.css') || url.pathname.endsWith('.js')) {
    event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
  } else if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(cacheFirstStrategy(request, RUNTIME_CACHE, 31536000000)); // 1 year
  } else if (url.pathname.match(/\.(png|jpg|jpeg|webp|svg|ico|gif)$/)) {
    event.respondWith(cacheFirstStrategy(request, DYNAMIC_CACHE));
  } else if (url.hostname === 'quickchart.io' || url.hostname === 'www.youtube.com') {
    event.respondWith(networkFirstStrategy(request, DYNAMIC_CACHE));
  } else {
    event.respondWith(networkFirstStrategy(request, RUNTIME_CACHE));
  }
});

// Cache strategies with advanced error handling
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

// Background sync for enhanced reliability
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync') {
    event.waitUntil(performBackgroundSync());
  }
});

async function performBackgroundSync() {
  try {
    console.log('[SW] Performing background sync');
    // Refresh critical resources
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

// Periodic cache cleanup
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'CACHE_CLEANUP') {
    event.waitUntil(performCacheCleanup());
  }
});

async function performCacheCleanup() {
  const cacheNames = await caches.keys();

  await Promise.all(cacheNames.map(async cacheName => {
    const cache = await caches.open(cacheName);
    const requests = await cache.keys();

    if (requests.length > PERF_CONFIG.maxEntries) {
      // Remove oldest entries
      const sortedRequests = await Promise.all(
        requests.map(async request => {
          const response = await cache.match(request);
          return {
            request,
            date: new Date(response.headers.get('date') || 0)
          };
        })
      );

      sortedRequests.sort((a, b) => a.date - b.date);
      const toDelete = sortedRequests.slice(0, requests.length - PERF_CONFIG.maxEntries);

      await Promise.all(toDelete.map(item => cache.delete(item.request)));
    }
  }));
}

// Enhanced push notification support
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'GA Salary Calculator updated',
    icon: './icon-192.png',
    badge: './icon-192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '2'
    },
    actions: [
      {
        action: 'explore',
        title: 'Open Calculator',
        icon: './icon-192.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: './icon-192.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('GA Salary Calculator', options)
  );
});

self.addEventListener('notificationclick', event => {
  console.log('[SW] Notification click received.');

  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('./')
    );
  }
});

console.log('[SW] Service worker v1.2.1 loaded successfully');