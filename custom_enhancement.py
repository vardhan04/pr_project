import cv2
import numpy as np
import os
import shutil

def enhance_image(image_path, output_path):
    # Reading the image
    image = cv2.imread(image_path)

    # Applying gamma correction to adjust brightness
    gamma = 1.2  # Reduced gamma value to avoid over-brightening
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]).astype("uint8")
    adjusted = cv2.LUT(image, table)

    # Converting to LAB color space
    lab = cv2.cvtColor(adjusted, cv2.COLOR_BGR2LAB)

    # Splitting into channels
    l, a, b = cv2.split(lab)

    # Applying CLAHE to the L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    # Merging the CLAHE enhanced L-channel back with A and B channels
    limg = cv2.merge((cl, a, b))

    # Converting back to BGR color space
    enhanced_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Sharpening the image
    kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
    sharpened = cv2.filter2D(enhanced_image, -1, kernel)

    # Applying slight Gaussian blur to reduce noise
    final_image = cv2.GaussianBlur(sharpened, (3, 3), 0)

    # Saving the result
    cv2.imwrite(output_path, final_image)

def process_directory(base_dir, output_base_dir):
    # Create output directories if they don't exist
    for subfolder in ['train', 'test', 'valid']:
        images_path = os.path.join(output_base_dir, f"enhanced_{subfolder}", "images")
        labels_path = os.path.join(output_base_dir, f"enhanced_{subfolder}", "labels")
        os.makedirs(images_path, exist_ok=True)
        os.makedirs(labels_path, exist_ok=True)

        # Process images and labels
        input_images_dir = os.path.join(base_dir, subfolder, "images")
        input_labels_dir = os.path.join(base_dir, subfolder, "labels")
        output_images_dir = images_path
        output_labels_dir = labels_path

        # Enhance images and save them
        for file_name in os.listdir(input_images_dir):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(input_images_dir, file_name)
                output_path = os.path.join(output_images_dir, file_name)
                enhance_image(input_path, output_path)
                print(f"Enhanced {file_name}")

        # Copy labels
        for file_name in os.listdir(input_labels_dir):
            input_label_path = os.path.join(input_labels_dir, file_name)
            output_label_path = os.path.join(output_labels_dir, file_name)
            shutil.copy(input_label_path, output_label_path)
            print(f"Copied label {file_name}")


if __name__ == "__main__":
    # Directory paths
    base_directory = "ExDark-12"
    output_base_directory = "ExDark-12"

    # Process directories
    process_directory(base_directory, output_base_directory)
