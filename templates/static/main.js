var dataChannelLog = document.getElementById('data-channel'),
	iceConnectionLog = document.getElementById('ice-connection-state'),
	iceGatheringLog = document.getElementById('ice-gathering-state'),
	signalingLog = document.getElementById('signaling-state');

// peer connections
var pc = null;

// data channel
var dc = null, dcInterval = null;

function createPeerConnection() {
	var config = { sdpSemantics: 'unified-plan' };
	
	if (document.getElementById('use-stun').checked) {
		config.iceServers = [{ urls: ['stun:stun.l.google.com:19302'] }];
	}

	pc = new RTCPeerConnection(config);

	// register event listeners
	pc.addEventListener('icegatheringstatechange', () => {
		iceGatheringLog.textContent += ' -> ' + pc.iceGatheringState;
	}, false);
	iceGatheringLog.textContent = pc.iceGatheringState;

	pc.addEventListener('iceconnectionstatechange', () => {
		iceConnectionLog.textContent += ' -> ' + pc.iceConnectionState;
	}, false);
	iceConnectionLog.textContent = pc.iceConnectionState;

	pc.addEventListener('signalingstatechange', () => {
		signalingLog.textContent += ' -> ' + pc.signalingState;
	}, false);
	signalingLog.textContent = pc.signalingState;

	// connect audio / video
	pc.addEventListener('track', (evt) => {
	if (evt.track.kind == 'video')
		document.getElementById('video').srcObject = evt.streams[0];
	else
		document.getElementById('audio').srcObject = evt.streams[0];
	});

	return pc;
}

function enumerateInputDevices() {
	const populateSelect = (select, devices) => {
		let counter = 1;
		devices.forEach((device) => {
			const option = document.createElement('option');
			option.value = device.deviceId;
			option.text = device.label || ('Device #' + counter);
			select.appendChild(option);
			counter += 1;
		});
	};

	navigator.mediaDevices.enumerateDevices().then((devices) => {
		populateSelect(
			document.getElementById('audio-input'),
			devices.filter((device) => device.kind == 'audioinput')
		);
		populateSelect(
			document.getElementById('video-input'),
			devices.filter((device) => device.kind == 'videoinput')
		);
	}).catch((e) => {
		alert(e);
	});
}

function negotiate() {
	return pc.createOffer().then((offer) => {
		return pc.setLocalDescription(offer);
	}).then(() => {
		// wait for ICE gathering to complete
		return new Promise((resolve) => {
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
	}).then(() => {
		var offer = pc.localDescription;
		var codec;

		codec = document.getElementById('audio-codec').value;
		if (codec !== 'default') {
			offer.sdp = sdpFilterCodec('audio', codec, offer.sdp);
		}

		codec = document.getElementById('video-codec').value;
		if (codec !== 'default') {
			offer.sdp = sdpFilterCodec('video', codec, offer.sdp);
		}

		document.getElementById('offer-sdp').textContent = offer.sdp;
		console.log(offer);
		
		return fetch('/offer', {
			body: JSON.stringify({
				sdp: offer.sdp,
				type: offer.type,
				// video_transform: document.getElementById('video-transform').value
			}),
			headers: {
				'Content-Type': 'application/json'
			},
			method: 'POST'
		});
	}).then((response) => {
		return response.json();
	}).then((answer) => {
		document.getElementById('answer-sdp').textContent = answer.sdp;
		return pc.setRemoteDescription(answer);
	}).catch((e) => {
		alert(e);
	});
}

function start() {
	document.getElementById('start').style.display = 'none';
	pc = createPeerConnection();
	
	var time_start = null;
	
	const current_stamp = () => {
		if (time_start === null) {
			time_start = new Date().getTime();
			return 0;
		} else {
			return new Date().getTime() - time_start;
		}
	};

	if (document.getElementById('use-datachannel').checked) {
		var parameters = JSON.parse(document.getElementById('datachannel-parameters').value);

		dc = pc.createDataChannel('chat', parameters);
		dc.addEventListener('close', () => {
			clearInterval(dcInterval);
			dataChannelLog.textContent += '- close\n';
		});
		dc.addEventListener('open', () => {
			dataChannelLog.textContent += '- open\n';
			dcInterval = setInterval(() => {
				var message = 'ping ' + current_stamp();
				dataChannelLog.textContent += '> ' + message + '\n';
				dc.send(message);
			}, 1000);
		});
		dc.addEventListener('message', (evt) => {
			dataChannelLog.textContent += '< ' + evt.data + '\n';
			if (evt.data.substring(0, 4) === 'pong') {
				var elapsed_ms = current_stamp() - parseInt(evt.data.substring(5), 10);
				dataChannelLog.textContent += ' RTT ' + elapsed_ms + ' ms\n';
			}
		});
	}

	// Build media constraints.
	const constraints = {
		audio: false,
		video: false
	};

	if (document.getElementById('use-audio').checked) {
		const audioConstraints = {};

		const device = document.getElementById('audio-input').value;
		if (device) {
			audioConstraints.deviceId = { exact: device };
		}
		constraints.audio = Object.keys(audioConstraints).length ? audioConstraints : true;
	}

	if (document.getElementById('use-video').checked) {
		const videoConstraints = {};

		const device = document.getElementById('video-input').value;
		if (device) {
			videoConstraints.deviceId = { exact: device };
		}

		const resolution = document.getElementById('video-resolution').value;
		if (resolution) {
			const dimensions = resolution.split('x');
			videoConstraints.width = parseInt(dimensions[0], 0);
			videoConstraints.height = parseInt(dimensions[1], 0);
		}
		constraints.video = Object.keys(videoConstraints).length ? videoConstraints : true;
	}

	// Acquire media and start negotiation.
	if (constraints.audio || constraints.video) {
		if (constraints.video) {
			document.getElementById('media').style.display = 'block';
		}

		navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
			stream.getTracks().forEach((track) => {
				pc.addTrack(track, stream);
			});
			return negotiate();
		}, (err) => {
			alert('Could not acquire media: ' + err);
		});
	} else {
		negotiate();
	}

	document.getElementById('stop').style.display = 'inline-block';
}

function stop() {
	document.getElementById('stop').style.display = 'none';
		
	// close data channel
	if (dc) {
		dc.close();
	}

	// close transceivers
	if (pc.getTransceivers) {
		pc.getTransceivers().forEach((transceiver) => {
			if (transceiver.stop) {
				transceiver.stop();
			}
		});
	}
	
	// close local audio / video
	pc.getSenders().forEach((sender) => {
		sender.track.stop();
	});

	// close peer connection
	setTimeout(() => {
		pc.close();
	}, 500);
}

	