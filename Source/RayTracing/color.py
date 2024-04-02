class Color:
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)  
    
    def __mul__(self, other):
        return Color(self.r * other, self.g * other, self.b * other)
    
    def __truediv__(self, other):
        return Color(self.r / other, self.g / other, self.b / other)
    
    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b})"
    
    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"
    
    def to_tuple(self):
        return (self.r, self.g, self.b)