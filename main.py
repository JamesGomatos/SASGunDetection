from flask import Flask,redirect, render_template, request, url_for, redirect
import os 
import json
import cv2
import swat
import pandas as pd


app = Flask(__name__)

# app vars:
cas_library = "AI" # name of the CAS library in which this astore model is stored

@app.route("/")
def main():
    return render_template('home.html', domain='http://ec2-18-206-15-177.compute-1.amazonaws.com')


@app.route("/work")
def work():
    return render_template('work.html', domain='http://ec2-18-206-15-177.compute-1.amazonaws.com')
    
  
@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    
    
    if not os.path.isdir(target):
        os.mkdir(target)
        
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    
    print(destination)
    # connect to ESP
    esp = esppy.ESP('http://ec2-18-206-15-177.compute-1.amazonaws.com:23456')
    
    projects = esp.get_projects()
    project = projects['ImageScoring']
    
    score_files = destination
    glob.glob(score_files)
    


    print("executed")
    # connect to img_src window and publish images
    img_src = project['cq1']['img_src']
    img_pub = img_src.create_publisher()

    scr_win = project['cq1']['score']
    img_sub = scr_win.create_subscriber()
    scr_win.subscribe(mode='updating',limit=1)

    for ID, img_filename in enumerate(glob.glob(score_files)):
        with open(img_filename, 'rb') as img_file:
            img_string = base64.b64encode(img_file.read())
        img_pub.send(f'i,n,{ID},{img_string.decode()}\n')
        time.sleep(1)
        urlll = img_sub.url
        print(urlll)
    
    dd = scr_win.data["Predicted"]
  
    return render_template("complete.html",domain='https://ec2-18-206-15-177.compute-1.amazonaws.com')
    
if __name__ == "__main__":
    DEBUG = False
    
     #import packages
    import sys, glob, base64, time
    sys.path.append('/ai2018/computer-vision/python-esp-master')
    import esppy

    
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    
    
    #scr_win = project['cq1']['score']
    #img_sub = scr_win.create_subscriber()
    
    
    # img_sub.subscribe()
    app.run(host="ec2-18-206-15-177.compute-1.amazonaws.com",ssl_context=('cert.pem', 'key.pem'), port=7003)