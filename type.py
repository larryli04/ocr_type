import pyautogui as gui
import pytesseract
import cv2
from PIL import Image, ImageGrab
import time
import numpy
from pynput.mouse import Listener

longText = True #use this if ur using a type software that doesn't scroll

startx = 0
starty = 0

endx = 0
endy = 0

print("You have 3 seconds to navigate to where the text stream will be")
time.sleep(3)

print("Listening for input window...")

def on_click(x, y, button, pressed):
    global startx, starty, endx, endy
    if(pressed):
        startx = x
        starty = y
    if not pressed:
        endx = x
        endy = y
        # Stop listener
        return False

with Listener(on_click=on_click) as listener:
    listener.join()

print("Starting coordinates: {0}, {1}".format(startx, starty))
print("Ending coordinates: {0}, {1}".format(endx, endy))

print("You now have 3 seconds to focus the keyboard")
time.sleep(3)
start = time.time()
while((time.time() < (start+60)) or (longText == False)):
    im = ImageGrab.grab(bbox = (startx,starty,endx,endy))

    im = numpy.array(im)
    im = im[:,:,::-1].copy()

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    #_, res = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)

    res = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,55,20)
    print(type(gray))
    #cv2.imshow("image",res)
    #cv2.waitKey(0)
    text = pytesseract.image_to_string(res)

    text = text.replace("\n"," ")
    
    
    #text = text[:-2]
    print(text)
    #time.sleep(1)
    gui.write(text)
