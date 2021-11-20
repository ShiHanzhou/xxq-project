# -*- coding: utf-8 -*-
'''
用法：
提供对应的人脸收集API，需要传入对应的编号和类别.
之后还需要将对应的数据插入到数据库中，以及即时的反馈信息
'''
import argparse
from detection.facial import FaceUtil
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import shutil
import time

# 全局参数
image_dir = 'D://pythonCharm/Intrusion_detection/images'

action_list = ['blink', 'open_mouth', 'smile', 'rise_head', 'bow_head', 'look_left', 'look_right']
action_map = {'blink': '请眨眼', 'open_mouth': '请张嘴',
              'smile': '请笑一笑', 'rise_head': '请抬头',
              'bow_head': '请低头', 'look_left': '请看左边',
              'look_right': '请看右边'}
collecting_type = ['person']


def CollectingFace(id):

    # 控制参数
    error = 0
    start_time = None
    limit_time = 2  # 2 秒

    # 设置摄像头
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    faceutil = FaceUtil()

    counter = 0
    while True:
        counter += 1
        _, image = cam.read()
        if counter <= 10:  # 放弃前10帧
            continue
        image = cv2.flip(image, 1)

        if error == 1:
            end_time = time.time()
            difference = end_time - start_time
            print(difference)
            if difference >= limit_time:
                error = 0

        face_location_list = faceutil.get_face_location(image)
        for (left, top, right, bottom) in face_location_list:
            cv2.rectangle(image, (left, top), (right, bottom),
                          (0, 0, 255), 2)

        cv2.imshow('Collecting Faces', image)  # show the image
        # Press 'ESC' for exiting video
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break

        face_count = len(face_location_list)
        if error == 0 and face_count == 0:  # 没有检测到人脸
            print('[WARNING] 没有检测到人脸')
            error = 1
            start_time = time.time()
        elif error == 0 and face_count == 1:  # 可以开始采集图像了
            print('[INFO] 可以开始采集图像了')
            break
        elif error == 0 and face_count > 1:  # 检测到多张人脸

            error = 1
            start_time = time.time()
        else:
            pass

    # 新建目录
    if os.path.exists(os.path.join(image_dir,id)):
        shutil.rmtree(os.path.join(image_dir, id), True)
    os.mkdir(os.path.join(image_dir, id))

    # 开始采集人脸
    for action in action_list:
        action_name = action_map[action]

        counter = 1
        for i in range(15):
            print('%s-%d' % (action_name, i))
            _, img_OpenCV = cam.read()
            img_OpenCV = cv2.flip(img_OpenCV, 1)
            origin_img = img_OpenCV.copy()  # 保存时使用

            face_location_list = faceutil.get_face_location(img_OpenCV)
            for (left, top, right, bottom) in face_location_list:
                cv2.rectangle(img_OpenCV, (left, top),
                              (right, bottom), (0, 0, 255), 2)

            img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV,
                                                   cv2.COLOR_BGR2RGB))

            # 转换回OpenCV格式
            img_OpenCV = cv2.cvtColor(np.asarray(img_PIL),
                                      cv2.COLOR_RGB2BGR)

            cv2.imshow('Collecting Faces', img_OpenCV)  # show the image

            image_name = os.path.join(image_dir,id, action + '_' + str(counter) + '.jpg')
            cv2.imwrite(image_name, origin_img)
            # Press 'ESC' for exiting video
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break
            counter += 1

    # 结束
    print('[INFO] 采集完毕')
    time.sleep(4)
    # 释放全部资源
    cam.release()
    cv2.destroyAllWindows()


CollectingFace("sxd")