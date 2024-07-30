import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pygame
from datetime import datetime
import cv2
import dlib
import time
import numpy as np
from scipy.spatial import distance as dist
from scipy.spatial.distance import cdist
from imutils import face_utils
import sqlite3
from flask import Flask, render_template, Response, request

app = Flask(__name__)
camera = cv2.VideoCapture(0)

Blink, yawn = 0, 0

insert_query = '''
        INSERT INTO Face_Recognition_data_status(Trip_ID, Timestamp, Eye_Hull, Lip_Hull)
        VALUES (?, ?, ?, ?)
'''

insert_query1 = """
        INSERT INTO Face_Recognition_data_submit(Trip_ID, Timestamp, Blink, Yawn) 
        VALUES (?, ?, ?, ?)
"""

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def lip_distance(shapes):
    top_lip = np.hstack((shapes[50:53], shapes[61:64]))
    low_lip = np.hstack((shapes[56:59], shapes[65:68]))
    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)
    distance = cdist([top_mean], [low_mean], metric='euclidean')[0, 0]
    return distance

def play_alert_sound():
    pygame.mixer.init()
    alert_sound = pygame.mixer.Sound("assets/music.wav")
    return alert_sound.play()


threshold = 0.25
frame_check = 20
frame_lip = 55
timestamp_value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("assets/shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS['right_eye']

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global Blink, yawn
    flag = 0
    conn = sqlite3.connect("db.sqlite3")
    last = 0
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = cv2.resize(frame, (860, 640))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEar = eye_aspect_ratio(leftEye)
            rightEar = eye_aspect_ratio(rightEye)
            ear = (leftEar + rightEar) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            distance = lip_distance(shape)
            lip = shape[48:60]
            cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)
            if ear < threshold:
                flag += 1
                cv2.putText(frame, "******Blink******", (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                if flag >= frame_check:
                    if time.time() - last > 6:
                        Blink += 1  # Increment Blink count
                        last = time.time()
                    cv2.putText(frame, "******Drowsy******", (330, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    play_alert_sound()
                    conn.execute(insert_query, (Trip_ID, timestamp_value, flag, distance))
                    conn.commit()
            else:
                flag = 0
            if distance >= frame_lip:
                if time.time() - last > 6:
                        yawn += 1  # Increment Yawn count
                        last = time.time()
                cv2.putText(frame, "*Yawning*", (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    conn.close()

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['POST'])
def getvalue():
    global  Trip_ID
    Trip_ID = request.form['ID']
    return render_template('pass.html', I=Trip_ID)

@app.route('/store_data', methods=['POST'])
def store_data():
    global Trip_ID, Blink, yawn, timestamp_value
    file = open("DriverSessionDetails.txt", "w+")
    file.write("\t\t\t\tDriverMonitoringSystemForTravelAgencies\n")
    file.write("\Transport Trip Id : " + Trip_ID + "\n")
    file.write("\nNumber of times felt sleepy:" + str(Blink) + "\n")
    file.write("\nNumber of times yawned:" + str(yawn) + "\n")
    file.write("\nAmount of time felt sleepy:-" + str(timestamp_value))
    file.close()
    return render_template('pass.html')

@app.route('/send_email', methods=['POST'])
def send_email_controller():
    global  Trip_ID, Blink, yawn, timestamp_value
    conn = sqlite3.connect("db.sqlite3")
    conn.execute(insert_query1, (Trip_ID, timestamp_value, Blink, yawn))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Face_Recognition_data_submit ORDER BY ID DESC LIMIT 1')
    last_driver_submit = cursor.fetchone()
    conn.commit()
    sender_email = 'seeramsrinivas1@gmail.com'
    sender_password = 'ifxh qzfy kgjf fqpz'  # replace with your actual password
    recipient_email = 's180094@rguktsklm.ac.in'  # replace with recipient email
    subject = 'Driver Monitoring System'
    message = 'Hello, please find attachments containing the session details'
    attachments = ["DriverSessionDetails.txt",]
    send_email(sender_email, sender_password, recipient_email, subject, message, attachments)
    return render_template('Data.html', last_driver_submit=last_driver_submit)

def send_email(sender_email, sender_password, recipient_email, subject, message, attachments=[]):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment}")
        msg.attach(part)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)