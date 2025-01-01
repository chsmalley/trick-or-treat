import os
import cv2
import threading
import asyncio
from collections import OrderedDict
import picamera

from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
from nerf_shooter import main as nerf_main
from pitrack import H264EncodedStreamTrack
from aiortc.rtcrtpparameters import RTCRtpCodecCapability
from rtcrtpsender import RTCRtpSender

FRAME_RATE = 30
CAMERA_RESOLUTION = (640, 480)
BASE_PATH = os.path.dirname(__file__)

audio = None
camera = None

codec_parameters = OrderedDict(
    [
        ("packetization-mode", "1"),
        ("level-asymmetry-allowed", "1"),
        ("profile-level-id", "42001f"),
    ]
)
pi_capability = RTCRtpCodecCapability(
    mimeType="video/H264", clockRate=90000, channels=None, parameters=codec_parameters
)
preferences = [pi_capability]
pcs = set()

class CameraStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        
    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return VideoFrame.from_ndarray(frame, format="rgb24")

async def index(request):
    content = open('index2.html', 'r').read()
    return web.Response(content_type='text/html', text=content)

async def javascript(request):
    content = open(os.path.join(BASE_PATH, "client2.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

async def shoot(request):
    print("running shoot")
    script_thread = threading.Thread(target=nerf_main)
    script_thread.start()
    return web.json_response({"status": "shooting nerf dart..."})

async def offer(request):
    global audio, camera
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    video_track = H264EncodedStreamTrack(FRAME_RATE)
    if not camera:
        camera = picamera.PiCamera()
        camera.resolution = CAMERA_RESOLUTION
        camera.framerate = FRAME_RATE
    else:
        camera.stop_recording()

    camera.start_recording(
        video_track,
        format="h264",
        profile="constrained",
        inline_headers=True,
        sei=False,
    )

    # Read audio stream from `hw:1,0` (via alsa, from card1, device0. see output from `arecord -l`)
    # Please check default Capture volume by `amixer`. You can set Capture volume by `amixer sset 'Capture' 80%`
    try:
        audio = MediaPlayer(
            "hw:1,0", format="alsa", options={"channels": "1", "sample_rate": "44100"}
        )
    except:
        print("Could not open or read audio device.")
        audio = None

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print("ICE connection state is %s" % pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    await pc.setRemoteDescription(offer)
    for t in pc.getTransceivers():
        if t.kind == "audio" and audio and audio.audio:
            pc.addTrack(audio.audio)
        if t.kind == "video" and video_track:
            t.setCodecPreferences(preferences)
            pc.addTrack(video_track)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


if __name__ == "__main__":
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get("/client2.js", javascript)
    app.router.add_post('/offer', offer)
    app.router.add_post('/shoot', shoot)

    web.run_app(app, port=8080)
