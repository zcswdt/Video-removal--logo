# Video-removal -logo

​        本代码仓库使用opencv中的图像修复技术来对视频中的每一帧进行修复，从而得到干净去除掉水印的视频，同时保留了视频的音频部分。

# Dependent environment

```text
pip install opencv-python
pip install moviepy
pip install pydub
```

# How to remove

1.找到水印的位置，对于视频中logo会出现在相对固定位置的去除方法。比如抖音，快手，logo会出现在视频的左上角或者视频的右下角的时候，我们使用图像处理的基本知识来定位找到水印的位置。

2.读取视频的每一帧图像，创建一个和原图大小的mask，使得找到的水印的标识显现在mask图像中。

3.使用形态学膨胀操作，将找到的logo标识进行膨胀处理。

4.使用opencv中cv.inpant图像修复技术来对图像进行修复，去除logo。

5.处理视频中需要裁剪的视频帧数，并且计算得到裁剪时间，同步裁剪视频的音频文件，对视频中的音频文件进行裁剪处理，减掉片尾。

6.裁剪后的视频和裁剪后的音频进行合成视频，得到去除logo后的视频。

# image display

![](F:\git_respo\zcs_code\Video-removal -logo\picure\display.png)

# Code usage

1.先执行remove_logo.py文件来去除水印和得到裁剪掉片尾的音频文件。

```python
python remove_logo.py
```

2.运行Combine-audio-video.py来对去除logo的视频和音频文件进行合并。合并的视频文件保存在save_path文件夹中

```python
python Combine-audio-video.py
```

# The video address after removing the logo

链接：https://pan.baidu.com/s/1jB_-ES_JyIq-Bfu4H82Phg 
提取码：hnr9 

