function handleSubmit () {
  document.location += document.getElementById('url').value
}

function showURIs () {
  var ul = document.getElementById('uriList')

  if (ul.childNodes.length > 0) {
    return // Prevent multiple adds of the URI list to the DOM
  }

  for (var uri in uris) {
    uris[uri].forEach(function (datetime) {
      var li = document.createElement('li')
      var a = document.createElement('a')
      a.href = uri
      a.appendChild(document.createTextNode(uri))
      dt = document.createTextNode(' (' + datetime + ')')
      
      li.appendChild(a)
      li.appendChild(dt)
      ul.appendChild(li)
    })
  }
  document.getElementById('memCountListLink').classList = ['activated']
  document.getElementById('uris').classList.remove('hidden')
}

function addEventListeners () {
  var target = document.getElementById('memCountListLink')
  target.addEventListener('click', showURIs, false)
  
  getIPFSWebUIAddress()
}

function setPlurality () {
  var count = document.getElementById('memCountInt').innerHTML
  if (count === "1") {
    document.getElementById('plural').classList.add('hidden')
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
  var fail = function () {console.log('fail')}
  var err = function () {console.log('err')}
  makeAnAJAXRequest('/config/openEndedPlaceHolder', setIPFSWebUILink, fail, err)
}

function updateIPFSDaemonButtonUI () {
  window.setTimeout(function () {
    document.location.reload(true)
  }, 4000)
}

function sendCommandToIPFSDaemon (cmd) {
  var failFunction = function () {console.log('Comm w/ ipfs daemon failed.');}
  var errFunction = function () {console.log('Error talking to ipfs daemon.');}
  makeAnAJAXRequest('/daemon/' + cmd, updateIPFSDaemonButtonUI,
    failFunction, errFunction)
}

function makeAnAJAXRequest(address, successFunction, failFunction, errorFunction) {
 var xmlhttp = new XMLHttpRequest()

  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState === XMLHttpRequest.DONE) {
      if (xmlhttp.status === 200) {
        successFunction(xmlhttp.responseText)
      } else if (xmlhttp.status === 400) {
        failFunction()
      } else {
        errorFunction
      }
    }
  }

  xmlhttp.open('GET', address, true)
  xmlhttp.send()

}
