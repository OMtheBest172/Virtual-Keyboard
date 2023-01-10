import cv2
import numpy as np
from mediapipe.python._framework_bindings import packet
from cvzone.HandTrackingModule import HandDetector
import cvzone
import mediapipe as mp
import time
from time import sleep



cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

detector = HandDetector(detectionCon = 0.8)
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]
finalText = ""
def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
      x, y = button.pos
      w, h = button.size
      cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),30, rt=0,)
      cv2.rectangle(imgNew, button.pos, (x + w, y + h), (255, 165, 0), cv2.FILLED)
      cv2.putText(imgNew, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 255, 255), 5)

    out = img.copy()
    alpha = 0.8
    mask = img.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

class Button():
    def __init__(self,pos,text,size=[85,85]):
           self.pos = pos
           self.size = size
           self.text = text





buttonlist = []

for i in range(len(keys)):

    for j, key in enumerate(keys[i]):
        buttonlist.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonlist)

    if lmList:
         for button in buttonlist:
             x, y = button.pos
             w, h = button.size

             if x< lmList[8][0]<x+w and y<lmList[8] [1]<y+h:

                 cv2.rectangle(img, button.pos, (x + w, y + h), (255, 128, 0), cv2.FILLED)
                 cv2.putText(img, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN,
                           5, (255, 255, 255), 5)
                 l,_,_ = detector.findDistance(8, 12, img,draw=False)
                 print(l)

                 if l<60:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 15, y + 65), cv2.FONT_HERSHEY_PLAIN,
                               5, (255, 255, 255), 5)
                    finalText += button.text
                    sleep(1)
#(x axix Width) (y axis)
    cv2.rectangle(img, (50,350 ), (400, 430), (255, 165, 0), cv2.FILLED)
    cv2.putText(img, finalText, (55, 410), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 255, 255), 5)

    #(lenght, Width)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff ==ord('q'):
     break