from PIL import Image, ImageFilter
from tkinter import filedialog
import tkinter as tk

# Hide the main Tk window
root = tk.Tk()
root.withdraw()

# Open file dialog to select image
file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.png *.jpg *.jpeg")])

if file_path:
    image = Image.open(file_path)
    blurred = image.filter(ImageFilter.GaussianBlur(radius=50))
    blurred.save("blurred_output.png")
    print("Image blurred and saved as blurred_output.png")
else:
    print("No file selected.")
