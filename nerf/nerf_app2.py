import cv2
import threading
import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
from nerf_shooter import main as nerf_main

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
    params = await request.json()
    offer = RTCSessionDescription(sdp=params['sdp'], type=params['type'])

    pc = RTCPeerConnection()
    pc.addTrack(CameraStreamTrack())

    @pc.on("icegatheringstatechange")
    async def on_icegatheringstatechange(event):
        if pc.iceGatheringState == "complete":
            iceGatheringCompleted.set()

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    
    return web.json_response({
        'sdp': pc.localDescription.sdp,
        'type': pc.localDescription.type
    })


if __name__ == "__main__":
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_get("/client2.js", javascript)
    app.router.add_post('/offer', offer)
    app.router.add_post('/shoot', shoot)

    web.run_app(app, port=8080)
