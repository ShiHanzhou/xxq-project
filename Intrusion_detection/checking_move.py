import base64
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import paramiko
from Demos.security.sspi import socket_server

from detection.track import CentroidTracker
from detection.track import TrackableObject
from imutils.video import FPS
import numpy as np
import imutils
import argparse
import time
import cv2
import os
import dlib
import socket
import json
import Email
import compare
import threading
import pymysql
import datetime

path1 = r"D:\PythonCharm\Intrusion_detection\Image"
size = [125, 47, 375, 234]
num = len([lists for lists in os.listdir(path1) if os.path.isfile(os.path.join(path1, lists))])


def recvlink(client):
    while True:

        recevinfoa = client.recvfrom(1024)
        global size
        size_str = recevinfoa[0].decode('utf-8')
        size = list(str(size_str).split())
        for i in range(len(size)):
            size[i] = int(size[i])


def connect():
    while True:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host = '192.168.0.110'
        # 设置被监听的端口号,小于1024的端口号不能使用，因为他们是Internet标准服务的端口号
        port = 5354
        # 绑定地192.168.0.114址
        socket_server.bind((host, port))
        socket_server.listen(5)
        global clientsocket
        clientsocket, addr = socket_server.accept()
        clientsocket.send('success'.encode('utf-8'))
        # 和客户端一样开启一个线程接受客户端的信息
        t = threading.Thread(target=recvlink, args=(clientsocket,))
        t.start()
        print('已连接')


def checking():
    # 得到当前时间
    current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(time.time()))
    print('[INFO] %s 禁止区域检测程序启动了.' % current_time)

    # 传入参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required=False, default='',
                    help="")
    args = vars(ap.parse_args())

    # 全局变量
    prototxt_file_path = 'models/mobilenet_ssd/MobileNetSSD_deploy.prototxt'
    model_file_path = 'models/mobilenet_ssd/MobileNetSSD_deploy.caffemodel'
    output_fence_path = 'supervision/image'
    skip_frames = 15  # of skip frames between detections
    python_path = '/home/reed/anaconda3/envs/tensorflow/bin/python'

    # minimum probability to filter weak detections
    minimum_confidence = 0.6

    # 物体识别模型能识别的物体（21种）
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair",
               "cow", "diningtable", "dog", "horse", "motorbike",
               "person", "pottedplant", "sheep", "sofa", "train",
               "tvmonitor"]

    print("[INFO] starting video stream...")

    vs = cv2.VideoCapture('yard_01.mp4')
    quality = 40  # 图像的质量
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    time.sleep(2)

    # 加载物体识别模型
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(prototxt_file_path, model_file_path)

    W = None
    H = None

    ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
    trackers = []
    trackableObjects = {}

    totalFrames = 0
    totalDown = 0

    # start the frames per second throughput estimator
    fps = FPS().start()
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # loop over frames from the video stream

    while True:
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=500)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if W is None or H is None:
            (H, W) = frame.shape[:2]
        status = "Waiting"
        rects = []

        if totalFrames % skip_frames == 0:
            status = "Detecting"
            trackers = []
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            net.setInput(blob)
            detections = net.forward()

            for i in np.arange(0, detections.shape[2]):

                # extract the confidence (i.e., probability) associated with the prediction
                confidence = detections[0, 0, i, 2]
                if confidence > minimum_confidence:
                    idx = int(detections[0, 0, i, 1])

                    if CLASSES[idx] != "person":
                        continue

                    box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    (startX, startY, endX, endY) = box.astype("int")

                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)
                    trackers.append(tracker)

        else:
            for tracker in trackers:
                # set the status of our system to be 'tracking' rather than 'waiting' or 'detecting'
                status = "Tracking"
                # update the tracker and grab the updated position
                tracker.update(rgb)
                pos = tracker.get_position()

                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())

                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 255, 0), 2)

                # add the bounding box coordinates to the rectangles list
                rects.append((startX, startY, endX, endY))

        (X1, Y1, X2, Y2) = (size[0], size[1], size[2], size[3])
        cv2.rectangle(frame, (X1, Y1), (X2, Y2),
                      (0, 0, 255), 2)

        objects = ct.update(rects)
        i = 0
        for (objectID, centroid) in objects.items():
            to = trackableObjects.get(objectID, None)
            # if there is no existing trackable object, create one
            if to is None:
                to = TrackableObject(objectID, centroid)

            else:
                to.centroids.append(centroid)

                if not to.counted:

                    if Y1 < centroid[1] < Y2 and X1 < centroid[0] < X2:

                        to.counted = True

                        cv2.imwrite(
                            os.path.join(output_fence_path, 'pic.jpg'),
                            frame)  # snapshot
                        #str = compare.compare('D:/pythonCharm/Intrusion_detection/supervision/image/pic.jpg')
                        #t6 = threading.Thread(target=compare.compare, args=('D:/pythonCharm/Intrusion_detection/supervision/image/pic.jpg',))
                        #t6.start()
                        totalDown += 1
                        current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(time.time()))
                        print('[EVENT] %s, 院子, 有人闯入禁止区域!!!' % current_time)
                        t3 = threading.Thread(target=Email.sendpic)
                        t4 = threading.Thread(target=Email.Email)

                        t3.start()
                        t4.start()



            trackableObjects[objectID] = to
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4,
                       (0, 255, 0), -1)

        info = [
            # ("Up", totalUp),
            ("Down", totalDown),
            ("Status", status),
        ]

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # show the output frame
        cv2.imshow("Prohibited Area", frame)
        try:
            img_encode = cv2.imencode(".jpg", frame, encode_param)[1]
            data_encode = np.array(img_encode)
            str_encode = data_encode.tobytes()
            clientsocket.send(str_encode)
        except:
            pass

        k = cv2.waitKey(15) & 0xff
        if k == 27:
            break

        totalFrames += 1
        fps.update()

    fps.stop()
    vs.release()
    cv2.destroyAllWindows()


def recvpic():
    try:
        cout = 1
        global num
        len = num

        conn = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', port=3306, user='root',
                               passwd='POiu0987', db='shi_pin_xxq', charset='utf8')
        print('successfully connect')

        cursor = conn.cursor()
        sql = "SELECT photo FROM face_recognize"  # 将数据插入到mysql数据库中，指令
        cursor.execute(sql)

        for row in cursor.fetchall():
            for pic in row:
                if cout > len:
                    img = base64.b64decode(pic)
                    num = num + 1
                    fh = open("D:/pythonCharm/Intrusion_detection/Image/img_{}.jpg".format(num), "wb")
                    fh.write(img)
                cout = cout + 1

        conn.commit()  # 更新数据库
        cursor.close()
        conn.close()
    except Exception as e:
        print("读取失败", e)


t1 = threading.Thread(target=connect)

t2 = threading.Thread(target=checking)

t3 = threading.Thread(target=recvpic)

t1.start()
t2.start()
t3.start()
