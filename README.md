
# Un peu de contexte
Ce projet est conçu pour le Département de génie électrique du Cégep de Sherbrooke. On utilise un bras robot 6 axes d'Elephant Robotics. 
Le bras robot a un RasberryPI 4 d'intégré. Ce Pi4 contient les scripts python pour gérer le mouvement des servomoteurs du bras robot. Pour interfacer le module de vision par ordinateur, 
nous utilisons un JetSon Nano de Nvidia. Ce microordinateur traite les données nécessaires et envoie les informations au Pi4 par le port série. Pour plus d'information sur la connexion, 
veuillez vous référer au plan de connexion.


## Architecture Github

*Voici l'architecture de dossier de notre projet accompagné d'une brève description!*

- [Logiciel](InteractoBot/Logiciel)
  - [Archives](InteractoBot/Logiciel/Archive)
    - [Bras robot](InteractoBot/Logiciel/Archive/Bras_Robot_Arch)
    - [Fichiers du cours préparatoire au projet](InteractoBot/Logiciel/Archive/Prep_automne_2023_backup)
    - [Microcontroleur](InteractoBot/Logiciel/Archive/microcontroleur_arch)
    - [Codes de tests](InteractoBot/Logiciel/Archive/tests)
  - [MicroControleur](InteractoBot/Logiciel/MicroControleur)
  - [Pi_bras_robot](InteractoBot/Logiciel/Pi_bras_robot)
  - [Sources](InteractoBot/Logiciel/Sources)

### Archive
Nous avons eu à faire l'archivage de nos solutions de tests, nos versions de code précédentes ainsi que les fichiers de notre cours préparatoire à ce projet. L'objectif derrière cet archivage est d'épurer l'architecture de notre Github et mieux catégoriser nos fichiers.

### Microordinateur
Ce dossier contient notre solution finale, utilise le Jetson Nano, le script devrait être aussi fonctionnel sur le Rasberry PI, en assumant que les libraires sont installées correctement.

### PI_bras_robot
Ce dossier contient la version du code qui est implémenté dans le Rasberry PI 4 embarqué dans le MyCobot 280 Pi.

### Sources
On retrouve ici les fichiers autres qui ont été utilisés et qui ne sont pas du code.

