/* eslint-env serviceworker */

var baseDatetime = ''

self.addEventListener('install', function (event) {
  console.log('Installing ServiceWorker.')
})

self.addEventListener('activate', function (event) {
  console.log('Activating ServiceWorker.')
})

self.addEventListener('fetch', function (event) {
  var request = event.request
  
  var url = new URL(event.request.url)
  var isNavigation = event.request.mode === 'navigate'
  var isWebUI = event.request.url.indexOf('/webui/') !== -1
  var isDaemon = event.request.url.indexOf('/daemon/') !== -1
  var isReplayRoot = (url.pathname === '/' || url.pathname === '')

  var referrerDatetime = event.request.referrer.match(/\/([0-9]{14})\//)
  if (referrerDatetime !== null) {
    referrerDatetime = referrerDatetime[1]
  }

  if (isNavigation || isReplayRoot || isDaemon) {
    return // Internal asset, no SW needed
  }

  // TODO: consult the referrer header on each request instead of using a global var
  //if ( event.request.url.split('/')[2] !== document.location.host) {
  if (!isNavigation && !isWebUI && !isDaemon) { // Do not rewrite webui embedded resources or daemon
       // TODO: use a 3XX redirect to better guide the browser
       //  if hostname == referrer, check to ensure serviceworker does not run infinitely on each embedded resource
    request = reroute(event.request, referrerDatetime) // Only embedded resources
    console.log('REROUTING request for ' + event.request.url + ' to ' + request.url)
  }

  event.respondWith(
    fetch(request).then(serverFetch, serverFailure).catch(serverFailure)
  )

  function serverFetch (response) {
    console.log('Fetching from server.')
    return response
  }

  function serverFailure () {
    console.log('Fetching from server failed.')
    return new Response('<h1>Service Unavailable</h1>', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: new Headers({
        'Content-Type': 'text/html'
      })
    })
  }

  function reroute (request, datetime) {
    return new Request(`http://127.0.0.1:5000/memento/${datetime}/${request.url}`) // TODO: Rm hard-code for server
  }
})
