import glm
import math

from RayTracing.ray import Ray,Hit

class Shape:
    def __init__(self) -> None:
        pass
        
    def intersect(self, ray : Ray , shape_position : glm.vec3) -> Hit:
        return None
    
    
        
class Sphere(Shape):
    def __init__(self, radius) -> None:
       super().__init__()
       self.radius = radius
       
    def intersect(self, ray : Ray ,  shape_position : glm.vec3) -> Hit:
        a : float = glm.dot(ray.direction, ray.direction)
        b : float = 2 * glm.dot(ray.direction , (ray.origin - shape_position))
        c : float = glm.dot(ray.origin - shape_position , ray.origin - shape_position) - math.pow(self.radius,2)
        
        delta : float = math.pow(b,2) - 4*a*c
        
        
        if (delta < 0):
            return None # no hit
        
        else:  
            t1 = ( -b + math.sqrt(delta) ) / ( 2 * a )
            t2 = ( -b - math.sqrt(delta) ) / ( 2 * a )
            
            if (t1 < 0 and t2 < 0):
                return None # no hit
            
            else:
                if ((t1 >= 0 and t2 < 0) or (t1 < 0 and t2 >= 0)):
                    distance = max(t1,t2)
                    is_backface = True
                else:
                    distance = min(t1,t2)
                    is_backface = False
                    
                hit_pos = ray.origin + ray.direction*distance 
                normal = hit_pos - shape_position
                return Hit( distance, hit_pos, normal, is_backface )
  
            
class Point(Shape):
    def __init__(self) -> None:
        super().__init__()
        
    def intersect(self, ray: Ray, shape_position: glm.vec3) -> Hit:
        
        min_dot = 0.95
        
        dot = glm.dot(glm.normalize(ray.direction),glm.normalize(shape_position - ray.origin))
        
        if dot < 0:
            return None # no hit
        else:
            if dot >= min_dot:
                distance = (shape_position - ray.origin)[0] / ray.direction[0]
                return Hit( distance, shape_position, glm.vec3(1),False)
        
        