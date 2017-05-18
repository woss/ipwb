function handleSubmit () {
  document.location += document.getElementById('url').value
}

function showURIs () {
  var ul = document.getElementById('uriList')

  if (ul.childNodes.length > 0) {
    return // Prevent multiple adds of the URI list to the DOM
  }

  var htmlPages = 0
  for (var uri in uris) {
    for (var datetimesI = 0; datetimesI < uris[uri]['datetimes'].length; datetimesI++) {
      var datetime = uris[uri]['datetimes'][datetimesI]

      var li = document.createElement('li')
      var a = document.createElement('a')
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
  document.getElementById('memCountListLink').classList = ['activated']
  document.getElementById('uris').classList.remove('hidden')
  setPlurality()
  setShowAllButtonStatus()
}

function addEventListeners () {
  var target = document.getElementById('memCountListLink')
  target.addEventListener('click', showURIs, false)

  var showAllInListingButton = document.getElementById('showEmbeddedURI')
  showAllInListingButton.onclick = function showAllURIs () {
    document.getElementById('uriList').classList.add('forceDisplay')
  }

  getIPFSWebUIAddress()
}

function setPlurality () {
  var urimCount = document.getElementById('memCountInt').innerHTML
  var htmlFilesPlurality = document.getElementById('htmlPages').innerHTML

  if (urimCount === '1') {
    document.getElementById('plural').classList.add('hidden')
  }
  if (htmlFilesPlurality === '1') {
    document.getElementById('htmlPagesPlurality').classList.add('hidden')
  }
}

function setShowAllButtonStatus () {
  var urimCount = document.getElementById('memCountInt').innerHTML
  var htmlFilesPlurality = document.getElementById('htmlPages').innerHTML
  if (urimCount === htmlFilesPlurality) {
    document.getElementById('showEmbeddedURI').setAttribute('disabled','disabled')
  }
}

function assignStatusButtonHandlers () {
  var button = document.getElementsByTagName('button')[0]
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
  var setIPFSWebUILink = function (resp) {
    document.getElementById('webui').setAttribute('href', 'http://' + resp)
    console.log(resp)
  }
  var fail = function () { console.log('fail') }
  var err = function () { console.log('err') }
  makeAnAJAXRequest('/config/openEndedPlaceHolder', setIPFSWebUILink, fail, err)
}

function updateIPFSDaemonButtonUI () {
  window.setTimeout(function () {
    document.location.reload(true)
  }, 4000)
}

function sendCommandToIPFSDaemon (cmd) {
  var failFunction = function () { console.log('Comm w/ ipfs daemon failed.') }
  var errFunction = function () { console.log('Error talking to ipfs daemon.') }
  makeAnAJAXRequest('/daemon/' + cmd, updateIPFSDaemonButtonUI,
    failFunction, errFunction)
}

function makeAnAJAXRequest (address, successFunction, failFunction, errorFunction) {
  var xmlhttp = new XMLHttpRequest()

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
