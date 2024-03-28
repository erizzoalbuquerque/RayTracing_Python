from RayTracing.film import Film
from RayTracing.camera import Camera
from RayTracing.scene import Scene

def render(film : Film, camera : Camera, scene : Scene):
    print("Starting render...")
    print(f"film resolution is: {film.height} X {film.width}")
    print(f"Scene has {len(scene.instances)} instances.")
    
    for i in range(film.width):
        for j in range(film.height):
            #print(f"Rendering pixel {i}, {j}...")
            (x,y) = film.get_sample(i,j)
            #print(f"Rendering sample {x}, {y}...")
            ray = camera.generate_ray(x,y)
            #print(ray.direction)
            color = scene.trace_ray(ray)
            film.set_pixel_value(i,j,color)
            #print(color)
    