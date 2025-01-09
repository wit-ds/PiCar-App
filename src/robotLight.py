#!/usr/bin/env python3
# File name   : servo.py
# Description : Control lights
# Author	  : William
# Date		: 2019/02/23
import time
import RPi.GPIO as GPIO

#  Définition des ports GPIO
port1 = 5  # Port GPIO pour le phare avant droit
port2 = 6  # Port GPIO pour le phare avant gauche
port3 = 13 # Port GPIO pour le phare de la caméra

class RobotLight():
	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(port1, GPIO.OUT)
		GPIO.setup(port2, GPIO.OUT)
		GPIO.setup(port3, GPIO.OUT)

	def switch(self, port, status):
		if port == 1:
			if status == 1:
				GPIO.output(5, GPIO.HIGH)
			elif status == 0:
				GPIO.output(5,GPIO.LOW)
			else:
				pass
		elif port == 2:
			if status == 1:
				GPIO.output(6, GPIO.HIGH)
			elif status == 0:
				GPIO.output(6,GPIO.LOW)
			else:
				pass
		elif port == 3:
			if status == 1:
				GPIO.output(13, GPIO.HIGH)
			elif status == 0:
				GPIO.output(13,GPIO.LOW)
			else:
				pass
		else:
			print('Wrong Command: Example--switch(3, 1)->to switch on port3')

	def set_all_switch_off(self):
		self.switch(1,0)
		self.switch(2,0)
		self.switch(3,0)

if __name__ == '__main__':
	RL=RobotLight()
	RL.switch(1,1)
	time.sleep(2)
	RL.switch(2,1)
	time.sleep(2)
	RL.switch(3,1)
	time.sleep(2)
	RL.set_all_switch_off()