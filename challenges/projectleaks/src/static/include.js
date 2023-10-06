host = document.location.origin
window.addEventListener("DOMContentLoaded", function() {
    frame = document.createElement('iframe')
    frame.src = host+'/note'
    frame.setAttribute('sandboxed','')
    document.body.appendChild(frame)

    // frame = document.getElementById('frame')
    // frame.src = host + '/note'
    // frame.setAttribute('sandboxed','')

}, false);
