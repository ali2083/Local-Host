import numpy as np
from flask import (
    Blueprint, render_template, request, redirect, session, flash, url_for, jsonify, Response
)
from aiortc import RTCPeerConnection, RTCSessionDescription
import cv2
import json
import uuid
import asyncio
import logging
import time
import pyautogui

bp = Blueprint('stream', __name__)


def screen_frames():
    while True:
        start_time = time.time()

        image = pyautogui.screenshot()
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ret, buffer = cv2.imencode('.png', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        elapsed_time = time.time() - start_time
        logging.debug(f"Frame generation time: {elapsed_time} seconds")


def generate_frames():
    camera = cv2.VideoCapture(0)  # ==============IMPORTANT============
    while True:
        start_time = time.time()
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # concat frame one by one and show result
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            elapsed_time = time.time() - start_time
            logging.debug(f"Frame generation time: {elapsed_time} seconds")


async def offer_async():
    params = await request.json
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    # Create an RTCPeerConnection instance
    pc = RTCPeerConnection()

    # Generate a unique ID for the RTCPeerConnection
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pc_id = pc_id[:8]

    # Create and set the local description
    await pc.createOffer(offer)
    await pc.setLocalDescription(offer)

    # Prepare the response data with local SDP and type
    response_data = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

    return jsonify(response_data)


def offer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    future = asyncio.run_coroutine_threadsafe(offer_async(), loop)
    return future.result()


@bp.route('/offer', methods=['POST'])
def offer_route():
    return offer()


@bp.route('/stream', methods=['GET', 'POST'])
def stream():
    return render_template('stream.html')


@bp.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@bp.route('/screen_feed')
def screen_feed():
    return Response(screen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
