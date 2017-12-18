function handleSubmit () {
  document.location += 'memento/*/' + document.getElementById('url').value
}

function shortestFirst(a, b) {
  if (a.length < b.length) {return -1}
  if (a.length > b.length) {return 1}
  return 0
}

function showURIs () {
  let ul = document.getElementById('uriList')
  if (ul.childNodes.length > 0) {
    return // Prevent multiple adds of the URI list to the DOM
  }

  let htmlPages = 0
  const uriKeys = Object.keys(uris).sort(shortestFirst)
  for (let uri of uriKeys) {
    for (let datetimesI = 0; datetimesI < uris[uri]['datetimes'].length; datetimesI++) {
      let datetime = uris[uri]['datetimes'][datetimesI]

      let li = document.createElement('li')
      let a = document.createElement('a')
      a.href = datetime + '/' + uri
      a.appendChild(document.createTextNode(uri))
      dt = document.createTextNode(' (' + datetime + ')')

      li.appendChild(a)
      li.appendChild(dt)
      li.setAttribute('data-mime', uris[uri]['mime'])
      ul.appendChild(li)
    }
    uris[uri]['mime'] === 'text/html' ? ++htmlPages : ''
  }
  document.getElementById('htmlPages').innerHTML = htmlPages
  document.getElementById('memCountListLink').className = ['activated']
  document.getElementById('uris').classList.remove('hidden')
  setPlurality()
  setShowAllButtonStatus()

  setUIExpandedState(uris)
  // Maintain visible state of URI display for future retrieval
  window.localStorage.setItem('showURIs', true)
}

function setUIExpandedState(urisObj) {
  const urisHash  = calculateURIsHash(urisObj)
  setURIsHash(urisHash)
}

function calculateURIsHash(urisObj) {
  return JSON.stringify(urisObj).hashCode()
}

function getURIsHash() {
  return window.localStorage.getItem('urisHash')
}

function setURIsHash(hashIn) {
  return window.localStorage.setItem('urisHash', hashIn)
}

String.prototype.hashCode = function () {
  let hash = 0
  let i
  let chr
  if (this.length === 0) {
    return hash
  }
  for (i = 0; i < this.length; i++) {
    chr   = this.charCodeAt(i)
    hash  = ((hash << 5) - hash) + chr
    hash |= 0; // Convert to 32bit integer
  }
  return hash
};

function addEventListeners () {
  let target = document.getElementById('memCountListLink')
  target.addEventListener('click', showURIs, false)

  let showAllInListingButton = document.getElementById('showEmbeddedURI')
  showAllInListingButton.onclick = function showAllURIs () {
    document.getElementById('uriList').classList.add('forceDisplay')
  }

  getIPFSWebUIAddress()
  updateServiceWorkerVersionUI()

  let reinstallServiceWorkerButton = document.getElementById('reinstallServiceWorker')
  reinstallServiceWorkerButton.onclick = reinstallServiceWorker

  setShowURIsVisibility()
}

function setShowURIsVisibility () {
  const previousHash = getURIsHash() + ''
  const newHash = calculateURIsHash(uris) + ''

  if (window.localStorage.getItem('showURIs') && previousHash === newHash) {
    showURIs()
  }
}

function setPlurality () {
  const urimCount = document.getElementById('memCountInt').innerHTML
  const htmlFilesPlurality = document.getElementById('htmlPages').innerHTML

  if (urimCount === '1') {
    document.getElementById('plural').classList.add('hidden')
  }
  if (htmlFilesPlurality === '1') {
    document.getElementById('htmlPagesPlurality').classList.add('hidden')
  }
}

function setShowAllButtonStatus () {
  const urimCount = document.getElementById('memCountInt').innerHTML
  const htmlFilesPlurality = document.getElementById('htmlPages').innerHTML
  if (urimCount === htmlFilesPlurality) {
    document.getElementById('showEmbeddedURI').setAttribute('disabled','disabled')
  }
}

function assignStatusButtonHandlers () {
  let button = document.getElementsByTagName('button')[0]
  if (button.innerHTML === 'Start') {
    button.addEventListener('click', startIPFSDaemon)
  } else {
    button.addEventListener('click', stopIPFSDaemon)
  }
}

function startIPFSDaemon () {
  sendCommandToIPFSDaemon('start')
  this.innerHTML = 'Starting...'
  this.setAttribute('disabled', 'disabled')
}

function stopIPFSDaemon () {
  sendCommandToIPFSDaemon('stop')
  this.innerHTML = 'Stopping...'
  this.setAttribute('disabled', 'disabled')
}

function getIPFSWebUIAddress () {
  const setIPFSWebUILink = function (resp) {
    document.getElementById('webui').setAttribute('href', 'http://' + resp)
  }
  const fail = function () { console.log('fail') }
  const err = function () { console.log('err') }
  makeAnAJAXRequest('/config/openEndedPlaceHolder', setIPFSWebUILink, fail, err)
}

function updateIPFSDaemonButtonUI () {
  window.setTimeout(function () {
    document.location.reload(true)
  }, 4000)
}

function sendCommandToIPFSDaemon (cmd) {
  const failFunction = function () { console.log('Comm w/ ipfs daemon failed.') }
  const errFunction = function () { console.log('Error talking to ipfs daemon.') }
  makeAnAJAXRequest('/daemon/' + cmd, updateIPFSDaemonButtonUI,
    failFunction, errFunction)
}

function makeAnAJAXRequest (address, successFunction, failFunction, errorFunction) {
  let xmlhttp = new XMLHttpRequest()

  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState === XMLHttpRequest.DONE) {
      if (xmlhttp.status === 200) {
        successFunction(xmlhttp.responseText)
      } else if (xmlhttp.status === 400) {
        failFunction()
      } else {
        errorFunction()
      }
    }
  }

  xmlhttp.open('GET', address, true)
  xmlhttp.send()
}

function injectIPWBJS () {
  registerServiceWorker()
  // TODO: Add ipwb replay banner
}

function getServiceWorkerVersion () {
  return fetch(self.location.href)
  .then(function (resp) {
    return Promise.resolve(resp.headers.get('Server').split('/')[1])
  })
}


function reinstallServiceWorker () {
  console.log('Deleting old serviceWorker')
  deleteServiceWorker()
  document.getElementById('serviceWorkerVersion').innerHTML = 'Updating...'
  installServiceWorker()
  updateServiceWorkerVersionUI()
}

function deleteServiceWorker () {
  navigator.serviceWorker.getRegistrations().then(function (registrations) {
    for (let registration of registrations) {
      registration.unregister()
    }
  })
}

function updateServiceWorkerVersionUI () {
  getServiceWorkerVersion().then(function (resp) {
    console.log('updating to ...' + resp)
    document.getElementById('serviceWorkerVersion').innerHTML = 'ver. ' + resp
  })
}

function installServiceWorker () {
  let newInstallation = false

  if (navigator.serviceWorker.controller === null) { // Ideally we would use serviceWorker.getRegistration
    newInstallation = true
  }

  navigator.serviceWorker.register('/serviceWorker.js').then(function(registration) {
    console.log('ServiceWorker registration successful with scope: ', registration.scope)
  }).catch(function(err) {
    console.log('ServiceWorker registration failed: ', err)
  }).then(function(rr){
    const dt = document.location.href.split('/')[3]
    const viewingMemento = dt.length === 14 && parseInt(dt, 10) + '' === dt

    // Reload the page with processing by the newly installed Service Worker
    if (newInstallation && viewingMemento) {
      document.location.reload()
    }
  })
}

function registerServiceWorker () {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', installServiceWorker)
  } else {
    console.log('Browser does not support Service Worker.')
  }
}

function serviceWorkerUpToDate () {

}

function updateServiceWorker () {

}

function reloadPageFromServiceWorker () {
  console.log('reloading page from serviceWorker!')
}
