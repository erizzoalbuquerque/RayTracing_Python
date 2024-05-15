import glm
class Ray:
    def __init__(self, origin : glm.vec3, direction : glm.vec3):
        self.origin = origin
        self.direction = glm.normalize(direction)

   
class Hit:
    def __init__(self, distance : float = -1 , position : glm.vec3 = glm.vec3(), normal : glm.vec3 = glm.vec3(1), is_backface : bool = False) -> None:
        self.distance = distance
        self.position = position
        self.normal = glm.normalize(normal)
        self.is_backface = is_backface