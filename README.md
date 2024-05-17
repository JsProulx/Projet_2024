
# Un peu de contexte
Ce projet est conçu pour le Département de Technique de Génie Électrique du Cégep de Sherbrooke. On utilise un bras robot 6 axes d'Elephant Robotics. 
Le bras robot a un RasberryPI 4 d'intégré. Ce Pi4 contient les scripts python pour gérer le mouvement des servos moteurs du bras robot. Pour interfacer le module de vision par odinateur, 
nous utilisons un JetSon Nano de Nvidia. Ce microcontroleur traite les données nécessaires et envoie les informations au Pi4 via le port serie. Pour plus d'information sur la connexion, 
veuillez vous référer au plan de connexion.


## Architecture Github

* Voici l'architecture de dossier de notre projet accompagné d'une brève description! *

### Microcontroleur
Ce dossier contient les versions de codes qui ont été implémenté dans le microcontroleur qui gère l'acquisition visuel et la détection de la main. Notre solution finale utilise le Jetson Nano, mais les scripts devraient tous être fonctionnel sur rasberry PI, en assumant que les libraries sont installées correctement.

### PI_bras_robot
Ce dossier contien lea version du code qui est implémenté dans le Rasberry PI 4 embarqué dans le MyCobot 280PI.

### Sources
On retrouve ici les fichiers autres qui ont été utilisé qui ne sont pas du code.

### Archive
Ce fichier sert d'archive pour les codes précédent, les tests ainsi que les fichier du cours préparatoire à ce projet.


