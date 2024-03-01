*------------------------------------------------*
*--- À lire pour l'utilisation du bras robot ----*
*------------------------------------------------*


*---------- Section sur le bras robot -----------*
Modèle: MyCobot 280PI
Site officiel : https://www.elephantrobotics.com/en/mycobot-pi/
Manuel technique : https://www.elephantrobotics.com/wp-content/uploads/2021/03/myCobot-User-Mannul-EN-V20210318.pdf
Documentation : https://docs.elephantrobotics.com/docs/gitbook-en/

Ce bras robot a un RasberryPi 4 d'intégré. Ce PI est configurer avec une image ''custom'' de la compagnie Elephant Robotics.
On peut la télécharger via ce lien: 

La communication entre les servos du bras robot et le Pi est fait via
le port serie ttyAMA0.

le code qui est présent sur le bras robot a été programmé directement sur l'appareil. Une copie de ce code figure dans le github du projet. Vous y trouverez deux codes nommez : 
    - Jeu1_suiveur.py
    - Jeu2_.py


*-------------------------------------------------*
*---    À lire pour l'acquisition d'image     ----*
*-------------------------------------------------*

Appreil: Jetson Nano 3450
site officiel : https://developer.nvidia.com/embedded/jetson-nano-developer-kit
«Get started»: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit

Jetson nano est un petit ordinateur fait pour supporter de l'intelligence artificiel conçu pour traiter des résolution d'images allant jusqu'à 4k. Il est excellent dans le context de traitement d'image ce qui est un élément crucial pour le bon fonctionnement de l'activité du suiveur de main comme l'on doit traiter une image en temps réel. Nous avons eu à apporter les modifications suivantes:

- Installer Python 3.10:
    1 - sudo apt update
    2 - sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
    3 - (Choisir l'emplacement d'installation) wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
    4 - tar -xf Python-3.10.0.tgz
    5 - cd Python-3.10.0
    6 - ./configure --enable-optimizations
    7 - make -j "Nombre de coeurs"
    8 - sudo make altinstall
    
- Installer OpenCV
    1 - sudo apt install python3-opencv
- Installer MediaPipe
    1 - 
- Installer Serial
    1 - 

La communication série du Jetson est sur la pin UartRX sur le port: /dev/ttyS0





