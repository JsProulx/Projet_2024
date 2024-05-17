# Architecture Github
Répertoire «Logiciel»: contient tous les logiciels que nous avons fait pour le projet (version actuelle, versions antérieures, backups, tests et même le code de notre cours de préparation de projet)




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
