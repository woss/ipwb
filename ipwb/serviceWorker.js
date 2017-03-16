console.log('Loading ServiceWorker.')

self.addEventListener('install', function(event) {
  console.log('Installing ServiceWorker.')
})

self.addEventListener('activate', function(event) {
  console.log('Activating ServiceWorker.')
})

self.addEventListener('fetch', function(event) {
  console.log('Fetch event triggered.')
  console.log(event.request)
  var request = event.request
  if (event.request.mode != 'navigate' && 
      event.request.url.indexOf('/webui/') === -1) // Do not rewrite webui embedded resources
  {
       console.log('REROUTING request for ' + event.request.url)

       request = reroute(event.request) // Only embedded resources
  }

  event.respondWith(
    fetch(request).then(serverFetch, serverFailure).catch(serverFailure)
  )

  function serverFetch(response) {
    console.log('Fetching from server.')
    console.log(response);
    return response;
  }

  function serverFailure() {
    console.log('Fetching from server failed.');
    return new Response('<h1>Service Unavailable</h1>', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: new Headers({
        'Content-Type': 'text/html'
      })
    })
  }

  function reroute(request) {
    return new Request('http://127.0.0.1:5000/memento/'+request.url) // TODO: Rm hard-code for server
  }
})