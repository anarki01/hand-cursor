import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy as autopy

from pynput.mouse import Button, Controller


#####################
wCam, hCam = 640, 480
frameR = 150 # Frame Reduction
smoothening = 7

#####################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector(maxHands=1)

wScr, hScr = autopy.screen.size()

test = True

mouse = Controller()



while True:

    # 1. Find hand landmark
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle finger
    if len(lmList)!=0:
        x1,y1 = lmList[8][1:]
        x2, y2 = lmList[4][1:]
        x0, y0 = lmList[16][1:]
        x4, y4 = lmList[20][1:]


        #print(x1,y1,x2,y2)

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)

        cv2.rectangle(img, (frameR, frameR-80), (wCam - frameR, hCam - frameR-80),
                      (255, 0, 255), 2)



        # 4. Only Index: Moving Mode
        if test == True: #fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1:

            # 5. Convert Webcam coordinates to Screen Coordinates

            x3 = np.interp(x0, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y0, (frameR-80, hCam - frameR-80), (0, hScr))

            # 6. Smoothen Values


            # 8. Both index and middle fingers are up: clicking mode
        #if fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:



            # 9. Find distance between fingers

            length, img, lineInfo = detector.findDistance(4, 8, img)
            length2, img, lineInfo2 = detector.findDistance(4, 20, img)

            #print(length)

            #print(lineInfo)

            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)

                # 10. Click mouse if distance short

                mouse.press(Button.left)


                clocX = plocX + (x3 - plocX) / (smoothening + 6)
                clocY = plocY + (y3 - plocY) / (smoothening + 6)

                # 7. Move mouse
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x0, y0), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)


                plocX, plocY = clocX, clocY



            elif length > 30:

                mouse.release(Button.left)

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening




                # 7. Move mouse
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x0, y0), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x4, y4), 15, (255, 0, 255), cv2.FILLED)

                plocX, plocY = clocX, clocY


            if length2 < 25:
                cv2.circle(img, (lineInfo[3], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)

                # 10. Click mouse if distance short

                mouse.click(Button.right, 1)



    # 11. Frame rate
    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display

    cv2.imshow("Image", img)
    cv2.waitKey(1)



