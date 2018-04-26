function registerServiceWorker () {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js', {scope: '/'})
    .then(function (reg) {
      console.log('Registration succeeded. Scope is ' + reg.scope)
      setActionButtonEnabled(true)
    }).catch(function (error) {
      console.log('Registration failed with ' + error)
    })
  }
}

function unregisterServiceWorker () {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(function(registrations) {
      for(let registration of registrations) {
        registration.unregister()
        console.log('Unregistration succeeded.')
        setActionButtonEnabled(false)
      }
    })
  }
}

function setActionButtonEnabled (enabled) {
  let button = document.getElementById('sendActionToSW')
  if (enabled) {
    button.removeAttribute('disabled')
  } else {
    button.setAttribute('disabled', 'disabled')
  }
}

function serviceWorkerRegistered () {
  return navigator.serviceWorker.getRegistrations().then(registrations => {
    return registrations.length == 1
  })
}

function toggleServiceWorkerRegistration () {
    let button = document.getElementsByTagName('button')[0]
    
    serviceWorkerRegistered().then(swExists => {
      var action = null
      if (swExists) {
        action = unregisterServiceWorker
        button.innerHTML = 'Register ServiceWorker'   
      } else {
        action = registerServiceWorker
        button.innerHTML = 'Unregister ServiceWorker'    
      }
      action()
    })
}

function communicateToSW () {
    return new Promise(function(resolve, reject){
        var mChan = new MessageChannel()

        mChan.port1.onmessage = function (event) {
            if (event.data.error) {
                reject(event.data.error)
            }else{
                resolve(event.data)
            }
        }

        navigator.serviceWorker.controller.postMessage('Do the thing!', [mChan.port2]);
    })
}

document.addEventListener('DOMContentLoaded', function(event) {
    let button = document.getElementById('enabledSW')
    let swAction = document.getElementById('sendActionToSW')
    button.onclick = toggleServiceWorkerRegistration
    swAction.onclick = function () {
      communicateToSW().then(msg => {
        let m = document.getElementById('swMsg')
        m.innerHTML = msg
        m.classList.add('success')
      })
    }
    
    serviceWorkerRegistered().then(swExists => {
      if (swExists) {
        button.innerHTML = 'Unregister ServiceWorker'
        setActionButtonEnabled(true)   
      } else {
        button.innerHTML = 'Register ServiceWorker'
        setActionButtonEnabled(false)
      }
    })
})