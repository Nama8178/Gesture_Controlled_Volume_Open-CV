import cv2
import mediapipe as mp
import time 

class handDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon  # Keep as float
        self.trackCon = trackCon  # Keep as float
        self.model_complexity = model_complexity
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None  # Initialize results attribute

    def findHands(self, img, Draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)  # Save results to self.results
    
        if self.results.multi_hand_landmarks:
            for handlns in self.results.multi_hand_landmarks:
                if Draw:
                    self.mpDraw.draw_landmarks(img, handlns, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lnList = []
        if self.results and self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, ln in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(ln.x * w), int(ln.y * h)
                lnList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
        return lnList        

def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lnList = detector.findPosition(img)
        if len(lnList) != 0:
            print(lnList[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
    
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
    
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
if __name__ == "__main__":
    main()
