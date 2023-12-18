from pymycobot.mycobot import MyCobot
import tkinter as tk
from tkinter import *
import time

mc = MyCobot('/dev/ttyAMA0',1000000)

def update_scale_value(scale_index):
    # Update scale value based on corresponding entry value
    new_value = float(scale_entries[scale_index].get())
    scales[scale_index].set(new_value)
    mc.send_angle(scale_index+1,int(new_value),35)  #+1 car les indexes de joints partent a 1

def update_entry_value(scale_index):
    # Update entry value based on corresponding scale value
    new_value = scales[scale_index].get()
    scale_entries[scale_index].delete(0, tk.END)
    scale_entries[scale_index].insert(0, str(new_value))
    mc.send_angle(scale_index+1,int(new_value),35) #+1 car les indexes de joints partent a 1

def Fermeture_interface_de_gestion():

    mc.send_angle(1,0,15)
    mc.send_angle(2,-135.0,15)
    mc.send_angle(3,155,15)
    mc.send_angle(4,-150.0,15)
    mc.send_angle(5,-90.0,15)
    mc.send_angle(6,0,15)

    time.sleep(10)

    mc.release_all_servos()

for i in range (6):
    mc.send_angle(i+1,int(0),35)


root = tk.Tk()
root.title("Mycobot-Joints")

lables = []
scales = []
scale_entries = []
#images = ["/home/ubuntu/Desktop/Projet_Finale_Jean-Seb et philippe/joint1.png","/home/ubuntu/Desktop/Projet_Finale_Jean-Seb et philippe/joint2.png","/home/ubuntu/Desktop/Projet_Finale_Jean-Seb et philippe/joint3.png","/home/ubuntu/Desktop/Projet_Finale_Jean-Seb et philippe/joint4.png","/home/ubuntu/Desktop/Projet_Finale_Jean-Seb et philippe/joint5.png","/home/ubuntu/Desktop/Projet_Finale_Jean-Seb et philippe/joint6.png"]

for i in range(6):  # Create 6 scales and corresponding entry fields
    #on load les images
    """img = Image.open(images[i])
    img = img.resize((50,50))
    photo = ImageTk.PhotoImage(img)"""

    #section pour faire les label
    label_Pot_var = tk.StringVar()
    label_Pot_var.set("Joint{}".format(i+1)) 
    label_Pot = tk.Label(root, textvariable= label_Pot_var)
    label_Pot.pack()
    
    #section pour faire les slider
    scale_var = tk.DoubleVar()
    scale = tk.Scale(root, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, variable=scale_var)
    scale.pack()

    #section pour faire les textbox
    entry = tk.Entry(root)
    entry.pack()

    """ #Section pour faire l'imports d'images des articulations
    image_label = tk.Label(root, image = photo)
    image_label.image = photo
    image_label.pack(side = tk.LEFT)"""

    scales.append(scale_var)
    scale_entries.append(entry)
    

    
    # Binding entry change to update scale value
    entry.bind("<Return>", lambda event, x=i: update_scale_value(x))
    # Binding scale movement to update entry value
    scale.bind("<ButtonRelease-1>", lambda event, x=i: update_entry_value(x))

root.mainloop()



Fermeture_interface_de_gestion()