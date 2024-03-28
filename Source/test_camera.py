from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.instance import Instance
from RayTracing.shapes import Shape,Sphere,Point
from RayTracing.render import render

import glm

def CreateScene():
    instances = []       
    
    instances.append( Instance(glm.vec3(0, 0, 10), Sphere(1)) )
    instances.append( Instance(glm.vec3(-10, 0, 0), Sphere(1)) )
    instances.append( Instance(glm.vec3(0, 0, -10), Sphere(1)) )
    instances.append( Instance(glm.vec3(10, 0, 0), Sphere(1)) )
    
    scene = Scene(instances)
    
    return scene

def CreateCameraMovement(number_of_points):
    
    position = []
    target = []
    
    for i in range(number_of_points):
        position.append(glm.vec3(0,0,0))
        target.append(glm.vec3(glm.sin( i * 2 * glm.pi() / number_of_points) * 10, 0, glm.cos( i * 2 *glm.pi() / number_of_points ) * 10))
    
    return position,target              


if __name__ == '__main__':
    FILE_EXTENSION =  ".png"
    FILE_PATH =  "../Images/Test_Camera"
    WIDTH = 256
    HEIGHT = 128
    NUMBER_OF_POINTS = 12
    
    
    film = Film(WIDTH,HEIGHT)
    scene = CreateScene()
    
    cam_position,cam_target = CreateCameraMovement(NUMBER_OF_POINTS)    
    
    for i in range(NUMBER_OF_POINTS):

        camera = Camera(60, 10, WIDTH/HEIGHT, cam_position[i], cam_target[i], glm.vec3(0,1,0))
        render(film, camera, scene)
         # Save Image
        film.save_image(FILE_PATH, str(i)+FILE_EXTENSION)
    

    
    

    
   