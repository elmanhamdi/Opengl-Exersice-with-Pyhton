# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

from builtins import staticmethod

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class UserInterface:

    @staticmethod
    def glut_text_draw(x, y, text, font=GLUT_BITMAP_HELVETICA_12, color=[1, 1, 1, 1]):

        blending = False
        if glIsEnabled(GL_BLEND):
            blending = True

        glEnable(GL_BLEND)
        glColor3f(color[0], color[1], color[2])
        glWindowPos2f(x, y)
        for ch in text:
            glutBitmapCharacter(font, ctypes.c_int(ord(ch)))

        if not blending:
            glDisable(GL_BLEND)

    # This code is not generic
    @staticmethod
    def draw_info(width, height, light1=None, light2=None):
        UserInterface.glut_text_draw(5, 50, "Z:", color=[0.9, 0.5, 0])
        UserInterface.glut_text_draw(20, 50, "light1 on/off")
        UserInterface.glut_text_draw(5, 35, "X:", color=[0.9, 0.5, 0])
        UserInterface.glut_text_draw(20, 35, "light2 on/off")
        UserInterface.glut_text_draw(5, 20, "C:", color=[0.9, 0.5, 0])
        UserInterface.glut_text_draw(20, 20, "light1 Blinn on/off")
        UserInterface.glut_text_draw(5, 5, "V:", color=[0.9, 0.5, 0])
        UserInterface.glut_text_draw(20, 5, "light2 Blinn on/off")
        UserInterface.glut_text_draw(5, 65, "A:", color=[0.5, 0.5, 0.9])
        UserInterface.glut_text_draw(20, 65, "light1 animation on/off")

        if light1 != None:
            UserInterface.glut_text_draw(width - 100, height - 20, "light1 : ")
            statuslight1 = "OFF" if light1.lightIntensity == 0 else "ON"
            statusColor1 = [0.9, 0.3, 0.3] if light1.lightIntensity == 0 else [0.3, 0.9, 0.3]
            UserInterface.glut_text_draw(width - 60, height - 20, statuslight1, color=statusColor1)

            statuslight3 = "OFF" if light1.specularStrength == 0 else "ON"
            statusColor3 = [0.9, 0.3, 0.3] if light1.specularStrength == 0 else [0.3, 0.9, 0.3]
            UserInterface.glut_text_draw(width - 141, height - 50, "light1's Blinn : ")
            UserInterface.glut_text_draw(width - 60, height - 50, statuslight3, color=statusColor3)

        if light2 != None:
            statuslight2 = "OFF" if light2.lightIntensity == 0 else "ON"
            statusColor2 = [0.9, 0.3, 0.3] if light2.lightIntensity == 0 else [0.3, 0.9, 0.3]
            UserInterface.glut_text_draw(width - 100, height - 35, "light2 : ")
            UserInterface.glut_text_draw(width - 60, height - 35, statuslight2, color=statusColor2)

            statuslight4 = "OFF" if light2.specularStrength == 0 else "ON"
            statusColor4 = [0.9, 0.3, 0.3] if light2.specularStrength == 0 else [0.3, 0.9, 0.3]
            UserInterface.glut_text_draw(width - 141, height - 65, "light2's Blinn : ")
            UserInterface.glut_text_draw(width - 60, height - 65, statuslight4, color=statusColor4)

        UserInterface.glut_text_draw((width - 300) / 2, height - 20, "          q => Open-Close Normal Map")
        UserInterface.glut_text_draw(width - 220, 10, "Use ALT and  MOUSE to use camera")

    @staticmethod
    def printConsoleUI():
        # Print message to console, and kick off the main to get it rolling.

        print("\n WELCOME TO CORE PROFILE PARTY")

        print("\n MAIN KEYS")
        print("ESC			(Hit ESC key to quit.)")

        print("\n FREE CAMERA MOVEMENTS KEYS")
        print("b	- Move forward")
        print("n	- Move backword  ")
        print("h	- Move left")
        print("k 	- Move right")
        print("j	- Move down")
        print("u	- Move up")
        print("8	- Rotate up")
        print("2	- Rotate dowm")
        print("4	- Rotate left")
        print("6	- Rotate right")
        print("1	- Rotate overhead right")
        print("3	- Rotate overhead left")
        print("Note: you can freely move in 3d space")

        print("\n CONTINUOUS ANIMATION")
        print("z	- Light1 on/off")
        print("x	- Light2 on/off")
        print("c	- Light1's Blinn on/off")
        print("v 	- Light2's Blinn on/off")
        print("a	- Light1 animation")

        print("\n BONUS")
        print("q	- Switch Normal Map Property")

        print("-----------------------------------------------------------\n")
