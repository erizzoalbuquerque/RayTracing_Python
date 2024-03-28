from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.instance import Instance
from RayTracing.shapes import Shape,Sphere,Point
from RayTracing.render import render

import glm

def CreateScene():
    sphere_instance = Instance( glm.vec3(-5,1,-5), Sphere(1) )
    sphere_instance2 = Instance( glm.vec3(3,0,1.25), Sphere(1))
    point_instance = Instance( glm.vec3(0,2,-10), Point())
    scene = Scene([sphere_instance])
    #scene = Scene([point_instance])
    #scene = Scene([])
    
    return scene


if __name__ == '__main__':
    FILE_NAME =  "output.png"
    FILE_PATH =  "../Images"
    WIDTH = 256
    HEIGHT = 128
    
    film = Film(WIDTH,HEIGHT)
    
    camera = Camera(60, 10, WIDTH/HEIGHT, glm.vec3(0,0,0), glm.vec3(0,0,-10), glm.vec3(0,1,0))
    
    scene = CreateScene()
    
    render(film, camera, scene)

    film.image.show()   
    
    # Save Image
    film.save_image(FILE_PATH,FILE_NAME)