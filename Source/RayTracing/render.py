from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.color import Color

from timeit import default_timer as timer

def render(film : Film, camera : Camera, scene : Scene):
    print("Starting render...")
    print(f"film resolution is: {film.width} X {film.height}")
    print(f"Scene has {len(scene.instances)} instances.")
    
    film_sample_count = film.sample_count
    print(f"Film sample count is {film_sample_count}.")
    
    total_pixels = film.width * film.height
    pixels_printed = 0
    
    start_time = timer()
    
    for i in range(film.width):
        for j in range(film.height):
            
            color = Color(0,0,0)            
            for k in range(film_sample_count):
                #print(f"Rendering pixel {i}, {j}...")
                (x,y) = film.get_sample(i,j)
                #print(f"Rendering sample {x}, {y}...")
                ray = camera.generate_ray(x,y)
                #print(ray.direction)
                color += scene.trace_ray(ray)
            color /= film_sample_count

            color = (color.r, color.g, color.b)   
            film.set_pixel_value(i,j,color)
            #print(color)
            
            pixels_printed += 1
            progress = pixels_printed / total_pixels * 100
            if progress % 10 == 0:
                print_progress(progress)
            
    end_time = timer()
    
    print(f"Render time: {end_time - start_time} seconds." )
    

def print_progress(progress):
    print(f"Progress: {progress:.2f}%", end='\r')
    