import glm

from RayTracing.color import Color
from RayTracing.ray import Hit
from RayTracing.light import Light

class Material:
    
    def _init_(self):
        pass
    
    def eval(self, lights: list[Light] , hit : Hit , ray_origin : glm.vec3, ambient_light_intensity : float) -> Color:
        pass

class PhongMaterial(Material):
    
    def __init__(self, ambient : Color, diffuse : Color, specular : Color, shininess : float) -> None:
        #self.ambient = ambient
        self.ambient = diffuse
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        
    def eval(self, scene, hit: Hit, ray_origin: glm.vec3, ambient_light_intensity : float) -> Color:
        
        color = self.ambient * scene.ambient_light_intensity
        
        v = glm.normalize(ray_origin - hit.position)
        
        for light in scene.lights:
            (radiance, light_direction) = light.get_radiance(scene, hit.position)
            color += self.diffuse * max(0.0, glm.dot(hit.normal, light_direction)) * radiance
            reflection_direction = glm.reflect(-light_direction, hit.normal)
            color += self.specular * max(0.0, (glm.dot(v, reflection_direction))) ** self.shininess * radiance
                        
        return color