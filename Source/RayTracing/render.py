from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene
from RayTracing.color import Color

from timeit import default_timer as timer

def render(film : Film, camera : Camera, scene : Scene):
    print("Starting render...")
    print(f"film resolution is: {film.width} X {film.height}")
    print(f"Scene has {len(scene.instances)} instances.")
    
    start_time = timer()
    
    for i in range(film.width):
        for j in range(film.height):
            #print(f"Rendering pixel {i}, {j}...")
            (x,y) = film.get_sample(i,j)
            #print(f"Rendering sample {x}, {y}...")
            ray = camera.generate_ray(x,y)
            #print(ray.direction)
            color = scene.trace_ray(ray)
            color = (color.r, color.g, color.b)
            film.set_pixel_value(i,j,color)
            #print(color)
            
    end_time = timer()
    
    print(f"Render time: {end_time - start_time} seconds." )
    