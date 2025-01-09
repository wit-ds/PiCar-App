#!/usr/bin/env/python

import RPi.GPIO as GPIO
import time

class MotorController:
    """
    Classe pour contrôler deux moteurs à l'aide d'un Raspberry Pi et de la bibliothèque RPi.GPIO.
    """

    def __init__(self, en_a, in1, in2, en_b, in3, in4, reverse=False):
        """
        Initialise les broches GPIO, configure le PWM pour les deux moteurs et définit le mode de direction.

        :param en_a: Broche GPIO pour l'activation du moteur A.
        :param in1: Broche GPIO pour la direction 1 du moteur A.
        :param in2: Broche GPIO pour la direction 2 du moteur A.
        :param en_b: Broche GPIO pour l'activation du moteur B.
        :param in3: Broche GPIO pour la direction 1 du moteur B.
        :param in4: Broche GPIO pour la direction 2 du moteur B.
        :param reverse: Booléen pour inverser les directions avant et arrière.
        """
        self.en_a = en_a
        self.in1 = in1
        self.in2 = in2
        self.en_b = en_b
        self.in3 = in3
        self.in4 = in4
        self.reverse = reverse

        # Configuration du mode de numérotation des broches
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Configuration des broches en sortie
        GPIO.setup(self.en_a, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en_b, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)

        # Initialisation du PWM sur les broches d'activation des moteurs
        self.pwm_a = GPIO.PWM(self.en_a, 1000)  # Fréquence de 1 kHz
        self.pwm_b = GPIO.PWM(self.en_b, 1000)  # Fréquence de 1 kHz

        # Démarrage du PWM avec un rapport cyclique de 0 (moteurs arrêtés)
        self.pwm_a.start(0)
        self.pwm_b.start(0)

    def set_motor(self, pwm, in_pin1, in_pin2, direction, speed):
        """
        Configure la direction et la vitesse d'un moteur spécifique.

        :param pwm: Instance PWM associée au moteur.
        :param in_pin1: Broche GPIO pour la direction 1 du moteur.
        :param in_pin2: Broche GPIO pour la direction 2 du moteur.
        :param direction: 'forward' pour avancer, 'backward' pour reculer.
        :param speed: Vitesse du moteur (0 à 100).
        """
        # Inversion de la direction si reverse est True
        if self.reverse:
            direction = 'backward' if direction == 'forward' else 'forward'

        # Définition de la direction du moteur
        if direction == 'forward':
            GPIO.output(in_pin1, GPIO.HIGH)
            GPIO.output(in_pin2, GPIO.LOW)
        else:  # direction == 'backward'
            GPIO.output(in_pin1, GPIO.LOW)
            GPIO.output(in_pin2, GPIO.HIGH)

        # Ajustement de la vitesse du moteur
        pwm.ChangeDutyCycle(speed)

    def move_forward(self, speed):
        """
        Fait avancer les deux moteurs à la vitesse spécifiée.

        :param speed: Vitesse des moteurs (0 à 100).
        """
        self.set_motor(self.pwm_a, self.in1, self.in2, 'forward', speed)
        self.set_motor(self.pwm_b, self.in3, self.in4, 'forward', speed)

    def move_backward(self, speed):
        """
        Fait reculer les deux moteurs à la vitesse spécifiée.

        :param speed: Vitesse des moteurs (0 à 100).
        """
        self.set_motor(self.pwm_a, self.in1, self.in2, 'backward', speed)
        self.set_motor(self.pwm_b, self.in3, self.in4, 'backward', speed)

    def turn_left(self, speed):
        """
        Fait tourner le robot vers la gauche en inversant le moteur gauche et en avançant le moteur droit.

        :param speed: Vitesse des moteurs (0 à 100).
        """
        self.set_motor(self.pwm_a, self.in1, self.in2, 'backward', speed)
        self.set_motor(self.pwm_b, self.in3, self.in4, 'forward', speed)

    def turn_right(self, speed):
        """
        Fait tourner le robot vers la droite en avançant le moteur gauche et en inversant le moteur droit.

        :param speed: Vitesse des moteurs (0 à 100).
        """
        self.set_motor(self.pwm_a, self.in1, self.in2, 'forward', speed)
        self.set_motor(self.pwm_b, self.in3, self.in4, 'backward', speed)

    def stop(self):
        """
        Arrête les deux moteurs en mettant le rapport cyclique à 0 et en définissant les broches de direction à LOW.
        """
        self.pwm_a.ChangeDutyCycle(0)
        self.pwm_b.ChangeDutyCycle(0)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)

    def cleanup(self):
        """
        Arrête les moteurs et réinitialise les configurations GPIO.
        """
        self.stop()
        GPIO.cleanup()

# Exemple d'utilisation de la classe MotorController
if __name__ == '__main__':
    try:
        # Initialisation du contrôleur de moteurs avec les broches GPIO correspondantes
        # et inversion de direction activée
        motor_controller = MotorController(
            en_a=4, in1=26, in2=21, en_b=17, in3=27, in4=18, reverse=True
        )

        # Avancer (qui sera inversé en reculer) à 50% de la vitesse pendant 2 secondes
        motor_controller.move_forward(50)
        time.sleep(2)

        # Tourner à gauche à 50% de la vitesse pendant 1 seconde
        motor_controller.turn_left(50)
        time.sleep(1)

        # Tourner à droite à 50% de la vitesse pendant 1 seconde
        motor_controller.turn_right(50)
        time.sleep(1)

        # Reculer (qui sera inversé en avancer) à 50% de la vitesse pendant 2 secondes
        motor_controller.move_backward(50)
        time.sleep(2)

        # Arrêter les moteurs
        motor_controller.stop()
    except KeyboardInterrupt:
        # Gestion de l'interruption clavier pour arrêter proprement les moteurs
        pass
    finally:
        # Nettoyage des configurations GPIO
        motor_controller.cleanup()
