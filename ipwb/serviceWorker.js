/* eslint-env serviceworker */

let baseDatetime = ''

function getMyVersion () {
  fetch(self.location.href)
  .then(function (resp) {
    console.log('Running ServiceWorker version ' + resp.headers.get('Server'))
  })
}

self.addEventListener('install', function (event) {
  console.log('Installing ServiceWorker.')
})

self.addEventListener('activate', function (event) {
  console.log('Activating ServiceWorker.')
})

self.addEventListener('fetch', function (event) {
  let request = event.request

  const url = new URL(event.request.url)
  const isNavigation = event.request.mode === 'navigate'
  const isWebUI = event.request.url.indexOf('/webui/') !== -1
  const isDaemon = event.request.url.indexOf('/daemon/') !== -1
  const isConfig = event.request.url.indexOf('/config/') !== -1
  const isReplayRoot = (url.pathname === '/' || url.pathname === '')
  const isRootMemento = event.request.url === event.request.referrer
  //var isAMemento = event.request.url.indexOf('/memento/') !== -1 || event.request.url.match('\/[0-9]{14}\/') !== null
  const isAMemento = event.request.url.match('\/[0-9]{14}\/') !== null

  let referrerDatetime = event.request.referrer.match(/\/([0-9]{14})\//)
  if (referrerDatetime !== null) {
    referrerDatetime = referrerDatetime[1]
  }

  if (isNavigation || isReplayRoot || isDaemon || isConfig) {
    return // Internal asset, no SW needed
  }

  // TODO: consult the referrer header on each request instead of using a global var
  //if ( event.request.url.split('/')[2] !== document.location.host) {
  if (!isNavigation && !isWebUI && !isDaemon && !isRootMemento && !isConfig && !isAMemento) { // Do not rewrite webui embedded resources or daemon
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
    getMyVersion()
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
    return new Request(`${self.location.origin}/memento/${datetime}/${request.url}`)
  }
})
