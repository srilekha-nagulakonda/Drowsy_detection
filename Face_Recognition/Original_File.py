import dlib
import cv2
import math
import pyaudio
import wave
import numpy as np
import time
from imutils import face_utils
"""Importing necessary libraries for sending mails"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

Name = input("Please enter your name : ")
EmpId = input("Enter employee ID : ")
SessionStart = time.time()
SessionStart1 = time.ctime(SessionStart)

cap = cv2.VideoCapture(0)
detect = dlib.get_frontal_face_detector()
face_predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

blink_times = []
# To track the timestamp of eye blinks
yawn_times = []
# To track the timestamp of yawning
sleep_times = []
# To track the timestamp of sleep

blink_times1 = []
# To track the timestamp of eye blinks
yawn_times1 = []
# To track the timestamp of yawning
sleep_times1 = []
# To track the timestamp of sleep

amount_of_time_felt_asleep = 0  # To track total amount of time slept
sleep = 0
sleep_start = time.time()  # to capture sleep instance start
sleep_end = time.time()  # to capture sleep instance end
drowsy = 0
hours = 0
minutes = 0
seconds = 0
active = 0
blink_count = 0
yawn_count = 0
no_of_blinks = 0
no_of_yawns = 0
status = ""
no_of_sleeps = 0
color = (0, 0, 0)
blink_threshold = 10
yawn_threshold = 40
last_blink_time = time.time()
last_yawn_time = time.time()
prev = ""


def compute(p1, p2):
    p1_to_p2_distance = np.linalg.norm(p1 - p2)
    return p1_to_p2_distance


def check_blinking(p1, p2, p3, p4, p5, p6):
    top = compute(p2, p4) + compute(p3, p5)
    bottom = compute(p1, p6)
    r = top / (2.0 * bottom)
    if r < 0.21:
        return 0
    elif 0.21 < r <= 0.25:
        return 1
    else:
        return 2


def is_mouth_opened(landmarks):
    lip_upper = landmarks[50:53]
    lip_upper_mean = np.mean(lip_upper, axis=0)
    lip_lower = landmarks[56:59]
    lip_lower_mean = np.mean(lip_lower, axis=0)
    distance = np.abs(lip_upper_mean[1] - lip_lower_mean[1])
    return distance > 25


def play_alert_sound():
    wf, p = wave.open("assets/music.wav", 'rb'), pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)
    while data := wf.readframes(1024):
        stream.write(data)
    stream.stop_stream(), stream.close(), p.terminate()


def CALC_HOURLY_CLASSIFICATION(data, start, end):
    hour = math.ceil((end - start) / 3600)
    Lists = []
    for ii in range(hour):
        Min = 0
        Max = 0
        for j in range(len(data)):
            if data[j] >= (start + 3600 * ii):
                Min = j
                break
        for k in range(Min, len(data)):
            if data[k] < (start + 3600 * (ii + 1)):
                Max = k
        if Max >= Min:
            Lists.append(Max - Min + 1)
        else:
            Lists.append(0)
    return Lists


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect(gray)
    face_frame = frame.copy()

    # f denote face

    for f in faces:
        y1 = f.top()
        y2 = f.bottom()
        x1 = f.left()
        x2 = f.right()

        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks_in_face = face_predict(gray, f)
        landmarks_in_face = face_utils.shape_to_np(landmarks_in_face)

        left_blink = check_blinking(landmarks_in_face[36], landmarks_in_face[37], landmarks_in_face[38],
                                    landmarks_in_face[41], landmarks_in_face[40], landmarks_in_face[39])
        right_blink = check_blinking(landmarks_in_face[42], landmarks_in_face[43], landmarks_in_face[44],
                                     landmarks_in_face[47], landmarks_in_face[46], landmarks_in_face[45])
        mouth_open = is_mouth_opened(landmarks_in_face)

        if left_blink == 0 or right_blink == 0:
            if sleep == 0:
                sleep_start = time.time()
            sleep += 1
            drowsy = 0
            active = 0
            blink_count += 1
            if sleep > blink_threshold:
                sleep_end = time.time()
                status = "SLEEPING !!!"
                sleep_times.append(time.ctime(sleep_end))
                sleep_times1.append(sleep_end)
                no_of_sleeps += 1
                sleep = 0  # made modification at 14:16
                amount_of_time_felt_asleep += (sleep_end - sleep_start)
                color = (255, 0, 0)
                # playsound('/Users/charan/Desktop/Hari/alert.wav')  # Play the alert sound
                play_alert_sound()
        elif left_blink == 1 or right_blink == 1:
            sleep = 0
            active = 0
            drowsy += 1
            if drowsy > 6:
                status = "Drowsy !"
                # play_alert_sound()
                color = (0, 0, 255)
        else:
            drowsy = 0
            sleep = 0
            active += 1
            if active > 6:
                status = "Active :)"
                color = (0, 255, 0)

        if mouth_open:
            yawn_count += 1
            last_yawn_time = time.time()

        if time.time() - last_blink_time > 20:
            blink_count = 0
        if time.time() - last_yawn_time > 5:
            yawn_count = 0

        if blink_count >= blink_threshold and status != "SLEEPING !!!":
            print("Blinked eyes detected!")
            no_of_blinks += 1
            blink_count = 0
            last_blink_time = time.time()
            blink_times.append(time.ctime(last_blink_time))
            blink_times1.append(last_blink_time)

        if yawn_count >= yawn_threshold:
            print("Yawn detected!")
            yawn_count = 0
            no_of_yawns += 1
            last_yawn_time = time.time()
            yawn_times1.append(last_yawn_time)
            yawn_times.append(time.ctime(last_yawn_time))

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks_in_face[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:
        print("Number of times felt sleepy:", no_of_sleeps)
        print("Number of times blinked eyes:", no_of_blinks)
        print("Number of times yawned:", no_of_yawns)
        print("Number of  minutes felt asleep:", end=" ")
        hours = amount_of_time_felt_asleep // 3600
        amount_of_time_felt_asleep = amount_of_time_felt_asleep - hours * 3600
        minutes = amount_of_time_felt_asleep // 60
        amount_of_time_felt_asleep = amount_of_time_felt_asleep - minutes * 60
        seconds = amount_of_time_felt_asleep
        print(hours, "Hours ", minutes, "Minutes ", seconds, "seconds.")
        SessionEnd = time.time()
        SessionEnd1 = time.ctime(SessionEnd)
        break

cap.release()
cv2.destroyAllWindows()

file = open("DriverSessionDetails.txt", "w+")
file.write("\t\t\t\tDriverMonitoringSystemForTravelAgencies\n")
file.write("\nName of the driver : " + Name + "\n")
file.write("\nDriver Employee Id : " + EmpId + "\n")
file.write("\nSession started at" + str(SessionStart1))
file.write("\nSession ended at" + str(SessionEnd1))
file.write("\nNumber of times felt sleepy:" + str(no_of_sleeps) + "\n")
file.write("\nNumber of times blinked eyes:" + str(no_of_blinks) + "\n")
file.write("\nNumber of times yawned:" + str(no_of_yawns) + "\n")
file.write("\nAmount of time felt sleepy" + str(hours) + "Hours" + str(minutes) + "Minutes" + str(seconds) + "Seconds")

SleepTimesfile = open("sleeptimes.txt", "w+")
YawnTimesfile = open("yawntimes.txt", "w+")
BlinkTimesfile = open("blinktimes.txt", "w+")

if len(sleep_times) == 0:
    SleepTimesfile.write("No sleeping instances recorded")
if len(yawn_times) == 0:
    YawnTimesfile.write("No Yawning instances recorded ")
if len(blink_times) == 0:
    BlinkTimesfile.write("No Blinking instances recorded")

SleepTimesfile.write("\n\nSleeptimes\n\n")
for i in sleep_times:
    SleepTimesfile.write(str(i) + "\n")
YawnTimesfile.write("\n\nyawntimes\n\n")
for i in yawn_times:
    YawnTimesfile.write(str(i) + "\n")
BlinkTimesfile.write("\n\nblinktimes\n\n")
for i in blink_times:
    BlinkTimesfile.write(str(i) + "\n")

SleepTimesfile.close()
YawnTimesfile.close()
BlinkTimesfile.close()

time_of_driving = SessionEnd - SessionStart
Hours_of_driving = time_of_driving // 3600
file.write("\n\nNote:\n\n")
# no of yawns threshold 3 per hour , and 5 per hour for blinks
if no_of_sleeps > 0 and no_of_yawns > (3 * Hours_of_driving) and no_of_blinks > (5 * Hours_of_driving):
    file.write(
        "Drivers didn't driving carefully, It look like he didn't had proper sleep, it may dangerous for passangers.\n "
        "He is not good fit for driving")
elif no_of_sleeps > 0 and no_of_yawns > (3 * Hours_of_driving):
    file.write(
        "Drivers feeling drowsy more than usual.\n Can be eligible for driving short distances with some more attention")
elif no_of_sleeps > 0 and no_of_blinks > (5 * Hours_of_driving):
    file.write(
        "Drivers feeling drowsy more than usual.\n Can be eligible for driving short distances with some more attention")
elif no_of_yawns > (3 * Hours_of_driving) and no_of_blinks > (5 * Hours_of_driving):
    file.write(
        "Drivers feeling drowsy more than usual.\n Can be eligible for driving short distances with some more attention")
elif no_of_sleeps > 0:
    file.write("Driver felt sleepy in session out of it remaining is fine, can be sent to short drives with attention")
elif no_of_yawns > (3 * Hours_of_driving) or no_of_blinks > (5 * Hours_of_driving):
    file.write("Suitable for short drives and can be sent to long drives if some more attention possessed")
else:
    file.write("Driver is absolutely fine and He is good fit for long drives")

yawn_classification = CALC_HOURLY_CLASSIFICATION(yawn_times1, SessionStart, SessionEnd)
for i in range(len(yawn_classification)):
    file.write("No of yawns in hour" + str(i + 1) + " : " + str(yawn_classification[i]) + '\n')
blink_classification = CALC_HOURLY_CLASSIFICATION(blink_times1, SessionStart, SessionEnd)
for i in range(len(blink_classification)):
    file.write("No of blinks in hour" + str(i + 1) + " : " + str(blink_classification[i]) + '\n')
sleep_classification = CALC_HOURLY_CLASSIFICATION(sleep_times1, SessionStart, SessionEnd)
for i in range(len(sleep_classification)):
    file.write("No of sleeps in hour" + str(i + 1) + " : " + str(sleep_classification[i]) + "\n")

file.close()


def send_email(sender_email, sender_password, recipient_email, subject, message, attachments=None):
    # Create the email message
    if attachments is None:
        attachments = []
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add the message body
    msg.attach(MIMEText(message, 'plain'))

    # Add attachments, if any
    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment}")
        msg.attach(part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


# Example usage
sender_email = 'seeramsrinivas1@gmail.com'
sender_password = 'ifxh qzfy kgjf fqpz'
recipient_email = 's180094@rguktsklm.ac.in'
subject = 'DriverMonitoringSystem'
message = 'Hello, please find attachments containing the session details'
attachments = ["DriverSessionDetails.txt", "sleeptimes.txt", "yawntimes.txt", "blinktimes.txt"]

send_email(sender_email, sender_password, recipient_email, subject, message, attachments)
