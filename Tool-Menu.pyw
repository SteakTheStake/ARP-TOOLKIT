
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess

def open_tool(tool_script):
    subprocess.run(["python", tool_script])

# GUI Initialization
root = tk.Tk()
root.title("ARP Menu")

# Display Title
title_label = ttk.Label(root, text="ARP TOOLKIT", font=("Arial", 24))
title_label.grid(row=0, column=0, padx=20, pady=20)

try:
    logo_img = Image.open("data/logo.png")
    logo_img = logo_img.resize((100, 100))
    logo_img = ImageTk.PhotoImage(logo_img)
    
    logo_label = ttk.Label(root, image=logo_img)
    logo_label.grid(row=1, column=0, padx=20, pady=20)
except Exception as e:
    print(f"Could not load logo: {e}")

# List of Tools
tools = [
    {"name": "CTM ToolKit", "script": "data/CTM-PROP.pyw"},
    {"name": "Image Resize ToolKit", "script": "data/RESIZE.pyw"},
    # Add more tools here as dictionaries with 'name' and 'script' keys
]

# Display Buttons for Tools
for idx, tool in enumerate(tools):
    btn = ttk.Button(root, text=tool["name"], command=lambda tool_script=tool["script"]: open_tool(tool_script))
    btn.grid(row=2+idx, column=0, padx=20, pady=5)
    
root.mainloop()
