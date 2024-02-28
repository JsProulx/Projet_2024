from pymycobot.mycobot import MyCobot
import time
import random

#test sur le plan x,y, l'angle du tool est de 0,0,0
mc = MyCobot('/dev/ttyAMA0',1000000)
#Constante de la valeure de X, X indique la distance entre la base du robot et le bout
Distance_preset_X = 140   
#Valeure par defaut des angle de la "tete" du robot
rx = -81
ry = 53
rz = -85
#Valeure par defaut vitesse
vitesse = 90
#Constante pour les types de mouvements
Angulaire = 0
lineaire = 1
#Constantes des limites de la plage
min_Z = 185
max_Z =330
min_Y = -140
max_Y = 140
#Constantes de la resolution de l'ecran : 852x480
dim_Y = 852
dim_Z = 480
#Calcul du ration mm/pixels
mmpix_Y = 280/dim_Y
mmpix_Z = 145/dim_Z

while True:

    for i in range(0,250): 

        tempz = random.randint(0,250)

        dep_Y = mmpix_Y*(i*2)  
        dep_Y = dep_Y - 140 
        dep_Z = mmpix_Z*(tempz*2)
        dep_Z = dep_Z + 185

        if dep_Y > -115 and dep_Y < 115 and dep_Z < 210 and dep_Z >= 185:
            pass
        else:
            if dep_Y >= 0:
                if dep_Y < 3 and dep_Y != 0:
                    rx = rx-2.5 
                    rz = rz-1
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
                else :
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
            elif dep_Y < 0:
                if dep_Y > -3 and dep_Y != 0:
                    rx = rx-2.5
                    rz = rz-1
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
                else :
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
            print(dep_Y)
            print(dep_Z)
            print("\n""\r",rx,",",ry,",",rz,"\n""\r")
            time.sleep(0.00001) 
    
    for i in reversed(range(0,250)):

        tempz = random.randint(0,250)

        dep_Y = mmpix_Y*(i*2)
        dep_Y = dep_Y - 140
        dep_Z = mmpix_Z*(tempz*2)
        dep_Z = dep_Z + 185

        if dep_Y > -115 and dep_Y < 115 and dep_Z < 210 and dep_Z >= 185:
            pass
        else:
            if dep_Y >= 0:
                if dep_Y < 3 and dep_Y != 0:
                    rx = rx+2.5
                    rz = rz+1
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
                else :
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
            elif dep_Y < 0:
                if dep_Y > -3 and dep_Y != 0:
                    rx = rx+2.5
                    rz = rz+1
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
                else:
                    mc.send_coords([Distance_preset_X,dep_Y,dep_Z,rx,ry,rz],vitesse,Angulaire)
            print(dep_Y)
            print(dep_Z)
            print("\n""\r",rx,",",ry,",",rz,"\n""\r")
            time.sleep(0.00001)
