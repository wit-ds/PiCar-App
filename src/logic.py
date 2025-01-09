#!/usr/bin/env/python

import motorController

motorCtrl = motorController.MotorController(4, 26, 21, 17, 27, 18, True)

class PiCar:

    def __init__(self):
        self.speed_set = 100

    def propulsion(self, command_input, response):
        if 'forward' == command_input:
            print("forward")
            motorCtrl.move_forward(self.speed_set)
        
        elif 'backward' == command_input:
            print("backward")
            motorCtrl.move_backward(self.speed_set)

        elif 'DS' in command_input:
            print("stop")
            motorCtrl.stop()

    