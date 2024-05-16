import sys
import glm

from RayTracing.ray import Ray,Hit
from RayTracing.instance import Instance, ObjectInstance, LightInstance
from RayTracing.color import Color
import random

class Scene:
    def __init__(self, instances : list[Instance], ambient_light_intensity : float = 0.0) -> None:
        self.instances = instances
        self.light_instances = []
        self.object_instances = []
        self.lights = []
        
        for instance in self.instances:
            if type(instance) == LightInstance:
                self.light_instances.append(instance)
                self.lights.append(instance.light)
            elif type(instance) == ObjectInstance:    
                self.object_instances.append(instance)
                
        self.ambient_light_intensity = ambient_light_intensity     
                     
        
    def compute_intersection(self, ray) -> tuple[Instance, Hit]:
       
        hit_instance = None
        hit = None
        
        nearest_hit_distance = sys.float_info.max
        
        for instance in self.instances:
           new_hit = instance.intersect(ray)
           
           if new_hit is not None:
                              
               if new_hit.distance < nearest_hit_distance:
                    nearest_hit_distance = new_hit.distance
                    hit_instance = instance
                    hit = new_hit
        
        return (hit_instance,hit)
    
    
    def trace_ray(self,ray) -> Color:
        
        color = Color(0,0,0)
        
        (hit_instance, hit) = self.compute_intersection(ray)
                        
        if hit_instance is not None: 
            
            if type(hit_instance) is LightInstance:
                
                light_instance : LightInstance = hit_instance                
                r = hit.distance
                intensity = light_instance.light.power / r**2 + self.ambient_light_intensity
                color = Color(intensity, intensity, intensity)
            
            elif type(hit_instance) == ObjectInstance:
                
                object_instance : ObjectInstance = hit_instance 
                
                color = object_instance.material.eval(self, hit, ray.origin , self.ambient_light_intensity)      
        
        else: # Hit nothing
            color = self.get_background_color(ray)
        
        return color
    
           
    def get_background_color(self, ray : Ray) -> Color:      
        
        r,g,b, = 0,0,0
        
        return Color(r,g,b)
    
    
    
    def trace_path(self, ray, max_depth : int) -> Color:
        
        # Init variables
        L = Color(0,0,0)
        beta = Color(1,1,1)
        
        current_ray = Ray(ray.origin, ray.direction)
        
        # loop over different depths of the path
        for i in range(1 , max_depth + 1):
            
            (hit_instance, hit) = self.compute_intersection(current_ray)
            
            # If there is no hit, break the loop. We do nothing. Color is what we got so far...
            if (hit_instance is None):
                break
            
            if type(hit_instance) is LightInstance:
                
                light = hit_instance.light
                
                # If we hit a light, we return the power of the light
                if (i == 1):
                    return light.power * Color(1,1,1)
                # If we hit a light after the first hit, we stop. Because we already estimated the power of the light in the previous iteration 
                else:
                    break
                
            elif type(hit_instance) == ObjectInstance:
                
                # Calculate direct light contribution
                material = hit_instance.material
                
                p = hit.position
                n = hit.normal
                
                Le = self.get_light_radiance(p,n)
                L += (Le * material.brdf()) * beta
                
                w_i_h, pdf = material.get_sample()
                
                w_i = self.hemisphere_to_global(p, n, w_i_h)
                
                # update variables for next iteration
                beta *= ( material.brdf() * max(0,glm.dot(n,w_i)) ) / pdf                
                current_ray = Ray(p, w_i)
                
        return L
    
    def get_light_radiance(self, p, n):
        
        light_instance, lpdf = self.sample_light()
        
        s, n_s, pdf = light_instance.light.get_sample(p)
        
        w_i = glm.normalize(s - p)
        ray = Ray(p, w_i)
        
        (hit_instance, hit) = self.compute_intersection(ray)
        
        if (hit_instance is None):
            return Color(0,0,0)
        
        if (hit_instance != light_instance):
            return Color(0,0,0)
        
        d = glm.length(s - p)
        
        irradiance = light_instance.light.get_irradiance()
        
        return ( irradiance * max( 0, glm.dot(n, w_i) ) * max( 0, glm.dot(n_s,-w_i) ) ) / ( d**2 * lpdf * pdf )
    
    
    def sample_light(self) -> tuple[LightInstance, float]:
        '''Sample a light randomly based on its power'''
        
        total_power = sum(light.power for light in self.lights)
        random_value = random.uniform(0, total_power)
        
        cumulative_power = 0
        for light_instance in self.light_instances:
            cumulative_power += light_instance.light.power
            if random_value <= cumulative_power:
                return light_instance, light_instance.light.power / total_power
        
        return None, 0
    
    def hemisphere_to_global(self, p : glm.vec3, n : glm.vec3, w_i_h : glm.vec3):
        
        t = glm.vec3(1,0,0)
        
        if glm.abs(glm.dot(t,n)) > 0.9:
            t = glm.vec3(0,1,0)
            
        b = glm.normalize(glm.cross(n,t))
        t = glm.cross(b,n)
        M = glm.mat3(t,b,n)
        
        return glm.normalize(M * w_i_h - p) 