import cv2
import numpy as np
from HandTrackingModule import HandDetector
import time
import autopy

wCam, hCam = 640, 480
smoothing = 6

cap = cv2.VideoCapture(0)

pTime = 0
plocX, plocY = 0,0
clocY, clocY = 0,0

cap.set(3, wCam)
cap.set(4, hCam)
detector = HandDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr) #1440.0 900.0

while True:
    # 1. find hand landmarks

    success, img = cap.read()
    _, img = detector.findHands(img)
    # position of these hands i.e bounding box
    lmList, bbox = detector.findPosition(img)
    # print(lmList)


    # 2. find Tip of the index & middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # index finger
        x2, y2 = lmList[12][1:]  # middle finger
        # print(x1, y1, x2, y2)

        # 3. check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. Only index finger : moving mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:


            # 5. Convert Coordinates <<-- imp for correct positioning
            x3 = int(np.interp(x1, ((1/4)*wCam, wCam-((1/4)*wCam)), (0, int(wScr))))   #changes done here are -5
            y3 = int(np.interp(y1, ((1/4)*hCam, hCam-((1/4)*hCam)), (0, int(hScr))))  #changes done here are -5


            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothing
            clocY = plocY + (y3 - plocY) / smoothing
            # 7. Move Mouseq
            print(int(wScr-clocX), int(clocY))
            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)

            if(wScr-x3 == 1440 or y3 == 900):
                if(y3 == 0):
                    autopy.mouse.move(int(wScr - clocX) - 1, int(clocY))


                elif(wScr-x3 == 0):
                    autopy.mouse.move(int(wScr - clocX), int(clocY)-1)
                else:
                    autopy.mouse.move(int(wScr - clocX) - 1, int(clocY) - 1)

            else:
                autopy.mouse.move(int(wScr - clocX), int(clocY))
            
            plocX, plocY = clocX, clocY


        # 8. Both index & middle fingers are up : then clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            length,img,lineInfo = detector.findDistance(8, 12, img)
            print("middle length",length)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (255, 0, 0), cv2.FILLED)
                autopy.mouse.click()
                time.sleep(0.3)
        # both thumb and index are up

        if fingers[1] == 1 and fingers[0] == 1:
            length,img,lineInfo = detector.findDistance(4, 8, img)
            print("Thumb length", length)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (255, 0, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
                time.sleep(0.3)

    # 9. Find distance between fingers
    # 10. Click mouse if distance is short

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12. Display
    cv2.imshow("Image", img)
    if (cv2.waitKey(1) == ord("q")):
        break



