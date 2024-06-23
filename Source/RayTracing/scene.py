import math
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
                
        self.ambient_light_power = ambient_light_intensity     
                     
        
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
                intensity = light_instance.light.power / r**2 + self.ambient_light_power
                color = Color(intensity, intensity, intensity)
            
            elif type(hit_instance) == ObjectInstance:
                
                object_instance : ObjectInstance = hit_instance 
                
                color = object_instance.material.eval(self, hit, ray.origin , self.ambient_light_power)      
        
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
                if (i == 1):
                    return self.ambient_light_power * Color(1,1,1)
                else:
                    break
            
            if type(hit_instance) is LightInstance:
                
                light = hit_instance.light
                
                # If we hit a light, we return the power of the light
                if (i == 1):
                    return light.power * Color(1,1,1)
                # If we hit a light after the first hit, we stop, because we already estimated direct light in the previous iteration 
                else:
                    break
                
            elif type(hit_instance) == ObjectInstance:
                
                material = hit_instance.material
                
                # MIS - Sample Direct Light Contribution               
                
                p = hit.position
                n = hit.normal
                
                Le, w_i_l, geometric_factor, l_pdf = self.get_light_radiance(p,n)
                
                m_pdf = material.get_sample_pdf(n, -current_ray.direction)
                #mis_weight = self.get_mis_weight(l_pdf, m_pdf * geometric_factor)
                mis_weight = 1
                
                brdf =  material.brdf(n, w_i_l, -current_ray.direction)
                
                L += beta * Le * brdf * mis_weight / l_pdf
                
                w_i, pdf = material.get_sample(n, -current_ray.direction)
                
                # update variables for next iteration
                beta *= ( material.brdf(n, w_i_l, -current_ray.direction) * max(0,glm.dot(n,w_i)) ) / pdf                
                current_ray = Ray(p, w_i)
                
        return L
    
    def get_light_radiance(self, p : glm.vec3, n : glm.vec3) -> tuple[float, glm.vec3, float, float]:
        
        light_instance, lpdf = self.sample_light()
        
        if (light_instance is not None):        
            s, n_s, pdf = light_instance.light.get_sample(p)
            w_i = glm.normalize(s - p)
        else:
            w_i, n_s, pdf = self.sample_ambient_light()
                
        ray = Ray(p, w_i)
        
        (hit_instance, hit) = self.compute_intersection(ray)
        
        # Ambient light ----------------------
        if (light_instance is None): 
            if (hit_instance is None):
                return self.ambient_light_power * max( 0, glm.dot(n, w_i) ), w_i , 0, lpdf * pdf
            else:
                return 0 , w_i, 0, lpdf * pdf
        
        # Regular light ----------------------
        
        geometric_factor = self.get_geometric_factor(p, s, n_s)
        
        if (hit_instance != light_instance):
            return 0 , w_i, geometric_factor, lpdf * pdf
        
        irradiance = light_instance.light.get_irradiance()
        
        return ( irradiance * max( 0, glm.dot(n, w_i) ) * geometric_factor ), w_i, geometric_factor, lpdf * pdf
    
    
    def sample_light(self) -> tuple[LightInstance, float]:
        '''Sample a light randomly based on its power'''
        
        #random_value = random.randint(0, len(self.lights))
        #
        #if random_value == len(self.lights):
        #    return None, 1/(len(self.lights)+1)
        #else:
        #    return self.light_instances[random_value], 1/(len(self.lights)+1)            
                
        total_power = sum(light.power for light in self.lights) + self.ambient_light_power
        if (total_power == 0):
            return None, 0
        
        random_value = random.uniform(0, total_power)
        
        cumulative_power = 0
        for light_instance in self.light_instances:
            cumulative_power += light_instance.light.power
            if random_value <= cumulative_power:
                return light_instance, light_instance.light.power / total_power
        
        return None, self.ambient_light_power / total_power
    
    
    def sample_ambient_light(self):
        eps_1 = random.random()
        eps_2 = random.random()
        
        z = 1 - 2 * eps_1
        x = math.sqrt(1 - z**2) * math.cos(2 * math.pi * eps_2)
        y = math.sqrt(1 - z**2) * math.sin(2 * math.pi * eps_2)

        
        return glm.vec3(x,y,z), glm.normalize(-glm.vec3(x,y,z)), 1/(4*math.pi) 
    
    
    def get_geometric_factor(self, p : glm.vec3, s : glm.vec3, n_s : glm.vec3) -> float:
        d = glm.length(s - p)
        w_i = glm.normalize(s - p)
        return max( 0, glm.dot(n_s, -w_i) ) / d**2
    
    def get_mis_weight(self, main_pdf : float, other_pdf : float) -> float:
        # using balance heuristic
        return main_pdf / (main_pdf + other_pdf)
    