from PIL import Image
from random import random

class Film:
    def __init__(self, width : int, height: int, sample_count : int = 1):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), "pink")
        self.sample_count = sample_count
        
    def get_sample(self, i, j):
        if self.sample_count == 1:
            offset = (0.5,0.5)
        else:
            offset = (random(),random())
        
        return ( (i + offset[0]) / self.width , (j + offset[1]) / self.height)
        
    def set_pixel_value(self, x, y, color):
        self.image.putpixel((x, self.height - y - 1), (int(color[0]* 255), int(color[1]* 255), int(color[2]*255)) ) 
        
    def save_image(self, file_path, file_name):
        self.image.save(file_path + "/" + file_name)
        
        