import cv2
import numpy as np

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
    
denoise_image("./Images","output.png")