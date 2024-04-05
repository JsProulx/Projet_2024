
import cv2
import mediapipe as mp
import time


def main():
    pTime = 0  # temps précédent
    cTime = 0  # temps courant
    cap = cv2.VideoCapture(0)

    # Définir la taille de l'image à afficher
    #cette section est importante car le calcul de la position de la
    #tete du robot depend de la taille de l'image. Ce calcul est fait par le bras robot.
    display_width = 852  # Largeur de l'écran souhaitée
    display_height = 480  # Hauteur de l'écran souhaitée

   
    while True:
        success, img_noflip = cap.read()
        img = cv2.flip(img_noflip, 1)  # Retourner l'image horizontalement
        img = cv2.resize(img, (display_width, display_height))  # Redimensionner l'image
        

        
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
