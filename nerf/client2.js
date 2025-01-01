async function shoot() {
    const response = await fetch('/shoot', {
        method: 'POST'
    });
    const result = await response.json();
    document.getElementById('scriptStatus').textContent = result.status;
}


function negotiate() {
    pc.addTransceiver('video', {direction: 'recvonly'});
    pc.addTransceiver('audio', {direction: 'recvonly'});
    return pc.createOffer().then(function(offer) {
        return pc.setLocalDescription(offer);
    }).then(function() {
        // wait for ICE gathering to complete
        return new Promise(function(resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function() {
        var offer = pc.localDescription;
        return fetch('/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then(function(response) {
        return response.json();
    }).then(function(answer) {
        return pc.setRemoteDescription(answer);
    }).catch(function(e) {
        alert(e);
    });
}

async function startStream() {
    // var config = {
    //     sdpSemantics: 'unified-plan'
    // };

    // pc = new RTCPeerConnection(config);

    // // connect audio / video
    // pc.addEventListener('track', function(evt) {
    //     if (evt.track.kind == 'video') {
    //         document.getElementById('video').srcObject = evt.streams[0];
    //     } else {
    //         document.getElementById('audio').srcObject = evt.streams[0];
    //     }
    // });
    
    // negotiate();


    const pc = new RTCPeerConnection();
    pc.addTransceiver('video', { direction: 'recvonly' });

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    const response = await fetch('/offer', {
        method: 'POST',
        body: JSON.stringify(pc.localDescription)
    });

    const answer = await response.json();
    await pc.setRemoteDescription(answer);

    pc.ontrack = function(event) {
        document.getElementById('video').srcObject = event.streams[0];
    };
}

document.getElementById('shootButton').addEventListener('click', shoot);
document.getElementById('startButton').addEventListener('click', startStream);
window.onload = startStream;
