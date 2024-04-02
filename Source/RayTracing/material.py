from RayTracing.color import Color

class Material:
    
    def _init_():
        pass

class PhongMaterial(Material):
    
    def __init__(self, ambient : Color, diffuse : Color, specular : Color, shininess : float) -> None:
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess