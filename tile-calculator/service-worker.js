
// Advanced Service Worker for Offline Functionality
const CACHE_VERSION = 'v3.0.0';
const CACHE_NAME = 'zovo-tools-' + CACHE_VERSION;

const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/css/main.css',
  '/js/main.js',
  '/manifest.json'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name.startsWith('zovo-tools-') && name !== CACHE_NAME)
          .map(name => {
            console.log('Deleting cache:', name);
            return caches.delete(name);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - network first, cache fallback strategy
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Cache successful responses
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Fallback to cache
        return caches.match(event.request);
      })
  );
});

// Background sync for analytics
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync-analytics') {
    event.waitUntil(syncAnalytics());
  }
});

async function syncAnalytics() {
  // Sync pending analytics data when online
  const analyticsQueue = await getStoredAnalytics();
  if (analyticsQueue.length > 0) {
    // Send queued analytics data
    for (const data of analyticsQueue) {
      try {
        await fetch('/api/analytics', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: { 'Content-Type': 'application/json' }
        });
      } catch (error) {
        console.log('Analytics sync failed:', error);
      }
    }
    // Clear queue after successful sync
    await clearAnalyticsQueue();
  }
}
