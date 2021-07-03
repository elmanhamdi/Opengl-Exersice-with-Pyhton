# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from utils.mat3d import Mat3d
from utils.pos3d import Pos3d
from object_tools.object import Object

import numpy
import random
from PIL import Image
from math import sqrt


class CpObject(Object):

    def __setFaceColors(self, type="None", colors=[]):
        if (type == "random"):
            faceColors = []
            for i in range(self.nFaces):
                faceColors.append([random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1])

        else:
            faceColors = [[1, 1, 1, 1]] * self.nFaces
        return faceColors

    def __init__(self, vertices, faces=None, faceColors=None, fragmentShader=None, vertexShader=None, faceColorstype="",
                 vertexUVs=None, vertexUVsfaces=None, textureSrc=None, textureSrc2=None, normalMap=None):

        Object.__init__(self, self.vertex_lst_to_points(vertices))
        self.faces = faces
        self.VAO = None
        self.VBO = None
        self.VBOData = None
        self.programID = None
        self.nFaces = len(self.faces)
        self.nVertices = self.nFaces * len(faces[0])
        self.vertexDim = 4 if len(vertices) != 0 else len(vertices[0])
        self.faceColors = faceColors if faceColors is not None else self.__setFaceColors(faceColorstype)
        self.vertexShader = vertexShader
        self.fragmentShader = fragmentShader
        self.nFaceCorner = len(faces[0])

        # !
        self.tex1ID = None
        self.tex2ID = None
        self.vertexUVs = vertexUVs
        self.textureSrc = textureSrc
        self.textureSrc2 = textureSrc2
        self.vertexUVsfaces = vertexUVsfaces
        self.normalMap = normalMap
        self.normalMapStat = 0  # 1 if normalMap is not None else 0

        # This is external part!!
        # self.ThreeCornerVertices = self.findVertices(3, faces)
        # self.FourCornerVertices = self.findVertices(4, faces)
        # self.nThreeDim = len(self.ThreeCornerVertices)
        # self.nFourDim = len(self.FourCornerVertices)

        self.textureRate = numpy.float32(0)

    def updateTextureRate(self, activity='increase', value=numpy.float32(0.1)):
        if (activity == "increase"):
            if (self.textureRate <= 1):
                self.textureRate += value
                if self.textureRate > 0.95:
                    self.textureRate = 1.0

        else:
            if (self.textureRate >= 0):
                self.textureRate -= value
                if self.textureRate < 0.05:
                    self.textureRate = 0.0

        glUseProgram(self.programID)
        myAttrib_location = glGetUniformLocation(self.programID, "textureRate")
        glUniform1f(myAttrib_location, self.textureRate)
        glUseProgram(0)

    def switchNormalMapStat(self):
        self.normalMapStat = 0 if self.normalMapStat else 1

        glUseProgram(self.programID)
        normalStatLocation = glGetUniformLocation(self.programID, "normalMapStat")
        glUniform1i(normalStatLocation, self.normalMapStat)
        glUseProgram(0)

    def findVertices(self, corner, faces):
        tmp_lst = []
        for face in faces:
            if (len(face) == corner):
                tmp_lst.append(face)
        return tmp_lst

    # Function that accepts a list of shaders, compiles them, and returns a handle to the compiled program
    def createProgram(self, shaderList):
        programID = glCreateProgram()

        for shader in shaderList:
            glAttachShader(programID, shader)

        glLinkProgram(programID)

        status = glGetProgramiv(programID, GL_LINK_STATUS)
        if status == GL_FALSE:
            snfoLog = glGetProgramInfoLog(programID)

        # important for cleanup
        for shaderID in shaderList:
            glDetachShader(programID, shaderID)

        return programID

    # Function that creates and compiles shaders according to the given type (a GL enum value) and
    # shader program (a string containing a GLSL program).
    def createShader(self, shaderType, shaderCode):
        shaderID = glCreateShader(shaderType)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)

        status = None
        glGetShaderiv(shaderID, GL_COMPILE_STATUS, status)
        if status == GL_FALSE:
            # Note that getting the error log is much simpler in Python than in C/C++
            # and does not require explicit handling of the string buffer
            strInfoLog = glGetShaderInfoLog(shaderID)
            strShaderType = ""
            if shaderType is GL_VERTEX_SHADER:
                strShaderType = "vertex"
            elif shaderType is GL_GEOMETRY_SHADER:
                strShaderType = "geometry"
            elif shaderType is GL_FRAGMENT_SHADER:
                strShaderType = "fragment"

            print(b"Compilation failure for " + strShaderType + b" shader:\n" + strInfoLog)

        return shaderID

    # Initialize the OpenGL environment
    def initObject(self, cameraPos=None, lights=[], ):
        self.initProgram()
        self.initVertexBufferData()
        self.initVertexBuffer()
        if (self.textureSrc != None):
            self.initTextures(self.textureSrc, self.textureSrc2)
        if (self.normalMap != None):
            self.initNormalMap()
        if len(lights):
            self.initLightParams(cameraPos, lights)
            if (cameraPos != None):
                self.initShadowProperties(lights)

    def initNormalMap(self):
        glUseProgram(self.programID)
        normalStatLocation = glGetUniformLocation(self.programID, "normalMapStat")
        glUniform1i(normalStatLocation, self.normalMapStat)
        glUseProgram(0)

        if self.normalMap != None:
            glUseProgram(self.programID)
            # load texture

            normalMap = self.loadTexture('textures/normalMap.png')

            # set shader stuff
            normalMapLocation = glGetUniformLocation(self.programID, "normalMap")

            glUniform1i(normalMapLocation, normalMap)
            # now activate texture units
            # glActiveTexture(GL_TEXTURE0 )

            # reset program
            glUseProgram(0)

    def initLightParams(self, cameraPos, lights):
        glUseProgram(self.programID)
        lightsParams = []

        nofLightsLocation = glGetUniformLocation(self.programID, "nofLights")
        lightParametersLocation = glGetUniformLocation(self.programID, "lightParameters")

        for light in lights:
            # we need to bind to the program to set lighting related params

            # Append light type #1
            from lights import SpotLight
            if type(light) != SpotLight:
                lightsParams.append(0)
            else:
                lightsParams.append(1)

            # Extend light Positions #3
            lightsParams.extend([light.lightPos[0], light.lightPos[1], light.lightPos[2]])

            # Extend light Colors #4
            lightsParams.extend([light.lightColor[0], light.lightColor[1], light.lightColor[2], light.lightColor[3]])

            # Append light Intensity #1
            lightsParams.append(light.lightIntensity)

            # Append light specularStrength #1
            lightsParams.append(light.specularStrength)

            if (cameraPos != None):
                # Extend light Positions #3
                lightsParams.extend([cameraPos[0], cameraPos[1], cameraPos[2]])

                from lights import SpotLight
                if type(light) == SpotLight:
                    # Append light CutOff
                    lightsParams.append(light.cutOff)
                    # Extend light Direction #3
                    lightsParams.extend([light.direction[0], light.direction[1], light.direction[2]])
                    lightsParams.append(light.shadowStatus)

                else:
                    # Append light CutOff
                    lightsParams.append(0.0)
                    # Extend light Direction #3
                    lightsParams.extend([0.0, 0.0, 0.0])

                    lightsParams.append(0)


            else:
                print('Please add camera position,or light specturum will be fail.')
                lightsParams.extend([0.0, 0.0, 0.0])

                # Append light CutOff
                lightsParams.append(0.0)

                # Extend light Direction #3
                lightsParams.extend([0.0, 0.0, 0.0])

                lightsParams.append(0)

        nofLights = len(lights)
        glUniform1i(nofLightsLocation, nofLights)
        glUniform1fv(lightParametersLocation, 18 * nofLights, lightsParams)

        # reset programxz
        glUseProgram(0)

    def initShadowProperties(self, lights):
        glUseProgram(self.programID)
        lightsViewSpacesLocation = glGetUniformLocation(self.programID, "lightsViewSpaces")
        lightsProjSpacesLocation = glGetUniformLocation(self.programID, "lightsProjSpaces")
        lightsShadowMapsLocation = glGetUniformLocation(self.programID, "lightsShadowMaps")

        lightsViewSpaces = []
        lightsProjSpaces = []
        lightsShadowMaps = []
        for light in lights:
            from lights import SpotLight
            if type(light) == SpotLight:
                # Append light CutOff

                camZAxis, camYAxis, camXAxis = light.camera.get_directions(dtype="float32")

                viewMatrix = Mat3d.getViewMatrix(camZAxis, camYAxis, camXAxis, light.camera.eye).tolist()
                lightsViewSpaces.append(viewMatrix)

                projMatrix = Mat3d.getProjMatrix(light.camera.camNear, light.camera.camFar, light.camera.camAspect,
                                                 light.camera.camFov).tolist()
                lightsProjSpaces.append(projMatrix)

                lightsShadowMaps.append(light.depthTexture)

            else:

                lightsViewSpaces.append([[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]])

                lightsProjSpaces.append([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

                lightsShadowMaps.append(numpy.uint32(0))

            nofLights = len(lights)
            glUniformMatrix4fv(lightsViewSpacesLocation, nofLights, GL_FALSE, lightsViewSpaces)
            glUniformMatrix4fv(lightsProjSpacesLocation, nofLights, GL_FALSE, lightsProjSpaces)

            glUniform1iv(lightsShadowMapsLocation, nofLights, lightsShadowMaps)

        # reset programSS
        glUseProgram(0)

    # Set up the list of shaders, and call functions to compile them
    def initProgram(self):
        shaderList = []

        shaderList.append(self.createShader(GL_VERTEX_SHADER, self.vertexShader))
        shaderList.append(self.createShader(GL_FRAGMENT_SHADER, self.fragmentShader))
        self.programID = self.createProgram(shaderList)

        for shader in shaderList:
            glDeleteShader(shader)

    # vector stuff
    def dot(self, vec1, vec2):
        return 1.0 * numpy.dot(vec2, vec1)

    def cross(self, vec1, vec2):
        result = numpy.cross(vec1[0:3], vec2[0:3], axisa=0, axisb=0, axisc=0)
        return numpy.array([result[0], result[1], result[2], 0.0], dtype='float32')

    def normalize(self, vec):
        vecLen = sqrt(1.0 * numpy.dot(vec, vec))
        return vec / vecLen

    def initVertexBufferData(self):
        finalVertexPositions = []
        finalVertexColors = []
        finalVertexUvs = []
        finalVertexNormals = []

        # now assemble arrays
        vertices = self.points_to_vertices(self.points);
        faceID = 0
        for f_i in range(len(self.faces)):
            # go over faces and assemble an array for all vertex data
            if self.nFaceCorner > 2:
                edge1 = numpy.array([a - b for a, b in zip(vertices[self.faces[f_i][1]], vertices[self.faces[f_i][0]])],
                                    dtype='float32')
                edge2 = numpy.array([a - b for a, b in zip(vertices[self.faces[f_i][2]], vertices[self.faces[f_i][0]])],
                                    dtype='float32')
                faceNormal = self.normalize(self.cross(edge1, edge2))
            else:
                faceNormal = [0, 0, 0, 0]

            for v_i in range(len(self.faces[f_i])):

                finalVertexPositions.extend(vertices[self.faces[f_i][v_i]])
                finalVertexColors.extend(self.faceColors[faceID])
                if (self.vertexUVs != None):
                    finalVertexUvs.extend(self.vertexUVs[self.vertexUVsfaces[f_i][v_i]])
                else:
                    finalVertexUvs.extend([0, 0])
                finalVertexNormals.extend(faceNormal)

            faceID += 1

        self.VBOData = numpy.array(finalVertexPositions + finalVertexColors + finalVertexUvs + finalVertexNormals,
                                   dtype='float32')

    # Set up the vertex buffer that will store our vertex coordinates for OpenGL's access
    def initVertexBuffer(self):

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        # bind to our VAO
        glBindVertexArray(self.VAO)

        # now change the state S- it will be recorded in the VAO
        # set array buffer to our ID
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # set data
        # !!!!bufferData = numpy.concatenate((vertexPositions, vertexColors, vertexUVs))
        elementSize = numpy.dtype(numpy.float32).itemsize

        # third argument is criptic - in c_types if you multiply a data type with an integer you create an array of that type
        glBufferData(GL_ARRAY_BUFFER,
                     len(self.VBOData) * elementSize,
                     self.VBOData,
                     GL_STATIC_DRAW
                     )

        # setup vertex attributes
        offset = 0

        # location 0
        glVertexAttribPointer(0, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        # define colors which are passed in location 1 - they start after all positions and has four floats consecutively
        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(1, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)

        # define uvs which are passed in location 2 - they start after all positions and colors and has two floats per vertex
        offset += elementSize * self.vertexDim * self.nVertices
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, elementSize * 2, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(2)

        # define normals which are passed in location 3 - they start after all positions, colors and uvs and has four floats per vertex
        offset += elementSize * 2 * self.nVertices
        glVertexAttribPointer(3, self.vertexDim, GL_FLOAT, GL_FALSE, elementSize * self.vertexDim,
                              ctypes.c_void_p(offset))
        glEnableVertexAttribArray(3)
        # reset array buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Added ids to global lists

    # ! texture stuff
    def initTextures(self, texFilename, texFilename2=None):
        # we need to bind to the program to set texture related params
        glUseProgram(self.programID)

        # load texture

        self.tex1ID = self.loadTexture(texFilename)

        # set shader stuff
        tex1Location = glGetUniformLocation(self.programID, "tex1")

        glUniform1i(tex1Location, self.tex1ID)
        # now activate texture units
        glActiveTexture(GL_TEXTURE0 + self.tex1ID)

        if (texFilename2 != None):
            # load texture
            self.tex2ID = self.loadTexture(texFilename2)
            tex2Location = glGetUniformLocation(self.programID, "tex2")

            glUniform1i(tex2Location, self.tex2ID)
            glActiveTexture(GL_TEXTURE0 + self.tex2ID)

        glUseProgram(self.programID)
        myAttrib_location = glGetUniformLocation(self.programID, "textureRate")
        glUniform1f(myAttrib_location, self.textureRate)

        # reset program
        glUseProgram(0)

    def loadTexture(self, texFilename):
        # load texture - flip int verticallt to convert from pillow to OpenGL orientation
        image = Image.open(texFilename).transpose(Image.FLIP_TOP_BOTTOM)

        # create a new id
        texID = glGenTextures(1)
        # bind to the new id for state
        glBindTexture(GL_TEXTURE_2D, texID)

        # set texture params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # copy texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                     numpy.frombuffer(image.tobytes(), dtype=numpy.uint8))
        glGenerateMipmap(GL_TEXTURE_2D)

        return texID

    def vertex_lst_to_points(self, vertices):
        points = []
        for vertex in vertices:
            points.append(Pos3d(vertex[0], vertex[1], vertex[2]))
        return points

    def points_to_vertices(self, points):
        vertices = []
        for p in points:
            vertices.append([p.x, p.y, p.z, p.w])
        return vertices

    def setFaceColors(self, faceColors):
        self.faceColors = faceColors

    def showAllProperties(self):
        print("vertices:", self.points_to_vertices(self.points), "\n")
        print("faces:", self.faces, "\n")
        print("VAO:", self.VAO)
        print("VBO:", self.VBO)

        print("programID:", self.programID)
        print("nFaces:", self.nFaces)
        print("nVertices:", self.nVertices)
        print("vertexDim:", self.vertexDim)

        print(" :vertexUVs", self.vertexUVs)
        print("n:vertexUVs", self.vertexUVsfaces)

        print("faceColors", self.faceColors)

        print("Data", self.VBOData)

        print("--------------------------------------------------------------")
