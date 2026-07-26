/* 箱庭クロニクル Service Worker — 更新優先 + オフラインフォールバック
 * v25: GitHub Pages更新後も古いindex.htmlが残り続ける問題を解消。
 */
const CACHE = "hakoslg-v25";
const ASSETS = ["./", "./index.html"];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(new Request(event.request, { cache: "no-cache" }))
      .then(response => {
        if (response && response.ok) {
          const copy = response.clone();
          caches.open(CACHE).then(cache => cache.put(event.request, copy));
        }
        return response;
      })
      .catch(async () => {
        const cached = await caches.match(event.request);
        if (cached) return cached;
        return caches.match("./index.html");
      })
  );
});
