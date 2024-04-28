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
    
class AreaLight(Light):
        
        def __init__(self, power : float, e_i : glm.vec3, e_j : glm.vec3, n_samples_root_squared : int , sampling_type : str) -> None:
            super().__init__(power)
            self.e_i = e_i
            self.e_j = e_j
            self.n_samples_root_squared = n_samples_root_squared
            self.n_samples = n_samples_root_squared**2
            self.sampling_type = sampling_type
            
            self.normal = glm.normalize(glm.cross(e_i, e_j))
            self.area = glm.length(glm.cross(e_i, e_j))
            
            print("Area Light using ", self.sampling_type, " sampling with ", self.n_samples, " samples")
            
        
        def get_sample(self) -> list[glm.vec3]:
            import RayTracing.sampling_utils as su
            
            if (self.sampling_type == "REGULAR"):
                offsets_i = su.get_regular_sampling(self.n_samples_root_squared)
                offsets_j = su.get_regular_sampling(self.n_samples_root_squared)
            elif (self.sampling_type == "UNIFORM"):
                offsets_i = su.get_uniform_sampling(self.n_samples_root_squared)
                offsets_j = su.get_uniform_sampling(self.n_samples_root_squared)
            elif (self.sampling_type == "STRATIFIED"):
                offsets_i = su.get_stratified_sampling(self.n_samples_root_squared)
                offsets_j = su.get_stratified_sampling(self.n_samples_root_squared)
            else:
                print("Error: Sampling type not recognized")
            
            offsets = []
            for offset_i in offsets_i:
                for offset_j in offsets_j:
                    #offsets.append(self.position + x * self.e_i + y * self.e_j)
                    offsets.append(self.position + offset_i * self.e_i + offset_j * self.e_j - (0.5 * self.e_i + 0.5 * self.e_j) )
                    
            #print("Offsets: ", offsets)
                    
            return offsets    
                            
            
        def get_radiance(self, scene, target_position : glm.vec3) -> tuple[float,glm.vec3]:
            
            radiance_vector = glm.vec3(0,0,0)
            
            samples = self.get_sample()
            
            for sample in samples:
                radiance, light_vector = self.sample_radiance(scene, target_position , sample)
                radiance_vector += radiance * light_vector
    
            return glm.length(radiance_vector), glm.normalize(radiance_vector)
        
        
        def sample_radiance(self, scene, target_position : glm.vec3, sample_position : glm.vec3) -> tuple[float,glm.vec3]:
            
            from RayTracing.ray import Ray
            from RayTracing.instance import LightInstance
            
            sample_normal = self.normal
            
            delta = sample_position - target_position 
            
            light_direction = glm.normalize(delta)            
            
            ray = Ray(target_position, light_direction)
            hit_instance,hit = scene.compute_intersection(ray)
            
            if hit_instance is  None:
                return 0.0, light_direction
            
            if type(hit_instance) != LightInstance:
                return 0.0, light_direction
            
            if hit_instance.light != self:
                return 0.0, light_direction
            
            radius = glm.length(delta)
            radiance = (self.power / self.area * max(0, glm.dot(-light_direction,sample_normal)) / radius**2) * (self.area / self.n_samples) 
    
            return radiance, light_direction