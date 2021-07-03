# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

MAX_NUM_OF_LIGHTS = 8


class Scene:
    def __init__(self):
        self.nodes = []
        self.lights = []

    def add(self, node):
        self.nodes.append(node)

    def addLight(self, light):
        # print(type(light))

        if len(self.lights) > MAX_NUM_OF_LIGHTS + 1:
            print("Max light size  has been exceed")
            exit(1)

        self.lights.append(light)
