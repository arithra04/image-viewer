from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")
        self.image_list = []
        self.image_index = 0

        self.label = Label(self.root)
        self.label.pack(expand=True)

        frame = Frame(self.root)
        frame.pack(pady=10)

        self.prev_button = Button(frame, text="<< Prev", command=self.prev_image)
        self.prev_button.grid(row=0, column=0)

        self.next_button = Button(frame, text="Next >>", command=self.next_image)
        self.next_button.grid(row=0, column=1)

        self.exit_button = Button(frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=0, column=2)

        self.load_button = Button(self.root, text="Load Images", command=self.load_images)
        self.load_button.pack(pady=10)

        self.show_default_image()

    def show_default_image(self):
        try:
            print("Trying to load default.jpg...")
            image = Image.open("default.jpg")
            image = image.resize((600, 400), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.label.config(image=self.photo)
            self.root.title("Image Viewer - Default")
            print("Default image loaded successfully.")
        except Exception as e:
            self.label.config(text="Default image not found or failed to load.", font=("Arial", 16))
            print("Error loading default image:", e)

    def load_images(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        self.image_list = [os.path.join(folder_path, file)
                           for file in os.listdir(folder_path)
                           if file.lower().endswith(supported_formats)]

        if not self.image_list:
            messagebox.showerror("Error", "No supported image files found!")
            self.show_default_image()
            return

        self.image_index = 0
        self.show_image()

    def show_image(self):
        image_path = self.image_list[self.image_index]
        image = Image.open(image_path)
        image = image.resize((600, 400), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.label.config(image=self.photo)
        self.root.title(f"Image Viewer - {os.path.basename(image_path)}")

    def next_image(self):
        if self.image_list:
            self.image_index = (self.image_index + 1) % len(self.image_list)
            self.show_image()

    def prev_image(self):
        if self.image_list:
            self.image_index = (self.image_index - 1) % len(self.image_list)
            self.show_image()

# Run the application
if __name__ == "__main__":
    root = Tk()
    viewer = ImageViewer(root)
    root.mainloop()
