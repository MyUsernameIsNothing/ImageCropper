import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps
import os

# === Image Processing Functions ===

def reduce_grayscale(img, bits):
    img = img.convert("L")
    levels = 2 ** bits
    return img.point(lambda x: int(x / 256 * levels) * int(256 / levels))

def amberize(img, bits):
    gray = reduce_grayscale(img, bits)
    return ImageOps.colorize(gray, black="black", white="#FFBF00")

def reduce_rgb(img, bits):
    factor = 256 // (2 ** bits)
    return img.point(lambda x: int(x / factor) * factor)

def process_image(path, width, height, mode, bits, out_format):
    img = Image.open(path).convert("RGB")
    img = img.resize((width, height), Image.LANCZOS)

    if mode == "Grayscale":
        if bits not in [1, 2, 4, 8, 16]:
            raise ValueError("Invalid bit depth for Grayscale")
        img = reduce_grayscale(img, bits)

    elif mode == "Amber":
        if bits not in [1, 2, 4, 8, 12]:
            raise ValueError("Invalid bit depth for Amber")
        img = amberize(img, bits)

    elif mode == "Color":
        if bits not in range(1, 65):
            raise ValueError("Invalid bit depth for Color")
        img = reduce_rgb(img, bits)

    else:
        raise ValueError("Unknown color mode")

    # Save output
    base = os.path.splitext(os.path.basename(path))[0]
    out_path = f"{base}_converted.{out_format.lower()}"
    img.save(out_path)
    messagebox.showinfo("Done", f"Image saved as {out_path}")

# === GUI Setup ===

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.bmp;*.jpg;*.jpeg;*.png")])
    entry_path.delete(0, tk.END)
    entry_path.insert(0, file_path)

def update_bit_depth_options(*args):
    mode = var_mode.get()
    menu = dropdown_bits["menu"]
    menu.delete(0, "end")
    if mode == "Grayscale":
        options = [1, 2, 4, 8, 16]
    elif mode == "Amber":
        options = [1, 2, 4, 8, 12]
    elif mode == "Color":
        options = [1, 2, 3, 4, 5, 8, 12, 16, 32, 48, 64]
    else:
        options = []
    for opt in options:
        menu.add_command(label=str(opt), command=lambda v=opt: var_bits.set(v))
    var_bits.set(options[0])

def run_conversion():
    try:
        path = entry_path.get()
        w = int(entry_width.get())
        h = int(entry_height.get())
        mode = var_mode.get()
        bits = int(var_bits.get())
        out_format = var_format.get()
        process_image(path, w, h, mode, bits, out_format)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Image Cropper")

# File selection
tk.Label(root, text="Image Path:").grid(row=0, column=0)
entry_path = tk.Entry(root, width=40)
entry_path.grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2)

# Resolution
tk.Label(root, text="Width:").grid(row=1, column=0)
entry_width = tk.Entry(root)
entry_width.insert(0, "720")
entry_width.grid(row=1, column=1)

tk.Label(root, text="Height:").grid(row=2, column=0)
entry_height = tk.Entry(root)
entry_height.insert(0, "720")
entry_height.grid(row=2, column=1)

# Color Mode
tk.Label(root, text="Color Mode:").grid(row=3, column=0)
var_mode = tk.StringVar(value="Grayscale")
tk.OptionMenu(root, var_mode, "Grayscale", "Amber", "Color", command=update_bit_depth_options).grid(row=3, column=1)

# Bit Depth
tk.Label(root, text="Bit Depth:").grid(row=4, column=0)
var_bits = tk.StringVar()
dropdown_bits = tk.OptionMenu(root, var_bits, "")
dropdown_bits.grid(row=4, column=1)
update_bit_depth_options()

# Output Format
tk.Label(root, text="Output Format:").grid(row=5, column=0)
var_format = tk.StringVar(value="bmp")
tk.OptionMenu(root, var_format, "bmp", "png", "jpg").grid(row=5, column=1)

# Convert Button
tk.Button(root, text="Convert", command=run_conversion).grid(row=6, column=1)

root.mainloop()