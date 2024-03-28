from RayTracing.ray import Ray,Hit
from RayTracing.instance import Instance
import sys

class Scene:
    def __init__(self, instances : list[Instance]) -> None:
        self.instances = instances
        
    def compute_intersection(self, ray) -> Hit:
       
        hit = Hit()
        
        nearest_hit_distance = sys.float_info.max
        
        for instance in self.instances:
           new_hit = instance.intersect(ray)
           if new_hit.instance is not None:
               if new_hit.distance < nearest_hit_distance:
                   hit = new_hit
        
        return hit
    
    def trace_ray(self,ray):
        
        hit = self.compute_intersection(ray)
        
        if hit.instance is not None:
            return (1,1,1)
        else:
            return self.get_background_color(ray)
        
        
    def get_background_color(self, ray : Ray) -> tuple[float,float,float]:
        r = ray.direction.x
        g = ray.direction.y
        b = ray.direction.z        
        
        return (r,g,b)
    
    
    
           
           
           
           
        