import glm
from .material import Material
from .shapes import Shape
from .ray import Ray, Hit
from .light import Light
from .transform import Transform

class Instance:
    
    def __init__(self, transform : Transform, shape : Shape) -> None:
        self.transform = transform
        self.shape = shape
        
    def intersect(self, ray : Ray) -> Hit:
        
        # Convert to local space
        local_ray = self.transform.inverse_transform_ray(ray)
        
        local_hit = self.shape.intersect(local_ray)
        
        if local_hit is not None:
            # Convert back to global space
            hit = self.transform.transform_hit(local_hit, ray.origin)            
            return hit
        
        else:
            return None
          

class ObjectInstance(Instance):
    
    def __init__(self, transform : Transform, shape : Shape, material : Material) -> None:
        super().__init__(transform, shape)
        self.material = material        

            
class LightInstance(Instance):
    
    def __init__(self, transform : Transform, shape : Shape, light : Light) -> None:
        super().__init__(transform, shape)
        self.light = light
        light.position = self.transform.get_position()