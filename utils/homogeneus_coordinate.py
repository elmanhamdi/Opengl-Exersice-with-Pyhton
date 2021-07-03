# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021


class HomogeneusCoor:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def add(self, cord):  # It can caused some errors
        x = self.x + cord.x
        y = self.y + cord.y
        z = self.z + cord.z

        return self.__class__(x, y, z)

    def sub(self, cord):
        x = self.x - cord.x
        y = self.y - cord.y
        z = self.z - cord.z

        return self.__class__(x, y, z)

    def mul(self, value):
        x = self.x * value
        y = self.y * value
        z = self.z * value
        w = self.w * value

        tmp = self.__class__(x, y, z)
        tmp.w = w
        return tmp

    def normalize(self):
        l = ((self.x ** 2) + (self.y ** 2) + (self.z ** 2)) ** (1 / 2)
        return self.__class__(self.x / l, self.y / l, self.z / l)

    @staticmethod
    def list_to_homo(lst):
        return HomogeneusCoor(lst[0], lst[1], lst[2], lst[3])

    def to_str(self):
        str = '', self.x, self.y, self.z, self.w
        return str
