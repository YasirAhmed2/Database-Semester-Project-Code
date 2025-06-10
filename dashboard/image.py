from PIL import Image, ImageFilter
import os
print(os.path.exists("assets/airplane-bg.png"))
img = Image.open("assets/airplane-bg.png")

    # Apply Gaussian blur with a radius
blurred_image = img.filter(ImageFilter.GaussianBlur(radius=3))

blurred_image.save("gaussian_blurred_image.png")