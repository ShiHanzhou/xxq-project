# encoding:utf-8
from detection.facial import FaceUtil
import os
import re
import urllib.request
import json
import base64
import tkinter.messagebox
import ast
import time

import cv2

'''
人脸对比
'''


def compare(path):
    judge = True
    count = 0
    n = 0
    list = []
    faceutil = FaceUtil()

    def read_directory(directory_name):
        for filename in os.listdir(directory_name):
            img = directory_name + "/" + filename
            list.append(img)

    read_directory("D:/pythonCharm/Intrusion_detection/Image")
    while judge:
        if count == len(list):
            break
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
        filename1 = list[count]
        filename2 = path
        f = open(filename1, 'rb')
        f2 = open(filename2, 'rb')
        img_test1 = base64.b64encode(f.read())
        img_test2 = base64.b64encode(f2.read())

        image = cv2.imread(filename2)
        face_location_list = faceutil.get_face_location(image)
        for (left, top, right, bottom) in face_location_list:
            cv2.rectangle(image, (left, top), (right, bottom),
                          (0, 0, 255), 2)
        #cv2.imshow('faces', image)
        #cv2.waitKey(0)
        face_count = len(face_location_list)
        if face_count == 0:  # 没有检测到人脸
            print('[WARNING] 没有检测到人脸')

            return '无人脸'

        params = json.dumps(
            [{"image": '' + str(img_test1, 'utf-8') + '', "image_type": "BASE64", "face_type": "LIVE",
              "quality_control": "NONE"},
             {"image": '' + str(img_test2, 'utf-8') + '', "image_type": "BASE64", "face_type": "LIVE",
              "quality_control": "NONE"}])

        access_token = '24.876b4dce2d0b344fc3e9992bf0773139.2592000.1629819230.282335-24602668'
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params.encode("utf-8"))
        request.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(request)
        content = response.read()
        if content:
            print(content)
        content = content.decode("utf-8")
        content = ast.literal_eval(content)
        # tkinter.messagebox.showinfo('图片相似度', "两个人的相似度为：%d" % content['result']['score'] + "%")
        count += 1
        if content['result']['score'] > 70:
            print('11111111')
            result = re.split('[/.]', list[count - 1])
            judge = False
            return result[5]

    return '陌生人'
