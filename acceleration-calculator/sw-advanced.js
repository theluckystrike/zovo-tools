// Advanced Service Worker v4.0 - acceleration-calculator
// Intelligent caching with physics calculation optimization and real-time data sync

const CACHE_VERSION = '4.0.1774512400';
const CACHE_PREFIX = 'zovo-accelerationcalculator';
const STATIC_CACHE = CACHE_PREFIX + '-static-' + CACHE_VERSION;
const DYNAMIC_CACHE = CACHE_PREFIX + '-dynamic-' + CACHE_VERSION;
const PHYSICS_CACHE = CACHE_PREFIX + '-physics-' + CACHE_VERSION;
const INTEGRATION_CACHE = CACHE_PREFIX + '-integration-' + CACHE_VERSION;

// Cache duration optimized for physics calculations
const CACHE_DURATIONS = {
  static: 30 * 24 * 60 * 60 * 1000,    // 30 days for static assets
  dynamic: 7 * 24 * 60 * 60 * 1000,    // 7 days for dynamic content
  physics: 24 * 60 * 60 * 1000,        // 24 hours for physics data
  integration: 60 * 60 * 1000          // 1 hour for integration data
};

// Static assets optimized for physics calculations
const STATIC_ASSETS = [
  '/free-tools/acceleration-calculator/',
  '/free-tools/acceleration-calculator/index.html',
  '/free-tools/acceleration-calculator/manifest.json',
  '../tool-integration-system.js',
  '../related-tools-widget.js',
  '../tool-comparison-system.js',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.11.0/math.min.js'
];

// Physics and integration APIs
const PHYSICS_APIS = [
  '/api/physics/acceleration',
  '/api/physics/motion',
  '/api/physics/kinematics',
  '/api/physics/units',
  '/api/integration/motion-data'
];

// Install event with physics optimization
self.addEventListener('install', event => {
  console.log('[SW] Installing acceleration calculator service worker v4.0');

  event.waitUntil(
    Promise.all([
      // Cache static assets with reload to ensure freshness
      caches.open(STATIC_CACHE).then(cache => {
        console.log('[SW] Precaching static assets for physics calculations');
        return cache.addAll(STATIC_ASSETS.map(url => new Request(url, { cache: 'reload' })));
      }),

      // Initialize specialized physics cache
      caches.open(PHYSICS_CACHE).then(cache => {
        console.log('[SW] Initializing physics calculation cache');
        return cache.put('/offline-physics-formulas', new Response(JSON.stringify({
          linear_acceleration: 'a = (v_f - v_i) / t',
          kinematic_equations: {
            position: 'x = x₀ + v₀t + ½at²',
            velocity: 'v = v₀ + at',
            velocity_squared: 'v² = v₀² + 2a(x - x₀)'
          },
          centripetal_acceleration: 'a_c = v² / r = ω²r',
          angular_acceleration: 'α = (ω_f - ω_i) / t',
          gravitational_acceleration: 'g = 9.8066 m/s²'
        }), {
          headers: { 'Content-Type': 'application/json' }
        }));
      }),

      // Initialize other caches
      caches.open(DYNAMIC_CACHE),
      caches.open(INTEGRATION_CACHE)
    ]).then(() => {
      console.log('[SW] All physics calculation caches initialized');
      self.skipWaiting();
    })
  );
});

// Activate with intelligent cleanup
self.addEventListener('activate', event => {
  console.log('[SW] Activating acceleration calculator service worker');

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
              console.log('[SW] Deleting old physics cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      }),

      // Take immediate control
      self.clients.claim(),

      // Initialize physics calculation background sync
      self.registration.sync.register('physics-calculation-sync').catch(() => {
        console.log('[SW] Background sync not supported, using fallback');
      })
    ]).then(() => {
      console.log('[SW] Physics calculation service worker activated');
    })
  );
});

// Advanced fetch handler with physics optimization
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests and extensions
  if (request.method !== 'GET' || url.protocol === 'chrome-extension:') {
    return;
  }

  // Route to specialized handlers
  if (isPhysicsAPI(request)) {
    event.respondWith(handlePhysicsAPI(request));
  } else if (isIntegrationAPI(request)) {
    event.respondWith(handleIntegrationAPI(request));
  } else if (isStaticAsset(request)) {
    event.respondWith(handleStaticAsset(request));
  } else if (isDocument(request)) {
    event.respondWith(handleDocument(request));
  } else {
    event.respondWith(handleDynamic(request));
  }
});

// Physics API handler with calculation caching
async function handlePhysicsAPI(request) {
  const cache = await caches.open(PHYSICS_CACHE);

  try {
    // Try network first for accurate physics calculations
    const response = await Promise.race([
      fetch(request),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Physics API timeout')), 3000)
      )
    ]);

    if (response.ok) {
      // Cache successful physics calculations
      await cache.put(request, response.clone());
      addPhysicsCalculationHeaders(response);
    }
    return response;

  } catch (error) {
    console.warn('[SW] Physics API failed, checking cache:', error);

    // Try cached physics data
    const cached = await cache.match(request);
    if (cached && !isExpired(cached, CACHE_DURATIONS.physics)) {
      return addOfflineHeaders(cached, 'physics-cache');
    }

    // Fallback to offline physics formulas
    return handleOfflinePhysicsCalculation(request);
  }
}

// Integration API handler for cross-tool data flow
async function handleIntegrationAPI(request) {
  const cache = await caches.open(INTEGRATION_CACHE);
  const url = new URL(request.url);

  try {
    const response = await fetch(request);

    if (response.ok) {
      // Cache integration data temporarily
      await cache.put(request, response.clone());

      // Broadcast integration success to other tools
      broadcastIntegrationEvent('integration_success', {
        source: 'acceleration-calculator',
        endpoint: url.pathname,
        timestamp: Date.now()
      });
    }
    return response;

  } catch (error) {
    console.warn('[SW] Integration API failed:', error);

    const cached = await cache.match(request);
    if (cached && !isExpired(cached, CACHE_DURATIONS.integration)) {
      return addOfflineHeaders(cached, 'integration-cache');
    }

    // Return integration failure response
    return new Response(JSON.stringify({
      error: 'Integration temporarily unavailable',
      fallback: true,
      retry_after: 60,
      offline_capabilities: [
        'basic calculations',
        'formula reference',
        'unit conversions'
      ]
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Offline physics calculation fallback
async function handleOfflinePhysicsCalculation(request) {
  const cache = await caches.open(PHYSICS_CACHE);
  const formulas = await cache.match('/offline-physics-formulas');

  if (formulas) {
    const physicsData = await formulas.json();

    // Basic offline calculation capability
    return new Response(JSON.stringify({
      offline: true,
      message: 'Offline physics calculation mode',
      available_formulas: physicsData,
      note: 'For advanced calculations, please connect to internet',
      timestamp: new Date().toISOString()
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'X-Offline-Mode': 'true',
        'X-Physics-Fallback': 'basic-formulas'
      }
    });
  }

  return new Response(JSON.stringify({
    error: 'Physics calculation unavailable offline',
    retry: 'Please check internet connection'
  }), {
    status: 503,
    headers: { 'Content-Type': 'application/json' }
  });
}

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
    return await cache.match(request) || generateOfflineAsset();
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

    // Return physics-optimized offline page
    return generatePhysicsOfflinePage();
  }
}

// Stale-while-revalidate for dynamic content
async function handleDynamic(request) {
  const cache = await caches.open(DYNAMIC_CACHE);
  const cached = await cache.match(request);

  if (cached) {
    // Background revalidation
    fetch(request).then(response => {
      if (response.ok) {
        cache.put(request, response);
      }
    }).catch(() => {});

    return cached;
  }

  try {
    const response = await fetch(request);
    if (response.ok) {
      await cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    return new Response('Content unavailable offline', { status: 503 });
  }
}

// Background sync for physics calculations
self.addEventListener('sync', event => {
  console.log('[SW] Background sync triggered:', event.tag);

  if (event.tag === 'physics-calculation-sync') {
    event.waitUntil(syncPhysicsCalculations());
  }
});

async function syncPhysicsCalculations() {
  try {
    // Sync any queued physics calculations
    const pendingCalculations = await getPendingPhysicsCalculations();

    for (const calc of pendingCalculations) {
      try {
        const response = await fetch('/api/physics/sync', {
          method: 'POST',
          body: JSON.stringify(calc),
          headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
          await removePendingCalculation(calc.id);
          console.log('[SW] Synced physics calculation:', calc.id);
        }
      } catch (error) {
        console.error('[SW] Failed to sync calculation:', error);
      }
    }
  } catch (error) {
    console.error('[SW] Physics sync failed:', error);
  }
}

// Push notifications for calculation results
self.addEventListener('push', event => {
  if (!event.data) return;

  const data = event.data.json();
  const options = {
    body: data.body || 'Physics calculation completed',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [100, 50, 100, 50, 100],
    data: {
      ...data.data,
      source: 'acceleration-calculator'
    },
    actions: [
      {
        action: 'view_result',
        title: 'View Result',
        icon: '/icons/icon-72x72.png'
      },
      {
        action: 'share_calculation',
        title: 'Share',
        icon: '/icons/icon-72x72.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(
      data.title || 'Acceleration Calculator',
      options
    )
  );
});

// Notification click handler
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'view_result') {
    event.waitUntil(
      clients.openWindow('/free-tools/acceleration-calculator/?result=' +
        encodeURIComponent(event.notification.data.calculation_id))
    );
  } else if (event.action === 'share_calculation') {
    event.waitUntil(handleShareCalculation(event.notification.data));
  } else {
    event.waitUntil(
      clients.openWindow('/free-tools/acceleration-calculator/')
    );
  }
});

// Utility functions
function isPhysicsAPI(request) {
  const url = new URL(request.url);
  return PHYSICS_APIS.some(api => url.pathname.includes(api)) ||
         url.pathname.includes('/physics/') ||
         url.pathname.includes('/calculation/');
}

function isIntegrationAPI(request) {
  const url = new URL(request.url);
  return url.pathname.includes('/integration/') ||
         url.pathname.includes('/cross-tool/') ||
         url.pathname.includes('/workflow/');
}

function isStaticAsset(request) {
  const url = new URL(request.url);
  return url.pathname.includes('/js/') ||
         url.pathname.includes('/css/') ||
         url.pathname.includes('font') ||
         url.pathname.includes('manifest.json') ||
         url.pathname.endsWith('.js') ||
         url.pathname.endsWith('.css');
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

function addPhysicsCalculationHeaders(response) {
  response.headers.set('X-Physics-Calculated', 'true');
  response.headers.set('X-Cache-Strategy', 'network-first-physics');
  return response;
}

function addOfflineHeaders(response, source) {
  const headers = new Headers(response.headers);
  headers.set('X-Served-By', 'ServiceWorker-Cache');
  headers.set('X-Cache-Source', source);
  headers.set('X-Offline-Mode', 'true');

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}

function generatePhysicsOfflinePage() {
  return new Response(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Offline - Acceleration Calculator</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        body {
          font-family: 'Inter', sans-serif;
          background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
          color: #e0e0e8;
          text-align: center;
          padding: 2rem;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .offline-container { max-width: 600px; margin: 0 auto; }
        .offline-icon { font-size: 4rem; margin-bottom: 1.5rem; animation: pulse 2s infinite; }
        .offline-title { color: #00ff88; font-size: 2.2rem; margin-bottom: 1rem; font-weight: 600; }
        .offline-message { font-size: 1.1rem; line-height: 1.6; margin-bottom: 2rem; color: #a0a0b0; }
        .physics-formulas {
          background: rgba(0,255,136,0.05);
          border: 1px solid rgba(0,255,136,0.2);
          border-radius: 12px;
          padding: 1.5rem;
          margin: 2rem 0;
          text-align: left;
        }
        .formula-title { color: #00ff88; font-size: 1.2rem; margin-bottom: 1rem; font-weight: 500; }
        .formula {
          margin: 0.5rem 0;
          padding: 0.5rem;
          background: rgba(0,0,0,0.3);
          border-radius: 6px;
          font-family: monospace;
          font-size: 0.95rem;
        }
        .retry-btn {
          background: linear-gradient(135deg, #00ff88, #00cc70);
          color: #0a0a0f;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s ease;
        }
        .retry-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,255,136,0.3); }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
      </style>
    </head>
    <body>
      <div class="offline-container">
        <div class="offline-icon">🚀</div>
        <h1 class="offline-title">Acceleration Calculator</h1>
        <p class="offline-message">
          You're currently offline, but basic physics calculations are still available!
        </p>

        <div class="physics-formulas">
          <div class="formula-title">📐 Available Physics Formulas</div>
          <div class="formula">Linear Acceleration: a = (v_f - v_i) / t</div>
          <div class="formula">Position: x = x₀ + v₀t + ½at²</div>
          <div class="formula">Velocity: v = v₀ + at</div>
          <div class="formula">Centripetal: a_c = v² / r</div>
          <div class="formula">Angular: α = (ω_f - ω_i) / t</div>
          <div class="formula">Gravity: g = 9.8066 m/s²</div>
        </div>

        <button class="retry-btn" onclick="window.location.reload()">
          🔄 Try Again
        </button>
      </div>
    </body>
    </html>
  `, {
    status: 503,
    headers: { 'Content-Type': 'text/html' }
  });
}

function generateOfflineAsset() {
  return new Response('Asset unavailable offline', {
    status: 503,
    headers: { 'Content-Type': 'text/plain' }
  });
}

function broadcastIntegrationEvent(type, data) {
  // Broadcast to all clients
  self.clients.matchAll().then(clients => {
    clients.forEach(client => {
      client.postMessage({
        type: 'INTEGRATION_EVENT',
        eventType: type,
        data: data,
        timestamp: Date.now()
      });
    });
  });
}

// Placeholder functions for physics sync
async function getPendingPhysicsCalculations() {
  return []; // Would integrate with IndexedDB
}

async function removePendingCalculation(id) {
  console.log('[SW] Removing calculation:', id);
}

async function handleShareCalculation(data) {
  console.log('[SW] Sharing calculation:', data);
}

console.log('[SW] Acceleration Calculator Service Worker v4.0 - Physics optimization enabled');