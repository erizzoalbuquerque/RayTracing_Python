import glm

class Light:
        
    def __init__(self, power : float) -> None:
        self.power = power
        


class pointLight(Light):
    
    def __init__(self, power : float) -> None:
        super().__init__(power)