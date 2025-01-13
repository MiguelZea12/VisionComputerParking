from flask import Flask, Response, render_template, jsonify, request
from flask_cors import CORS
import random
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
from services.parking_service import process_frame

video_state = {"play": True}

def generate_frames():
    cap = cv2.VideoCapture('parking1.mp4')  
    delay = 0.3  

    while True:
        if video_state["play"]:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
                continue

            frame = process_frame(frame) 
            ret, buffer = cv2.imencode('.jpg', frame)  
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            time.sleep(delay)
        else:
            time.sleep(0.1) 

