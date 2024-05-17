# micro-ordinateur
Ce répertoire contient le programme d'acquisition d'image contenu sur le Jetson Nano et compatible avec le Raspberry pi 4 (si les librairies nécessaires sont préalablement installées).

Les Versions précédentes du projet ont été déplacées dans le dossier «microcontroleur_arch» à des fins d'épurer les sections de code actif

Ce code utilise OpenCV pour la capture vidéo ainsi que MediaPipe pour la détection de mains.

Si une main est détectée, il envoie sa position et son orientation sur le port série.

*La version actuelle du programme est celle qui se nomme : «suiveur_presentoir_VX_X_X_actif»*

*Ces scripts se trouvent dans le répertoire /home/Documents/ du Jetson*

## À lire pour l'acquisition d'image 
Nous avons exploré deux solutions pour la capture vidéo:

**Jetson Nano 3450**

  - Avantages: Plus performant (il a un processeur graphique dédié et un radiateur). Permet d'avoir 10 -20 fps
  
  - Inconvénients: Installation des librairies nécessaires (mediapipe et opencv) beaucoup plus difficile. Ça prend des versions spécifiques des librairies,
  ce qui rend l'installation des dépendances plus difficile, et une version spécifique de python. Ces versions spécifiques sont nécessaires à utiliser correctement les ressources du Jetson.

  - ***Le Jetson Nano est la solution que nous avons privilégiée. C'est ce micro-ordinateur que nous utilisons***
 
**Rasberry Pi 4**
  - Avantages: implantation plus facile. Le Rasberry Pi est compatible avec des versions plus récentes de Linux, ce qui permet la compatibilité avec
  les librairies. Tout est plus facile à appliquer.

  - Inconvénients: Les performances sont limitées par les composantes physiques.
  
### Solution pour le Jetson Nano P3450

> [!NOTE]
> La procédure qui suit est là à titre informative. Pour vous éviter de la faire, nous avons fait une image .iso de notre système. (nom de l'image)
> Il y a aussi certains problèmes avec cette installation. Il y a place a l'optimisation. Elle est par contre suffisante pour notre utilisation.

[site officiel](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)

[«Get started»](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)

Jetson Nano est un micro-ordinateur fait pour supporter de l'intelligence artificielle conçu pour traiter des résolutions d'images allant jusqu'au 4k. Il est excellent dans le contexte de traitement d'image, ce qui est un élément crucial pour le bon fonctionnement de l'activité du suiveur de main comme l'on doit traiter une image en temps réel. La première étape est de «flasher» une carte micro SD avec l'image officielle fournis par NVIDIA. 

[Lien pour le téléchargement](https://developer.nvidia.com/jetson-nano-sd-card-image)

Cette image utilise Ubuntu 18.04. Nous avons utilisé Balena Etcher pour flasher la carte. Il est fortement recommandé d'utiliser une carte d'au moins 64 GB.
Une fois l'image prête, insérez la carte dans le Jetson et alimentez-le. Une configuration de base doit être faite, suivez les étapes présentées à l'écran.
Une fois la configuration terminée, on doit modifier la date et l'heure du Jetson. Le Jetson a un RTC, mais il faut souder une batterie pour s'en servir, ce que nous n’avons pas fait.

        sudo date MMDDhhmmYYYY.ss  #MoisJourHeureMinutesAnnées.Secondes (Il n'est pas crucial que les secondes soient exactes)

Une fois la date configurée, branchez le Jetson à Internet via un câble Ethernet. Le Jetson n'a pas de module Wi-Fi de base. Mettez ensuite à jour les paquets et les «drivers»:

        sudo apt update && sudo apt upgrade

Le programme Python qui gère les jeux utilise les librairies OpenCV et Mediapipe pour la capture vidéo et la détection d'une main.

 - https://opencv.org/
 - https://developers.google.com/mediapipe

L'installation de ces librairies sur Jetson n'est malheureusement pas très intuitive. Voici les guides que nous avons suivis:

- [ce vidéo](https://www.youtube.com/watch?v=ij9bIET4rCU&ab_channel=EranFeit)
- Voir également ce [repertoire github](https://github.com/PINTO0309/mediapipe-bin/tree/main) (référencé dans le vidéo)
- Le vidéo suit ce [guide de l'utilisateur feitgemel](https://github.com/feitgemel/Jetson-Nano-Python/blob/master/Install-MediaPipe/How%20to%20Install%20MediaPipe%20on%20jetson-nano%202022.txt)
- Ce [guide](https://jetson-docs.federicolanzani.com/libraries/mediapipe/overview#mediapipe-wheels) est aussi très intéressant et explore plusieurs solutions

Pour installer les librairies, nous nous sommes principalement basés sur ce [guide](https://github.com/feitgemel/Jetson-Nano-Python/blob/master/Install-MediaPipe/How%20to%20Install%20MediaPipe%20on%20jetson-nano%202022.txt) cité ci-haut.

#### Problème potentiel

Il y a certaines commandes qui peuvent poser problème:

        sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0
        
H5PY est une dépendance de MediaPipe essentiel pour stocker les données et faire les calculs nécessaires. Il faut installer cette version spécifiquement, sinon ce n'est pas compatible
avec notre version de python (3.6.9) et de Mediapipe. Cette solution sur ce [forum](https://forums.developer.nvidia.com/t/failed-building-wheel-of-h5py/263322/5) permet de 
faire l'installation.

        sudo pip3 install opencv_contrib_python

Cette commande ne cause pas d'erreur normalement, mais elle peut être très longue puisqu'elle permet d'installer OpenCV. Il faut être patient :).

        ./v0.8.5/numpy119x/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64_numpy119x_jetsonnano_L4T32.5.1_download.sh

Cette procédure fait installer Mediapipe v0.8.5. Cette version est fonctionnelle, mais moins optimale que certaines versions plus récentes. La version la plus récente de Mediapipe compatible avec notre système est v0.8.9. C'est donc la version que j'ai installée. Le «wheel» d'installation est disponible dans ce [git](https://github.com/anion0278/mediapipe-jetson/tree/main/dist)

        git clone https://github.com/anion0278/mediapipe-jetson/tree/main/dist
        pip3 install mediapipe-0.8.9_cuda102-cp36-cp36m-linux_aarch64.whl


Le reste de la procédure de feitgemel est, normalement, fonctionnelle.

La communication série du Jetson est sur la pine UartTX sur le port: /dev/ttyS0

Nous n'avons pas réussi à créer une configuration du Jetson qui lui permet de démarrer le logiciel d'acquisition d'image. Nous avons essayé les méthodes proposées
sur la communauté de Nvidia mais ces méthodes n'ont pas fonctionné (créer un service ou utiliser «Startup Applications»). 

En revanche, nous l'avons configuré de sorte que le programme se démarre lorsque le profile .bashrc est chargé. Donc, par exemple, dès qu'un terminal est ouvert!
Nous avons configuré le .bashrc à l'aide de la commande :

        cd
        sudo nano .bashrc

Le contenu suivant a été ajouter à la fin du fichier:

        echo "phijes" | sudo -S chmod 666 /dev/ttyS0
        /usr/bin/python3 /home/phijes/Documents/suiveur_presentoir_V1_0_2.py

## Solution pour le Rasberry PI

L'installation des librairies est beaucoup plus simple sur Rasberry PI, car nous pouvons installer l'image qu'on veut. Nous avons imagé la carte SD avec Rasberry Pi Imager. Nous avons pris l'image recommandée par le logiciel (BookWorm avec bureau). Une fois la carte SD imagé, on peut l'insérer dans le PI et l'alimenter. Une fois partie et connectée à internet, faire les commandes suivantes:

    sudo apt update && sudo apt upgrade

Le Rasberry PI4 est compatible avec les dernières versions de Python. Nous avons installé Python 3.10 pour être sur de la compatibilité avec MediaPipe.

Installer Python 3.10:

    sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
    
    cd /emplacement/choisi/pour/l'installation

    wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
      
    tar -xf Python-3.10.0.tgz
  
    cd Python-3.10.0
  
    ./configure --enable-optimizations
  
    make -j "Nombre de cœurs"
  
    sudo make altinstall
    
Installer OpenCV:

    sudo apt install python3-opencv
    
Installer MediaPipe

    git clone https://github.com/google/mediapipe.git
    
    cd mediapipe
    
    python3 -m pip install .

Installer Serial pour la communication série
    
    sudo pip3 install serial
    sudo pip3 install pyserial

La communication série du Rasberry PI est sur la pin UartRX sur le port: /dev/ttyS0


