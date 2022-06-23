# filter

## 專案介紹
My filter for final report

## 程式架構
![](https://github.com/Cgost/filter/blob/main/Architecture_diagram/main.png)

## 使用技術
工具名稱|用途
--------|---------
Python3 | 控制一切
Github   | 存放原始碼

## 成品展示
初始畫面
![](https://github.com/Cgost/filter/blob/main/demo/result_page1.PNG)

列出當前目錄下所有的 jpg 檔，要求使用者選擇其中一張圖片
![](https://github.com/Cgost/filter/blob/main/demo/result_page2.PNG)

調整參數
![](https://github.com/Cgost/filter/blob/main/demo/result_page3-2.PNG)

輸出結果
![](https://github.com/Cgost/filter/blob/main/demo/result_page3-1.PNG)

感謝使用
![](https://github.com/Cgost/filter/blob/main/demo/result_page4.PNG)

## 引用模組
```python
# bedore start, are you on google drive(default not)?
google_drive = 0
#---------------------------------------#
#             imoprt model              #
#---------------------------------------#
import numpy as np
import cv2
import math
from numpy.random import uniform, normal, exponential, rayleigh
from matplotlib import pyplot as   plt

if google_drive:
  from IPython.core.pylabtools import print_figure
  from google.colab import drive
  from google.colab.patches import cv2_imshow
else:
  import os
```
