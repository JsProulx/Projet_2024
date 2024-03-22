*------------------------------------------------*

*--- À lire pour l'utilisation du bras robot ----*

*------------------------------------------------*

Ce projet est conçu pour le Département de Technique de Génie Électrique du Cégep de Sherbrooke. On utilise un bras robot 6 axes d'Elephant Robotics. 
Le bras robot a un RasberryPI 4 d'intégré. Ce Pi4 contient les scripts python pour gérer le mouvement des servos moteurs du bras robot. Pour interfacer la manette et 
le module de vision par odinateur, nous utilisons un JetSon Nano de Nvidia. Ce microcontroleur traite les données nécessaires et envoie les informations au Pi4 via le port serie. Pour plus d'information sur la connexion, veuillez vous référer au plan de connexion.

*---------- Section sur le bras robot -----------*

Modèle: MyCobot 280PI
Site officiel : https://www.elephantrobotics.com/en/mycobot-pi/
Manuel technique : https://www.elephantrobotics.com/wp-content/uploads/2021/03/myCobot-User-Mannul-EN-V20210318.pdf
Documentation : https://docs.elephantrobotics.com/docs/gitbook-en/

Ce bras robot a un RasberryPi 4 d'intégré. Ce PI est configurer avec une image ''custom'' de la compagnie Elephant Robotics.
On peut la télécharger via ce lien: https://www.elephantrobotics.com/en/downloads/
Dans notre cas, nous avons l'image ubuntu 20.04 pour le MyCobot 280 PI.

La communication entre les servos du bras robot et le Pi est fait via
le port serie ttyAMA0.

le code qui est présent sur le bras robot a été programmé directement sur l'appareil. Une copie de ce code figure dans le github du projet. Vous y trouverez deux codes nommez : 
    - Jeu1_suiveur.py
    - Jeu2_.py


*-------------------------------------------------*

*---    À lire pour l'acquisition d'image     ----*

*-------------------------------------------------*

Nous avons exploré deux solution pour la capture vidéo: 
- Jetson Nano 3450
  Avantages: Plus performant (il a un processeur graphique dédié). Permet d'avoir 15-20 fps
  
  Inconvénients: Installation des libraries nécessaires (mediapipe et opencv) beaucoup plus difficile. Ça prend des versions spécifique des libraries, ce qui implique l'installation de dépendance plus difficile, et une version spécifique de pyhton (ce qui fait que le code ne peut pas être 
 
- Rasberry Pi 4
   

Appreil: Jetson Nano 3450

site officiel : https://developer.nvidia.com/embedded/jetson-nano-developer-kit

«Get started»: https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit

Jetson nano est un micro controleur fait pour supporter de l'intelligence artificiel conçu pour traiter des résolution d'images allant jusqu'à 4k. Il est excellent dans le context de traitement d'image ce qui est un élément crucial pour le bon fonctionnement de l'activité du suiveur de main comme l'on doit traiter une image en temps réel. 
La première étape est de flasher une carte micro SD avec l'image officielle fournis par NVIDIA.

Lien pour le téléchargement : https://developer.nvidia.com/jetson-nano-sd-card-image

Cette image utilise Ubuntu 18.04. Nous avons utiliser Balena Etcher pour flasher la carte. Il est fortement recommandé d'utilisé une carte d'au moins 64GB.
Une fois l'image prête, insérez la carte dans le Jetson et alimentez-le. Un configuration de base doit être faite, suivez les étapes présentées à l'écran.
Une fois la configuration terminée, on doit modifier la date et l'heure du Jetson. Le Jetson a un RTC, mais il faut souder une batterie pour 
s'en servir, ce que nous avons pas fait.

        sudo date MMDDhhmmYYYY

Une fois la date bonne, branchez le Jetson a Internet via un cable Ethernet. Le Jetson n'as pas de module Wi-Fi de base. Mettez ensuite a jour les paquets et les drivers:

        sudo apt update && sudo apt upgrade

Le programme Python qui gère les jeux utilise les libraries OpenCV et Mediapipe pour la capture video et la détection d'une main. 

 - https://opencv.org/
 - https://developers.google.com/mediapipe

L'installation de ces libraries sur Jetson ne sont malheureusement pas très intuitive. Voici les guides que nous avons suivi:

- https://www.youtube.com/watch?v=ij9bIET4rCU&ab_channel=EranFeit
- Voir également ce github (référencé dans le video) https://github.com/PINTO0309/mediapipe-bin/tree/main
- Le video suit le guide suivant https://github.com/feitgemel/Jetson-Nano-Python/blob/master/Install-MediaPipe/How%20to%20Install%20MediaPipe%20on%20jetson-nano%202022.txt
- Ce guide est aussi très intéressant et explore plusieurs solutions: https://jetson-docs.federicolanzani.com/libraries/mediapipe/overview#mediapipe-wheels


----- a enlever ou modifier ----
Nous avons eu à apporter les modifications suivantes:

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
    1 - git clone https://github.com/google/mediapipe.git
    2 - cd mediapipe
    3 - python3 -m pip install .

- Installer Serial
    1 - sudo pip3 install serial
    2 - sudo pip3 install pyserial

La communication série du Jetson est sur la pin UartRX sur le port: /dev/ttyS0





