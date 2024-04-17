"""
Auteur: Philippe Ramalho et Jean-Sebastien Proulx
Hiver 2024
Ce programme permet de détecter une main dans une vidéo et de trouver la position de 
la paume de la main ainsi que la distance entre l'index et le pouce. On utilise la librairie
MediaPipe pour la détection de la main. On utilise aussi la librairie OpenCV pour l'affichage de la
capture vidéo et le traitement des images. On utilise aussi la librairie serial pour la communication
série avec le raspi4 dans le bras robot. J'ai fait une classe detectMain pour faciliter la gestion
de la détection de la main. On peut utiliser cette classe pour d'autres versions du programme.

Les informations de positions de la main sont envoyées par communication série au bras robot.
"""
#!/usr/bin/python3

import cv2
import mediapipe as mp
import time

import serial

port_serie = serial.Serial('/dev/ttyS0', 9600)  # Initialisation de la communication série

class detectMain():
    #Initialisation de la classe
    def __init__(self, mode=False, maxHands=1, detectionCon=0.8, trackCon=0.5):
        self.mode = mode    # Mode de détection, image ou vidéo
        self.maxHands = maxHands    # Nombre de main à détecter
        self.detectionCon = detectionCon    # Seuil de détection
        self.trackCon = trackCon    # Seuil de suivi

        self.mpHands = mp.solutions.hands   # Création de l'objet main
        self.hands = self.mpHands.Hands(self.mode, int(self.maxHands), int(self.detectionCon), self.trackCon)       # Initialisation de l'objet main
        self.mpDraw = mp.solutions.drawing_utils  # Création de l'objet dessin

    #Cette méthode prend une image en entrée et retourne l'image avec les points des mains détectées dessinés dessus   
    def trouvePointsMain(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convertit l'image en RGB
        self.results = self.hands.process(imgRGB)   

        point_main = None
        if self.results.multi_hand_landmarks:
            point_main = self.results.multi_hand_landmarks[0]  # On ne prend que la première main détectée

            if draw:
                self.mpDraw.draw_landmarks(img, point_main, self.mpHands.HAND_CONNECTIONS)  # Dessine les points et les lignes
        
        return img, point_main

    #Cette méthode prend une image et les points de la main en entrée et retourne l'image avec un point sur la paume de la main
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
    #Cette methode prend une image et les points de la main en entree et calcul la distance enntre l'index et le pouce
    #retourne 1 si la distance est inferieur a 50 sinon 0
    def distanceIndexPouce(self, img, point_main):
        distance = 0
        if point_main:
            #Extrait la position de la paume de la main
            index_landmark = point_main.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP]    #objet de position de l'index. A 2 propriétés x et y
            pouce_landmark = point_main.landmark[self.mpHands.HandLandmark.THUMB_TIP]   # objet de position du pouce. A 2 propriétés x et y
            img_hauteur, img_largeur, _ = img.shape                     # Récupère la hauteur et la largeur de l'image
            index_position = (int(index_landmark.x * img_largeur), int(index_landmark.y * img_hauteur))     # Position de l'index en par rapport à l'image
            pouce_position = (int(pouce_landmark.x * img_largeur), int(pouce_landmark.y * img_hauteur))      # Position du pouce en par rapport à l'image
            distance = int(((index_position[0] - pouce_position[0])**2 + (index_position[1] - pouce_position[1])**2)**0.5)  # Calcul (en pixel) de la distance entre l'index et le pouce avec pythagore: racine carrée de (x2-x1)² + (y2-y1)²
            #cv2.line(img, index_position, pouce_position, (255, 0, 255), 2)  # Dessine une ligne entre l'index et le pouce
            if distance < 90:
                return 1 , distance
        
        return 0, distance


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = detectMain()

    # Définir la taille de l'image à afficher
    #cette section est importante car le calcul de la position de la
    #tete du robot depend de la taille de l'image. Ce calcul est fait par le bras robot.
    display_width = 852  # Largeur de l'écran souhaitée
    display_height = 480  # Hauteur de l'écran souhaitée
    
   

   
    while True:
        success, img_noflip = cap.read()
        img = cv2.flip(img_noflip, 1)  # Retourner l'image horizontalement
        img = cv2.resize(img, (display_width, display_height))  # Redimensionner l'image
        img, main_points = detector.trouvePointsMain(img)       # Trouver les points de la main sur img, retourne la nouvelle image avec les points de la main
        img, paume_position = detector.trouvePositionPaume(img, main_points) # Trouver la position de la paume de la main sur img, retourne la nouvelle image avec un point sur la paume

	
        #si on detecte une main
        if paume_position:
            # Calculer la distance entre l'index et le pouce
            distance = detector.distanceIndexPouce(img, main_points)

            Z_converti = 480-paume_position[1]  # Convertir la position de la paume en coordonnées cartésiennes
            text = f"Position de la main: {paume_position[0]}, {Z_converti}, Disance index/pouce : {distance[1]}" # Convertir les coordonnées en texte
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA) # Dessiner le texte sur l'image
            stringEnvoi = str(paume_position[0]) + "," + str(Z_converti)+","+ str(distance[0]) + "\n"  # Créer une chaîne de caractères pour envoyer les coordonnées de la paume
            port_serie.write(stringEnvoi.encode())    
            
            print(stringEnvoi)
	

        #pour le calcul du fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)        # Afficher l'image
        cv2.waitKey(1)  #changer si on veut changer la vitesse de la vidéo

        # Vérifier si la touche 'q' est enfoncée ou si la fenêtre est fermée
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
