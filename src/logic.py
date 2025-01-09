#!/usr/bin/env/python

import components.propulsion as propulsionCtrl
import components.neoPixel as neoPixelCtrl

# Définition des couleurs (RGB)
colorRed = (255, 0, 0)
colorGreen = (0, 255, 0)
colorBlue = (0, 0, 255)

class PiCar:

    def __init__(self):
        self.speed_set = 100
        self.propulsion = propulsionCtrl.Propulsion(4, 26, 21, 17, 27, 18, True)
        try:
            self.neoPixel=neoPixelCtrl.NeoPixel()
            self.neoPixel.start()
            self.neoPixel.breath(0,255,0)
        except:
            pass
    
    def setError(self, message, error):
        print(message)
        print(error)
        self.neoPixel.setColor(colorRed[0], colorRed[1], colorRed[2])
        
    def setInitied(self):
        self.neoPixel.breath(0,0,255)

    def move(self, command_input, response):
        if 'forward' == command_input:
            print("forward")
            self.propulsion.move_forward(self.speed_set)
        
        elif 'backward' == command_input:
            print("backward")
            self.propulsion.move_backward(self.speed_set)

        elif 'DS' in command_input:
            print("stop")
            self.propulsion.stop()

    def cleanup(self):
        """
        Arrête les moteurs et réinitialise les configurations GPIO.
        """
        self.propulsion.stop()
        self.propulsion.cleanup()
        self.neoPixel.setColor(0, 0, 0)
