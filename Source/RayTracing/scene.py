import sys
import glm

from RayTracing.ray import Ray,Hit
from RayTracing.instance import Instance, ObjectInstance, LightInstance
from RayTracing.color import Color

class Scene:
    def __init__(self, instances : list[Instance], ambient_light_intensity : float = 0.0) -> None:
        self.instances = instances
        self.light_instances = []
        self.object_instances = []
        self.lights = []
        
        for instance in self.instances:
            if type(instance) == LightInstance:
                self.light_instances.append(instance)
                self.lights.append(instance.light)
            elif type(instance) == ObjectInstance:    
                self.object_instances.append(instance)
                
        self.ambient_light_intensity = ambient_light_intensity     
                     
        
    def compute_intersection(self, ray) -> tuple[Instance, Hit]:
       
        hit_instance = None
        hit = None
        
        nearest_hit_distance = sys.float_info.max
        
        for instance in self.instances:
           new_hit = instance.intersect(ray)
           
           if new_hit is not None:
                              
               if new_hit.distance < nearest_hit_distance:
                    nearest_hit_distance = new_hit.distance
                    hit_instance = instance
                    hit = new_hit
        
        return (hit_instance,hit)
    
    
    def trace_ray(self,ray) -> Color:
        
        color = Color(0,0,0)
        
        (hit_instance, hit) = self.compute_intersection(ray)
                        
        if hit_instance is not None: 
            
            if type(hit_instance) is LightInstance:
                
                light_instance : LightInstance = hit_instance                
                r = hit.distance
                intensity = light_instance.light.power / r**2 + self.ambient_light_intensity
                color = Color(intensity, intensity, intensity)
            
            elif type(hit_instance) == ObjectInstance:
                
                object_instance : ObjectInstance = hit_instance 
                
                # get all visible lights from the hit point
                visible_lights = []
                for light_instance in self.light_instances:
                    light_ray = Ray(hit.position, glm.normalize(light_instance.position - hit.position))
                    (light_hit_instance, light_hit) = self.compute_intersection(light_ray)
                    
                    if light_hit_instance == light_instance:
                        visible_lights.append(light_instance.light)                
                               
                color = object_instance.material.eval(visible_lights, hit, ray.origin , self.ambient_light_intensity)      
        
        else: # Hit nothing
            color = self.get_background_color(ray)
        
        return color

       
    def get_background_color(self, ray : Ray) -> Color:
        r = ray.direction.x
        g = ray.direction.y
        b = ray.direction.z        
        
        return Color(r,g,b)
    
    
    
           
           
           
           
        