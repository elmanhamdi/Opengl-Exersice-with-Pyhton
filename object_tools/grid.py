# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021


import math

from utils import *
from object_tools import *


class Grid(CpObject):
    def __init__(self, size, fragmentShader = None, vertexShader = None, ):
        vertices,lines, line_colors = self.create_grid(size)
        CpObject.__init__(self, vertices, faces=lines, faceColors=line_colors, fragmentShader=fragmentShader, vertexShader=vertexShader)


    @staticmethod
    def create_grid(size):
        half_size = int(size/2)
        vertices = []
        lines = []
        line_colors = []
        rate = 1
        for i in range(-half_size, half_size, 1):
            if i % 4 == 0:
                line_colors.append([0.2,0.2,0.2, 1])
                line_colors.append([0.2,0.2,0.2, 1])
            else:
                line_colors.append([0.3, 0.3, 0.3, 1])
                line_colors.append([0.3, 0.3, 0.3, 1])

            vertices.append([i/rate, 0, -half_size/rate, 1])
            vertices.append([i/rate, 0,  half_size/rate, 1])
            lines.append([len(vertices) - 2, len(vertices) - 1])

            vertices.append([-half_size/rate, 0, i/rate, 1])
            vertices.append([half_size/rate, 0, i/rate, 1])
            lines.append([len(vertices) - 2, len(vertices) - 1])

        return vertices, lines, line_colors


