import threading

import pygame
import os
import kivy

os.environ['DISPLAY'] = ":0.0"
os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.uix.slider import Slider
from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.uix.image import Image
from kivy.animation import Animation

from datetime import datetime
time = datetime

from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *
from time import sleep

from dpeaDPi.DPiComputer import *
from time import sleep


MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("My Stepper", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
STEPPER_SCREEN_NAME = 'stepper'
SERVO_SCREEN_NAME = 'servo'
TALON_SCREEN_NAME = 'talon'


# STEPPER SETUP BELOW
# STEPPER SHIT
# create stepper object
dpiStepper = DPiStepper()
# set the stepper board number
dpiStepper.setBoardNumber(0)
microstepping = 8
dpiStepper.setMicrostepping(microstepping)
# # waitToFinishFlg = True
# initialize stepper
if dpiStepper.initialize() != True:
    print("Communication with the DPiStepper board failed.")

# SERVO SETUP BELOW
# SERVO SHIT
dpiComputer = DPiComputer()
# create DPiComputer object
dpiComputer.initialize()
# initialize to computers initial values


class MyStepperGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER



Window.clearcolor = (.132, .156, .194, 1)  # White

button_toggle = False

class StepperScreen(Screen):

    def switch(self):
        SCREEN_MANAGER.current = SERVO_SCREEN_NAME

    def switchscreen5(self):
        SCREEN_MANAGER.current = TALON_SCREEN_NAME

    def motorOnOff(self):
        # function that turns on and off the motor

        if self.ids.test_button.text == 'Off':

            print("motorOnOff() called: motor on code")

            self.ids.test_button.text = 'On'

            dpiStepper.enableMotors(True)

            steps_to_move = 100000

            # move the specified number of steps (what stepper, # of steps, wait til finished to move to next bit of code)
            dpiStepper.moveToRelativePositionInSteps(0, steps_to_move, waitToFinishFlg=False)

        else:
            # Disable the motors
            dpiStepper.enableMotors(False)

            self.ids.test_button.text = 'Off'

            print("motorOnOff() called: motor off")

    def switchDirection(self):
    #     motor switches direction
    # when button reads "flip it" it goes counterclockwise

        print("switchDirection() called: flip a biotch code")

        dpiStepper.enableMotors(True)

        if self.ids.test_button3.text == 'bop it, twist it':

            print("switchDirection() called: counterclockwise?")

            self.ids.test_button3.text = 'flip it'

            steps_to_move = -1000000

            # move the specified number of steps (what stepper, # of steps, wait til finished to move to next bit of code)
            dpiStepper.moveToRelativePositionInSteps(0, steps_to_move, waitToFinishFlg=False)

        elif self.ids.test_button3.text == 'flip it':
            print("switchDirection() called: clockwise?")

            self.ids.test_button3.text = 'bop it, twist it'

            steps_to_move = 1000000

            # move the specified number of steps (what stepper, # of steps, wait til finished to move to next bit of code)
            dpiStepper.moveToRelativePositionInSteps(0, steps_to_move, waitToFinishFlg=False)

        else:
            print("something not right")

            dpiStepper.enableMotors(False)

    dpiStepper.enableMotors(False)


    def motorSpecific1(self):
        # motor code with specific pattern
        # 1 revs/sec for 15 revolutions. print current position and pause

        print("motorSpecific1() called: beginning")

        stepper_num = 0
        dpiStepper.enableMotors(True)

        # # set current position to zero
        # dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0.0)

        currentPosition = dpiStepper.getCurrentPositionInRevolutions(0)[1]

        # set speed
        speed_in_revolutions_per_sec = 1.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)

        # move the specified number of steps (what stepper, # position to move to in rev, wait til finished to move to next bit of code)
        dpiStepper.moveToAbsolutePositionInRevolutions(0, 15, waitToFinishFlg=True)
        # waitToFinishFlg=True

        # while not dpiStepper.getMotionComplete(0):
        #     pass

        print("current position in revs: " + str(currentPosition))
        print("motorSpecific1() called: end of one")
        dpiStepper.enableMotors(False)


    def motorSpecific2(self):
        # 5 revs/sec for 10 revolutions. print current position and stop for 8
        print("motorSpecific2() called: beginning of two")

        stepper_num = 0
        dpiStepper.enableMotors(True)

        currentPosition = dpiStepper.getCurrentPositionInRevolutions(0)[1]

        speed_in_revolutions_per_sec = 5.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)

        dpiStepper.moveToRelativePositionInRevolutions(0, 10, waitToFinishFlg=True)

        dpiStepper.enableMotors(False)

        print("current position in revs: " + str(currentPosition))
        print("motorSpecific2() called: end of two")


    def motorSpecific3(self):
        # goes home and stops for 30 secs and then prints get position value
        print("motorSpecific3() called: beginning of three")

        stepper_num = 0
        dpiStepper.enableMotors(True)

        currentPosition = dpiStepper.getCurrentPositionInRevolutions(0)
        # [1]
        # home = dpiStepper.setCurrentPositionInRevolutions(0, 0.0)

        speed_in_revolutions_per_sec = 1.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)

        directionToMoveTowardHome = 1  # 1 Positive Direction -1 Negative Direction
        MaxDistanceToMoveInRevolutions = 1
        # WHAT IS THE POINT OF HOMING IF IT JUST MOVES THE MAX DIST EVERY DAMN TIME

        dpiStepper.moveToHomeInRevolutions(stepper_num, directionToMoveTowardHome, speed_in_revolutions_per_sec, MaxDistanceToMoveInRevolutions)

        dpiStepper.enableMotors(False)

        print("current position in revs: " + str(currentPosition))
        print("motorSpecific3() called: end of three")

    def motorSpecific4(self):
        # 5 revs/sec for 10 revolutions. print current position and stop for 8
        print("motorSpecific4() called: beginning of four")

        stepper_num = 0
        dpiStepper.enableMotors(True)

        currentPosition = dpiStepper.getCurrentPositionInRevolutions(0)[1]

        speed_in_revolutions_per_sec = 8.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)

        dpiStepper.moveToRelativePositionInRevolutions(0, -100, waitToFinishFlg=True)

        dpiStepper.enableMotors(False)

        print("current position in revs: " + str(currentPosition))
        print("motorSpecific4() called: end of four")

    def motorSpecific5(self):
        # goes home and stops for 30 secs and then prints get position value
        print("motorSpecific5() called: beginning of five")

        stepper_num = 0
        dpiStepper.enableMotors(True)

        currentPosition = dpiStepper.getCurrentPositionInRevolutions(0)
        # [1]
        # home = dpiStepper.setCurrentPositionInRevolutions(0, 0.0)

        speed_in_revolutions_per_sec = 1.0
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)

        directionToMoveTowardHome = 1  # 1 Positive Direction -1 Negative Direction
        MaxDistanceToMoveInRevolutions = 1

        dpiStepper.moveToHomeInRevolutions(stepper_num, directionToMoveTowardHome, speed_in_revolutions_per_sec, MaxDistanceToMoveInRevolutions)

        dpiStepper.enableMotors(False)

        print("current position in revs: " + str(currentPosition))
        print("motorSpecific5() called: end of five")

    # dpiStepper.getMotionComplete(False)
    # use this^ instead

    def motorSpecificMother(self):
        print("there will be pauses between movements.")
        print("please do not press anything else during this time")
        self.motorSpecific1() #15 revs
        sleep(10)
        self.motorSpecific2() #10 revs
        sleep(8)
        self.motorSpecific3() #homing
        sleep(30)
        self.motorSpecific4()  # 100 revs counter direction
        sleep(10)
        self.motorSpecific5()  # homie round 2
        print("all done")

    def sliderSpeed(self):
        # use slider to change speed
        print("sliderSpeed() called: you touched the slider")

        stepper_num = 0
        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0)

        gear_ratio = 1
        motor_step_per_revolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motor_step_per_revolution)

        dpiStepper.enableMotors(True)

        speed_in_revolutions_per_sec = int(self.ids.slider.value)
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)

        dpiStepper.moveToAbsolutePositionInRevolutions(stepper_num, 20, waitToFinishFlg=False)

        # sleep(2)
        # dpiStepper.enableMotors(False)


class ServoScreen(Screen):
    def switchscreen2(self):
        SCREEN_MANAGER.current = STEPPER_SCREEN_NAME

    def servo(self):
        print("servo moving")
        # Rotate Servo 0 CW
        i = 0
        servo_number = 0
        for i in range(180):
            dpiComputer.writeServo(servo_number, i)
            sleep(.05)

        # print("  Rotate Servo 0 CCW")
        # i = 0
        # servo_number = 0
        # for i in range(180, 0, -1):
        #     dpiComputer.writeServo(servo_number, i)
        #     sleep(.05)
    #      counter clockwise version

    def limitswitch(self):
        print("switch tings")
        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)
        while True:
            if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):
                # binary bitwise AND of the value returned from read.gpio()
                sleep(1)
                if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):  # a little debounce logic
                    print("Input 0 is HIGH")
            else:
                print("Input 0 is LOW")
                threading.Thread(target=self.servo).start()
                sleep(1)

    def switchthreading(self):
        threading.Thread(target=self.limitswitch).start()
        sleep(2)


class TalonScreen(Screen):
    def switchscreent1(self):
        SCREEN_MANAGER.current = STEPPER_SCREEN_NAME

    def talon(self, x, y, s):
        print("talon moving")
        # green cw
        # red ccw
        # ah-rah-ange is stawp
        # 180 is cw and fast, 0 is ccw and fast, 0 is no movement

        # motor will spin from x to y. will run through fn x amount of times
        # s is time it takes to complete motion.
        i = 0
        servo_number = 0
        for i in range(x, y, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(s)
        print("done")

    def talonspecific(self, x):
        # CW, green light, takes about 20/90
        print("talon specific")
        i = 0
        servo_number = 0
        for i in range(x, 90, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(.2)

    def talonstop(self):
        print("making it stop")
        i = 0
        servo_number = 0
        for i in range(90):
            dpiComputer.writeServo(servo_number, i)
            sleep(0.0)

    def talonthreading(self):
        def talonthreadingbs():
            self.talon(180, 90, .05)
            sleep(.05)
            self.talonspecific(180)
            self.talon(90, 0, .05)
        threading.Thread(target=talonthreadingbs).start()

    def talonlimitswitch(self):
        print("switch tings")
        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)
        while True:
            if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):
                # binary bitwise AND of the value returned from read.gpio()
                sleep(1)
                if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):  # a little debounce logic
                    print("Input 0 is HIGH")
            else:
                print("Input 0 is LOW")
                threading.Thread(target=self.talon(180, 90, .07)).start()
                sleep(1)


Builder.load_file('stepper.kv')
Builder.load_file('servo.kv')
Builder.load_file('talon.kv')
SCREEN_MANAGER.add_widget(StepperScreen(name=STEPPER_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ServoScreen(name=SERVO_SCREEN_NAME))
SCREEN_MANAGER.add_widget(TalonScreen(name=TALON_SCREEN_NAME))

def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    MyStepperGUI().run()