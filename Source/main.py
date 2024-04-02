from RayTracing.color import Color
from RayTracing.light import Light, PointLight
from RayTracing.material import Material, PhongMaterial
from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.instance import Instance, LightInstance, ObjectInstance
from RayTracing.shapes import Shape,Sphere,Point
from RayTracing.render import render

import glm

def CreateScene():
    
    instances = []
    
    instances.append( ObjectInstance( glm.vec3(0,0,10), Sphere(1), PhongMaterial(Color(1,1,1), Color(1,0,0), Color(1,1,1), 10 ) ) )
    instances.append( LightInstance( glm.vec3(0,4,10), Sphere(0.1), PointLight(10) ) )
    #instances.append( Instance( glm.vec3(0,0,10), Point() ) )

    scene = Scene(instances)
    
    return scene


if __name__ == '__main__':
    FILE_NAME =  "output.png"
    FILE_PATH =  "../Images"
    WIDTH = 256
    HEIGHT = 128
    
    film = Film(WIDTH,HEIGHT)
    
    camera = Camera(60, 10, WIDTH/HEIGHT, glm.vec3(0,0,0), glm.vec3(0,0,10), glm.vec3(0,1,0))
    
    scene = CreateScene()
    
    render(film, camera, scene)

    film.image.show()   
    
    # Save Image
    film.save_image(FILE_PATH,FILE_NAME)