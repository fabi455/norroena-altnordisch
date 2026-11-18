const VERSION = 'norroena-offline-v2';
const CORE = ['./', './index.html', './style.css', './app.js', './content.js', './manifest.webmanifest', './icons/norroena.svg'];
self.addEventListener('install', event => event.waitUntil((async () => {
  const cache = await caches.open(VERSION);
  await cache.addAll(CORE);
  await self.skipWaiting();
})()));
self.addEventListener('activate', event => event.waitUntil((async () => {
  for (const name of await caches.keys()) if (name !== VERSION) await caches.delete(name);
  await self.clients.claim();
})()));
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const u = new URL(event.request.url);
  if (u.origin !== self.location.origin) return;
  event.respondWith((async () => {
    const cache = await caches.open(VERSION);
    const found = await cache.match(event.request);
    if (found) return found;
    try {
      const fresh = await fetch(event.request);
      if (fresh.ok && (u.pathname.endsWith('.mp3') || u.pathname.endsWith('.js') || u.pathname.endsWith('.css'))) {
        cache.put(event.request, fresh.clone()).catch(() => {});
      }
      return fresh;
    } catch {
      return new Response('Offline-Datei nicht verfügbar', {status: 503});
    }
  })());
});
