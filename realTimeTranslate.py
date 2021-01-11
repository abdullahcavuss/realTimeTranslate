import pytesseract
import cv2
import numpy as np
from win32 import win32gui
from pythonwin import win32ui
from win32.lib import win32con
from win32 import win32api
import time
import pyautogui, sys
from mtranslate import translate
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

def cv2_img_add_text(img, text, left_corner: Tuple[int, int],
                     text_rgb_color=(255, 0, 0), text_size=24, font='./font/Roboto-Black.ttf', **option):
    pil_img = img
    if isinstance(pil_img, np.ndarray):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font_text = ImageFont.truetype(font=font, size=text_size, encoding=option.get('encoding', 'utf-8'))
    draw.text(left_corner, text, text_rgb_color, font=font_text)
    cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
    if option.get('replace'):
        img[:] = cv2_img[:]
        return None
    return cv2_img

def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)
    
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

pytesseract.pytesseract.tesseract_cmd = r"C:\Tesseract-OCR\tesseract.exe"

oldResult = ""
w=1000
h=130
while True:

    x, y = pyautogui.position() 
    frame = grab_screen((x-20,y-20,x+w,y+h)) #you can change translating area height with + or - keys

    details = pytesseract.image_to_string(frame)
    details = details[:-2]
    
    result = translate(details, 'tr','en') #change language translate(text,dest,src)
    if(result != oldResult):
        print(result)
    oldResult = result
    frame = cv2.blur(frame,(20,20))
    frame = cv2_img_add_text(frame, result, (0, 0), text_rgb_color=(0, 0, 0), text_size=24)

    cv2.namedWindow("translate")        
    cv2.moveWindow("translate", x-20,y+200) 
    cv2.imshow("translate", frame)
    
    key = cv2.waitKey(1)
    if key == 43:
        h = h + 40 
    elif key == 45:
        h = h - 40
    elif key == 27:
        break

cv2.destroyAllWindows()
