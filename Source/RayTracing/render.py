from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.color import Color

from timeit import default_timer as timer

def render(film : Film, camera : Camera, scene : Scene, render_type : str, pt_max_depth : int, use_russian_roulette : bool, rr_min_depth : int):
    print("Starting render...")
    print(f"Render Type: {render_type}")
    print(f"film resolution is: {film.width} X {film.height}")
    print(f"Scene has {len(scene.instances)} instances.")
    print(f"Ambient light is {scene.ambient_light_power}.")
    
    film_sample_count = film.sample_count
    print(f"Film sample count is {film_sample_count}.")
    
    if (render_type == "PATH_TRACER"):
        print(f"Path Tracer max depth is {pt_max_depth}.")
        print(f"Russian Roulette is {use_russian_roulette}.")
        if (use_russian_roulette):
            print(f"Russian Roulette min depth is {rr_min_depth}.")
    
    total_pixels = film.width * film.height
    
    
    pixels_printed = 0
    progress = 0    
    start_time = timer()
    last_print_time = start_time
    
    for i in range(film.width):
        for j in range(film.height):
            
            color = Color(0,0,0)            
            for k in range(film_sample_count):
                #print(f"Rendering pixel {i}, {j}...")
                (x,y) = film.get_sample(i,j)
                #print(f"Rendering sample {x}, {y}...")
                ray = camera.generate_ray(x,y)
                #print(ray.direction)
                if (render_type == "RAY_TRACER"):
                    color += scene.trace_ray(ray)
                elif (render_type == "PATH_TRACER"):
                    color += scene.trace_path(ray, pt_max_depth, use_russian_roulette, rr_min_depth)
                else:
                    print("Error: Render type not recognized.")
                    return
                
                # Update progress
                current_progress = (k + j * film_sample_count + i * film.height * film_sample_count) / (total_pixels * film_sample_count)   * 100
                current_time = timer()
                
                if ( (current_progress % 10 < progress % 10) or ( (current_time - last_print_time) > 30) ):
                    print_progress(progress)
                    last_print_time = timer()
                progress = current_progress
                               
            color /= film_sample_count

            color = (color.r, color.g, color.b)   
            film.set_pixel_value(i,j,color)

            
    end_time = timer()
    
    print(f"Render time: {end_time - start_time} seconds." )
    

def print_progress(progress):
    print(f"Progress: {progress:.2f}%", end='\r')
    