from RayTracing.ray import Ray,Hit
from RayTracing.instance import Instance
import sys
import glm

class Scene:
    def __init__(self, instances : list[Instance]) -> None:
        self.instances = instances
        
    def compute_intersection(self, ray) -> tuple[Instance, Hit]:
       
        hit_instance = None
        hit = None
        
        nearest_hit_distance = sys.float_info.max
        
        for instance in self.instances:
           new_hit = instance.intersect(ray)
           
           if new_hit is not None:
                              
               if new_hit.distance < nearest_hit_distance:
                    hit_instance = instance
                    hit = new_hit

        
        return (hit_instance,hit)
    
    def trace_ray(self,ray):
        
        (hit_instance, hit) = self.compute_intersection(ray)
        
        if hit_instance is not None:
            color_intensity = max(0.2, glm.dot(hit.normal,glm.vec3(0,1,0)) )        
            return (color_intensity,color_intensity,color_intensity)
        else:
            return self.get_background_color(ray)
        
        
    def get_background_color(self, ray : Ray) -> tuple[float,float,float]:
        r = ray.direction.x
        g = ray.direction.y
        b = ray.direction.z        
        
        return (r,g,b)
    
    
    
           
           
           
           
        