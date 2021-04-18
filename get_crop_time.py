#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np



def is_gray(image):
    height, width = image.shape[:2]
    size = (int(width * 0.2), int(height * 0.2))
    shrink = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    # img.ravel() 将图像转成一维数组，这里没有中括号。
    hist, bins = np.histogram(shrink.ravel(), 256, [0, 256])

    # print(hist)
    no_zero = []
    sta = 0
    for i in range(len(hist)):
        if hist[i] > 1:
            sta += 1
    return sta


# 获取截取视频的时间点
def get_time(videopath):
    cap = cv2.VideoCapture(str(videopath))
    success, frame = cap.read()
    end_frame = 0
    # print('keyframe_id_set',keyframe_id_set)
    while (success):
        # 如果当前帧的图像是全灰度图，则中断程序，跳出循环
        t = is_gray(frame)
        if t < 10:
            break
        else:
            # 获取截取帧的视频帧数
            end_frame = end_frame + 1
            success, frame = cap.read()

    return end_frame
