#!/usr/bin/env python3
"""
Auteur: Philippe Ramalho et Jean-Sebastien Proulx
Hiver 2024
Ce programme prend les données reçues par communication série du programme suiveur_presentoir_VX.py
et les utilise pour contrôler le bras robot. On utilise la librairie pymycobot pour contrôler le bras
robot. Il a deux processus en parallèle, un pour lire les données reçues par communication série et
l'autre pour contrôler le bras robot. On utilise la librairie multiprocessing pour gérer les processus.
Le port serie ttyAMA0 est utilisé pour la communication série avec le bras robot. Le port série ttyUSB0
est utilisé pour la communication série avec le programme suiveur_presentoir_VX.py.

"""

# la premiere ligne est necessaire pour que ce script soit executer comme service au demarrage
#NE PAS METTRE D'ACCENT DANS CE CODE, CETTE VERSION DE PYTHON NE LES INTERPRETTENT PAS (meme en commentaire)

from pymycobot.mycobot import MyCobot
import time
import serial
from multiprocessing import Process, Value, Lock
import random



#test sur le plan x,y, l'angle du tool est de 0,0,0
mc = MyCobot('/dev/ttyAMA0',1000000)
mc.set_gripper_ini()
#Configuration du serial port
serial_Port = serial.Serial('/dev/ttyUSB0', 9600)



###########################################
#             Section - code              #
########################################### 
#Fonction pour lire le port serie. Prend 5 paramètres
#recep_z = valeur envoye par le Jetson pour l'axe des Z du bras
#recep_y = valeur envoye par le Jetson pour l'axe des Y du bras
#Read_flag = variable de verif de lecture sur le port serie (1 ou 0)
#Grabber_state = Valeur envoye par le jetson pour l'etat de la pince (1 ou 0)
#Lock = mutex()
def read_serial(recep_Z,recep_Y,read_flag,lock,Grabber_state,Grabber_twist):
    while True:
        received_string = serial_Port.readline().decode()           #recoi la string par le port serie
        #print(received_string)
        if received_string:
            temps = received_string.split(',')
            if len(temps) == 4:
                #ici on release et acquire pour permettre la concurence d'acces au variable syncronise 
                # lors de la reception des donnees
                lock.acquire()
                recep_Y.value = int(temps[0])
                lock.release()
                lock.acquire()
                recep_Z.value = int(temps[1])
                lock.release()
                lock.acquire()
                Grabber_state.value = int(temps[2])
                lock.release()
                lock.acquire()
                Grabber_twist.value = int(temps[3])
                print(Grabber_twist.value)
                lock.release()
                time.sleep(0.001)
                #print(recep_Y.value,recep_Z.value)
            lock.acquire()
            read_flag.value = 1
            lock.release()
#Fonction qui prend les varialble "synchronized" en parametre et les utilise pour
#faire bouger le robot

def idle_act0():

    #Section toc toc
    mc.send_coords([140,-69,269,-81,53,-85],90,0)   #Point référenciel
    time.sleep(1)
    mc.send_coords([165,-69,269,-81,53,-85],90,0)   #point avance fenetre
    time.sleep(1)
    mc.send_angle(4,25,90)  #recule
    time.sleep(0.2)
    mc.send_angle(4,10,90)  #cogne
    time.sleep(0.2)
    mc.send_angle(4,25,90)  #recule
    time.sleep(0.2)
    mc.send_angle(4,10,90)  #cogne
    time.sleep(0.2)
    mc.send_angle(4,25,90)  #recule
    time.sleep(0.2)
    
    #Section allo
    mc.send_coords([140,-69,269,-81,53,-85],90,0)   #Point référenciel
    time.sleep(1)
    mc.send_coords([140,-69,269,-81,53,-60],90,0)   #droite
    time.sleep(0.2)
    mc.send_coords([140,-69,269,-81,53,-120],90,0)  #gauche
    time.sleep(0.2)
    mc.send_coords([140,-69,269,-81,53,-60],90,0)   #droite
    time.sleep(0.2)
    mc.send_coords([140,-69,269,-81,53,-120],90,0)  #gauche
    time.sleep(0.2)
    mc.send_coords([140,-69,269,-81,53,-85],90,0)   #Point référenciel

def idle_act1():
    mc.send_coords([18,0,300,-90,45,90],90,0)
    sense=1      
    flag = False    #pour sortir de la while
    i = 0
    r=255
    g=0
    b=255
    #TODO : mettre la vitesse de deplacvement plus vite et faire la boucle des lumiere independante
    while flag == False:
        if i < 90 and sense==1:
            mc.send_angles([90,0,i,0,90,45],80)
            mc.set_color(r,g,b)
            i += 5
            r-=12
            if i==90:
                sense=2

        elif i <= 90 and sense==2:
            mc.send_angles([90,0,i,0,90,45],80)
            i -= 5
            r-=6
            if r<=0:
                r=0
            b-=18
            if b<=0:
                b=0
            g+=18
            if g>=255:
                g=255
            mc.set_color(r,g,b)
            if i==0:
                sense=3
        
        elif i > -90 and sense ==3:
            mc.send_angles([90,0,i,0,90,45],80)
            i -= 5
            r+=6
            g-=18
            if g<=0:
                g=0
            mc.set_color(r,g,b)
            if i <=-90:
                sense = 4

        elif i < 0 and sense ==4:
            mc.send_angles([90,0,i,0,90,45],80)
            i += 5
            r += 18
            g += 18
            b += 18
            if r >=255 or g>=255  or b >=255:
                r = 255
                g = 255
                b = 255
            mc.set_color(r,g,b)
            if i >= 0:
                mc.send_angles([0,-115,115,0,0,45],80)
                time.sleep(1)
                flag = True

def dodo_attente():
    #Variables pour la position de relachement des servos du robot
    pause_x = -14.3
    pause_y = -20.2
    pause_z = 186
    pause_Rx = -110.57
    pause_Ry = 41.6
    pause_Rz = -2.64
    
    mc.send_coords([140,-69,269,-81,53,-85],90,0) #point intermediaire (position centrale de la zone permise)
    time.sleep(2) 
    mc.send_coords([pause_x,pause_y,pause_z,pause_Rx,pause_Ry,pause_Rz],45,0)
    time.sleep(2) 
    mc.release_all_servos()    

def mouvement(recep_Z,recep_Y,shared_Read_flag,lock,Grabber_state,Grabber_twist):

    #Compteur pour compter le temps dinactivite du robot
    compteur_inactivite = 0

    #Valeure par defaut vitesse
    vitesse = 90
            
    #Constante pour les types de mouvements
    Angulaire = 0
    #lineaire = 1
    #Angulaire = 0

    while True:
        #print(shared_Read_flag.value)
        if shared_Read_flag.value == 1:
            #Constante de la valeure de X, X indique la distance entre la base du robot et le bout
            Distance_preset_X = 140   

            #Valeure par defaut de la rotation de la pince
            ry = 0
            
            #Valeure par defaut des angle de la "tete" du robot
            rx_m = -81
            rz_m = -85  #usually -85

            rx_p = -91
            rz_p = -89 #usually -89
            

            #Constantes de la resolution de l'ecran : 852x480
            dim_Y = 852
            dim_Z = 480
            
            #Calcul du ration mm/pixels
            mmpix_Y = 280/dim_Y
            mmpix_Z = 145/dim_Z

            #Verrou des variables des positions pour lors de la lecture 
            lock.acquire()
            temp_recep_Y = int(recep_Y.value)
            temp_recep_Z = int(recep_Z.value)
            lock.release()

            #Conversion des valeures reçu pour faire des mouvement contenu dans les limites desire
            dep_Y = mmpix_Y*temp_recep_Y
            dep_Y = dep_Y - 140         #-140 pour respecter les limites car on doit avoir negatif et positif
            #print(dep_Y)
            dep_Z = mmpix_Z*temp_recep_Z
            dep_Z = dep_Z + 185          #le +185 a pour but de faire respecter le limites de hauteur aux mouvement de haut en bas
            #print(dep_Z)
            #Travail de la variable de rotation de la pince afin qu'elle respecte certaines limites
            if Grabber_twist.value > 5 or Grabber_twist.value < -5:
                ry = Grabber_twist.value
                if ry >= 90:
                    ry = 90
                elif ry <= -90:
                    ry = -90
            else:
                ry = 0

            #Si les valeures de mouvement sont dans ces limites, ne fait rien sinon bouge
            if dep_Y > -115 and dep_Y < 115 and dep_Z < 210 and dep_Z >= 185 or temp_recep_Y ==0 and temp_recep_Z == 0 or dep_Z <= 200:
                pass
            else:
                compteur_inactivite = 0
                #Si le microcontroleur envoi que la pince doit etre fermer, ferme la pince avec une vitesse de 100% 
                if Grabber_state.value == 1:
                    mc.set_gripper_state(1,100)
                    if dep_Y >= 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_p,ry,rz_p],vitesse,Angulaire)
                    elif dep_Y < 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_m,ry,rz_m],vitesse,Angulaire)
                    time.sleep(0.001) 
                else:
                    #Si le microcontroleur envoi que la pince doit etre ouverte, ouvre la pince avec une vitesse de 100% 
                    mc.set_gripper_state(0,100)
                    if dep_Y >= 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_p,ry,rz_p],vitesse,Angulaire)
                    elif dep_Y < 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_m,ry,rz_m],vitesse,Angulaire)
                    time.sleep(0.001) 
            time.sleep(0.001)
            shared_Read_flag.value = 0
        
        #compteur pour tomber en veille apres un certain temps
        elif compteur_inactivite < 200: 
            if compteur_inactivite == 0 or compteur_inactivite == 1:
                mc.set_gripper_state(1,100)
            compteur_inactivite = compteur_inactivite + 1
            #print(compteur_inactivite)  #Lecture pour tester laugementation de la valeure de compteur dinactivite

        elif compteur_inactivite == 200 :
            dodo_attente()
            compteur_inactivite = 300

        elif compteur_inactivite >= 300 and compteur_inactivite < 3300: #Normalement 6300
            compteur_inactivite = compteur_inactivite + 1
            #print(compteur_inactivite)

        elif compteur_inactivite == 3300:   #Normalement 6300
            #print("test")
            selection_activite = random.randint(0,1)
            if selection_activite == 0:
                idle_act0()
                dodo_attente()
            elif selection_activite == 1:
                idle_act1()
                dodo_attente()

            compteur_inactivite = 300

        time.sleep(0.05) 

def main():

    lock = Lock()

    #Variables de donnees recues via le port serie
    shared_Recep_Z = Value('i',0)
    shared_Recep_Y = Value('i',0)
    shared_Read_flag = Value('i',0)
    Grabber_state = Value('i',0)
    Grabber_twist = Value('i',0)
    
    #definition des process
    process_Serial = Process(target=read_serial, args=(shared_Recep_Z,shared_Recep_Y,shared_Read_flag,lock,Grabber_state,Grabber_twist))
    process_Mouvement = Process(target=mouvement, args=(shared_Recep_Z,shared_Recep_Y,shared_Read_flag,lock,Grabber_state,Grabber_twist))

    #demarrage des process
    process_Serial.start()
    process_Mouvement.start()


#Appel de la fonction main au démarrage du programme
if __name__ == "__main__":
    main()
