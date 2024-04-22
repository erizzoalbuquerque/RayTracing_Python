import glm

from .ray import Ray, Hit

class Transform:
    
    def __init__(self, position : glm.vec3 = glm.vec3(0), rotation : glm.vec3 = glm.vec3(0), scale : glm.vec3 = glm.vec3(1)) -> None:
        
        S = glm.scale(scale)
        R = glm.rotate(glm.radians(rotation.y),glm.vec3(0,1,0)) * glm.rotate(glm.radians(rotation.x),glm.vec3(1,0,0)) * glm.rotate(glm.radians(rotation.z),glm.vec3(0,0,1))
        T = glm.translate(position)
        
        self.M = T * R * S * glm.mat4(1.0)
        self.M_inv = glm.inverse(self.M)
        
        
    def transform_point(self, point : glm.vec3) -> glm.vec3:
        return glm.vec3(self.M * glm.vec4(point, 1.0))
    
    
    def transform_direction(self, direction : glm.vec3) -> glm.vec3:
        return glm.vec3(self.M * glm.vec4(direction, 0.0))
    
    
    def inverse_transform_point(self, point : glm.vec3) -> glm.vec3:
        return glm.vec3(self.M_inv * glm.vec4(point, 1.0))
    
    
    def inverse_transform_direction(self, direction : glm.vec3) -> glm.vec3:
        return glm.vec3(self.M_inv * glm.vec4(direction, 0.0))
        
    
    def inverse_transform_ray(self, ray : Ray) -> Ray:        
        local_origin = self.inverse_transform_point(ray.origin)
        # new_ray.direction = glm.vec3(self.M_inv * glm.vec4(ray.direction, 0.0))
        local_direction = glm.vec3( glm.normalize(self.M_inv * (glm.vec4(ray.origin + ray.direction, 1.0) - glm.vec4(ray.origin, 1.0))) )
        
        return Ray(local_origin, local_direction)
    
    def transform_hit(self, hit : Hit, transformed_ray_origin : glm.vec3) -> Hit:        
        hit_global = Hit()
        
        hit_global.distance = glm.length(self.transform_point(hit.position) - transformed_ray_origin)
        hit_global.position = self.transform_point(hit.position)
        hit_global.normal = glm.vec3( glm.transpose(self.M_inv) * glm.vec4(hit.normal, 0.0))
        hit_global.is_backface = hit.is_backface
        
        return hit_global
    
    def get_position(self) -> glm.vec3:
        # return glm.vec3(self.transform_point(glm.vec3(0))
        return glm.vec3(self.M[3])
    
    
        
        

    
    