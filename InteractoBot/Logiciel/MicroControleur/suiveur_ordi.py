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


ce code est utiliser pour tester le programme sur un ordinateur personnel, donc pas d'envoie sur 
le bras robot.
"""
#!/usr/bin/python3

import cv2
import mediapipe as mp
import time
import math

#import serial

#port_serie = serial.Serial('/dev/ttyS0', 9600)  # Initialisation de la communication série

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
    #Cette methode prend une image et les points de la main en entree et calcul la distance enntre l'index et le pouce, relative
    #a la distance entre la jointure 1 du ptit doigt et la paume 
    def distanceIndexPouce(self, img, point_main):
        if point_main:

            img_hauteur, img_largeur, _ = img.shape         # Récupère la hauteur et la largeur de l'image
            
            #creation des 4 objet landmark pour les points de la main
            j1_tidoit_landmark =point_main.landmark[self.mpHands.HandLandmark.PINKY_MCP] #jointure 1 du ptit doigt
            base_paume_landmark = point_main.landmark[self.mpHands.HandLandmark.WRIST] #base de la paume
            top_index_landmark = point_main.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP]    #objet de position de l'index. A 2 propriétés x et y
            top_pouce_landmark = point_main.landmark[self.mpHands.HandLandmark.THUMB_TIP]   # objet de position du pouce. A 2 propriétés x et y

            #calcul de la position des points en pixel dans l'image (format (x,y))
            j1_tidoit_position = (int(j1_tidoit_landmark.x * img_largeur), int(j1_tidoit_landmark.y * img_hauteur))     
            base_paume_position = (int(base_paume_landmark.x * img_largeur), int(base_paume_landmark.y * img_hauteur))  
            top_index_position = (int(top_index_landmark.x * img_largeur), int(top_index_landmark.y * img_hauteur))     
            top_pouce_position = (int(top_pouce_landmark.x * img_largeur), int(top_pouce_landmark.y * img_hauteur))     

            #calcul de la distance entre les points en pixel
            distance_ti_paume = int(((j1_tidoit_position[0] - base_paume_position[0])**2 + (j1_tidoit_position[1] - base_paume_position[1])**2)**0.5)     ## Calcul (en pixel) de la distance entre la jointure 1 du ptit doigt et la aume avec pythagore: racine carrée de (x2-x1)² + (y2-y1)²
            distance_ind_pouce = int(((top_index_position[0] - top_pouce_position[0])**2 + (top_index_position[1] - top_pouce_position[1])**2)**0.5)  # Calcul (en pixel) de la distance entre l'index et le pouce avec pythagore: racine carrée de (x2-x1)² + (y2-y1)²

            #si la distance entre l'index et le pouce est inferieur a la motié de la distance entre la jointure 1 du ptit doigt et la paume, on ferme la main
            if distance_ind_pouce < distance_ti_paume/2:
                return 1, distance_ind_pouce
        return 0, distance_ind_pouce

    def rotation_main (self, img, point_main):
        if point_main:
            img_hauteur, img_largeur, _ = img.shape                     # Récupère la hauteur et la largeur de l'image
            
            direction = False  #direction de la rotation, True pour droite, False pour gauche
            angle = 0

            #on fait des landmark pour le poignet et le bout du majeur
            base_paume_landmark = point_main.landmark[self.mpHands.HandLandmark.WRIST] #base de la paume
            jointure2_landmark = point_main.landmark[self.mpHands.HandLandmark.MIDDLE_FINGER_MCP]    #objet de position du majeur. A 2 propriétés x et y

            #calcul de la position des points en pixel dans l'image (format (x,y))
            base_paume_position = (int(base_paume_landmark.x * img_largeur), int(base_paume_landmark.y * img_hauteur))
            jointure2_position = (int(jointure2_landmark.x * img_largeur), int(jointure2_landmark.y * img_hauteur))

            """#on décide de quel bord on tourne
            if jointure2_position[0] > base_paume_position[0]:
                direction = True
            else:
                direction = False"""
            
            #calcul des deltas
            delta_x = base_paume_position[0] - jointure2_position[0]
            delta_y = base_paume_position[1] - jointure2_position[1]

            #calcul de l'angle
            angle = int(math.degrees(math.atan2(delta_y, delta_x)))
            
            #si on veut mirroir l'angle
            angle = 180 - angle

            #on retourne l'angle selon la direction
            return angle


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
    
    compteur = 0

   
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
            
            #calcul de l'angle de rotation
            angle = detector.rotation_main(img, main_points)

            Z_converti = 480-paume_position[1]  # Convertir la position de la paume en coordonnées cartésiennes
            text = f"Position de la main: {paume_position[0]}, {Z_converti}" # Convertir les coordonnées en texte
            cv2.putText(img, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA) # Dessiner le texte sur l'image
            #print(distance)
            #stringEnvoi = str(paume_position[0]) + "," + str(Z_converti)+","+ str(distance[0]) + "\n"  # Créer une chaîne de caractères pour envoyer les coordonnées de la paume
            #port_serie.write(stringEnvoi.encode())    
            #print(stringEnvoi)
            print(angle)



        #pour le calcul du fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Suiveur de main", img)        # Afficher l'image
        cv2.waitKey(1)  #changer si on veut changer la vitesse de la vidéo

        # Vérifier si la touche 'q' est enfoncée ou si la fenêtre est fermée
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
