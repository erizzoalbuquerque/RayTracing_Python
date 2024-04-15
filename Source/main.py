from RayTracing.color import Color
from RayTracing.light import Light, PointLight, AreaLight
from RayTracing.material import Material, PhongMaterial
from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.instance import Instance, LightInstance, ObjectInstance
from RayTracing.transform import Transform
from RayTracing.shapes import Shape,Sphere,Point,Plane
from RayTracing.render import render

import glm

def CreateScene():
    
    instances = []
    
    # LIGHTS
    instances.append( LightInstance( Transform(glm.vec3(0,4,10)), Sphere(1), AreaLight(30, glm.vec3(.8,0,0),glm.vec3(0,0,.4),5, "STRATIFIED") ) )
    #instances.append( LightInstance( Transform(glm.vec3(0,4,10)), Sphere(0.2), PointLight(10) ) )
    #instances.append( LightInstance( Transform(glm.vec3(3,4,9)), Sphere(0.1), PointLight(7) ) )
    #instances.append( LightInstance( Transform(glm.vec3(-1,3,7)), Sphere(0.1), PointLight(20) ) )
        
    # OBJECTS
    instances.append( ObjectInstance( Transform(glm.vec3(0,0,10)), Plane( glm.vec3(0,1,0) ), PhongMaterial( Color(1,1,1), Color(0,1,0), Color(0,0,0), 10 ) ) )
    instances.append( ObjectInstance( Transform(glm.vec3(1,0.5,9)), Sphere(0.5), PhongMaterial( Color(1,1,1), Color(0,0,1), Color(1,1,1), 10 ) ) )
    instances.append( ObjectInstance( Transform(glm.vec3(0,0,10), glm.vec3(0,0,45), glm.vec3(1,3,1)), Sphere(1), PhongMaterial( Color(1,1,1), Color(1,0,0), Color(1,1,1), 10 ) ) )

    scene = Scene(instances, 0.2)
    
    return scene


if __name__ == '__main__':
    FILE_NAME =  "output.png"
    FILE_PATH =  "../Images"
    FILM_SAMPLE_COUNT = 4
    #WIDTH, HEIGHT = 128, 128
    WIDTH, HEIGHT = 360, 360
    
    film = Film(WIDTH,HEIGHT,FILM_SAMPLE_COUNT)
    
    
    camera_position = glm.vec3(0,3,0)
    camera_target = glm.vec3(0,1.5,10)
    
    camera = Camera(40, 10, WIDTH/HEIGHT, camera_position, camera_target, glm.vec3(0,1,0))
    
    scene = CreateScene()
    
    render(film, camera, scene)

    film.image.show()   
    
    # Save Image
    film.save_image(FILE_PATH,FILE_NAME)