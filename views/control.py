# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

from OpenGL.GLUT import *


class Event:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.button = -1
        self.state = -1
        self.altPressed = False
        self.mouseX = -1
        self.mouseY = -1


class Control:
    def __init__(self, viewCamera):
        self.cameraIsMoving = False
        self.event = Event()
        self.camera = viewCamera

        # The function called whenever a key is pressed.

    def keyPressedforCamera(self, key, x, y):

        if ord(key) == 27:  # ord() is needed to get the keycode
            glutLeaveMainLoop()

        elif ord(key) == 52:
            self.camera.rotate(0, 1)
        elif ord(key) == 54:
            self.camera.rotate(0, -1)
        elif ord(key) == 56:
            self.camera.rotate(1, 0)
        elif ord(key) == 50:
            self.camera.rotate(-1, 0)
        elif ord(key) == 49:  # 1
            self.camera.rotate_overhead(-0.1)
        elif ord(key) == 51:  # 3
            self.camera.rotate_overhead(+0.1)
        elif ord(key) == 107:  # k
            self.camera.translation(0, 0.1, 0)
        elif ord(key) == 106:  # u
            self.camera.translation(-0.1, 0, 0)
        elif ord(key) == 117:  # j
            self.camera.translation(0.1, 0, 0)
        elif ord(key) == 98:  # b
            self.camera.translation(0, 0, 0.1)
        elif ord(key) == 110:  # n
            self.camera.translation(0, 0, -0.1)

    def specialKeyPressed(self, key, x, y, active_object_i, nodes, active_object):
        if key == GLUT_KEY_RIGHT:
            active_object_i = (active_object_i + 1) % len(nodes)
            active_object = nodes[active_object_i]
        elif key == GLUT_KEY_LEFT:
            active_object_i = (active_object_i - 1) % len(nodes)
            active_object = nodes[active_object_i]

    def setCameraIsMoving(self, onOff):
        self.cameraIsMoving = onOff

    def isCameraMoving(self):
        return self.cameraIsMoving

    def mousePressed(self, button, state, x, y):

        self.event.x = x
        self.event.y = y
        self.event.state = state
        self.event.button = button

        # get status of alt key
        m = glutGetModifiers()
        self.event.altPressed = m & GLUT_ACTIVE_ALT

        self.mouseX = x
        self.mouseY = y

        if state == 0:
            if self.event.altPressed > 0:
                self.setCameraIsMoving(True)
        else:
            self.setCameraIsMoving(False)

    def mouseMove(self, x, y):
        if self.event.altPressed == False:
            return

        xSpeed = 0.02
        ySpeed = 0.02
        xOffset = (x - self.mouseX) * xSpeed
        yOffset = (y - self.mouseY) * ySpeed

        if (self.event.button == GLUT_RIGHT_BUTTON):
            self.camera.zoom(-yOffset)
        # self.camera.roll(yOffset)
        elif (self.event.button == GLUT_MIDDLE_BUTTON):
            self.camera.dolly(-yOffset, -xOffset, 0)
        elif (self.event.button == GLUT_LEFT_BUTTON):
            self.camera.yaw(yOffset)
            self.camera.pitch(-xOffset)
        # self.camera.dollyCamera(-xOffset, yOffset, 0)

        # store last positions
        self.mouseX = x
        self.mouseY = y

        # remember this point
        self.event.x = x
        self.event.y = y
