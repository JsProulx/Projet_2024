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
    """def mapToGrid(self, img, paume_position):
        grid_position = None

        if paume_position:  
            img_hauteur, img_largeur, _ = img.shape # Récupère la taille de l'image
            grid_largeur = img_largeur // 6 
            grid_hauteur = img_hauteur // 6
            
            #Determine la hauteure et la largeur de la grille
            row = min(max(paume_position[1] // grid_hauteur, 0), 5)  
            col = min(max(paume_position[0] // grid_largeur, 0), 5)  
            
            grid_position = (row, col)
        
        return grid_position"""
    

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = detectMain()

    # Définir la taille de l'image à afficher
    display_width = 1080  # Largeur de l'écran souhaitée
    display_height = 640  # Hauteur de l'écran souhaitée

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
   
    while True:
        success, img = cap.read()
        flipped_img = cv2.flip(img, 1)  # Retourner l'image horizontalement
        flipped_img = cv2.resize(flipped_img, (display_width, display_height))  # Redimensionner l'image
        flipped_img, main_points = detector.trouvePointsMain(flipped_img)
        flipped_img, paume_position = detector.trouvePositionPaume(flipped_img, main_points)
        
        # Calculer les coordonnées de début pour centrer l'image importée dans l'image vidéo
        debut_x = (display_width - largeurPhoto) // 2
        debut_y = display_height - nouvelle_hauteur

        # Insérer l'image importée redimensionnée dans le bas de l'image vidéo
        flipped_img[debut_y:debut_y + nouvelle_hauteur, debut_x:debut_x + largeurPhoto] = image_with_text_resized

        if paume_position:
            # Convertir les coordonnées en texte
            text = f"Position de la main: {paume_position[0]}, {paume_position[1]}"
            # Dessiner le texte sur l'image
            cv2.putText(flipped_img, text, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            stringEnvoi = str(paume_position[0]) + "," + str(paume_position[1])
            print(stringEnvoi)


        #pour le calcul du fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(flipped_img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", flipped_img)
        cv2.waitKey(1)  #changer si on veut changer la vitesse de la vidéo
        # Vérifier si la touche 'q' est enfoncée ou si la fenêtre est fermée
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
