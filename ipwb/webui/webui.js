function handleSubmit () {
  document.location += document.getElementById('url').value
}

function showURIs () {
  var ul = document.getElementById('uriList')

  if (ul.childNodes.length > 0) {
    return // Prevent multiple adds of the URI list to the DOM
  }

  for (var i = 0; i < uris.length; i++) {
    var li = document.createElement('li')
    var a = document.createElement('a')
    a.href = uris[i]
    a.appendChild(document.createTextNode(uris[i]))

    li.appendChild(a)
    ul.appendChild(li)
  }
  document.getElementById('memCountListLink').classList = ['activated']
  document.getElementById('uris').classList.remove('hidden')
}

function addEventListeners () {
  var target = document.getElementById('memCountListLink')
  target.addEventListener('click', showURIs, false)
}

function setPlurality () {
  var count = document.getElementById('memCountInt').innerHTML
  if (count === 1) {
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

function sendCommandToIPFSDaemon (cmd) {
  var xmlhttp = new XMLHttpRequest()

  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState === XMLHttpRequest.DONE) {
      if (xmlhttp.status === 200) {
        window.setTimeout(function () {
          document.location.reload(true)
        }, 4000)
      } else if (xmlhttp.status === 400) {
        console.log('error 400')
      } else {
        console.log('something else other than 200 was returned')
      }
    }
  }

  xmlhttp.open('GET', '/daemon/' + cmd, true)
  xmlhttp.send()
}
