from RayTracing.color import Color
from RayTracing.light import Light, PointLight, AreaLight
from RayTracing.material import Material, PhongMaterial, DebugMaterial
from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.instance import Instance, LightInstance, ObjectInstance
from RayTracing.transform import Transform
from RayTracing.shapes import Shape,Sphere,Point,Plane, Box
from RayTracing.render import render

import glm

def CreateScene(instances : list[Instance] = []):
    
    ambient_light_intensity = 0.2
    scene = Scene(instances, ambient_light_intensity)
    
    return scene

def CreateObjects():
                
    # OBJECTS -----------------------------------------------------
    # Planes
    red_plane = ObjectInstance( Transform(glm.vec3(2,0,0)), Plane( glm.vec3(-1,0,0) ), PhongMaterial( Color(1,0,0), Color(0,0,0), 10 ) )
    green_plane = ObjectInstance( Transform(glm.vec3(-2,0,0)), Plane( glm.vec3(1,0,0) ), PhongMaterial( Color(0,1,0), Color(0,0,0), 10 ) )
    white_plane = ObjectInstance( Transform(glm.vec3(0,0,2)), Plane( glm.vec3(0,0,-1) ), PhongMaterial( Color(1,1,1), Color(0,0,0), 10 ) )
    white_ceiling = ObjectInstance( Transform(glm.vec3(0,4,0)), Plane( glm.vec3(0,-1,0) ), PhongMaterial( Color(1,1,1), Color(0,0,0), 10 ) )
    white_floor = ObjectInstance( Transform(glm.vec3(0,0,0)), Plane( glm.vec3(0,1,0) ), PhongMaterial( Color(1,1,1), Color(0,0,0), 10 ) )
    
    #instances = [red_plane, green_plane, white_plane, white_ceiling, white_floor]
    instances = [white_floor]
    
    # unit_sphere
    #instances.append( ObjectInstance( Transform(glm.vec3(0,2,0)), Sphere(0.5), PhongMaterial( Color(1,1,0), Color(1,1,1), 10 ) ) )
    #instances.append( ObjectInstance( Transform(glm.vec3(0,2,0)), Sphere(0.5), DebugMaterial() ) )
    
    # box
    instances.append( ObjectInstance( Transform(glm.vec3(0.7,1.25,1.1), glm.vec3(0,45,0)), Box(glm.vec3(1,2.5,1)), PhongMaterial( Color(1,1,1), Color(1,1,1), 10 ) ) )
    #instances.append( ObjectInstance( Transform(glm.vec3(0.7,1.25,0.7), glm.vec3(30,20,0)), Box(glm.vec3(1,1,1)), DebugMaterial() ) )
    
    # elipsoide
    instances.append( ObjectInstance( Transform(glm.vec3(-0.7,0,-0.7), glm.vec3(0,0,45), glm.vec3(1,2,1)), Sphere(0.5), PhongMaterial( Color(1,1,1), Color(1,1,1), 10 ) ) )
        
    return instances

def CreateLights():
    
    instances = []
    
    # LIGHTS -----------------------------------------------------
    point_light = LightInstance( Transform(glm.vec3(0,4,0)), Sphere(0.1), PointLight(5))
    aux_point_light = LightInstance( Transform(glm.vec3(-1,4,1)), Sphere(0.1), PointLight(3))
    area_light = LightInstance( Transform(glm.vec3(-1,4,0)), Box(glm.vec3(2.1,0.1,1.1)), AreaLight( 15, glm.vec3(2,0,0), glm.vec3(0,0,1), 4, "STRATIFIED" ) )
    mini_area_light = LightInstance( Transform(glm.vec3(0,4,0)), Box(glm.vec3(0.26,0.1,0.25)), AreaLight( 10, glm.vec3(0.5,0,0), glm.vec3(0,0,0.25), 4, "REGULAR" ) )
    
    #instances = [point_light]
    #instances = [point_light,aux_point_light]
    instances = [area_light]
    #instances = [mini_area_light]
    
    return instances    


if __name__ == '__main__':
    FILE_NAME =  "output.png"
    FILE_PATH =  "../Images"
    FILM_SAMPLE_COUNT = 1
    #WIDTH, HEIGHT = 128, 128
    WIDTH, HEIGHT = 360, 360
    
    film = Film(WIDTH,HEIGHT,FILM_SAMPLE_COUNT)
    
    instances = CreateObjects() + CreateLights()
    
    scene = CreateScene(instances)    
    
    camera_position = glm.vec3(0,2,-5)
    camera_target = glm.vec3(0,2,0)    
    camera = Camera(60, 5, WIDTH/HEIGHT, camera_position, camera_target, glm.vec3(0,1,0))
    
    render(film, camera, scene)

    film.image.show()   
    
    # Save Image
    film.save_image(FILE_PATH,FILE_NAME)