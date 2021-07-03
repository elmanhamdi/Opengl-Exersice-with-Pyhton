# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021


import math

from utils import *
from object_tools import *

class Conic(CpObject):
    def __init__(self, r, h, sub_div = 3, fragmentShader = None, vertexShader = None, faceColorstype = ""):
        #Radius of sphere
        self.r = r 
        #Radius of height
        self.h = h 
        self.sub_div = 3 if sub_div < 3 else sub_div  #Number of subdivision  
          
        faces, vertices = self.create_points(r, h, sub_div)
        CpObject.__init__(self, self.__pos_vertices_to_list(vertices), faces = faces, fragmentShader = fragmentShader, vertexShader = vertexShader, faceColorstype = faceColorstype)



    def increase_subdiv(self):
        self.__change_subdiv(self.sub_div + 1)
        
        
    def decrease_subdiv(self):
        self.__change_subdiv(self.sub_div - 1)

    def __change_subdiv(self,subdiv):
        tmp_sub_div = self.sub_div
        self.sub_div = 3 if subdiv < 3 else subdiv
        if self.sub_div == tmp_sub_div:
            return -1  	
        
        t_faces, t_vertices = self.create_points(self.r, self.h, self.sub_div)
        temp_obj = CpObject(self.__pos_vertices_to_list(t_vertices), faces = t_faces, faceColorstype = "random")
        
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

    def create_points(self,r, h, subdiv):
        pi = math.pi
        h = h / 2
        first_point = Pos3d(0, -h ,r)
        origin = Pos3d(0, 0, 0)
        top_point = Pos3d(0,h,0)
        angle = 2 * pi / subdiv
        points = [origin, first_point]


        for i in range(1,subdiv):
            point = Pos3d.rotate_point(first_point, origin, angle*i)
            points.append(point)


        points.append(top_point)
        top_point_i = len(points) - 1



        faces = []

        for i in range(1,len(points) - 1):
            if (i == len(points) - 2):
                faces.append([top_point_i, i, 1])
                print('else')
               #faces.append([i , subdiv + i + 1, 1])
               #faces.append([subdiv + i + 1 ,  1, subdiv + 2])
            else:
               faces.append([top_point_i, i, i + 1])

               #faces.append([i , subdiv + i + 1, i + 1])
               #faces.append([subdiv + i + 1,  subdiv+ i + 2, i + 1])
        return  faces, points

        
    def __pos_vertices_to_list(self,vertices):
        vertices_lst = []
        for v in vertices:
            vertices_lst.append([v.x, v.y, v.z, v.w])
            
        return vertices_lst


