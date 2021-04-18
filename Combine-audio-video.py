#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import cv2
import os
import sys
import numpy as np
import math

# 捕获音频
from moviepy.editor import *
from pydub import AudioSegment

#去除水印后的视频
video_path = r'D:\person_work\github\video-qushuiyin\watermark-master\1\out_path'

#裁剪后的音频文件
music_path =r'D:\person_work\github\video-qushuiyin\watermark-master\1\crop_music'

filenames = os.listdir(video_path)

# 遍历每个文件
for fn in filenames:
        
    # 每个文件的完整路径
    vidio_path_name = os.path.join(video_path, fn)
  
    vid = os.path.basename(vidio_path_name).split('.')[0]

    #音频文件完整路径
    music_name = vid+'.mp3'
    music_path_name = os.path.join(music_path, music_name)
 
    # 读取音频
    audio_end = AudioFileClip(music_path_name)
    
    videoclip_logo = VideoFileClip(vidio_path_name)
    # 将提取的音频和第二个视频文件进行合成
    videoclip_3 = videoclip_logo.set_audio(audio_end)
    
    if not os.path.exists("save_path"):
        os.makedirs("save_path")
    
    vidio_id_end = vid + ".mp4"
    save_video = os.path.join("save_path", vidio_id_end)
    
    print('save_video',save_video)
    # 输出新的视频文件
    videoclip_3.write_videofile(save_video)





