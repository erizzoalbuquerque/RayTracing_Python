import glm

class Light:
        
    def __init__(self, power : float) -> None:
        self.power = power
        self.position = glm.vec3(0,0,0)
        
    def get_radiance(self, position: glm ) -> tuple[float,glm.vec3]:
        pass        

class PointLight(Light):
    
    def __init__(self, power : float) -> None:
        super().__init__(power)
      
    def get_radiance(self, target_position: glm ) -> tuple[float,glm.vec3]:
        
        light_direction = glm.normalize(self.position - target_position)
        
        radius = glm.length(self.position - target_position)
        radiance = self.power / radius**2

        return radiance, light_direction