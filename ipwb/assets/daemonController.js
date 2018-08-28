let remainingTries = 0

function recheckDaemonStatus () {
  const running = document.getElementById('status').innerHTML === 'Running'
  remainingTries = 10

  if (!running) {
    makeAnAJAXRequest('/ipfsdaemon/status', checkStatus, null, errorOnStatusCheck)
  }
}

function checkStatus (resp) {
  if (remainingTries > 0) { // Top polling after 10 sec/tries
    remainingTries -= 1
  }
  if (resp.indexOf('Not Running') > -1) {
    window.setTimeout(function () {
      makeAnAJAXRequest('/ipfsdaemon/status', checkStatus, null, errorOnStatusCheck)
    }, 1000)
  } else {
    document.location.reload(true)
  }
}

function errorOnStatusCheck () {
  console.log('error on daemon status check')
}

document.addEventListener('DOMContentLoaded', recheckDaemonStatus, false)
