
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os

# Import global variables from CTM-SPLIT.pyw
try:
    from CTM import last_used_num_rows, last_used_num_cols, last_used_tile_range
except ImportError:
    last_used_num_rows, last_used_num_cols, last_used_tile_range = None, None, None

def save_properties():

    # Get the Block Name from the text entry
    block_name = block_name_entry.get()
    if block_name:
        properties_text += f"matchTiles={block_name}\n"

    selected_ctm_method = ctm_method_var.get()
    
    properties_text = f"method={selected_ctm_method}\n"
    
    if last_used_num_rows is not None:
        properties_text += f"width={last_used_num_rows}\n"
    if last_used_num_cols is not None:
        properties_text += f"height={last_used_num_cols}\n"
    if last_used_tile_range is not None:
        properties_text += f"tiles={last_used_tile_range[0]}-{last_used_tile_range[1]}\n"

    
    # Add other fields here as you build up the GUI
    # For example, if you add an entry for `tiles`:
    # tiles_value = tiles_entry.get()
    # properties_text += f"tiles={tiles_value}\n"

    
    selected_folder = folder_var.get()
    filename = filename_entry.get()
    
    if selected_folder == "Select folder":
        messagebox.showwarning("Warning", "Please select a folder.")
        return
    
    if filename == "Enter filename":
        messagebox.showwarning("Warning", "Please enter a filename.")
        return
    
    
    selected_folder = folder_var.get()
    
    if selected_folder == "Select folder":
        messagebox.showwarning("Warning", "Please select a folder.")
        return
    
    
    width = width_entry.get()
    height = height_entry.get()

    output_path = os.path.join("assets/minecraft/optifine/ctm", selected_folder, f"{filename}.properties")


    
    selected_folder = folder_var.get()
    
    if selected_folder == "Select folder":
        messagebox.showwarning("Warning", "Please select a folder.")
        return
    
    
    width = width_entry.get()
    height = height_entry.get()
    
    if width:
        properties_text += f"width={width}\n"
    if height:
        properties_text += f"height={height}\n"

    output_path = os.path.join("assets/minecraft/optifine/ctm", selected_folder, f"{filename}.properties")


    tiles_input0 = tiles_input0_entry.get()
    tiles_input1 = tiles_input1_entry.get()
    if tiles_input0 and tiles_input1:
        properties_text += f"tiles={tiles_input0}-{tiles_input1}\n"

    if not output_path:
        return
    
    with open(output_path, "w") as file:
        file.write(properties_text)
    
    messagebox.showinfo("Success", "Properties file has been saved.")

# GUI Initialization
root = tk.Tk()
root.title("CTM Properties Generator")

# Widgets
ctm_method_var = tk.StringVar()
ctm_method_var.set("repeat")  # Default value


# Text entry for Block Name
block_name_label = tk.Label(window, text="Block Name:")
block_name_label.pack()
block_name_entry = tk.Entry(window)
block_name_entry.pack()
ctm_method_label = ttk.Label(root, text="CTM Method:")
ctm_method_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

ctm_method_dropdown = ttk.OptionMenu(root, ctm_method_var, "repeat", "ctm", "ctm_compact", "horizontal", "vertical", "top", "random", "repeat", "fixed", "vertical+", "horizontal+")
ctm_method_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# GUI components for "tiles"
tiles_label = ttk.Label(root, text="Amount of Tiles:")
tiles_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

tiles_input0_entry = ttk.Entry(root)
tiles_input0_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tiles_dash_label = ttk.Label(root, text="-")
tiles_dash_label.grid(row=1, column=2, padx=5, pady=10, sticky="w")

tiles_input1_entry = ttk.Entry(root)
tiles_input1_entry.grid(row=1, column=3, padx=10, pady=10, sticky="w")


# GUI components for folder selection and filename
folder_var = tk.StringVar()
folder_var.set("Select folder")  # Default value

folder_dropdown = ttk.OptionMenu(root, folder_var, "Select folder", "assets/minecraft/optifine/ctm/", "custom_folder")
folder_dropdown.grid(row=2, column=0, padx=10, pady=10, sticky="w")

filename_entry = ttk.Entry(root)
filename_entry.grid(row=3, column=0, padx=10, pady=10, sticky="w")
filename_entry.insert(0, "Filename")  # Default text


# GUI components for dynamic folder selection
def update_folder_options():
    try:
        folder_options = os.listdir("assets/minecraft/optifine/ctm")
    except FileNotFoundError:
        folder_options = ["Folder not found"]
    
    folder_dropdown["menu"].delete(0, tk.END)
    for folder in folder_options:
        folder_dropdown["menu"].add_command(label=folder, command=tk._setit(folder_var, folder))

folder_var = tk.StringVar()
folder_var.set("Select folder")  # Default value

folder_label = ttk.Label(root, text="Folder:")
folder_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

folder_dropdown = ttk.OptionMenu(root, folder_var, "Select folder")
folder_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")

update_folder_options()


# GUI components for width and height of pattern
width_label = ttk.Label(root, text="Repeat CTM Width:")
width_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
width_entry = ttk.Entry(root)
width_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

height_label = ttk.Label(root, text="Repeat CTM Height:")
height_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
height_entry = ttk.Entry(root)
height_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

save_button = ttk.Button(root, text="Save Properties", command=save_properties)
save_button.grid(row=10, column=1, padx=10, pady=10)

root.mainloop()