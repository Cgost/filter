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

#----------------------------------------#
#            all funnction.              #
#----------------------------------------#
# get img
def get_img(img_path = '01.jpg'):
  # connect google drive and get image
  if google_drive:
    drive.mount('/content/drive')
    img = cv2.imread(img_path,-1)
  img = cv2.imread(img_path,-1)
  print(img.shape)
  return img

# show the img
def show(img):
  plt.figure(figsize=(20,5))
  plt.imshow(img, cmap='gray')
  plt.tight_layout()
  plt.show()

# gray
def gray_color(img):
  print('gray the img...')
  new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  if debug: show(new_img)
  return new_img

# bone
def bone_color(img):
  print('bone the img...')
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  new_img = cv2.applyColorMap(img, cv2.COLORMAP_BONE)
  if debug: show(new_img)
  return new_img

# bilateralFilter
def bilateral_Filter(img):
  print('bilateralFilter...')
  new_img = cv2.bilateralFilter(img, d=0, sigmaColor=30, sigmaSpace=15)
  if debug: show(new_img)
  return new_img

# RGB_histogram_eqqlization
def RGB_histogram_eqqlization(img):
  print('RGB eqqlization the img...')
  new_img = img.copy()
  for k in range(3):
    new_img[:,:,k] = cv2.equalizeHist( img[:,:,k] )
  if debug: show(new_img)
  return new_img

# GaussianBlur
def Gaussian_Blur(img, num):
  print('Blur the img...')
  new_img = cv2.GaussianBlur(img, (5,5), num)
  if debug: show(new_img)
  return new_img

# Gaussian_noise
def Gaussian_noise(img, mean=0, sigma=0.1):
  print('Picture add gaussian noise: ')
  img = img / 255
  # random noise
  noise = np.random.normal(mean, sigma, img.shape)
  # noise + img
  gaussian_out = img + noise
  gaussian_out = np.clip(gaussian_out, 0, 1)
  
  new_img = np.uint8(gaussian_out*255)
  if debug: show(new_img)
  return new_img

# color_temperature
def color_temperature(img, num):
  print('heating/colding the img...')
  imgB = img[:, :, 0] 
  imgG = img[:, :, 1]
  imgR = img[:, :, 2] 
  # cool_style
  if num < 0:
    bAve = cv2.mean(imgB)[0] - num
    gAve = cv2.mean(imgG)[0] - num
    rAve = cv2.mean(imgR)[0]
  # warm_style
  else:
    bAve = cv2.mean(imgB)[0]
    gAve = cv2.mean(imgG)[0] + num
    rAve = cv2.mean(imgR)[0] + num
  aveGray = (int)(bAve + gAve + rAve) / 3

  # get resoult
  bCoef = aveGray / bAve
  gCoef = aveGray / gAve
  rCoef = aveGray / rAve
  imgB = np.floor((imgB * bCoef))
  imgG = np.floor((imgG * gCoef))
  imgR = np.floor((imgR * rCoef))

  imgb = imgB
  imgb[imgb > 255] = 255
  imgg = imgG
  imgg[imgg > 255] = 255
  imgr = imgR
  imgr[imgr > 255] = 255

  new_img = np.dstack((imgb, imgg, imgr)).astype(np.uint8) 
  if debug: show(new_img)
  return new_img

# contrast_and_brightness
def contrast_and_brightness(img, brightness=0 , contrast=100):
  print('contrast/brightness...')
  B = brightness / 255.0
  c = contrast / 255.0 
  k = math.tan((45 + 44 * c) / 180 * math.pi)

  img = (img - 127.5 * (1 - B)) * k + 127.5 * (1 + B)
  # 所有值必須介於 0~255 之間，超過255 = 255，小於 0 = 0
  new_img = np.clip(img, 0, 255).astype(np.uint8)
  if debug: show(new_img)
  return new_img

#--------------------------------------#
#             main step.               #
#--------------------------------------#

def bright_style(img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # contrast_and_brightness(img, brightness=0 , contrast=100)
  img = contrast_and_brightness(img, 0, 15)
  # RGB_histogram_eqqlization
  img = RGB_histogram_eqqlization(img)
  # GaussianBlur
  img = Gaussian_Blur(img, 0)
  # color_temperature(img, num)
  img = color_temperature(img, -10)
  
  if not debug: show(img)
  return img

def cold_style(img):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # RGB_histogram_eqqlization
  img = RGB_histogram_eqqlization(img)
  # bilateralFilter
  img = bilateral_Filter(img)
  # color_temperature(img, num)
  img = color_temperature(img, -20)
  # add noise
  img = Gaussian_noise(img, mean=0, sigma=0.1)
  # contrast_and_brightness(img, brightness=0 , contrast=100)
  img = contrast_and_brightness(img, 0, -20)

  if not debug: show(img)
  return img

def retro_style(img, how_old=0):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # contrast_and_brightness(img, brightness=0 , contrast=100)
  img = contrast_and_brightness(img, 0, -50)
  # bone
  img = bone_color(img)
  # GaussianBlur
  img = Gaussian_Blur(img, 20)
  # add noise
  img = Gaussian_noise(img, mean=0, sigma=how_old)
  
  if not debug: show(img)
  return img

def solemn_style(img, how_old=0):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  # contrast_and_brightness(img, brightness=0 , contrast=100)
  img = contrast_and_brightness(img, 0, -50)
  # bone
  img = gray_color(img)
  # GaussianBlur
  img = Gaussian_Blur(img, 20)
  # add noise
  img = Gaussian_noise(img, mean=0, sigma=how_old)

  if not debug: show(img)
  return img

#--------------------------------------#
#              debug here              #
#--------------------------------------#
# eaizer to find the bug
debug = 0
# check all style
check_all_style = 0
if check_all_style:
  img = get_img('01.jpg')
  print('generate the bright_style img...\n')
  bright_style(img)

  print('generate the cold_style img...\n')
  cold_style(img)

  print('generate the retro_style img...\n')
  retro_style(img, how_old=0)

  print('generate the solemn_style img...\n')
  solemn_style(img, how_old=0)

#--------------------------------------------------------------#
            #--------------------------------------#
            #               main UI                #
            #--------------------------------------#
#--------------------------------------------------------------#
# process
def all_style(style=0, img='', output='output.jpg', how_old=0):
  if style==1:
    print('generate the bright_style img...\n')
    output = 'bright_style_' + output
    new_img = bright_style(img)
  elif style==2:
    print('generate the cold_style img...\n')
    output = 'cold_style_' + output
    new_img = cold_style(img)
  elif style==3:
    print('generate the retro_style img...\n')
    output = 'retro_style_' + output
    new_img = retro_style(img, how_old=0)
  elif style==4:
    print('generate the solemn_style img...\n')
    output = 'solemn_style_' + output
    new_img = solemn_style(img, how_old=0)
  else:
    print('illego style\n')
    if not google_drive: os.system("pause")
    return 0
  
  path = output
  if google_drive: path = '/content/drive/MyDrive/影像處理/' + output
  new_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB)
  cv2.imwrite(path, new_img)

# main
def main(google_drive=0):
  # page 1
  print('+------------------------------------------+')
  print('           u der may der filter')
  print('+------------------------------------------+')
  if not google_drive: os.system("echo. >WARNING&findstr /a:c . WARNING*&del WARNING")
  print('         nothing and jst enjoy it')
  print('+------------------------------------------+')
  if not google_drive: os.system("pause")
  if not google_drive: os.system("cls")
  # page 2
  print('+------------------------------------------+')
  print('           u der may der filter')
  print('+------------------------------------------+')
  if not google_drive: os.system("dir /B *jpg")
  print('+------------------------------------------+')
  img_path = input('type the img name you wanna modify: ')
  img = get_img(img_path)
  output = input('type the file name you wanna store: ')
  if not google_drive: os.system("cls")
  # page 3
  print('+------------------------------------------+')
  print('           u der may der filter')
  print('+------------------------------------------+')
  print('            1. bright style')
  print('            2. cold style')
  print('            3. retro style')
  print('            4. solem style')
  print('+------------------------------------------+')
  style = int(input('choise 1 kind of style: '))
  if style==3 or style==4:
    how_old = float(input('how old do you wnat(ex:0.3): '))
  else:
    how_old = 0
  all_style(style=style, img=img, output=output, how_old=how_old)

if google_drive:
  main(google_drive)
else:
  while 1:
    os.system("cls")
    main(google_drive)
    print('+------------------------------------------+')
    print('              thx for using')
    print('+------------------------------------------+')
    os.system("pause")
