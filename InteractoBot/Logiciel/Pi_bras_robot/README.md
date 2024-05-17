# Pi_bras_robot

Le code qui se retrouve dans le Raspberry PI du bras robot est main.py. Il se trouve dans le répertoire /home/Desktop/script_demar

## Section sur le bras robot

Modèle: MyCobot 280 Pi

[Site officiel](https://www.elephantrobotics.com/en/mycobot-pi/)

[Manuel technique](https://www.elephantrobotics.com/wp-content/uploads/2021/03/myCobot-User-Mannul-EN-V20210318.pdf)

[Documentation](https://docs.elephantrobotics.com/docs/gitbook-en/)

Ce bras robot a un RasberryPi 4 d'intégré. Ce PI est configuré avec une image ''custom'' de la compagnie Elephant Robotics.
On peut la télécharger via ce [lien](https://www.elephantrobotics.com/en/downloads/)
Dans notre cas, l'image fournie est basée sur ubuntu 20.04 pour le MyCobot 280 PI.

La communication entre les servos du bras robot et le Pi est faite via
le port série ttyAMA0.

Le code présent sur le bras robot a été programmé directement sur l'appareil. Une copie de ce code figure dans le GitHub du projet dans la section du bras robot.
