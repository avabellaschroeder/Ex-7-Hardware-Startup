#os.environ['DISPLAY'] = ":0.0"
#os.environ['KIVY_WINDOW'] = 'egl_rpi'
import pygame
import os

from pidev.Joystick import Joystick

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
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'stepper'



# microstepping = 8
# dpiStepper.setMicrostepping(microstepping)



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



dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)
# initialize stepper

if dpiStepper.initialize() != True:
    print("Communication with the DPiStepper board failed.")

dpiStepper.enableMotors(True)


class StepperScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



Builder.load_file('stepper.kv')
SCREEN_MANAGER.add_widget(StepperScreen(name=MAIN_SCREEN_NAME))


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__stepper__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    MyStepperGUI().run()