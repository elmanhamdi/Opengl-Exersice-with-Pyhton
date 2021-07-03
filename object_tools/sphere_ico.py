# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

import math

from utils import *
from object_tools import *


class Sphere(CpObject):
    def __init__(self, r, sub_div=1, fragmentShader=None, vertexShader=None, faceColorstype=""):
        faces, vertices = self.create_points(r, sub_div)
        CpObject.__init__(self, self.__pos_vertices_to_list(vertices), faces=faces, fragmentShader=fragmentShader,
                          vertexShader=vertexShader, faceColorstype=faceColorstype)

        # Radius of sphere
        self.r = r
        self.sub_div = 1 if sub_div < 1 else sub_div  # Number of subdivision

    def increase_subdiv(self):
        self.__change_subdiv(self.sub_div + 1)

    def decrease_subdiv(self):
        self.__change_subdiv(self.sub_div - 1)

    def __change_subdiv(self, subdiv):
        tmp_sub_div = self.sub_div
        self.sub_div = 1 if subdiv < 1 else subdiv
        if self.sub_div == tmp_sub_div:
            return -1

        faces, vertices = self.create_points(self.r, subdiv)
        temp_obj = CpObject(self.__pos_vertices_to_list(vertices), faces=faces, faceColorstype="random")

        self.vertices = temp_obj.vertices
        self.faces = temp_obj.faces
        self.nFaces = temp_obj.nFaces
        self.nVertices = temp_obj.nVertices
        self.vertexDim = temp_obj.vertexDim
        self.faceColors = temp_obj.faceColors
        self.points = temp_obj.points
        self.matrix = self.get_matrix(self.points)
        self.center = self.get_center(self.points)
        self.initObject()

    def create_points(self, r, subdiv):
        pi = math.pi
        angle_72 = (pi / 180) * 72
        angle_26_565 = math.atan(1 / 2)
        main_vertices = [0] * 12

        hAngle1 = (-pi / 2) - angle_72 / 2
        hAngle2 = (-pi / 2)

        main_vertices[0] = Pos3d(0, 0, r)
        # Every loop for 2 vertices
        for i in range(1, 6):
            z = r * math.sin(angle_26_565)
            xy = r * math.cos(angle_26_565)

            x1 = xy * math.cos(hAngle1)
            x2 = xy * math.cos(hAngle2)
            y1 = xy * math.sin(hAngle1)
            y2 = xy * math.sin(hAngle2)
            z1 = z
            z2 = -z

            main_vertices[i] = Pos3d(x1, y1, z1)
            main_vertices[i + 5] = Pos3d(x2, y2, z2)

            hAngle1 += angle_72
            hAngle2 += angle_72

        main_vertices[11] = Pos3d(0, 0, -r)

        mn = main_vertices
        main_triangles = [[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5], [0, 5, 1],
                          [1, 2, 6], [2, 3, 7], [3, 4, 8], [4, 5, 9], [5, 1, 10],
                          [1, 10, 6], [2, 6, 7], [3, 7, 8], [4, 8, 9], [5, 9, 10],
                          [11, 6, 7], [11, 7, 8], [11, 8, 9], [11, 9, 10], [11, 10, 6]]

        triangles_points_lst, vertices = self.__divide_triangles(main_vertices, main_triangles, r, subdiv)
        return triangles_points_lst, vertices

    def __divide_triangles(self, main_vertices, main_triangles, r, subdiv):
        triangles_lst = main_triangles
        vertices = main_vertices
        for i in range(subdiv - 1):
            tmp_triangles = []
            tmp_vertices = []
            for j in range(0, len(triangles_lst)):
                p1 = vertices[triangles_lst[j][0]]
                p2 = vertices[triangles_lst[j][1]]
                p3 = vertices[triangles_lst[j][2]]
                p1_2 = self.__compute_mid_point(p1, p2, r)
                p1_3 = self.__compute_mid_point(p1, p3, r)
                p2_3 = self.__compute_mid_point(p2, p3, r)

                tmp_vertices.append(p1)
                tmp_vertices.append(p2)
                tmp_vertices.append(p3)
                tmp_vertices.append(p1_2)
                tmp_vertices.append(p1_3)
                tmp_vertices.append(p2_3)

                len_vertices = len(tmp_vertices)

                p1_index = len_vertices - 6
                p2_index = len_vertices - 5
                p3_index = len_vertices - 4

                p1_2_index = len_vertices - 3
                p1_3_index = len_vertices - 2
                p2_3_index = len_vertices - 1

                tmp_triangles.append([p1_index, p1_2_index, p1_3_index])
                tmp_triangles.append([p1_2_index, p2_index, p2_3_index])
                tmp_triangles.append([p1_3_index, p2_3_index, p3_index])
                tmp_triangles.append([p1_2_index, p1_3_index, p2_3_index])

            triangles_lst = tmp_triangles
            vertices = tmp_vertices

        return triangles_lst, vertices

    def __compute_mid_point(self, p1, p2, r):
        x = p1.x + p2.x
        y = p1.y + p2.y
        z = p1.z + p2.z
        scale = r / ((x * x + y * y + z * z) ** (1 / 2))
        return Pos3d(x * scale, y * scale, z * scale)

    def __pos_vertices_to_list(self, vertices):
        vertices_lst = []
        for v in vertices:
            vertices_lst.append([v.x, v.y, v.z, v.w])

        return vertices_lst
