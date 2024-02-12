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


MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("My Stepper", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
STEPPER_SCREEN_NAME = 'stepper'

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

# create stepper object
dpiStepper = DPiStepper()

# set the stepper board number
dpiStepper.setBoardNumber(0)

microstepping = 8
dpiStepper.setMicrostepping(microstepping)

# waitToFinishFlg = True

# initialize stepper
if dpiStepper.initialize() != True:
    print("Communication with the DPiStepper board failed.")




class StepperScreen(Screen):

    # microstepping = 8
    # dpiStepper.setMicrostepping(microstepping)
    # speed_steps_per_second = 200 * microstepping
    # accel_steps_per_second_per_second = speed_steps_per_second
    # dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
    # dpiStepper.setSpeedInStepsPerSecond(1, speed_steps_per_second)
    # dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
    # dpiStepper.setAccelerationInStepsPerSecondPerSecond(1, accel_steps_per_second_per_second)


    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from StepperScreen.pressed()")

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


    def motorSpecific(self):
            # motor code with specific pattern

            dpiStepper.enableMotors(True)

            steps_to_move = 1000

            # move the specified number of steps (what stepper, # of steps, wait til finished to move to next bit of code)
            dpiStepper.moveToRelativePositionInSteps(0, steps_to_move, waitToFinishFlg=True)

            dpiStepper.enableMotors(False)

            print("motorSpecific() called: motor on code")

    def sliderSpeed(self):
        # use slider to change speed
        print("sliderSpeed() called: you touched the slider")

        stepper_num = 0
        dpiStepper.setCurrentPositionInSteps(stepper_num, 0)

        speed_steps_per_second = 200 * microstepping
        directionToMoveTowardHome = 1  # 1 Positive Direction -1 Negative Direction
        homeSpeedInStepsPerSecond = speed_steps_per_second / 2
        homeMaxDistanceToMoveInSteps = 3200

        dpiStepper.enableMotors(True)

        dpiStepper.moveToHomeInSteps(stepper_num, directionToMoveTowardHome, homeSpeedInStepsPerSecond, homeMaxDistanceToMoveInSteps)

        speed_in_revolutions_per_sec = int(self.ids.slider.value)
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)


        dpiStepper.moveToAbsolutePositionInSteps(stepper_num, 1600, waitToFinishFlg=False)

        dpiStepper.enableMotors(False)






Builder.load_file('stepper.kv')
SCREEN_MANAGER.add_widget(StepperScreen(name=STEPPER_SCREEN_NAME))


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

    