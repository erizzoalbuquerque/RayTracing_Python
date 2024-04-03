from RayTracing.color import Color
from RayTracing.light import Light, PointLight
from RayTracing.material import Material, PhongMaterial
from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.instance import Instance, LightInstance, ObjectInstance
from RayTracing.shapes import Shape,Sphere,Point,Plane
from RayTracing.render import render

import glm

def CreateScene():
    
    instances = []
    
    # LIGHTS
    instances.append( LightInstance( glm.vec3(0,4,10), Sphere(0.1), PointLight(10) ) )
        
    # OBJECTS
    instances.append( ObjectInstance( glm.vec3(0,0,10), Plane( glm.vec3(0,1,0) ), PhongMaterial( Color(1,1,1), Color(0,1,0), Color(0,0,0), 10 ) ) )
    instances.append( ObjectInstance( glm.vec3(1,0.5,9), Sphere(0.5), PhongMaterial( Color(1,1,1), Color(0,0,1), Color(1,1,1), 10 ) ) )
    instances.append( ObjectInstance( glm.vec3(0,0,10), Sphere(1), PhongMaterial( Color(1,1,1), Color(1,0,0), Color(1,1,1), 10 ) ) )

    scene = Scene(instances, 0.2)
    
    return scene


if __name__ == '__main__':
    FILE_NAME =  "output.png"
    FILE_PATH =  "../Images"
    WIDTH, HEIGHT = 256, 128
    #WIDTH, HEIGHT = 640, 360
    
    film = Film(WIDTH,HEIGHT)
    
    
    camera_position = glm.vec3(0,3,0)
    camera_target = glm.vec3(0,3,10)
    
    camera = Camera(60, 10, WIDTH/HEIGHT, camera_position, camera_target, glm.vec3(0,1,0))
    
    scene = CreateScene()
    
    render(film, camera, scene)

    film.image.show()   
    
    # Save Image
    film.save_image(FILE_PATH,FILE_NAME)