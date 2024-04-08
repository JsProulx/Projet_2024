#!/usr/bin/env python3

# la premiere ligne est necessaire pour que ce script soit executer comme service au demarrage

from pymycobot.mycobot import MyCobot
import time
import serial
from multiprocessing import Process, Value, Lock



#test sur le plan x,y, l'angle du tool est de 0,0,0
mc = MyCobot('/dev/ttyAMA0',1000000)
mc.set_gripper_ini()
#Configuration du serial port
serial_Port = serial.Serial('/dev/ttyUSB0', 9600)



###########################################
#             Section - code              #
########################################### 
def read_serial(recep_Z,recep_Y,read_flag,lock,Grabber_state):
    while True:
        received_string = serial_Port.readline().decode()
        print(received_string)
        if received_string:
            temps = received_string.split(',')
            if len(temps) == 3:
                lock.acquire()
                recep_Y.value = int(temps[0])
                lock.release()
                lock.acquire()
                recep_Z.value = int(temps[1])
                lock.release()
                lock.acquire()
                Grabber_state.value = int(temps[2])
                lock.release()
                time.sleep(0.001)
                #print(recep_Y.value,recep_Z.value)
            lock.acquire()
            read_flag.value = 1
            lock.release()

def mouvement(recep_Z,recep_Y,shared_Read_flag,lock,Grabber_state):

    #Compteur pour compter le temps dinactivite du robot
    compteur_inactivite = 0

    #Valeure par defaut vitesse
    vitesse = 90
            
    #Constante pour les types de mouvements
    Angulaire = 0
    #lineaire = 1
    #Angulaire = 0
    
    while True:
        print(shared_Read_flag.value)
        if shared_Read_flag.value == 1:
            #Constante de la valeure de X, X indique la distance entre la base du robot et le bout
            Distance_preset_X = 140   
            
            #Valeure paprocess_Serialr defaut des angle de la "tete" du robot
            rx_m = -81
            ry = 53
            rz_m = -85

            rx_p = -91
            rz_p = -89
            

            #Constantes de la resolution de l'ecran : 852x480
            dim_Y = 852
            dim_Z = 480
            
            #Calcul du ration mm/pixels
            mmpix_Y = 280/dim_Y
            mmpix_Z = 145/dim_Z

            lock.acquire()
            temp_recep_Y = int(recep_Y.value)
            temp_recep_Z = int(recep_Z.value)
            lock.release()

            dep_Y = mmpix_Y*temp_recep_Y
            dep_Y = dep_Y - 140 #-140 pour respecter les limites car on doit avoir negatif et positif
            #print(dep_Y)
            dep_Z = mmpix_Z*temp_recep_Z
            dep_Z = dep_Z + 185
            print(dep_Z)


            if dep_Y > -115 and dep_Y < 115 and dep_Z < 210 and dep_Z >= 185 or temp_recep_Y ==0 and temp_recep_Z == 0 or dep_Z <= 200:
                pass
            else:
                compteur_inactivite = 0
                if Grabber_state.value == 1:
                    print("M'a te pincer")
                    mc.set_gripper_state(1,100)
                    #print("J'ai vu et revu")
                    if dep_Y >= 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_p,ry,rz_p],vitesse,Angulaire)
                    elif dep_Y < 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_m,ry,rz_m],vitesse,Angulaire)
                    time.sleep(0.001) 
                else:
                    print("M'a pas te pincer")
                    mc.set_gripper_state(0,100)
                    #print("J'ai vu et revu")
                    if dep_Y >= 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_p,ry,rz_p],vitesse,Angulaire)
                    elif dep_Y < 0:
                        mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx_m,ry,rz_m],vitesse,Angulaire)
                    time.sleep(0.001) 
            time.sleep(0.001)
            shared_Read_flag.value = 0
        elif compteur_inactivite != 200: 
            #Variables pour la position de relachement des servos du robot
            pause_x = 11.4
            pause_y = -72.4
            pause_z = 227.5
            pause_Rx = 19.81
            pause_Ry = -24.49
            pause_Rz = 120.85

            if compteur_inactivite < 200:
                compteur_inactivite = compteur_inactivite + 1
            
            print(compteur_inactivite)  #Lecture pour tester laugementation de la valeure de compteur dinactivite

            if compteur_inactivite >= 200 :
                mc.send_coords([140,-69,269,-81,53,-85],vitesse,Angulaire)
                time.sleep(2) 
                mc.send_coords([pause_x,pause_y,pause_z,pause_Rx,pause_Ry,pause_Rz],vitesse,Angulaire)
                time.sleep(2) 
                mc.release_all_servos()
        time.sleep(0.05) 

def main():

    lock = Lock()
    print("Je suis le main")
    #Variables de donnees recues via le port serie
    shared_Recep_Z = Value('i',0)
    shared_Recep_Y = Value('i',0)
    shared_Read_flag = Value('i',0)
    Grabber_state = Value('i',0)
    
    process_Serial = Process(target=read_serial, args=(shared_Recep_Z,shared_Recep_Y,shared_Read_flag,lock,Grabber_state))
    process_Mouvement = Process(target=mouvement, args=(shared_Recep_Z,shared_Recep_Y,shared_Read_flag,lock,Grabber_state))

    process_Serial.start()
    process_Mouvement.start()


#Appel de la fonction main au démarrage du programme
if __name__ == "__main__":
    main()
