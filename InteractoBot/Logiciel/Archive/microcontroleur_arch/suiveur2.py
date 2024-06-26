import cv2
import mediapipe as mp
import time
from mediapipe.tasks.python import vision
from mediapipe.tasks import python

class detectMain():
    #Initialisation de la classe
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode    # Mode de détection, image ou vidéo
        self.maxHands = maxHands    # Nombre de main à détecter
        self.detectionCon = detectionCon    # Seuil de détection
        self.trackCon = trackCon    # Seuil de suivi

        self.mpHands = mp.solutions.hands   # Création de l'objet main
        self.hands = self.mpHands.Hands(self.mode, int(self.maxHands), int(self.detectionCon), self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils  # Création de l'objet dessin
        
    def trouvePointsMain(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        point_main = None
        if self.results.multi_hand_landmarks:
            point_main = self.results.multi_hand_landmarks[0]  # On ne prend que la première main détectée

            if draw:
                self.mpDraw.draw_landmarks(img, point_main, self.mpHands.HAND_CONNECTIONS)  # Dessine les points et les lignes
        
        return img, point_main

    def trouvePositionPaume(self, img, point_main):
        paume_position = None

        if point_main:
            #Extrait la position de la paume de la main
            paume_landmark = point_main.landmark[self.mpHands.HandLandmark.MIDDLE_FINGER_MCP]
            img_hauteur, img_largeur, _ = img.shape
            paume_position = (int(paume_landmark.x * img_largeur), int(paume_landmark.y * img_hauteur)) # Position de la paume en pixel
            
            # Met un point sur la paume
            cv2.circle(img, paume_position, 10, (255, 0, 255), cv2.FILLED)
        
        return img, paume_position
    # Convertit la position de la paume en position de grille
    def mapToGrid(self, img, paume_position):
        grid_position = None

        if paume_position:  
            img_hauteur, img_largeur, _ = img.shape # Récupère la taille de l'image
            grid_largeur = img_largeur // 6 
            grid_hauteur = img_hauteur // 6
            
            #Determine la hauteure et la largeur de la grille
            row = min(max(paume_position[1] // grid_hauteur, 0), 5)  
            col = min(max(paume_position[0] // grid_largeur, 0), 5)  
            
            grid_position = (row, col)
        
        return grid_position
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = detectMain()

    while True:
        success, img = cap.read()
        img, main_points = detector.trouvePointsMain(img)
        img, paume_position = detector.trouvePositionPaume(img, main_points)

        if paume_position:
            grid_position = detector.mapToGrid(img, paume_position)
            print("Paume Position (Pixel):", paume_position)
            print("Paume Grille Position:", grid_position)

        # Draw grid lines
        img_hauteur, img_largeur, _ = img.shape
        for i in range(1, 6):
            x = i * (img_largeur // 6)
            y = i * (img_hauteur // 6)
            cv2.line(img, (x, 0), (x, img_hauteur), (255, 0, 0), 1)
            cv2.line(img, (0, y), (img_largeur, y), (255, 0, 0), 1)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(200)


if __name__ == "__main__":
    main()
