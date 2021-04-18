#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import sys
import numpy as np
import math
import time

# 捕获音频
from moviepy.editor import *
from pydub import AudioSegment
from get_crop_time import get_time



'''
1.读取视频
2.读取视频的音频
3.找到视频的切分点
4.对视频进行切分
5.对音频进行切分
6.对视频调用去水印函数
7.去完水印的视频和音频合成
'''

def get_img_mask(im,file):
    shape = im.shape
    w = shape[1]
    h = shape[0]
    # print('shape[0]',shape[0])
    # print('shape[1]',shape[1])

    if int(h) > int(w):
        rect = (math.ceil(0.086 * h), math.ceil(0.41 * w))  # (H, W) 水印框大。 图像高宽为720,1280时为(110,300)
        # 左上角的位置      (15,15)
        pos1 = (math.ceil(0.02 * w), math.ceil(0.011 * h))
        # 右下角的位置   (405,1150)
        pos2 = (math.ceil(0.5625 * w), math.ceil(0.9 * h))
        nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)
        st_lt = 0

        # x先遍历高，y遍历宽
        for x in range(pos1[1], pos1[1] + rect[0]):
            for y in range(pos1[0], pos1[0] + rect[1]):
                px = im[x, y]  # im[0,1]  0代表图像的高，1代表图像的宽
                if sum(px) > 640:
                    nim[x, y] = 255
                    st_lt = st_lt + 1  # 像素超过一定数量就判定为右下角， 否则水印在左上角

        # st_lt = st_lt + 1  # 像素超过一定数量就判定为右下角， 否则水印在左上角
        #print('st_lt', st_lt)
        # 左上角logo的像素点为三千多，当低于1000个像素的时候，就认为logo移动到右下角了
        if st_lt < 1000:
            nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)  # clear
            # 先遍历宽，高
            for x in range(pos2[0], pos2[0] + rect[1]):
                for y in range(pos2[1], pos2[1] + rect[0] + 3):
                    px = im[y, x]
                    if sum(px) > 700:
                        nim[y, x] = 255
                        # for x in range(400, 720):

    else:
        nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)
        st_lt = 0
        '''
        对于1280*720的图片，左上角坐标为（10，10）（350,125）
        右下角的坐标为（940,580）（1270,710）
        '''
        # x先遍历高，y遍历宽
        for x in range(math.ceil(0.0078125 * h), math.ceil(0.0977 * h)):
            for y in range(math.ceil(0.0139 * w), math.ceil(0.486 * w)):
                px = im[x, y]  # im[0,1]  0代表图像的高，1代表图像的宽
                if sum(px) > 640:
                    nim[x, y] = 255
                    st_lt = st_lt + 1  # 像素超过一定数量就判定为右下角， 否则水印在左上角
        #print('st_lt', st_lt)
        # 左上角logo的像素点为三千多，当低于1000个像素的时候，就认为logo移动到右下角了
        if st_lt < 1000:
            nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)  # clear
            # 先遍历宽，高
            for x in range(math.ceil(0.7344 * w), math.ceil(0.9921 * w)):
                for y in range(math.ceil(0.805 * h), math.ceil(0.986 * h)):
                    px = im[y, x]
                    if sum(px) > 700:
                        nim[y, x] = 255

                        # 这里提取的水印的灰度图
    # if not os.path.exists("filter"):
        # os.makedirs("filter")
    # cv2.imwrite("filter/" + file, nim)
    return nim


# 传进来一张
def remove_logo(image,file):
    mask = get_img_mask(image,file)

    kernel = np.ones((3, 3), np.uint8)
    dilate = cv2.dilate(mask, kernel, iterations=3)
    kernel_2 = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(dilate, kernel_2, iterations=1)
    # cv2.imwrite("delate/" + file, dilate)

    sp = cv2.inpaint(image, dilate, 7, flags=cv2.INPAINT_TELEA)
    #滤波操作
    sp = cv2.bilateralFilter(sp, 5, 280, 50)

    return sp

   
    
if __name__ == '__main__':

    input_pa = r'D:\person_work\github\video-qushuiyin\watermark-master\1\input_path'
    print('input_pa',input_pa)
    filenames = os.listdir(input_pa)
    
    # 遍历每个文件
    for fn in filenames:
        t0 =time.time()
        # 每个文件的完整路径
        input_path = os.path.join(input_pa, fn)
              
        print('input_path',input_path)
        cap = cv2.VideoCapture(input_path)
        
        # # 读视频文件
        videoclip_1 = VideoFileClip(input_path)
        vidio_id = os.path.basename(input_path).split('.')[0]
        vidio_id_audio = vidio_id + '.wav'
        
        # c=os.path.splitext(input_path)[0]
        # 保存去除logo的视频文件
        vidio_id_save = vidio_id + '.mp4'
        if not os.path.exists("out_path"):
            os.makedirs("out_path")
        outpath = os.path.join("out_path", vidio_id_save)
        
        
        tm = get_time(input_path)
        print('tm',tm)
        
        # 对视频画面进行截取
        # 获取视频分辨率
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        
        #图片名称
        frame_png = vidio_id+'.png'
        
        # 输出文件编码，Linux下可选X264
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # 视频帧率
        fps = cap.get(cv2.CAP_PROP_FPS)
        print('fps', fps)
        success, image = cap.read()
        count = 0
        success = True
        # 输出
        out = cv2.VideoWriter(outpath, fourcc, fps, size)
        while (count < tm):
            success, image = cap.read()
        
            # 去水印，在写入视频
            re_logo = remove_logo(image,frame_png)
        
            out.write(re_logo)
            count += 1
        cap.release()
        
        print('time_all',time.time()-t0)
        # # 提取原始视频文件的音频部分
        audio_1 = videoclip_1.audio
        if not os.path.exists("audio_1_path"):
            os.makedirs("audio_1_path")
        
        save_audio_1 = os.path.join("audio_1_path", vidio_id_audio)
        audio_1.write_audiofile(save_audio_1)
        
        # 使用剪切音频的方法来对音频剪辑
        # 读取音频文件
        print('save_audio_1',save_audio_1)
        music = AudioSegment.from_wav(save_audio_1)
        t = tm/30
        
        # 截取前20秒,tm是求得的秒数
        clip = music[:t * 1000]
        if not os.path.exists("crop_music"):
            os.makedirs("crop_music")
        
        crop_id = vidio_id + '.mp3'
        print('crop_id',crop_id)
        crop_path = os.path.join('crop_music',crop_id)
        print('crop_path',crop_path)
        # 保存文件为clip.mp3，格式为mp3
        clip.export(crop_path, format='mp3')
        
        # cmd = "rm -rf %s" % res_video_file
        # subprocess.call(cmd, shell=True)
        