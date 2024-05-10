# À lire pour l'utilisation du bras robot 



Ce projet est conçu pour le Département de Technique de Génie Électrique du Cégep de Sherbrooke. On utilise un bras robot 6 axes d'Elephant Robotics. 
Le bras robot a un RasberryPI 4 d'intégré. Ce Pi4 contient les scripts python pour gérer le mouvement des servos moteurs du bras robot. Pour interfacer le module de vision par odinateur, 
nous utilisons un JetSon Nano de Nvidia. Ce microcontroleur traite les données nécessaires et envoie les informations au Pi4 via le port serie. Pour plus d'information sur la connexion, 
veuillez vous référer au plan de connexion.

## Section sur le bras robot

Modèle: MyCobot 280PI

[Site officiel](https://www.elephantrobotics.com/en/mycobot-pi/)

[Manuel technique](https://www.elephantrobotics.com/wp-content/uploads/2021/03/myCobot-User-Mannul-EN-V20210318.pdf)

[Documentation](https://docs.elephantrobotics.com/docs/gitbook-en/)

Ce bras robot a un RasberryPi 4 d'intégré. Ce PI est configurer avec une image ''custom'' de la compagnie Elephant Robotics.
On peut la télécharger via ce [lien](https://www.elephantrobotics.com/en/downloads/)
Dans notre cas, l'image fournie est basé sur ubuntu 20.04 pour le MyCobot 280 PI.

La communication entre les servos du bras robot et le Pi est fait via
le port serie ttyAMA0.

le code présent sur le bras robot a été programmé directement sur l'appareil. Une copie de ce code figure dans le github du projet dans la section du bras robot.

## À lire pour l'acquisition d'image 
Nous avons exploré deux solutions pour la capture vidéo:

**Jetson Nano 3450**

  - Avantages: Plus performant (il a un processeur graphique dédié et un radiateur). Permet d'avoir 10 -20 fps
  
  - Inconvénients: Installation des libraries nécessaires (mediapipe et opencv) beaucoup plus difficile. Ça prend des versions spécifique des libraries,
  ce qui rend l'installation des dépendances plus difficile, et une version spécifique de python. Ces versions spécifiques sont nécessaires utiliser correctement les ressources du Jetson.

  - ***Le Jetson Nano est la solution que nous avons prévilégié. C'est ce microcontroleur que nous utilisons***
 
**Rasberry Pi 4**
  - Avantages: implentation plus facile. Le rasberry Pi est compatible avec des versions plus récente de linux, ce qui permet la compatibilité avec
  les libraries. Tout est plus facile a appliqué.

  - Inconvénients: Les performances sont limité par les composantes physique.
  
### Solution pour le Jetson Nano P3450

> [!NOTE]
> La procédure qui suit est là à titre informative. Pour vous éviter de la faire, nous avons fait une image .iso de notre systeme. (nom de l'image)
> Il y a aussi certains problèmes avec cette installation. Il y a place a l'optimisation. Elle est par contre suffisante pour notre utilisation.

[site officiel](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)

[«Get started»](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)

Jetson nano est un microcontrôleur fait pour supporter de l'intelligence artificiel conçu pour traiter des résolutions d'images allant jusqu'à 4k. Il est excellent dans le contexte de traitement d'image ce qui est un élément crucial pour le bon fonctionnement de l'activité du suiveur de main comme l'on doit traiter une image en temps réel. La première étape est de «flasher» une carte micro SD avec l'image officielle fournis par NVIDIA. 

[Lien pour le téléchargement](https://developer.nvidia.com/jetson-nano-sd-card-image)

Cette image utilise Ubuntu 18.04. Nous avons utiliser Balena Etcher pour flasher la carte. Il est fortement recommandé d'utilisé une carte d'au moins 64GB.
Une fois l'image prête, insérez la carte dans le Jetson et alimentez-le. Un configuration de base doit être faite, suivez les étapes présentées à l'écran.
Une fois la configuration terminée, on doit modifier la date et l'heure du Jetson. Le Jetson a un RTC, mais il faut souder une batterie pour 
s'en servir, ce que nous avons pas fait.

        sudo date MMDDhhmmYYYY.ss  #MoisJourHeureMinutesAnnées.Secondes (Il n'est pas crucial que les secondes soient exactes)

Une fois la date configuré, branchez le Jetson à Internet via un cable Ethernet. Le Jetson n'a pas de module Wi-Fi de base. Mettez ensuite à jour les paquets et les drivers:

        sudo apt update && sudo apt upgrade

Le programme Python qui gère les jeux utilise les libraries OpenCV et Mediapipe pour la capture video et la détection d'une main.

 - https://opencv.org/
 - https://developers.google.com/mediapipe

L'installation de ces libraries sur Jetson n'est malheureusement pas très intuitive. Voici les guides que nous avons suivi:

- [ce video](https://www.youtube.com/watch?v=ij9bIET4rCU&ab_channel=EranFeit)
- Voir également ce [repertoire github](https://github.com/PINTO0309/mediapipe-bin/tree/main) (référencé dans le video)
- Le video suit ce [guide de l'utilisateur feitgemel](https://github.com/feitgemel/Jetson-Nano-Python/blob/master/Install-MediaPipe/How%20to%20Install%20MediaPipe%20on%20jetson-nano%202022.txt)
- Ce [guide](https://jetson-docs.federicolanzani.com/libraries/mediapipe/overview#mediapipe-wheels) est aussi très intéressant et explore plusieurs solutions

Pour installer les librairies, nous nous sommes principalement basé sur ce [guide](https://github.com/feitgemel/Jetson-Nano-Python/blob/master/Install-MediaPipe/How%20to%20Install%20MediaPipe%20on%20jetson-nano%202022.txt) cité ci-haut.

Il y a certaines commandes qui peuvent causer problème:

        sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0
        
H5PY est une dépendance de MediaPipe essentiel pour stocker les données et faire les calculs nécessaires. Il faut installer cette version spécifiquement, sinon ce n'est pas compatible
avec notre version de python (3.6.9) et de mediapipe. Cette solution sur ce [forum](https://forums.developer.nvidia.com/t/failed-building-wheel-of-h5py/263322/5) permet de 
faire l'installation.

        sudo pip3 install opencv_contrib_python

Cette commande ne cause pas d'erreure normalement, mais elle peut être très longue. Il faut être patient :)

        ./v0.8.5/numpy119x/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64_numpy119x_jetsonnano_L4T32.5.1_download.sh

Cette procédure fait installer mediapipe v0.8.5. Cette version est fonctionnel, mais moins optimal que certaines versions plus récentes. La version la plus récente de mediapipe compatible avec notre system est v0.8.9. C'est donc la version que j'ai installé. Le wheel d'installation est disponible dans ce [git](https://github.com/anion0278/mediapipe-jetson/tree/main/dist)

        git clone https://github.com/anion0278/mediapipe-jetson/tree/main/dist
        pip3 install mediapipe-0.8.9_cuda102-cp36-cp36m-linux_aarch64.whl


Le reste de la procédure de feitgemel est, normalement, fonctionnelle.

La communication série du Jetson est sur la pin UartTX sur le port: /dev/ttyS0

Nous n'avons pas réussi à créer une configuration du Jetson qui lui permet de démarrer le logiciel d'acquisition d'image. Nous avons essayer les méthodes proposés
sur la communauté d'Nvidia mais ces méthodes n'ont pas fonctionnés (créer un service ou utiliser «Startup Applications»). 

En revanche, nous l'avons configuré de sorte à ce que le programme se démarre lorsque le profile .bashrc est chargé. Donc, par exemple, dès qu'un terminal est ouvert!
Nous avons configurer le .bashrc à l'aide de la commande :

        cd
        sudo nano .bashrc

Le contenu suivant a été ajouter à la fin du fichier:

        echo "phijes" | sudo -S chmod 666 /dev/ttyS0
        /usr/bin/python3 /home/phijes/Documents/suiveur_presentoir_V1_0_2.py

## Solution pour le rasberry PI

L'installation des librairies est beaucoup plus simple sur Rasberry PI, car nous pouvons installer l'image qu'on veut. Nous avons imagé la carte SD avec Rasberry Pi Imager. Nous avons pris l'image recommandé par le logiciel (BookWorm avec Desktop). Une fois la carte SD imagé, on peut l'insérer dans le PI et l'alimenter. Une fois partie et connecté à internet, faire les commandes suivantes:

    sudo apt update && sudo apt upgrade

Le Rasberry PI4 est compatible avec les dernières version de Python. Nous avons installer Python 3.10 pour être sur de la compatibilité avec MediaPipe.

Installer Python 3.10:

    sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
    
    cd /emplacement/choisi/pour/l'installation

    wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
      
    tar -xf Python-3.10.0.tgz
  
    cd Python-3.10.0
  
    ./configure --enable-optimizations
  
    make -j "Nombre de coeurs"
  
    sudo make altinstall
    
Installer OpenCV:

    sudo apt install python3-opencv
    
Installer MediaPipe

    git clone https://github.com/google/mediapipe.git
    
    cd mediapipe
    
    python3 -m pip install .

Installer Serial pour la communication serie
    
    sudo pip3 install serial
    sudo pip3 install pyserial

La communication série du Rasberry PI est sur la pin UartRX sur le port: /dev/ttyS0

