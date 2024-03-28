import glm
from RayTracing.shapes import Shape
from RayTracing.ray import Ray, Hit

class Instance:
    
    def __init__(self, position : glm.vec3, shape : Shape) -> None:
        self.position = position
        self.shape = shape
        
    def intersect(self, ray : Ray) -> Hit:
        return self.shape.intersect(ray, self.position)