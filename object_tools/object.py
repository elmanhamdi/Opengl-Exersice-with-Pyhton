# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021


from utils.mat3d import Mat3d
from utils.homogeneus_coordinate import HomogeneusCoor
from utils.pos3d import Pos3d
from transformations.track import Track
from transformations.transformations import Transformations


class Object:

    def __init__(self, points, material='None'):
        self.points = points
        self.matrix = self.get_matrix(points)
        self.center = self.get_center(points)
        self.rotations = [0, 0, 0]
        self.translation_mat = Mat3d([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self.track_list = Track()
        self.material = material

    def get_material(self):
        return self.material

    def set_material(self, material):
        self.material = material

    def get_matrix(self, points):
        lst = []
        for i in points:
            k = [i.x, i.y, i.z, i.w]
            lst.append(k)
        return Mat3d(lst).transpose()

    def set_points(self, new_matrix):
        new_matrix = new_matrix.transpose()
        points = []
        for i in new_matrix.matrix_lst:
            a_point = []
            for j in i:
                a_point.append(j)
            p1 = HomogeneusCoor(a_point[0], a_point[1], a_point[2], a_point[3])

            points.append(p1)

        self.points = points
        self.matrix = self.get_matrix(points)
        self.center = self.get_center(points)

    def set_points_with_point_lst(self, points):
        self.points = points
        self.matrix = self.get_matrix(points)
        self.center = self.get_center(points)

    def get_center(self, points):
        center_x = 0
        center_y = 0
        center_z = 0
        num_points = len(points)

        for point in points:
            center_x += point.x
            center_y += point.y
            center_z += point.z

        center_x /= num_points
        center_y /= num_points
        center_z /= num_points

        return Pos3d(center_x, center_y, center_z)

    def rotate(self, deg_x, deg_y, deg_z, point=None):

        if point != None:
            m1 = Transformations.rotate_x(self, deg_x, point)
            m2 = Transformations.rotate_y(self, deg_y, point)
            m3 = Transformations.rotate_z(self, deg_z, point)
        else:
            m1 = Transformations.rotate_x(self, deg_x, self.center)
            m2 = Transformations.rotate_y(self, deg_y, self.center)
            m3 = Transformations.rotate_z(self, deg_z, self.center)

        self.translation_mat = self.translation_mat.mat_mul(m1)
        self.translation_mat = self.translation_mat.mat_mul(m2)
        self.translation_mat = self.translation_mat.mat_mul(m3)

    def transform(self, x, y, z):
        Transformations.translate(self, x, y, z)
