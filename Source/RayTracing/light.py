import glm

class Light:
        
    def __init__(self, power : float) -> None:
        self.power = power
        self.position = glm.vec3(0,0,0)
        
    def get_radiance(self, target_position : glm.vec3 ) -> tuple[float,glm.vec3]:
        pass        

class PointLight(Light):
    
    def __init__(self, power : float) -> None:
        super().__init__(power)
      
    def get_radiance(self, scene, target_position : glm.vec3  ) -> tuple[float,glm.vec3]:
        
        from RayTracing.ray import Ray
        from RayTracing.instance import LightInstance
        
        light_direction = glm.normalize(self.position - target_position)
        
        ray = Ray(target_position, light_direction)
        hit_instance,hit = scene.compute_intersection(ray)
        
        if hit_instance is  None:
            return 0.0, light_direction
        
        if type(hit_instance) != LightInstance:
            return 0.0, light_direction
        
        if hit_instance.light != self:
            return 0.0, light_direction
        
        radius = glm.length(self.position - target_position)
        radiance = self.power / radius**2

        return radiance, light_direction