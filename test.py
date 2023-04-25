
import pyautogui
import time
from pynput.keyboard import Controller, Key


keyboard=Controller()
while(True):
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

