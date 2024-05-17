import cv2
import mediapipe as mp
import time
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import serial

#port_serie = serial.Serial('/dev/ttyS0', 9600)  # Initialisation de la communication série

class detectMain():
    #Initialisation de la classe
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
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

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = detectMain()

    # Définir la taille de l'image à afficher
    display_width = 852  # Largeur de l'écran souhaitée
    display_height = 480  # Hauteur de l'écran souhaitée

    #section pour importer une image
    """
    #on importe le png 
    # Charger l'image avec l'encadré et le texte
    image_path = "texte.png"  # Remplacez "votre_image.jpg" par le chemin de votre image
    image_with_text = cv2.imread(image_path)

    largeurPhoto = 550

    #calcul pour garder le ration
    ratio = largeurPhoto / image_with_text.shape[1]
    nouvelle_hauteur = int(image_with_text.shape[0] * ratio)

    # Redimensionner l'image avec le nouveau ratio
    image_with_text_resized = cv2.resize(image_with_text, (largeurPhoto, nouvelle_hauteur))
    """
   
    while True:
        success, img_noflip = cap.read()
        img = cv2.flip(img_noflip, 1)  # Retourner l'image horizontalement
        img = cv2.resize(img, (display_width, display_height))  # Redimensionner l'image
        img, main_points = detector.trouvePointsMain(img)       # Trouver les points de la main sur img, retourne la nouvelle image avec les points de la main
        img, paume_position = detector.trouvePositionPaume(img, main_points) # Trouver la position de la paume de la main sur img, retourne la nouvelle image avec un point sur la paume

        #serction pour mettre l'image dans la vidéo
        
        """
        # Calculer les coordonnées de début pour centrer l'image importée dans l'image vidéo
        debut_x = (display_width - largeurPhoto) // 2
        debut_y = display_height - nouvelle_hauteur

        # Insérer l'image importée redimensionnée dans le bas de l'image vidéo
        img[debut_y:debut_y + nouvelle_hauteur, debut_x:debut_x + largeurPhoto] = image_with_text_resized
        """
        #si on detecte une main
        if paume_position:
            Z_converti = 480-paume_position[1]  # Convertir la position de la paume en coordonnées cartésiennes
            text = f"Position de la main: {paume_position[0]}, {Z_converti}" # Convertir les coordonnées en texte
            cv2.putText(img, text, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA) # Dessiner le texte sur l'image
            stringEnvoi = str(paume_position[0]) + "," + str(Z_converti)+ "1" + "\n"  # Créer une chaîne de caractères pour envoyer les coordonnées de la paume
            #port_serie.write(stringEnvoi.encode())    
            
            print(stringEnvoi)


        #pour le calcul du fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)        # Afficher l'image
        cv2.waitKey(1)  #changer si on veut changer la vitesse de la vidéo

        # Vérifier si la touche 'q' est enfoncée ou si la fenêtre est fermée
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
