
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from collections import defaultdict

def ensure_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def split_image(image_paths_group, rows, cols):
    ensure_directory("assets/minecraft/optifine/ctm")
    
    for root_name, image_paths in image_paths_group.items():
        # Create a sub-folder named after the root name of the image group
        output_subfolder = os.path.join("assets/minecraft/optifine/ctm", root_name)
        ensure_directory(output_subfolder)
        
        for suffix, image_path in image_paths.items():
            img = Image.open(image_path)
            width, height = img.size
            tile_width = width // cols
            tile_height = height // rows
            
            total_tiles = rows * cols
            current_tile = 0

            for i in range(0, rows):
                for j in range(0, cols):
                    left = j * tile_width
                    upper = i * tile_height
                    right = left + tile_width
                    lower = upper + tile_height
                    
                    img_cropped = img.crop((left, upper, right, lower))
                    output_path = os.path.join(output_subfolder, f"{current_tile}{suffix}.png")
                    img_cropped.save(output_path)
                    
                    print(f"Progress: {current_tile}/{total_tiles} tiles processed for {root_name}{suffix}.")
                    current_tile += 1

def browse_images(suffix):
    file_paths = filedialog.askopenfilenames(filetypes=[("PNG files", "*.png")])
    if not file_paths:
        return
    
    img_frame = img_frames[suffix]
    for widget in img_frame.winfo_children():
        widget.destroy()
    
    for file_path in file_paths:
        img = Image.open(file_path)
        img = img.resize((50, 50))
        img = ImageTk.PhotoImage(img)
        
        lbl = ttk.Label(img_frame, image=img)
        lbl.image = img
        lbl.pack(side=tk.LEFT)
    
    img_frames[suffix].file_paths = file_paths

def execute_split():
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    
    grouped_images = defaultdict(dict)
    
    for suffix, frame in img_frames.items():
        if hasattr(frame, "file_paths"):
            for file_path in frame.file_paths:
                root_name = os.path.splitext(os.path.basename(file_path))[0].replace("_n", "").replace("_s", "")
                grouped_images[root_name][suffix] = file_path

    split_image(grouped_images, rows, cols)

# GUI Initialization
root = tk.Tk()
root.title("Image Splitter")

# Widgets
suffices = ["", "_n", "_s"]
img_frames = {}

for idx, suffix in enumerate(suffices):
    btn = ttk.Button(root, text=f"Browse Texture{suffix}", command=lambda suffix=suffix: browse_images(suffix))
    btn.grid(row=0, column=idx, padx=10, pady=10)
    
    frame = tk.Frame(root)
    frame.grid(row=1, column=idx, padx=10, pady=10)
    img_frames[suffix] = frame

rows_label = ttk.Label(root, text="Rows:")
rows_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

rows_entry = ttk.Entry(root)
rows_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="e")

cols_label = ttk.Label(root, text="Columns:")
cols_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

cols_entry = ttk.Entry(root)
cols_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="e")

split_button = ttk.Button(root, text="Split Image", command=execute_split)
split_button.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
