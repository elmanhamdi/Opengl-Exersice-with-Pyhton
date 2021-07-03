# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

from utils.mat3d import Mat3d

class Transformations:

    @staticmethod
    def rotate_x(obj, degree, point=None):
        if point == None:
            mat = Mat3d.create_rotation_matrix_for_x_axis(degree)
            temp_mat = mat.mat_mul(obj.matrix)
            obj.track_list.add("RX", d=degree)
        else:
            temp_mat = Mat3d.create_translation_matrix(-point.x, -point.y, -point.z).mat_mul(obj.matrix)
            mat = Mat3d.create_rotation_matrix_for_x_axis(degree)
            temp_mat = mat.mat_mul(temp_mat)
            temp_mat = Mat3d.create_translation_matrix(point.x, point.y, point.z).mat_mul(temp_mat)
            obj.track_list.add("T", -point.x, -point.y, -point.z)
            obj.track_list.add("RX", d=degree)
            obj.track_list.add("T", point.x, point.y, point.z)

        obj.set_points(temp_mat)
        return mat

    @staticmethod
    def rotate_y(obj, degree, point=None):
        if point == None:
            mat = Mat3d.create_rotation_matrix_for_y_axis(degree)
            temp_mat = mat.mat_mul(obj.matrix)
            obj.track_list.add("RY", d=degree)

        else:
            temp_mat = Mat3d.create_translation_matrix(-point.x, -point.y, -point.z).mat_mul(obj.matrix)
            mat = Mat3d.create_rotation_matrix_for_y_axis(degree)
            temp_mat = mat.mat_mul(temp_mat)
            temp_mat = Mat3d.create_translation_matrix(point.x, point.y, point.z).mat_mul(temp_mat)
            obj.track_list.add("T", -point.x, -point.y, -point.z)
            obj.track_list.add("RY", d=degree)
            obj.track_list.add("T", point.x, point.y, point.z)

        obj.set_points(temp_mat)
        return mat

    @staticmethod
    def rotate_z(obj, degree, point=None):
        if point == None:
            mat = Mat3d.create_rotation_matrix_for_z_axis(degree)
            temp_mat = mat.mat_mul(obj.matrix)
            obj.track_list.add("RY", d=degree)

        else:
            temp_mat = Mat3d.create_translation_matrix(-point.x, -point.y, -point.z).mat_mul(obj.matrix)
            mat = Mat3d.create_rotation_matrix_for_z_axis(degree)
            temp_mat = mat.mat_mul(temp_mat)
            temp_mat = Mat3d.create_translation_matrix(point.x, point.y, point.z).mat_mul(temp_mat)
            obj.track_list.add("T", -point.x, -point.y, -point.z)
            obj.track_list.add("RY", d=degree)
            obj.track_list.add("T", point.x, point.y, point.z)

        obj.set_points(temp_mat)
        return mat

    @staticmethod
    def translate(obj, x, y, z):
        temp_mat = Mat3d.create_translation_matrix(x, y, z).mat_mul(obj.matrix)

        obj.set_points(temp_mat)

        obj.track_list.add("T", x=x, y=y, z=z)

    @staticmethod
    def scale(obj, value):
        temp_mat = Mat3d.create_scale_matrix(value).mat_mul(obj.matrix)

        obj.set_points(temp_mat)

        obj.track_list.add("S", s=value)
