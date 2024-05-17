
# Un peu de contexte
Ce projet est conçu pour le Département de Technique de Génie Électrique du Cégep de Sherbrooke. On utilise un bras robot 6 axes d'Elephant Robotics. 
Le bras robot a un RasberryPI 4 d'intégré. Ce Pi4 contient les scripts python pour gérer le mouvement des servos moteurs du bras robot. Pour interfacer le module de vision par odinateur, 
nous utilisons un JetSon Nano de Nvidia. Ce microcontroleur traite les données nécessaires et envoie les informations au Pi4 via le port serie. Pour plus d'information sur la connexion, 
veuillez vous référer au plan de connexion.


## Architecture Github

*Voici l'architecture de dossier de notre projet accompagné d'une brève description!*

- [Logiciel](InteractoBot/Logiciel)
  - [Archive](InteractoBot/Logiciel/Archive)
    - [Archive du bras robot](InteractoBot/Logiciel/Archive/Bras_Robot_Arch)
    - [Fichiers du cours préparatoire au projet](InteractoBot/Logiciel/Archive/Prep_automne_2023_backup)
    - [Archive du bras microcontroleur](InteractoBot/Logiciel/Archive/microcontroleur_arch)
    - [Archive des codes de tests](InteractoBot/Logiciel/Archive/tests)
  - [MicroControleur](InteractoBot/Logiciel/MicroControleur)
  - [Pi_bras_robot](InteractoBot/Logiciel/Pi_bras_robot)
  - [Sources](InteractoBot/Logiciel/Sources)

### Archive
Nous avons eu a faire l'archivage de nos solutions de tests, nos versions de code précédents celle utilisée ainsi que les fichiers de notre cours préparatoire à ce projet. L'objectif derrière cet archivage est d'épurer l'architecture de notre Github et mieux catégoriser nos fichiers.

### Microcontroleur
Ce dossier contient notre solution finale utilise le Jetson Nano, le script devrai être aussi fonctionnel sur le rasberry PI, en assumant que les libraries sont installées correctement.

### PI_bras_robot
Ce dossier contien la version du code qui est implémenté dans le Rasberry PI 4 embarqué dans le MyCobot 280PI.

### Sources
On retrouve ici les fichiers autres qui ont été utilisé qui ne sont pas du code.

### Archive
Ce fichier sert d'archive pour les codes précédent, les tests ainsi que les fichier du cours préparatoire à ce projet.


