import glm
import math
import random

from RayTracing.color import Color
from RayTracing.ray import Hit
from RayTracing.light import Light

class Material:
    
    def __init__(self):
        pass
    
    def eval(self, scene, hit: Hit, ray_origin: glm.vec3, ambient_light_intensity : float) -> Color:
        pass
    
    def get_sample(self) -> tuple[glm.vec3, float]:
        
        eps_1 = random.random()
        eps_2 = random.random()
        
        w_i_h = glm.vec3(
            math.sqrt(eps_1) * math.cos(2 * math.pi * eps_2),
            math.sqrt(eps_1) * math.sin(2 * math.pi * eps_2),
            math.sqrt(1 - eps_1)
        )
        
        pdf = math.sqrt( 1 - eps_1 ) / math.pi
        
        return w_i_h, pdf
    
    def brdf(self):
        return Color(1,0,1) # Not implemented pink color

class PhongMaterial(Material):
    
    def __init__(self, diffuse : Color, specular : Color, shininess : float) -> None:
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        
        self.ambient = self.diffuse
        
    def eval(self, scene, hit: Hit, ray_origin: glm.vec3, ambient_light_intensity : float) -> Color:
        
        color = self.ambient * scene.ambient_light_intensity
        
        v = glm.normalize(ray_origin - hit.position)
        
        for light in scene.lights:
            (radiance, light_direction) = light.get_radiance(scene, hit.position)
            color += self.diffuse * max(0.0, glm.dot(hit.normal, light_direction)) * radiance
            reflection_direction = glm.reflect(-light_direction, hit.normal)
            color += self.specular * max(0.0, (glm.dot(v, reflection_direction))) ** self.shininess * radiance
                        
        return color
    
class DebugMaterial(Material):
    
    def __init__(self) -> None:
        pass
    
    def eval(self, scene, hit: Hit, ray_origin: glm.vec3, ambient_light_intensity : float) -> Color:
        
        color = Color(abs(hit.normal.x), abs(hit.normal.y), abs(hit.normal.z))
        
        return color
    

class PTDiffuseMaterial(Material):
    
    def __init__(self, albedo : Color) -> None:
        self.albedo = albedo
        
    def eval(self, scene, hit: Hit, ray_origin: glm.vec3, ambient_light_intensity : float) -> Color:

        color = Color(0,0,0)
        
        for light in scene.lights:
            (radiance, light_direction) = light.get_radiance(scene, hit.position)
            color += self.albedo * max(0.0, glm.dot(hit.normal, light_direction)) * radiance
        
        return color
    
    def brdf(self):
        return self.albedo / math.pi