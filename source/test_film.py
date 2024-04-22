from RayTracing.film import Film

if __name__ == '__main__':
    FILE_NAME =  "testing_film.png"
    FILE_PATH =  "../images/Test_Film"
    WIDTH = 256
    HEIGHT = 128 
    
    film = Film(WIDTH,HEIGHT)
    
    # Generate Gradient
    for i in range(film.width):
        for j in range(film.height):
            if i < film.width/2:
                if j < film.height/2:
                    film.set_pixel_value(i, j, (1,0,0)) 
                else:
                    film.set_pixel_value(i, j, (0,1,0)) 
            else:
                if j < film.height/2:
                    film.set_pixel_value(i, j, (0,0,1)) 
                else:
                    film.set_pixel_value(i, j, (1,1,1)) 
    
    film.image.show()   
    
    # Save Image
    film.save_image(FILE_PATH,FILE_NAME)