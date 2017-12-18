/* eslint-env serviceworker */

// This makes a module available named "reconstructive"
importScripts('https://oduwsdl.github.io/reconstructive/reconstructive.js')

// Customize configs (defaults should work for IPWB out of the box)
// reconstructive.init({
//   version: 'reconstructive.js:v1',
//   urimPattern: self.location.origin + '/memento/<datetime>/<urir>',
//   showBanner: false
// })

// Add any custom exclusions or modify or delete default ones
//> reconstructive.exclusions
//< {
//<   notGet: f (event, config),
//<   localResource: f (event, config)
//< }

// Pass a custom function to generate banner markup
// reconstructive.bannerCreator(f (event, rewritten, config))
// Or update the rewriting logic
// reconstructive.updateRewriter(f (event, rewritten, config))

// This is unnecessary, but can be useful for debugging or in future
self.addEventListener('install', function (event) {
  console.log('Installing ServiceWorker.')
})

// This is unnecessary, but can be useful for debugging or in future
self.addEventListener('activate', function (event) {
  console.log('Activating ServiceWorker.')
})

self.addEventListener("fetch", function(event) {
  console.log('A fetch event triggered:', event);
  // Add any custom logic here to conditionally call the reroute function
  reconstructive.reroute(event);
})
