// Keeps the app's own files so it opens when the laptop can't be reached. Job data and clips always come
// from the network; app files are fetched fresh first and fall back to the saved copy.
const CACHE = "gcm-clipper-v1";
const SHELL = ["./", "index.html", "app.js", "style.css", "manifest.webmanifest", "icon-192.png", "icon-512.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.startsWith("/api/") || url.pathname.startsWith("/media/")) return;
  event.respondWith(fetch(event.request)
    .then((res) => {
      const copy = res.clone();
      if (res.ok) caches.open(CACHE).then((cache) => cache.put(event.request, copy));
      return res;
    })
    .catch(() => caches.match(event.request).then((hit) => hit || caches.match("index.html"))));
});
