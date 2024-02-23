import cv2
import mediapipe as mp
import time
import threading

class detectMain():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, int(self.maxHands), int(self.detectionCon), int(self.trackCon))
        self.mpDraw = mp.solutions.drawing_utils

    def trouvePointsMain(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        point_main = None
        if self.results.multi_hand_landmarks:
            point_main = self.results.multi_hand_landmarks[0]
            if draw:
                self.mpDraw.draw_landmarks(img, point_main, self.mpHands.HAND_CONNECTIONS)

        return img, point_main

    def trouvePositionPaume(self, img, point_main):
        paume_position = None

        if point_main:
            paume_landmark = point_main.landmark[self.mpHands.HandLandmark.MIDDLE_FINGER_MCP]
            img_hauteur, img_largeur, _ = img.shape
            paume_position = (int(paume_landmark.x * img_largeur), int(paume_landmark.y * img_hauteur))

            cv2.circle(img, paume_position, 10, (255, 0, 255), cv2.FILLED)

        return img, paume_position

def capture_thread(cap, shared_image, shared_lock):
    while True:
        res, img_noflip = cap.read()
        img = cv2.flip(img_noflip, 1)
        if res:
            shared_lock.acquire()
            shared_image = img.copy()
            shared_lock.release()
        time.sleep(0.01)

def detection_thread(detector, shared_image, shared_lock):
    while True:
        shared_lock.acquire()
        img = shared_image.copy()
        shared_lock.release()
        if img is not None:
            img = cv2.resize(img, (1080, 640))
            img, main_points = detector.trouvePointsMain(img)
            img, paume_position = detector.trouvePositionPaume(img, main_points)
            cv2.imshow("Image", img)
            if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
                break

def main():
    cap = cv2.VideoCapture(0)
    detector = detectMain()

    shared_image = None
    shared_lock = threading.Lock()

    capture_thread_obj = threading.Thread(target=capture_thread, args=(cap, shared_image, shared_lock))
    detection_thread_obj = threading.Thread(target=detection_thread, args=(detector, shared_image, shared_lock))

    capture_thread_obj.daemon = True
    detection_thread_obj.daemon = True

    capture_thread_obj.start()
    detection_thread_obj.start()

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
