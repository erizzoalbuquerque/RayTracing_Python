from PIL import Image

class Film:
    def __init__(self, width : int, height: int):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), "pink")
        
    def get_sample(self, i, j):
        return ( (i + 0.5) / self.width , (j + 0.5) / self.height)
        
    def set_pixel_value(self, x, y, color):
        self.image.putpixel((x, self.height - y - 1), (int(color[0]* 255), int(color[1]* 255), int(color[2]*255)) ) 
        
    def save_image(self, file_path, file_name):
        self.image.save(file_path + "/" + file_name)