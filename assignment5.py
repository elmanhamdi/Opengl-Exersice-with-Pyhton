# CENG 488 Assignment5 version2 by
# Elman Hamdi
# 240201036
# May 2021

from OpenGL.GLUT import *
from cameras import *
from utils import *
from object_tools import *
from scenes import *
from views import *
from lights import *

# Reads shaders from file
file = open("shaders/" + "VertexShader.glsl")
strVertexShader = file.read()
file = open("shaders/" + "FragmentShader.glsl")
strFragmentShader = file.read()

file = open("shaders/" + "VertexShader2.glsl")
strVertexShader2 = file.read()
file = open("shaders/" + "FragmentShader2.glsl")
strFragmentShader2 = file.read()

file = open("shaders/" + "VertexShader3.glsl")
strVertexShader3 = file.read()
file = open("shaders/" + "FragmentShader3.glsl")
strFragmentShader3 = file.read()

# Creates lights
lightObject = Conic(0.05, 0.1, sub_div=10, vertexShader=strVertexShader2, fragmentShader=strFragmentShader2)
light1 = SpotLight(direction=[0, -1, 0, 1], cutOff=50, lightPos=[0.9, 2.4, 0, 1], pointer=lightObject,
                   name_extension='1')
lightObject2 = Sphere(0.05, 2, vertexShader=strVertexShader2, fragmentShader=strFragmentShader2)
light2 = PointLight(lightPos=[0, 0.1, 1, 1], pointer=lightObject2, name_extension='2')

# Creates objects
obj_name = "cornell2.obj"
obj = ObjCreate.create_objs_list_for_coreprofile("objects/" + obj_name, scale=1 / 20)
cornell2 = CpObject(obj[0], obj[1], vertexShader=strVertexShader3, fragmentShader=strFragmentShader3, vertexUVs=obj[3],
                    vertexUVsfaces=obj[2], textureSrc="textures/texture1.png", textureSrc2="textures/texture.png",
                    normalMap="textures/normalMap.png")
obj_list = [cornell2]

# Creates Grid
grid = Grid(20, vertexShader=strVertexShader, fragmentShader=strFragmentShader)

# Creates Camera
camera = Camera(Pos3d(0.8,1.5,4), Pos3d(0,1.2,0))

# create View
view = View(camera, grid=grid)

# !!! Add view to light1 that is spot light
light1.view = view

# init scene
scene = Scene()
view.setScene(scene)

# Add light to scene lights list
# setIndex is important to determine light in list which is sended to shader
light1.setIndex(len(scene.lights))
scene.addLight(light1)
light2.setIndex(len(scene.lights))
scene.addLight(light2)

# add objects to scene obj list.
for obj in obj_list:
    scene.add(obj)

# Set visible object
view.setActiveObj(-1)


# The main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(view.width, view.height)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("CENG488 Assignment 5")

    # Init scene

    # scene.lights[0].initLight(cameraPos = [camera.eye.x, camera.eye.y, camera.eye.z], )
    scene.lights[0].initLight(cameraPos=[camera.eye.x, camera.eye.y, camera.eye.z],
                              programIDs=[scene.nodes[0].programID])
    # scene.lights[1].initLight(cameraPos = [camera.eye.x, camera.eye.y, camera.eye.z])
    scene.lights[1].initLight(cameraPos=[camera.eye.x, camera.eye.y, camera.eye.z],
                              programIDs=[scene.nodes[0].programID])
    scene.nodes[0].initObject(lights=view.scene.lights, cameraPos=[camera.eye.x, camera.eye.y, camera.eye.z])

    scene.lights[0].programIDs = [scene.nodes[0].programID]
    scene.lights[1].programIDs = [scene.nodes[0].programID]

    grid.initObject()

    glutDisplayFunc(view.display)
    glutReshapeFunc(view.reshape)
    glutKeyboardFunc(view.keyPressed)
    glutSpecialFunc(view.specialKeyPressed)
    glutTimerFunc(0, view.timer, 0)

    glutMouseFunc(view.control.mousePressed)
    glutMotionFunc(view.control.mouseMove)

    glutMainLoop()


UserInterface.printConsoleUI()

if __name__ == '__main__':
    main()
