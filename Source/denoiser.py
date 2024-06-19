import cv2
import numpy as np
import time

def denoise_image(path, filename):
    
    print("Creating denoised image...")  
    
    full_path = path + "/" + filename  
    
    # Load your noisy image
    noisy_image = cv2.imread(full_path)

    if noisy_image is None:
        print(f"Error: Unable to load image at {full_path}")
    else:
        # Apply Non-Local Means Denoising
        denoised_image = cv2.fastNlMeansDenoisingColored(noisy_image, None, 10, 10, 7, 21)

        # Save the denoised image
        cv2.imwrite(path + "/" + "denoised_nlm_image.png", denoised_image)
        
    print("Denoised image created.")
    

start_time = time.time()
denoise_image("./Images", "output.png")
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")