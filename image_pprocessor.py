import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter, ImageOps

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.original_image = Image.open("flower.jpg")  
        self.edited_image = self.original_image.copy()

        self.filter_var = tk.StringVar(value="Sepia")
        filter_options = [
            "Grayscale",
            "Sepia",
            "Invert",
            "Vertical Flip",
            "Mirror",
            "Highlight Purple",
            "Edge Detect",
            "Blur"
        ]

        self.filter_menu = ttk.Combobox(root, textvariable=self.filter_var, values=filter_options)
        self.filter_menu.grid(row=0, column=0, padx=10, pady=10)

        apply_button = tk.Button(root, text="Apply Filter", command=self.apply_filter)
        apply_button.grid(row=0, column=1, padx=10)

        reset_button = tk.Button(root, text="Reset to Original", command=self.reset_image)
        reset_button.grid(row=0, column=2, padx=10)

        self.image_label = tk.Label(root)
        self.image_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.display_image(self.original_image)

    def display_image(self, img):
        img = img.resize((900, 600))  
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self.tk_image)

    def reset_image(self):
        self.edited_image = self.original_image.copy()
        self.display_image(self.edited_image)

    def apply_filter(self):
        f = self.filter_var.get()
        img = self.original_image.copy()

        if f == "Grayscale":
            img = ImageOps.grayscale(img)

        elif f == "Sepia":
            sepia = []
            for i in range(256):
                r = int(i * 240/255)
                g = int(i * 200/255)
                b = int(i * 145/255)
                sepia.append((r, g, b))
            img = img.convert("L")
            img.putpalette([v for rgb in sepia for v in rgb])
            img = img.convert("RGB")

        elif f == "Invert":
            img = ImageOps.invert(img)

        elif f == "Vertical Flip":
            img = ImageOps.flip(img)

        elif f == "Mirror":
            img = ImageOps.mirror(img)

        elif f == "Highlight Purple":
            pixels = img.load()
            for x in range(img.width):
                for y in range(img.height):
                    r, g, b = pixels[x, y]
                    if r > 100:  
                        pixels[x, y] = (r, 0, r)
            img = img

        elif f == "Edge Detect":
            img = img.filter(ImageFilter.FIND_EDGES)

        elif f == "Blur":
            img = img.filter(ImageFilter.BLUR)

        self.edited_image = img
        self.display_image(img)


root = tk.Tk()
app = ImageProcessorApp(root)
root.mainloop()
