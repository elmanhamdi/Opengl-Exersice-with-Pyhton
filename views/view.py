# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021


from OpenGL.GL import *
from OpenGL.GLUT import *

from lights import SpotLight
from utils import *
from views.ui import UserInterface
from views.control import Control


class View:
    def __init__(self, camera, scene=None, grid=None, shadowStatus=False):
        self.camera = camera
        self.scene = scene
        self.grid = grid
        self.act_obj_i = None
        self.active_obj = None
        self.control = Control(self.camera)
        self.bgColor = [0.1, 0.1, 0.1, 1]
        self.width = 900
        self.height = 900
        self.spin = 1
        self.shadowStatus = shadowStatus

    def setScene(self, scene):
        self.scene = scene

    def setActiveObj(self, act_obj_i):
        self.act_obj_i = act_obj_i
        self.active_obj = self.scene.nodes[act_obj_i]

    def draw_grid(self):
        # use our program
        glUseProgram(self.grid.programID)

        # get matrices and bind them to vertex shader locations
        modelLocation = glGetUniformLocation(self.grid.programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, Mat3d.getModelMatrix(Pos3d(0.0, 0.0, 0.0)))
        viewLocation = glGetUniformLocation(self.grid.programID, "view")

        camZAxis, camYAxis, camXAxis = self.camera.get_directions(dtype="float32")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE,
                           Mat3d.getViewMatrix(camZAxis, camYAxis, camXAxis, self.camera.eye))
        projLocation = glGetUniformLocation(self.grid.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE,
                           Mat3d.getProjMatrix(self.camera.camNear, self.camera.camFar, self.camera.camAspect,
                                               self.camera.camFov))

        # bind to our VAO
        glBindVertexArray(self.grid.VAO)

        if (self.grid.nFaceCorner == 2):
            glDrawArrays(GL_LINES, 0, self.grid.nVertices)

        # reset to defaults
        glBindVertexArray(0)
        glUseProgram(0)

    def draw_light_obj(self, light):

        # use our program
        glUseProgram(light.pointer.programID)

        # get matrices and bind them to vertex shader locations
        modelLocation = glGetUniformLocation(light.pointer.programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, Mat3d.getModelMatrix(Pos3d(0.0, 0.0, 0.0)))
        viewLocation = glGetUniformLocation(light.pointer.programID, "view")

        camZAxis, camYAxis, camXAxis = self.camera.get_directions(dtype="float32")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE,
                           Mat3d.getViewMatrix(camZAxis, camYAxis, camXAxis, self.camera.eye))
        projLocation = glGetUniformLocation(light.pointer.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE,
                           Mat3d.getProjMatrix(self.camera.camNear, self.camera.camFar, self.camera.camAspect,
                                               self.camera.camFov))

        # bind to our VAO
        glBindVertexArray(light.pointer.VAO)

        glDrawArrays(GL_TRIANGLES, 0, light.pointer.nVertices)

        # reset to defaults
        glBindVertexArray(0)
        glUseProgram(0)

    def createShadowMap(self):
        if self.shadowStatus == False:
            for light in self.scene.lights:
                if type(light) == SpotLight:
                    if light.shadowStatus:
                        light.renderShadowMap()

    def display(self):

        self.createShadowMap()
        self.scene.nodes[0].initShadowProperties(self.scene.lights)  # !!!

        glClearColor(self.bgColor[0], self.bgColor[1], self.bgColor[2], self.bgColor[3])
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        UserInterface.draw_info(self.width, self.height, light1=self.scene.lights[0], light2=self.scene.lights[1])

        # use our program
        glUseProgram(self.active_obj.programID)

        # get matrices and bind them to vertex shader locations
        modelLocation = glGetUniformLocation(self.active_obj.programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, Mat3d.getModelMatrix(Pos3d(0.0, 0.0, 0.0)))
        viewLocation = glGetUniformLocation(self.active_obj.programID, "view")

        camZAxis, camYAxis, camXAxis = self.camera.get_directions(dtype="float32")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE,
                           Mat3d.getViewMatrix(camZAxis, camYAxis, camXAxis, self.camera.eye))
        projLocation = glGetUniformLocation(self.active_obj.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE,
                           Mat3d.getProjMatrix(self.camera.camNear, self.camera.camFar, self.camera.camAspect,
                                               self.camera.camFov))

        # bind to our VAO and Texture
        glBindVertexArray(self.active_obj.VAO)
        glActiveTexture(GL_TEXTURE0 + 1)
        glBindTexture(GL_TEXTURE_2D, 1)

        if (self.active_obj.nFaceCorner == 4):
            glDrawArrays(GL_QUADS, 0, self.active_obj.nVertices)

        if (self.active_obj.nFaceCorner == 3):
            glDrawArrays(GL_TRIANGLES, 0, self.active_obj.nVertices)

        if (self.active_obj.nFaceCorner == 2):
            glDrawArrays(GL_LINES, 0, self.active_obj.nVertices)

        self.scene.lights[0].updateCameraPos(
            [self.camera.eye.x, self.camera.eye.y, self.camera.eye.z, self.camera.eye.w])
        self.scene.lights[1].updateCameraPos(
            [self.camera.eye.x, self.camera.eye.y, self.camera.eye.z, self.camera.eye.w])
        self.draw_grid()
        self.draw_light_obj(self.scene.lights[0])
        self.draw_light_obj(self.scene.lights[1])

        # reset to defaults
        glBindVertexArray(0)
        glUseProgram(0)

        glutSwapBuffers()

        # The function called whenever a key is pressed.

    def keyPressed(self, key, x, y):
        self.control.keyPressedforCamera(key, x, y)
        if ord(key) == 27:  # ord() is needed to get the keycode
            glutLeaveMainLoop()

        elif ord(key) == 43:  # +
            self.active_obj.updateTextureRate("increase")

        elif ord(key) == 45:  # -
            self.active_obj.updateTextureRate("decrease")

        elif ord(key) == 104:  # h
            self.scene.nodes[0].transform(1, 0, 0)
            self.scene.nodes[0].initVertexBufferData()
            self.scene.nodes[0].initVertexBuffer()

        elif ord(key) == 122:  # z
            self.scene.lights[0].switchLight()
        elif ord(key) == 120:  # x
            self.scene.lights[1].switchLight()
        elif ord(key) == 99:  # c
            self.scene.lights[0].switchSpecular()
        elif ord(key) == 118:  # v
            self.scene.lights[1].switchSpecular()
        elif ord(key) == 97:  # a
            self.spin = 0 if self.spin == 1 else 1
        elif ord(key) == 113:  # a
            self.scene.nodes[0].switchNormalMapStat()

        self.display()

    def specialKeyPressed(self, key, x, y):
        self.control.specialKeyPressed(key, x, y, self.act_obj_i, self.scene.nodes, self.active_obj)
        self.display()

    # Called whenever the window's size changes (including once when the program starts)
    def reshape(self, w, h):
        self.width = w
        self.height = h
        glViewport(0, 0, w, h)

    def timer(self, value):
        if self.spin == 1:
            self.scene.lights[0].rotate(0, 3, 0)
            from cameras import Camera
            # self.camera = Camera(Pos3d(self.scene.lights[0].lightPos[0], self.scene.lights[0].lightPos[1], self.scene.lights[0].lightPos[2]), Pos3d(self.scene.lights[0].lightPos[0] + self.scene.lights[0].direction[0], self.scene.lights[0].lightPos[1] + self.scene.lights[0].direction[1], self.scene.lights[0].lightPos[2] + self.scene.lights[0].direction[2]))

        glutTimerFunc(16, self.timer, 0);
        glutPostRedisplay()
