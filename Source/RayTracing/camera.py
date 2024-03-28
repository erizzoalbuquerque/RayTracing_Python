import math
import glm
from RayTracing.ray import Ray

class Camera:
    def __init__(self, fov_deg, focus_distance, ratio, eye_position: glm.vec3, center_position : glm.vec3, up_direction : glm.vec3):
        self.fov = fov_deg
        self.focus_distance = focus_distance
        self.ratio = ratio
        self.eye_position = eye_position
        self.center_position = center_position
        self.up_direction = up_direction
        
        self.view_matrix = glm.lookAt(self.eye_position, self.center_position, self.up_direction) # from world to camera space
        self.view_matrix_inv =  glm.inverse(self.view_matrix) # from camera space to world space
        
        
    def generate_ray(self, x, y):
        delta_v = self.focus_distance * math.tan(self.fov * math.pi /180 /2)
        delta_u = delta_v * self.ratio
        p = glm.vec4(-delta_u + 2 * delta_u * x, -delta_v + 2* delta_v * y, -self.focus_distance, 1)
        
        o = glm.vec3(self.view_matrix_inv * glm.vec4(0,0,0,1))
        t = glm.vec3(self.view_matrix_inv * p)
        
        return Ray(o,glm.normalize(t-o))