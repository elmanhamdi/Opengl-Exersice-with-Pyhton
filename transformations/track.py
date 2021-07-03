# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021


from enum import Enum


class Transformations(Enum):
    RX = 1
    RY = 2
    RZ = 3
    S = 4
    T = 5


# This class for tracking changes on an object
class Track:

    def __init__(self, max_track_size=20):
        self.track_list = []
        self.max_track_size = max_track_size

    def add(self, tr, x=0, y=0, z=0, s=0, d=0):
        if len(self.track_list) == self.max_track_size:
            self.track_list.pop(0)
        if tr == "RX":
            self.track_list.append([Transformations.RX, d])
        elif tr == "RY":
            self.track_list.append([Transformations.RY, d])
        elif tr == "RZ":
            self.track_list.append([Transformations.RZ, d])
        elif tr == "S":
            self.track_list.append([Transformations.S, s])
        elif tr == "T":
            self.track_list.append([Transformations.T, x, y, z])
        else:
            print("This unexpected transformation value")

    def pop(self):
        if len(self.track_list) != 0:
            self.track_list.pop(len(self.track_list) - 1)
