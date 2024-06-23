class Color:
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def __add__(self, other):
        if isinstance(other, Color):
            return Color(self.r + other.r, self.g + other.g, self.b + other.b) 
        else:
            raise TypeError(f"{type(other)} is unsupported operand type for sum") 
    
    def __mul__(self, other):
        if isinstance(other, Color):
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)
        elif isinstance(other, int) or isinstance(other, float):
            return Color(self.r * other, self.g * other, self.b * other)
        else:
            raise TypeError(f"{type(other)} is unsupported operand type for multiplication")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def to_tuple(self):
        return (self.r, self.g, self.b)
    
    def __truediv__(self, other):
        if isinstance(other, Color):
            return Color(self.r / other.r, self.g / other.g, self.b / other.b)
        elif isinstance(other, int) or isinstance(other, float):
            return Color(self.r / other, self.g / other, self.b / other)
        else:
            raise TypeError(f"{type(other)} is unsupported operand type for division")
        
    def __str__(self) -> str:
        return f"Color({self.r},{self.g},{self.b})"
    
