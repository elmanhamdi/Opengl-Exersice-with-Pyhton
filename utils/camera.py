# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

import time
from object_tools.object import Object
from transformations.transformations import Transformations as tr
from utils.vec3d import Vec3d
from utils.mat3d import Mat3d

import numpy


class Camera:

    def __init__(self, eye, center):
        self.eye = eye
        self.center = center
        self.up = Vec3d(1, 0, 0)
        self.camNear = 1.0
        self.camFar = 100.0
        self.camAspect = 1.0
        self.camFov = 60.0

        self.cameraX = Vec3d(0.0, 0.0, 0.0)
        self.cameraY = Vec3d(0.0, 0.0, 0.0)
        self.cameraZ = Vec3d(0.0, 0.0, 0.0)
        self.createView(self.eye, \
                        self.center, \
                        self.up)

    def rotate_overhead(self, degree):

        front_vec, cross_vec, up_vec = self.__calculate_directions()

        new_up = up_vec.add(cross_vec.mul(degree * (1 / 45)))
        new_up = new_up.get_unit_vector().mul(up_vec.get_length())

        self.up = new_up

    def rotate(self, degree_ver, degree_hor, center=None):
        front_vec, cross_vec, up_vec = self.__calculate_directions()

        if center == None:
            center_obj = Object([self.center])

            tr.rotate_x(center_obj, degree_ver * up_vec.x, self.eye)
            tr.rotate_y(center_obj, degree_ver * up_vec.y, self.eye)
            tr.rotate_z(center_obj, degree_ver * up_vec.z, self.eye)

            tr.rotate_x(center_obj, degree_hor * cross_vec.x, self.eye)
            tr.rotate_y(center_obj, degree_hor * cross_vec.y, self.eye)
            tr.rotate_z(center_obj, degree_hor * cross_vec.z, self.eye)

            self.center = center_obj.points[0]
            front_vec = self.__calculate_front_vector(self.eye, self.center)
            self.up = self.__calculate_up_vector(front_vec, cross_vec)

        else:
            center_obj = Object([self.eye])

            tr.rotate_x(center_obj, degree_ver * up_vec.x, center)
            tr.rotate_y(center_obj, degree_ver * up_vec.y, center)
            tr.rotate_z(center_obj, degree_ver * up_vec.z, center)

            tr.rotate_x(center_obj, degree_hor * cross_vec.x, center)
            tr.rotate_y(center_obj, degree_hor * cross_vec.y, center)
            tr.rotate_z(center_obj, degree_hor * cross_vec.z, center)

            self.eye = center_obj.points[0]
            front_vec = self.__calculate_front_vector(self.eye, self.center)
            self.up = self.__calculate_up_vector(front_vec, cross_vec)

    def translation(self, x, y, z):

        front_vec, cross_vec, up_vec = self.__calculate_directions()
        front_vec = front_vec.mul(z)
        cross_vec = cross_vec.mul(x)
        up_vec = up_vec.mul(y)
        trans_vec = (front_vec.add(cross_vec)).add(up_vec)

        center_obj = Object([self.center])
        tr.translate(center_obj, trans_vec.x, trans_vec.y, trans_vec.z)
        self.center = center_obj.points[0]

        eye_obj = Object([self.eye])
        tr.translate(eye_obj, trans_vec.x, trans_vec.y, trans_vec.z)
        self.eye = eye_obj.points[0]

    def slow_center_change(self, new_center):
        partition = 10

        x = (new_center.x - self.center.x)
        y = (new_center.y - self.center.y)
        z = (new_center.z - self.center.z)

        for i in range(0, partition):
            self.center.x += x / partition
            self.center.y += y / partition
            self.center.z += z / partition
            if i == partition - 1:
                self.center.x = x
                self.center.y = y
                self.center.z = z
            time.sleep(1 / partition)

    @staticmethod
    def calculate_front_vector(eye, center):
        front = Vec3d.positions_to_vec(eye, center).get_unit_vector()
        return front

    def get_directions(self, dtype=None):
        front, cross, up = self.__calculate_directions()

        if dtype == "float32":
            front = numpy.array([front.x, front.y, front.z], dtype="float32")
            cross = numpy.array([cross.x, cross.y, cross.z], dtype="float32")
            up = numpy.array([up.x, up.y, up.z], dtype="float32")

        return front, cross, up

    def __calculate_directions(self):
        front = self.__calculate_front_vector(self.eye, self.center)
        cross_vec = front.cross_product(self.up).get_unit_vector()
        up = self.__calculate_up_vector(front, cross_vec)
        return front, cross_vec, up

    @staticmethod
    def __calculate_up_vector(front, cross):
        up = cross.cross_product(front).get_unit_vector()
        return up

    @staticmethod
    def __calculate_front_vector(eye, center):
        front = Vec3d.positions_to_vec(eye, center).get_unit_vector()
        return front

    @staticmethod
    def __calculate_vector_from_points(p1, p2):
        vec = Vec3d.positions_to_vec(p1, p2).get_unit_vector()
        return vec

    # This part implemented from advisor's cpde source to add mouse movement
    def createView(self, eyePoint, centerPoint, upVector):
        self.eye = eyePoint
        self.orgEye = eyePoint

        self.center = centerPoint
        self.orgCenter = centerPoint

        self.up = upVector
        self.orgUp = upVector

        self.computeCamSpace()

    def preDolly(self, x, y, z):

        unCam = self.unRotateCam()
        traCam = Mat3d.create_translation_matrix(x, y, z).transpose()
        toCam = self.rotateCam()

        return Mat3d.product3(unCam, traCam, toCam)

    def dolly(self, x, y, z):
        tx = self.preDolly(x, y, z)
        self.center = tx.vecmul(self.center)
        self.eye = tx.vecmul(self.eye)

    def zoom(self, z):
        tx = self.preDolly(0, 0, z)

        self.center = tx.vecmul(self.center)
        self.eye = tx.vecmul(self.eye)

    def dollyCamera(self, x, y, z):
        preViewVec = self.center - self.eye
        preViewVec = preViewVec.normalize()

        tx = self.preDolly(x, y, z)
        self.eye = tx.vecmul(self.eye)

        postViewVec = self.center - self.eye
        postViewVec = postViewVec.normalize()

        preViewVecYZ = Vec3d(0, preViewVec.y, preViewVec.z)
        preViewVecXZ = Vec3d(preViewVec.x, 0, preViewVec.z)
        postViewVecYZ = Vec3d(0, postViewVec.y, postViewVec.z)
        postViewVecXZ = Vec3d(postViewVec.x, 0, postViewVec.z)

        angleX = postViewVecYZ.angle(preViewVecYZ)
        angleY = postViewVecXZ.angle(preViewVecXZ)

        rot1 = Mat3d.create_rotation_matrix_for_x_axis(-angleX, typ='radian').transpose()
        rot2 = Mat3d.create_rotation_matrix_for_y_axis(-angleY, typ='radian').transpose()
        tmp1 = rot1.product(rot2)
        self.up = tmp1.vecmul(self.up)
        self.computeCamSpace()

    def dollyCenter(self, x, y, z):
        tx = self.preDolly(x, y, z)
        self.center = tx.vecmul(self.center)
        self.computeCamSpace()

    def _create_move_mat(self, point, d):
        moveBack = Mat3d.create_translation_matrix(point.x, point.y, point.z).transpose()
        rot = self.rotCamY(d)
        move = Mat3d.create_translation_matrix(-point.x, -point.y, -point.z).transpose()

        return Mat3d.product3(moveBack, rot, move)

    def pan(self, d):
        moveBack = Mat3d.create_translation_matrix(self.eye.x, self.eye.y, self.eye.z).transpose()
        rot = self.rotCamY(d)
        move = Mat3d.create_translation_matrix(-self.eye.x, -self.eye.y, -self.eye.z).transpose()

        tmp1 = Mat3d.product3(moveBack, rot, move)

        self.center = tmp1.vecmul(self.center)
        self.up = tmp1.vecmul(self.up)

        self.computeCamSpace()

    def tilt(self, d):
        moveBack = Mat3d.create_translation_matrix(self.eye.x, self.eye.y, self.eye.z).transpose()
        rot = self.rotCamX(d)
        move = Mat3d.create_translation_matrix(-self.eye.x, -self.eye.y, -self.eye.z).transpose()

        tmp1 = Mat3d.product3(moveBack, rot, move)

        self.center = tmp1.vecmul(self.center)
        self.up = tmp1.vecmul(self.up)

        self.computeCamSpace()

    def roll(self, d):
        moveBack = Mat3d.create_translation_matrix(self.eye.x, self.eye.y, self.eye.z).transpose()
        rot = self.rotCamZ(d)
        move = Mat3d.create_translation_matrix(-self.eye.x, -self.eye.y, -self.eye.z).transpose()

        tmp1 = Mat3d.product3(moveBack, rot, move)

        self.center = tmp1.vecmul(self.center)
        self.up = tmp1.vecmul(self.up)

        self.computeCamSpace()

    def yaw(self, d):
        moveBack = Mat3d.create_translation_matrix(self.center.x, self.center.y, self.center.z).transpose()
        rot = self.rotCamY(d)
        move = Mat3d.create_translation_matrix(-self.center.x, -self.center.y, -self.center.z).transpose()

        tmp1 = Mat3d.product3(moveBack, rot, move)

        self.eye = tmp1.vecmul(self.eye)
        self.up = tmp1.vecmul(self.up)

        self.computeCamSpace()

    def pitch(self, d):
        moveBack = Mat3d.create_translation_matrix(self.center.x, self.center.y, self.center.z).transpose()
        rot = self.rotCamX(d)
        move = Mat3d.create_translation_matrix(-self.center.x, -self.center.y, -self.center.z).transpose()

        tmp1 = Mat3d.product3(moveBack, rot, move)

        self.eye = tmp1.vecmul(self.eye)
        self.up = tmp1.vecmul(self.up)

        self.computeCamSpace()

    def rotateCam(self):
        return Mat3d([[self.cameraX.x, self.cameraX.y, self.cameraX.z, 0.0, ],
                      [self.cameraY.x, self.cameraY.y, self.cameraY.z, 0.0, ],
                      [self.cameraZ.x, self.cameraZ.y, self.cameraZ.z, 0.0, ],
                      [0.0, 0.0, 0.0, 1.0]]).transpose()

    def unRotateCam(self):
        return Mat3d([[self.cameraX.x, self.cameraY.x, self.cameraZ.x, 0.0, ],
                      [self.cameraX.y, self.cameraY.y, self.cameraZ.y, 0.0, ],
                      [self.cameraX.z, self.cameraY.z, self.cameraZ.z, 0.0, ],
                      [0.0, 0.0, 0.0, 1.0]]).transpose()

    def rotCamX(self, a):
        unCam = self.unRotateCam()
        rotCam = Mat3d.create_rotation_matrix_for_x_axis(a, typ='radian').transpose()
        toCam = self.rotateCam()

        return Mat3d.product3(unCam, rotCam, toCam)

    def rotCamY(self, a):
        unCam = self.unRotateCam()
        rotCam = Mat3d.create_rotation_matrix_for_y_axis(a, typ='radian').transpose()
        toCam = self.rotateCam()

        return Mat3d.product3(unCam, rotCam, toCam)

    def rotCamZ(self, a):
        unCam = self.unRotateCam()
        rotCam = Mat3d.create_rotation_matrix_for_z_axis(a, typ='radian').transpose()
        toCam = self.rotateCam()

        return Mat3d.product3(unCam, rotCam, toCam)

    def computeCamSpace(self):
        self.cameraZ = Vec3d(self.center.x - self.eye.x, self.center.y - self.eye.y, self.center.z - self.eye.z)
        self.cameraZ = self.cameraZ.normalize()

        self.cameraX = self.cameraZ.cross_product(self.up)
        self.cameraX = self.cameraX.normalize()

        self.cameraY = self.cameraX.cross_product(self.cameraZ)
