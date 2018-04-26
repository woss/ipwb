self.addEventListener('message', function (event) {
    console.log('SW Received Message: ' + event.data)
    event.ports[0].postMessage('SUCCESS');
})

self.addEventListener('install', function(event) {
    event.waitUntil(self.skipWaiting()); // Activate worker immediately
});

self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim()); // Become available to all pages
});