async function shoot() {
    const response = await fetch('/shoot', {
        method: 'POST'
    });
    const result = await response.json();
    document.getElementById('scriptStatus').textContent = result.status;
}

async function startStream() {
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
window.onload = startStream;
