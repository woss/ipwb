/* eslint-env serviceworker */

// This makes a module available named "reconstructive"
importScripts('/reconstructive.js')

// Customize configs
// reconstructive.init({
//   id: `${NAME}:${VERSION}`,
//   urimPattern: `${self.location.origin}/memento/<datetime>/<urir>`,
//   bannerElementLocation: `${self.location.origin}/reconstructive-banner.js`,
//   showBanner: false,
//   debug: false
// });
Reconstructive.init({
  showBanner: true,
  debug: true
})

// Add any custom exclusions or modify or delete default ones
//> reconstructive.exclusions
//< {
//<   notGet: f (event, config),
//<   localResource: f (event, config)
//< }
Reconstructive.exclusions.replayRoot = (event, config) => event.request.url.replace(/\/+$/, '') == self.location.origin
Reconstructive.exclusions.specialEndpint = function(event, config) {
  return ['/webui/', '/daemon/', '/config/'].some(ep => event.request.url.startsWith(self.location.origin + ep))
}

// Pass a custom function to generate banner markup
// reconstructive.bannerCreator(f (response, event, config) => string)
// Or update the rewriting logic
// reconstructive.updateRewriter(f (response, event, config) => Response)

// This is not necessary, but can be useful for debugging or in future
self.addEventListener('install', function (event) {
  console.log('Installing ServiceWorker.')
})

// This is not necessary, but can be useful for debugging or in future
self.addEventListener('activate', function (event) {
  console.log('Activating ServiceWorker.')
})

self.addEventListener('fetch', function(event) {
  // Add any custom logic here to conditionally call the reroute function
  Reconstructive.reroute(event);
})
