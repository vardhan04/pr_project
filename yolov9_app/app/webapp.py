
import argparse
import io
from PIL import Image
import datetime

import torch
import cv2
import numpy as np
import tensorflow as tf
from re import DEBUG, sub
import requests
import shutil
import time
import glob
import subprocess
from flask import Flask, render_template, request, redirect, send_file, Response, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
from subprocess import Popen
import re
from ultralytics import YOLO


app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')

    
@app.route("/", methods=["GET", "POST"])
def predict_img():
    f = None
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath,'uploads',f.filename)
            f.save(filepath)
            global imgpath
            predict_img.imgpath = f.filename
            print(predict_img)
                                               
            file_extension = f.filename.rsplit('.', 1)[1].lower() 
            
            if file_extension == 'jpg' or file_extension == 'png' or file_extension == 'jpeg':
                img = cv2.imread(filepath)
                #model = YOLO('yolov9c.pt')
                #model = YOLO('best1.pt')
                #model = YOLO('../../obtained_runs/detect/train/weights/best.pt')
                # Determine which model to use based on user selection
                model_type = request.form['model']
                if model_type == 'regular':
                    model_path = '../../obtained_runs/detect/train/weights/best.pt'
                elif model_type == 'enhanced':
                    img = enhance_image(img)
                    model_path = '../../enhanced_runs/detect/train/weights/best.pt'
                else:
                    return "Invalid model selection"
                model = YOLO(model_path)
                detections =  model(img, save=True) 
                return display(f.filename)
            else:
                print("Unsupported File format, please check the image format.")        

       
    # folder_path = 'runs/detect'
    # subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    # latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    # image_path = folder_path+'/'+latest_subfolder+'/'+f.filename 
    # return render_template('index.html', image_path=image_path)
    #return "done"

    if f:
        folder_path = 'runs/detect'
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
        latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
        image_path = folder_path+'/'+latest_subfolder+'/'+f.filename 
        return render_template('index.html', image_path=image_path)

    return render_template('index.html')

def enhance_image(image):
    # Applying gamma correction to adjust brightness
    gamma = 1.2  # Reduced gamma value to avoid over-brightening
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]).astype("uint8")
    adjusted = cv2.LUT(image, table)

    # Converting to LAB color space
    lab = cv2.cvtColor(adjusted, cv2.COLOR_BGR2LAB)

    # Splitting into channels
    l, a, b = cv2.split(lab)

    # Applying CLAHE to the L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    # Merging the CLAHE enhanced L-channel back with A and B channels
    limg = cv2.merge((cl, a, b))

    # Converting back to BGR color space
    enhanced_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Sharpening the image
    kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
    sharpened = cv2.filter2D(enhanced_image, -1, kernel)

    # Applying slight Gaussian blur to reduce noise
    final_image = cv2.GaussianBlur(sharpened, (3, 3), 0)

    return final_image


# #The display function is used to serve the image or video from the folder_path directory.
@app.route('/<path:filename>')
def display(filename):
    folder_path = 'runs/detect'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    directory = folder_path+'/'+latest_subfolder    
    print("printing directory: ",directory) 
    files = os.listdir(directory)
    latest_file = files[0]
    
    print(latest_file)

    filename = os.path.join(folder_path, latest_subfolder, latest_file)

    file_extension = filename.rsplit('.', 1)[1].lower()

    environ = request.environ
    if file_extension == 'jpg' or file_extension == 'png' or file_extension == 'jpeg':      
        return send_from_directory(directory,latest_file,environ)

    else:
        return "Invalid file format"


# # function to display the detected objects video on html page
@app.route("/video_feed")
def video_feed():
    pass
        
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov8 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    #model = YOLO('yolov9c.pt')
    #model = YOLO('best1.pt')
    model = YOLO('../../obtained_runs/detect/train/weights/best.pt')
    app.run(host="0.0.0.0", port=args.port) 
