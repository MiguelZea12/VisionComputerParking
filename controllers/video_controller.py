from flask import Blueprint, Response, request, jsonify
from services.video_service import generate_frames, video_state

video_controller = Blueprint('video_controller', __name__)

@video_controller.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@video_controller.route('/control_video', methods=['POST'])
def control_video():
    action = request.json.get('action')
    if action == "play":
        video_state["play"] = True
    elif action == "pause":
        video_state["play"] = False
    elif action == "restart":
        video_state["play"] = True
    return jsonify(status="success", state=video_state)
