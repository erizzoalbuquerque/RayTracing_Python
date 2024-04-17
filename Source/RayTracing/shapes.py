import glm
import math
import sys

from RayTracing.ray import Ray,Hit

MIN_DISTANCE_TOLERENCE = 10e-5

class Shape:
    def __init__(self) -> None:
        pass
        
    def intersect(self, ray : Ray ) -> Hit:
        return None
        
        
class Sphere(Shape):
    def __init__(self, radius) -> None:
       super().__init__()
       self.radius = radius
       
    def intersect(self, ray : Ray) -> Hit:
        a : float = glm.dot(ray.direction, ray.direction)
        b : float = 2 * glm.dot(ray.direction , (ray.origin))
        c : float = glm.dot(ray.origin , ray.origin) - math.pow(self.radius,2)
        
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
                    
                if glm.abs(distance) < MIN_DISTANCE_TOLERENCE:
                    return None
                    
                hit_pos = ray.origin + ray.direction*distance 
                normal = glm.normalize(hit_pos)
                
                return Hit( distance, hit_pos, normal, is_backface )
            
            
class Plane(Shape):
    
    def __init__(self, normal : glm.vec3) -> None:
        self.normal = glm.normalize( normal )
        
    def intersect(self, ray : Ray) -> Hit:
        
        denom = glm.dot(self.normal,ray.direction)
        
        if glm.abs(denom) > sys.float_info.epsilon:
            t = glm.dot(- ray.origin, self.normal) / denom
            if t >= 0:
                hit_pos = ray.origin + ray.direction * t
                
                if (denom> 0):
                    is_backface = True
                else:
                    is_backface = False
                    
                if (t < MIN_DISTANCE_TOLERENCE):
                    return None
                
                #print(f"Hit at {hit_pos} with normal {self.normal} and is_backface {is_backface}")
                return Hit(t, hit_pos, self.normal, is_backface)
            else:
                return None
        else:
            return None
  
            
class Point(Shape):
    def __init__(self) -> None:
        super().__init__()
        
    def intersect(self, ray: Ray) -> Hit:
        
        min_dot = 0.95
        
        dot = glm.dot(glm.normalize(ray.direction),glm.normalize(- ray.origin))
        
        if dot < 0:
            return None # no hit
        else:
            if dot >= min_dot:
                distance = (- ray.origin)[0] / ray.direction[0]
                return Hit( distance, 0, glm.normalize(glm.vec3(1)),False)
            

class Box(Shape):
        def __init__(self, size : glm.vec3) -> None:
            super().__init__()            
            
            self.bound_min = -size / 2
            self.bound_max = size / 2
            
        def intersect(self, ray : Ray) -> Hit:
            
            for i in range(3):
                if ray.direction[i] == 0:
                    ray.direction[i] = 10e-5
                        
            t0 = (self.bound_min - ray.origin) / ray.direction
            t1 = (self.bound_max - ray.origin) / ray.direction
            
            tnear = glm.min(t0,t1)
            tfar = glm.max(t0,t1)
            
            tmin = glm.max(tnear)
            tmax = glm.min(tfar)
            
            if tmin > tmax:
                return None
            
            if tmax < 0:
                return None
            
            if tmin < 0:
                is_backface = True
                distance = tmax
                index = tfar.to_list().index(tmax)               
            else:
                is_backface = False
                distance = tmin
                index = tnear.to_list().index(tmin)
               
            if distance < MIN_DISTANCE_TOLERENCE:
                return None
            
            hit_pos = ray.origin + ray.direction * distance
            
            # calculate normal
            center_point = (self.bound_min + self.bound_max) / 2            
            delta = hit_pos - center_point
            aux = glm.vec3(0)
            aux[index] = 1
            
            normal = glm.normalize(glm.dot(aux,delta) * aux)
            
            return Hit(distance, hit_pos, normal, is_backface)
                  
            

            
        
        
        