# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021


from utils.pos3d import Pos3d
import copy


class ObjCreate:

    @staticmethod
    def create_objs_list_for_coreprofile2(file_name, scale=1):

        # [[v],[f]:v,[f]:vt, [vt],[vn]]
        tmp_objects = [[], [], [], [], []]
        f = open(file_name, "r")
        lines = (f.read()).split('\n')
        for l in lines:
            lst = l.split(' ')
            if len(lst) != 0:
                a = lst[0:9]
                tmp = []
                if (lst[0] == "v") and (len(lst) == 4):
                    tmp = [float(lst[1]) * scale, float(lst[2]) * scale, float(lst[3]) * scale, 1]
                    tmp_objects[0].append(tmp)

                elif (lst[0] == "f"):
                    for i in lst[1:len(lst)]:
                        tmp.append([int(x) - 1 for x in i.split("/")][0])

                    tmp_objects[1].append(tmp)

                elif (lst[0] == "vt"):
                    for i in lst[1:len(lst)]:
                        tmp.append(float(i))
                    tmp_objects[3].append(tmp)

                elif (lst[0] == "vn"):
                    for i in lst[1:len(lst)]:
                        tmp.append(float(i))
                    tmp_objects[4].append(tmp)

        return tmp_objects

    @staticmethod
    def create_objs_list_for_coreprofile(file_name, scale=1):

        # [[v],[f]:v,[f]:vt, [vt],[vn]]
        tmp_objects = [[], [], [], [], []]
        f = open(file_name, "r")
        lines = (f.read()).split('\n')
        for l in lines:
            lst = l.split(' ')
            if len(lst) != 0:
                a = lst[0:9]
                tmp = []
                if (lst[0] == "v") and (len(lst) == 4):
                    tmp = [float(lst[1]) * scale, float(lst[2]) * scale, float(lst[3]) * scale, 1]
                    tmp_objects[0].append(tmp)

                elif (lst[0] == "f"):
                    for i in lst[1:len(lst)]:
                        tmp.append([int(x) - 1 for x in i.split("/")])

                    tmp_objects[1].append(tmp)

                elif (lst[0] == "vt"):
                    for i in lst[1:len(lst)]:
                        tmp.append(float(i))
                    tmp_objects[3].append(tmp)

                elif (lst[0] == "vn"):
                    for i in lst[1:len(lst)]:
                        tmp.append(float(i))
                    tmp_objects[4].append(tmp)

        tmp_objects[2] = ObjCreate.to_one_property_list(tmp_objects[1], 1)
        tmp_objects[1] = ObjCreate.to_one_property_list(tmp_objects[1], 0)

        return tmp_objects

    # Face list is like [[[2,3,4],[1,4,2],[3,5,3],[1,4,2]], ..]
    # This function select a index and create a list
    @staticmethod
    def to_one_property_list(faces, index):
        face_list = []

        for face in faces:
            tmp = []
            for i in face:
                tmp.append(i[index])
            face_list.append(tmp)
        return face_list
