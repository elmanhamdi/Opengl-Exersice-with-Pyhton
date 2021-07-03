# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

from OpenGL.GL import *
from OpenGL.GLUT import *

from lights import PointLight
from utils import *
from object_tools import *
from cameras import Camera

SHADOW_WIDTH, SHADOW_HEIGHT = 1024, 1024
LIGHT_PARAMETER_SIZE = 18

class SpotLight:

    def __init__(self, direction, cutOff, lightPos=[0, 0, 0, 1], lightColor=[1, 1, 1, 1], lightIntensity=0.5,
                 specularStrength=0.8, view=None,
                 pointer=None, programIDs=[], name_extension="", shadowStatus=1, index=-1):
        PointLight.__init__(self, index=index, lightPos=lightPos, lightColor=lightColor, lightIntensity=lightIntensity,
                            specularStrength=specularStrength,
                            pointer=pointer, programIDs=programIDs, name_extension=name_extension)
        self.direction = direction
        self.cutOff = cutOff
        self.shadowStatus = shadowStatus
        self.camera = Camera(Pos3d(lightPos[0], lightPos[1], lightPos[2]),
                             Pos3d(lightPos[0] + direction[0], lightPos[1] + direction[1], lightPos[2] + direction[2]))
        # self.camera.camAspect =1024
        # self.camera.camFov = 400

        self.depthTexture = -1
        self.FBO = -1
        self.programID = -1

        self.effectedObjects = []

        self.view = view


    def setIndex(self, index):
        self.index = index

    def addEffectedObject(self, programID):
        self.programIDs.append(programID)

    def switchLight(self):
        if self.lightIntensity:
            self.lightIntensity = 0.0
        else:
            self.lightIntensity = 0.5

        for programID in self.programIDs:
            # we need to bind to the program to set lighting related params
            glUseProgram(programID)
            lightIntensityLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 8)

            glUniform1f(lightIntensityLocation, self.lightIntensity)
            # reset program
            glUseProgram(0)

    def switchSpecular(self):
        if self.specularStrength:
            self.specularStrength = 0.0
        else:
            self.specularStrength = 0.5

        for programID in self.programIDs:
            # we need to bind to the program to set lighting related params
            glUseProgram(programID)
            lightSpecularStrengthLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 9)
            glUniform1f(lightSpecularStrengthLocation, self.specularStrength)
            # reset program
            glUseProgram(0)

    def transform(self, x, y, z):
        if (self.pointer != None):
            self.pointer.transform(x, y, z)
            self.pointer.initObject()

        self.lightPos[0] += x
        self.lightPos[1] += y
        self.lightPos[2] += z
        for programID in self.programIDs:
            glUseProgram(programID)
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 1)
            glUniform1f(lightPosLocation, self.lightPos[0])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 2)
            glUniform1f(lightPosLocation, self.lightPos[1])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 3)
            glUniform1f(lightPosLocation, self.lightPos[2])
            glUseProgram(0)

    def rotate(self, x, y, z):
        if (self.pointer != None):
            self.pointer.rotate(x, y, z, Pos3d(0, 1, 0))
            self.pointer.initObject()

        tmp_obj = Object([Pos3d(self.lightPos[0], self.lightPos[1], self.lightPos[2])])
        tmp_obj.rotate(x, y, z, Pos3d(0, 1, 0))
        self.lightPos[0] = tmp_obj.points[0].x
        self.lightPos[1] = tmp_obj.points[0].y
        self.lightPos[2] = tmp_obj.points[0].z

        self.direction[0] = 0 - self.lightPos[0]
        self.direction[1] = 1 - self.lightPos[1]
        self.direction[2] = 0 - self.lightPos[2]

        # For camera
        # self.camera = Camera(Pos3d(self.lightPos[0], self.lightPos[1], self.lightPos[2]), Pos3d(0, 1, 0))
        self.camera = Camera(Pos3d(self.lightPos[0], self.lightPos[1], self.lightPos[2]),
                             Pos3d(self.lightPos[0] + self.direction[0], self.lightPos[1] + self.direction[1],
                                   self.lightPos[2] + self.direction[2]))
        # self.camera.rotate(x,y, Pos3d(0, 1, 0))

        for programID in self.programIDs:
            glUseProgram(programID)
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 1)
            glUniform1f(lightPosLocation, self.lightPos[0])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 2)
            glUniform1f(lightPosLocation, self.lightPos[1])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 3)
            glUniform1f(lightPosLocation, self.lightPos[2])

            # reset program
            glUseProgram(0)

    def updateCameraPos(self, cameraPos):
        for programID in self.programIDs:
            glUseProgram(programID)
            if (cameraPos != None):
                camPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 10)
                glUniform1f(camPosLocation, cameraPos[0])
                camPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 11)
                glUniform1f(camPosLocation, cameraPos[1])
                camPosLocation = glGetUniformLocation(programID, "lightParameters") + ((self.index * LIGHT_PARAMETER_SIZE) + 12)
                glUniform1f(camPosLocation, cameraPos[2])

        # reset program
        glUseProgram(0)

    # Initialize the OpenGL environment
    def initLight(self, cameraPos=None, programIDs=None):
        if programIDs != None:
            self.programIDs = programIDs
        if (self.pointer != None):
            self.pointer.transform(self.lightPos[0], self.lightPos[1], self.lightPos[2])
            self.pointer.initObject()

        self.initFBO()
        self.initProgram()

    def initFBO(self):
        self.depthTexture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + self.depthTexture)
        glBindTexture(GL_TEXTURE_2D, self.depthTexture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, SHADOW_WIDTH, SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT,
                     None)
        # glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT,SHADOW_WIDTH, SHADOW_HEIGHT, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1.0, 1.0, 1.0, 1.0])
        # IMPORTANT: ustteki satirisi silip, onu ustindeki satirdali gl_clamp_to_border i gl_repeat gibi cevirme sansin var.

        self.FBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depthTexture, 0)

        # To discard color buffer
        glDrawBuffer(GL_NONE)
        # To avoid some problem on OpenGL3.x
        glReadBuffer(GL_NONE)

        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE):
            print('Some error while creating FBO')

        # Resetting

        glBindTexture(GL_TEXTURE_2D, 0)
        glActiveTexture(GL_TEXTURE0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def initProgram(self):
        self.programID = glCreateProgram()

        file = open("shaders/" + "VertexShaderForShadow.glsl")
        strVertexShader = file.read()
        file = open("shaders/" + "FragmentShaderForShadow.glsl")
        strFragmentShader = file.read()

        shader1ID = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(shader1ID, strVertexShader)
        glCompileShader(shader1ID)
        glAttachShader(self.programID, shader1ID)

        shader2ID = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(shader2ID, strFragmentShader)
        glCompileShader(shader2ID)
        glAttachShader(self.programID, shader2ID)

        glLinkProgram(self.programID)
        glDetachShader(self.programID, shader1ID)
        glDetachShader(self.programID, shader2ID)

        return self.programID

    def renderShadowMap(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

        # glClearColor(0.0, 0.0, 0.0, 0.0)
        glViewport(0, 0, SHADOW_WIDTH, SHADOW_HEIGHT)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        glClear(GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.programID)

        modelLocation = glGetUniformLocation(self.programID, "model")
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, Mat3d.getModelMatrix(Pos3d(0.0, 0.0, 0.0)))
        viewLocation = glGetUniformLocation(self.programID, "view")
        camZAxis, camYAxis, camXAxis = self.camera.get_directions(dtype="float32")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE,
                           Mat3d.getViewMatrix(camZAxis, camYAxis, camXAxis, self.camera.eye))
        projLocation = glGetUniformLocation(self.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE,
                           Mat3d.getProjMatrix(self.camera.camNear, self.camera.camFar, self.camera.camAspect,
                                               self.camera.camFov))

        # Rendering part this part will change
        # bind to our VAO and Texture
        glBindVertexArray(self.view.active_obj.VAO)

        if (self.view.active_obj.nFaceCorner == 4):
            glDrawArrays(GL_QUADS, 0, self.view.active_obj.nVertices)

        if (self.view.active_obj.nFaceCorner == 3):
            glDrawArrays(GL_TRIANGLES, 0, self.view.active_obj.nVertices)

        if (self.view.active_obj.nFaceCorner == 2):
            glDrawArrays(GL_LINES, 0, self.view.active_obj.nVertices)

        glBindVertexArray(0)
        glUseProgram(0)

        # glutSwapBuffers()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glCullFace(GL_BACK)
        glDisable(GL_CULL_FACE)
