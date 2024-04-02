import glm
from RayTracing.material import Material
from RayTracing.shapes import Shape
from RayTracing.ray import Ray, Hit
from RayTracing.light import Light

class Instance:
    
    def __init__(self, position : glm.vec3, shape : Shape) -> None:
        self.position = position
        self.shape = shape
        
    def intersect(self, ray : Ray) -> Hit:
        
        hit = self.shape.intersect(ray, self.position)
        
        if hit is not None:
            return hit
        else:
            return None
  

class ObjectInstance(Instance):
    
    def __init__(self, position : glm.vec3, shape : Shape, material : Material) -> None:
        super().__init__(position, shape)
        self.material = material        

            
class LightInstance(Instance):
    
    def __init__(self, position : glm.vec3, shape : Shape, light : Light) -> None:
        super().__init__(position, shape)
        self.light = light
        light.position = position