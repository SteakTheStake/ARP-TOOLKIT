import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Blacklisted directories
BLACKLISTED_DIRS = [
    '/assets/minecraft/textures/environment',
    '/assets/minecraft/textures/font',
    '/assets/minecraft/textures/gui',
    '/assets/minecraft/textures/misc'
]

def resize_image(image_path, percentage):
    try:
        # Open image
        img = Image.open(image_path)
        
        # Get original dimensions
        width, height = img.size
        
        # Calculate new dimensions based on the given percentage
        new_width = int(width * percentage / 100)
        new_height = int(height * percentage / 100)
        
        # Resize image using nearest-neighbor algorithm
        img_resized = img.resize((new_width, new_height), Image.NEAREST)
        
        # Save resized image to the same path, effectively replacing the original
        img_resized.save(image_path)
        
        print(f"Successfully resized {image_path} from {width}x{height} to {new_width}x{new_height}")
        
    except Exception as e:
        print(f"Could not resize {image_path}: {e}")

def resize_images_in_tree(folder_path, percentage):
    for root, dirs, files in os.walk(folder_path):
        # Check if the current directory is blacklisted
        if any(root.endswith(blacklist) for blacklist in BLACKLISTED_DIRS):
            print(f"Skipping blacklisted directory: {root}")
            continue

        for file in files:
            # Check if the file is an image (you can add more formats if needed)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                image_path = os.path.join(root, file)
                resize_image(image_path, percentage)

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        status_label.config(text=f"Selected folder: {folder_path}")

def start_resizing():
    global folder_path
    try:
        # Get the percentage from the text box
        percentage = float(percentage_entry.get())
        
        # Validate percentage
        if percentage <= 0 or percentage >= 100:
            status_label.config(text="Invalid percentage. Enter a number between 0 and 100.")
            return
        
        if folder_path:
            resize_images_in_tree(folder_path, percentage)
            status_label.config(text="Resizing completed!")
        else:
            status_label.config(text="No folder selected.")
            
    except ValueError:
        status_label.config(text="Please enter a valid number for percentage.")

# Initialize global variable for folder path
folder_path = None

# Create a simple GUI window
root = tk.Tk()
root.title("Image Resizer")

# Add a button for folder selection
select_button = tk.Button(root, text="Select Assets Folder", command=select_folder)
select_button.pack()

# Add a text box for entering the percentage
percentage_entry = tk.Entry(root)
percentage_entry.pack()
percentage_entry.insert(0, "50")  # Default value

# Add a button to start resizing
start_button = tk.Button(root, text="Start", command=start_resizing)
start_button.pack()

# Add a label to display the status
status_label = tk.Label(root, text="Please select a folder and enter the percentage.")
status_label.pack()

# Start the GUI event loop
root.mainloop()
