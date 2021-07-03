# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

from OpenGL.GL import *
import numpy
from utils import *
from object_tools import *

LIGHT_PARAMETER_SIZE = 18


class PointLight:
    def __init__(self, lightPos=[0, 0, 0, 1], lightColor=[1, 1, 1, 1], lightIntensity=0.5, specularStrength=0.8,
                 pointer=None, programIDs=[], name_extension="", index=-1):

        # Check some exceptions
        if len(lightPos) < 3:
            print("Unsufficient size of lightPos")
            exit(1)
        elif len(lightColor) < 3:
            print("Unsufficient size of lightColor")
            exit(1)

        self.lightPos = numpy.array([lightPos[0], lightPos[1], lightPos[2], 1.0], dtype='float32')
        self.lightColor = numpy.array([lightColor[0], lightColor[1], lightColor[2], 1], dtype='float32')
        self.lightIntensity = lightIntensity
        self.specularStrength = specularStrength
        self.pointer = pointer
        self.programIDs = programIDs
        self.name_extension = name_extension
        self.index = index

    def setIndex(self, index):
        self.index = index

    def addEffectedObject(self, programID):
        self.programIDs.append(programID)

    # Initialize the OpenGL environment
    def initLight(self, cameraPos=None, programIDs=None):
        if programIDs != None:
            self.programIDs = programIDs
        if (self.pointer != None):
            self.pointer.transform(self.lightPos[0], self.lightPos[1], self.lightPos[2])
            self.pointer.initObject()

    def switchLight(self):
        if self.lightIntensity:
            self.lightIntensity = 0.0
        else:
            self.lightIntensity = 0.5

        for programID in self.programIDs:
            # we need to bind to the program to set lighting related params
            glUseProgram(programID)
            lightIntensityLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 8)
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
            lightSpecularStrengthLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 9)
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
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 1)
            glUniform1f(lightPosLocation, self.lightPos[0])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 2)
            glUniform1f(lightPosLocation, self.lightPos[1])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 3)
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
        for programID in self.programIDs:
            glUseProgram(programID)

            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 1)
            glUniform1f(lightPosLocation, self.lightPos[0])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 2)
            glUniform1f(lightPosLocation, self.lightPos[1])
            lightPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                        (self.index * LIGHT_PARAMETER_SIZE) + 3)
            glUniform1f(lightPosLocation, self.lightPos[2])

            # reset program
            glUseProgram(0)

    def updateCameraPos(self, cameraPos):
        for programID in self.programIDs:
            glUseProgram(programID)
            if (cameraPos != None):
                camPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                            (self.index * LIGHT_PARAMETER_SIZE) + 10)
                glUniform1f(camPosLocation, cameraPos[0])
                camPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                            (self.index * LIGHT_PARAMETER_SIZE) + 11)
                glUniform1f(camPosLocation, cameraPos[1])
                camPosLocation = glGetUniformLocation(programID, "lightParameters") + (
                            (self.index * LIGHT_PARAMETER_SIZE) + 12)
                glUniform1f(camPosLocation, cameraPos[2])
        # reset program
        glUseProgram(0)
