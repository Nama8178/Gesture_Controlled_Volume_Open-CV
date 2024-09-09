import cv2
import time
import numpy as np
import Hand_tracking_module as htm
import math


from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###########################
wCam , hCam = 540, 380 
###########################

####### pycaw code ########
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

########## end ####################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)
volBar = 400
volper = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])
        
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]
        cx,cy = (x1 + x2)//2 , (y1 + y2)//2
        
        
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        cv2.line(img , (x1,y1),(x2,y2),(255,0,255),3)
        
        length = math.hypot(x2-x1 , y2-y1)
        print(length)
        
        #hand range 15 - 230
        # Vol range -65 - 0
        vol = np.interp(length,[19,210],[minVol,maxVol])
        volBar = np.interp(length,[19,210],[400,150])
        volper = np.interp(length,[19,210],[0,100])
        # print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        if length < 50:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
            
    cv2.rectangle(img,(50,150),(85,400),(180,100,0),3) 
    cv2.rectangle(img,(50,int(volBar)),(85,400),(180,100,0),cv2.FILLED)      
    cv2.putText(img, f'{int(volper)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(180,100,0),3)  
    
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    cv2.putText(img, f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)