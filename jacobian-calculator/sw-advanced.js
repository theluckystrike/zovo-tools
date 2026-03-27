// Advanced Service Worker v4.0 - jacobian-calculator
// Intelligent caching with network-first, cache-first, and stale-while-revalidate strategies

const CACHE_VERSION = '4.0.1774512394';
const CACHE_PREFIX = 'zovo-jacobiancalculator';
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
  '/free-tools/jacobian-calculator/',
  '/free-tools/jacobian-calculator/index.html',
  '/free-tools/jacobian-calculator/manifest.json',
  '../tool-integration-system.js',
  '../related-tools-widget.js',
  '../tool-comparison-system.js',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.11.0/math.min.js'
];

// Mathematical computation APIs to cache
const CACHEABLE_APIS = [
  '/api/jacobian/calculate',
  '/api/jacobian/derivatives',
  '/api/jacobian/matrix',
  '/api/jacobian/determinant',
  '/api/related-tools',
  '/api/tool-analytics'
];

// Install event - aggressive precaching
self.addEventListener('install', event => {
  console.log('[SW] Installing service worker for jacobian-calculator');

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
      console.log('[SW] All caches initialized');
      self.skipWaiting();
    })
  );
});

// Activate event - aggressive cleanup
self.addEventListener('activate', event => {
  console.log('[SW] Activating service worker');

  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(cacheName =>
              cacheName.startsWith(CACHE_PREFIX) &&
              !cacheName.includes(CACHE_VERSION)
            )
            .map(cacheName => {
              console.log('[SW] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      }),

      // Take control immediately
      self.clients.claim()
    ]).then(() => {
      console.log('[SW] Service worker activated successfully');
    })
  );
});

// Advanced fetch handler with multiple strategies
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests and chrome-extension requests
  if (request.method !== 'GET' || url.protocol === 'chrome-extension:') {
    return;
  }

  // Handle different resource types with optimal strategies
  if (isStaticAsset(request)) {
    event.respondWith(handleStaticAsset(request));
  } else if (isImage(request)) {
    event.respondWith(handleImage(request));
  } else if (isAPI(request)) {
    event.respondWith(handleAPI(request));
  } else if (isDocument(request)) {
    event.respondWith(handleDocument(request));
  } else {
    event.respondWith(handleDynamic(request));
  }
});

// Cache-first strategy for static assets
async function handleStaticAsset(request) {
  try {
    const cache = await caches.open(STATIC_CACHE);
    const cached = await cache.match(request);

    if (cached && !isExpired(cached, CACHE_DURATIONS.static)) {
      return cached;
    }

    const response = await fetch(request);
    if (response.ok) {
      await cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.error('[SW] Static asset fetch failed:', error);
    const cache = await caches.open(STATIC_CACHE);
    return await cache.match(request) || new Response('Asset unavailable', { status: 503 });
  }
}

// Cache-first strategy for images with WebP optimization
async function handleImage(request) {
  try {
    const cache = await caches.open(IMAGE_CACHE);
    const cached = await cache.match(request);

    if (cached && !isExpired(cached, CACHE_DURATIONS.images)) {
      return cached;
    }

    // Try to fetch WebP version first if supported
    const webpSupported = request.headers.get('Accept')?.includes('image/webp');
    let fetchRequest = request;

    if (webpSupported && !request.url.includes('.webp')) {
      const webpUrl = request.url.replace(/\.(jpg|jpeg|png)$/i, '.webp');
      try {
        const webpResponse = await fetch(webpUrl);
        if (webpResponse.ok) {
          await cache.put(request, webpResponse.clone());
          return webpResponse;
        }
      } catch (e) {
        // Fall back to original format
      }
    }

    const response = await fetch(fetchRequest);
    if (response.ok) {
      await cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.error('[SW] Image fetch failed:', error);
    const cache = await caches.open(IMAGE_CACHE);
    return await cache.match(request) || generatePlaceholderImage();
  }
}

// Network-first with fallback for API calls
async function handleAPI(request) {
  try {
    const response = await Promise.race([
      fetch(request),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('API timeout')), 5000)
      )
    ]);

    if (response.ok) {
      const cache = await caches.open(API_CACHE);
      await cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.warn('[SW] API fetch failed, trying cache:', error);
    const cache = await caches.open(API_CACHE);
    const cached = await cache.match(request);

    if (cached && !isExpired(cached, CACHE_DURATIONS.api)) {
      // Add offline header
      const headers = new Headers(cached.headers);
      headers.set('X-Served-By', 'ServiceWorker-Cache');
      headers.set('X-Cache-Date', new Date(cached.headers.get('date') || Date.now()).toISOString());

      return new Response(cached.body, {
        status: cached.status,
        statusText: cached.statusText,
        headers
      });
    }

    // Return offline response for jacobian calculations
    return new Response(JSON.stringify({
      error: 'Offline calculation not available',
      message: 'Please check your internet connection and try again',
      offline: true,
      timestamp: new Date().toISOString()
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Network-first with offline fallback for documents
async function handleDocument(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      await cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.warn('[SW] Document fetch failed, trying cache:', error);
    const cache = await caches.open(DYNAMIC_CACHE);
    const cached = await cache.match(request);

    if (cached) {
      return cached;
    }

    // Return offline page
    return new Response(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Offline - Jacobian Calculator</title>
        <style>
          body {
            font-family: 'Inter', sans-serif;
            background: #0a0a0f;
            color: #e0e0e8;
            text-align: center;
            padding: 2rem;
          }
          .offline-icon { font-size: 4rem; margin-bottom: 1rem; }
          .offline-title { color: #00ff88; font-size: 2rem; margin-bottom: 1rem; }
          .offline-message { font-size: 1.1rem; line-height: 1.6; max-width: 500px; margin: 0 auto; }
          .retry-btn {
            background: #00ff88;
            color: #0a0a0f;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1rem;
            margin-top: 2rem;
            cursor: pointer;
          }
        </style>
      </head>
      <body>
        <div class="offline-icon">📐</div>
        <h1 class="offline-title">Jacobian Calculator</h1>
        <p class="offline-message">
          You're currently offline. Some features may not be available,
          but basic calculations can still be performed.
        </p>
        <button class="retry-btn" onclick="window.location.reload()">
          Try Again
        </button>
      </body>
      </html>
    `, {
      status: 503,
      headers: { 'Content-Type': 'text/html' }
    });
  }
}

// Stale-while-revalidate for dynamic content
async function handleDynamic(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cached = await cache.match(request);

  // Serve from cache immediately if available
  if (cached) {
    // Background revalidation
    fetch(request).then(response => {
      if (response.ok) {
        cache.put(request, response);
      }
    }).catch(() => {
      // Ignore background update failures
    });

    return cached;
  }

  // No cache, fetch from network
  try {
    const response = await fetch(request);
    if (response.ok) {
      await cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    console.error('[SW] Dynamic content fetch failed:', error);
    return new Response('Content unavailable offline', { status: 503 });
  }
}

// Utility functions
function isStaticAsset(request) {
  const url = new URL(request.url);
  return url.pathname.includes('/js/') ||
         url.pathname.includes('/css/') ||
         url.pathname.includes('font') ||
         url.pathname.includes('manifest.json') ||
         url.pathname.endsWith('.js') ||
         url.pathname.endsWith('.css');
}

function isImage(request) {
  const url = new URL(request.url);
  return /\.(jpg|jpeg|png|gif|svg|webp|avif|ico)$/i.test(url.pathname);
}

function isAPI(request) {
  const url = new URL(request.url);
  return url.pathname.startsWith('/api/') ||
         CACHEABLE_APIS.some(api => url.pathname.includes(api));
}

function isDocument(request) {
  return request.destination === 'document';
}

function isExpired(response, duration) {
  const dateHeader = response.headers.get('date');
  if (!dateHeader) return true;

  const responseDate = new Date(dateHeader).getTime();
  return (Date.now() - responseDate) > duration;
}

function generatePlaceholderImage() {
  const svg = `
    <svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#1a1a1f"/>
      <text x="50%" y="50%" text-anchor="middle" dy="0.3em"
            fill="#666" font-family="Arial, sans-serif" font-size="16">
        Image unavailable offline
      </text>
    </svg>
  `;

  return new Response(svg, {
    status: 200,
    headers: { 'Content-Type': 'image/svg+xml' }
  });
}

// Background sync for offline calculations
self.addEventListener('sync', event => {
  console.log('[SW] Background sync triggered:', event.tag);

  if (event.tag === 'jacobian-calculation') {
    event.waitUntil(syncJacobianCalculations());
  }
});

async function syncJacobianCalculations() {
  try {
    // Get pending calculations from IndexedDB
    const calculations = await getPendingCalculations();

    for (const calc of calculations) {
      try {
        const response = await fetch('/api/jacobian/calculate', {
          method: 'POST',
          body: JSON.stringify(calc.data),
          headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
          await removePendingCalculation(calc.id);
          console.log('[SW] Synced calculation:', calc.id);
        }
      } catch (error) {
        console.error('[SW] Failed to sync calculation:', calc.id, error);
      }
    }
  } catch (error) {
    console.error('[SW] Background sync failed:', error);
  }
}

// Push notification handler
self.addEventListener('push', event => {
  if (!event.data) return;

  const data = event.data.json();
  const options = {
    body: data.body || 'New calculation result available',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: data.data || {},
    actions: [
      {
        action: 'open',
        title: 'View Result',
        icon: '/icons/icon-72x72.png'
      },
      {
        action: 'dismiss',
        title: 'Dismiss',
        icon: '/icons/icon-72x72.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(data.title || 'Jacobian Calculator', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.openWindow('/free-tools/jacobian-calculator/')
    );
  }
});

// Placeholder functions for IndexedDB operations
async function getPendingCalculations() {
  // Implementation would use IndexedDB to store offline calculations
  return [];
}

async function removePendingCalculation(id) {
  // Implementation would remove calculation from IndexedDB
  console.log('Removing calculation:', id);
}

console.log('[SW] Jacobian Calculator Service Worker v4.0 initialized');