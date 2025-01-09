#!/usr/bin/env/python

import components.propulsion as propulsionCtrl


class PiCar:

    def __init__(self):
        self.speed_set = 100
        self.propulsion = propulsionCtrl.Propulsion(4, 26, 21, 17, 27, 18, True)

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
