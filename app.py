import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import time


mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

cap = cv2.VideoCapture(0)

pTime = 0  

# ID ujung jari di Mediapipe: ibu jari (4), telunjuk (8), tengah (12), manis (16), kelingking (20)
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h, w, c = img.shape
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

           
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS,
                                  mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                  mpDraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))

           
            for tid in tipIds:
                x, y = lmList[tid]
                cv2.circle(img, (x, y), 12, (255, 0, 255), cv2.FILLED)
                cv2.putText(img, f"({x},{y})", (x + 15, y - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

           
            x1, y1 = lmList[4]
            x2, y2 = lmList[8]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        
            length = math.hypot(x2 - x1, y2 - y1)

      
            vol = np.interp(length, [20, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

     
            volBar = np.interp(length, [20, 200], [400, 150])
            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)


    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Gesture Volume Control", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
