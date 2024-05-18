# import os
# import tkinter as tk
# from tkinter import ttk, messagebox
# from PIL import Image, ImageTk

# # Here, we have tried to make it appealing by enabling navigation between the resultant images. Basic GUI used.
# class YOLOResultViewer:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("YOLO Result Viewer")
#         self.root.geometry("800x600")

#         # Define the path to the YOLO results, We have given standard path, please feel free to edit Prof.
#         self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "runs", "detect"))
#         self.folders = ['train', 'predict', 'val']
#         self.current_image_index = 0
#         self.image_paths = []

#         self.create_widgets()
#         self.load_images()
#         self.show_image()  # Display the resultant images.

#     # def create_widgets(self):
#     #     # Folder selection between Train, Test, Validation.
#     #     self.folder_var = tk.StringVar(value=self.folders[0])
#     #     self.folder_menu = ttk.OptionMenu(self.root, self.folder_var, self.folders[0], *self.folders, command=self.on_folder_change)
#     #     self.folder_menu.pack(pady=5)

#     #     # Navigation buttons
#     #     self.prev_button = ttk.Button(self.root, text="Previous", command=self.show_prev_image)
#     #     self.prev_button.pack(pady=5, side=tk.LEFT, padx=10)

#     #     self.next_button = ttk.Button(self.root, text="Next", command=self.show_next_image)
#     #     self.next_button.pack(pady=5, side=tk.RIGHT, padx=10)

#     #     # Displaying
#     #     self.image_canvas = tk.Canvas(self.root, width=500, height=400)
#     #     self.image_canvas.pack(pady=5)

#     #     # Image info label
#     #     self.info_label = ttk.Label(self.root, text="")
#     #     self.info_label.pack(pady=5)

#     def create_widgets(self):
#         # Dropdown menu for selecting result type
#         self.result_type_var = tk.StringVar(value="Regular Results (Viewable only after training v8)")
#         self.result_type_label = ttk.Label(self.root, text="Type of Results:")
#         self.result_type_label.pack(pady=5)
#         self.result_type_menu = ttk.OptionMenu(
#             self.root, self.result_type_var,
#             "Regular Results (Viewable only after training v8)",
#             "Regular Results (Viewable only after training v8)",
#             "Obtained Results ( Ready to View- Custom Trained)",
#             "Enhanced Results (Ready to View - Custom Trained)",
#             command=self.on_result_type_change
#         )
#         self.result_type_menu.pack(pady=5)

#         # Folder selection between Train, Test, Validation.
#         self.folder_var = tk.StringVar(value=self.folders[0])
#         self.folder_label = ttk.Label(self.root, text="Choose (Train/Test/Validation):")
#         self.result_type_label.pack(pady=5)
#         self.folder_menu = ttk.OptionMenu(self.root, self.folder_var, self.folders[0], *self.folders, command=self.on_folder_change)
#         self.folder_menu.pack(pady=5)

#         # Navigation buttons
#         self.prev_button = ttk.Button(self.root, text="Previous", command=self.show_prev_image)
#         self.prev_button.pack(pady=5, side=tk.LEFT, padx=10)

#         self.next_button = ttk.Button(self.root, text="Next", command=self.show_next_image)
#         self.next_button.pack(pady=5, side=tk.RIGHT, padx=10)

#         # Displaying
#         self.image_canvas = tk.Canvas(self.root, width=800, height=600)
#         self.image_canvas.pack(pady=5)

#         # Image info label
#         self.info_label = ttk.Label(self.root, text="")
#         self.info_label.pack(pady=5)

#     def on_result_type_change(self, event=None):
#         result_type = self.result_type_var.get()
#         if result_type == "Regular Results (Viewable only after training v8)":
#             self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "runs", "detect"))
#         elif result_type == "Obtained Results ( Ready to View- Custom Trained)":
#             self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "obtained_runs", "detect"))
#         elif result_type == "Enhanced Results (Ready to View - Custom Trained)":
#             self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "enhanced_runs", "detect"))
#         else:
#             messagebox.showerror("Error", "Invalid result type selected")

#         self.current_image_index = 0
#         self.load_images()
#         self.show_image()


#     def on_folder_change(self, event=None):
#         print("Folder changed to:", self.folder_var.get())  # Debug statement-1
#         self.current_image_index = 0
#         self.load_images()
#         self.show_image()

#     def load_images(self):
#         self.image_paths = []
#         selected_folder = self.folder_var.get()
#         folder_path = os.path.join(self.base_dir, selected_folder)
#         print("Loading images from folder:", folder_path)  # Debug statement-2
#         if os.path.exists(folder_path):
#             for file_name in os.listdir(folder_path):
#                 if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
#                     self.image_paths.append(os.path.join(folder_path, file_name))
#         print("Found images:", self.image_paths)  # Debug statement-3

#     def show_image(self):
#         if not self.image_paths:
#             self.image_canvas.delete("all")
#             self.info_label.config(text="No images found.")
#             return

#         file_path = self.image_paths[self.current_image_index]
#         print("Displaying image:", file_path)  # Debug statement-4
#         img = Image.open(file_path)
#         img = img.resize((500, 400), Image.LANCZOS)
#         img_tk = ImageTk.PhotoImage(img)

#         self.image_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
#         self.image_canvas.image = img_tk

#         folder_name = os.path.basename(os.path.dirname(file_path))
#         file_name = os.path.basename(file_path)
#         self.info_label.config(text=f"Folder: {folder_name} | File: {file_name}")

#     def show_prev_image(self):
#         if self.image_paths:
#             self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
#             self.show_image()

#     def show_next_image(self):
#         if self.image_paths:
#             self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
#             self.show_image()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = YOLOResultViewer(root)
#     root.mainloop()


import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class YOLOResultViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Result Viewer")
        self.root.geometry("1000x900")

        # Set the initial base directory to obtained_runs
        self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "obtained_runs", "detect"))

        self.folders = ['train', 'predict', 'val']
        self.current_image_index = 0
        self.image_paths = []

        self.create_widgets()
        self.load_images()

    def create_widgets(self):
        # Dropdown menu for selecting result type
        self.result_type_var = tk.StringVar(value="Obtained Results ( Ready to View- Custom Trained)")
        self.result_type_label = ttk.Label(self.root, text="Type of Results:")
        self.result_type_label.pack(pady=5)
        self.result_type_menu = ttk.OptionMenu(
            self.root, self.result_type_var,
            "Obtained Results ( Ready to View- Custom Trained)",
            "Obtained Results ( Ready to View- Custom Trained)",
            "Enhanced Results (Ready to View - Custom Trained)",
            "Regular Results (Viewable only after training v8)",
            command=self.on_result_type_change
        )
        self.result_type_menu.pack(pady=5)
        
        # Folder selection between Train, Test, Validation.
        self.folder_var = tk.StringVar(value=self.folders[0])
        self.folder_label = ttk.Label(self.root, text="Choose (Train/Test/Validation):")
        self.folder_label.pack(pady=5)
        self.folder_menu = ttk.OptionMenu(self.root, self.folder_var, self.folders[0], *self.folders, command=self.on_folder_change)
        self.folder_menu.pack(pady=5)

        # Image info labels
        self.folder_name_label = ttk.Label(self.root, text="")
        self.folder_name_label.pack(pady=5)
        self.file_name_label = ttk.Label(self.root, text="")
        self.file_name_label.pack(pady=5)

        # Navigation buttons
        self.prev_button = ttk.Button(self.root, text="Previous", command=self.show_prev_image)
        self.prev_button.pack(pady=5, side=tk.LEFT, padx=10)

        self.next_button = ttk.Button(self.root, text="Next", command=self.show_next_image)
        self.next_button.pack(pady=5, side=tk.RIGHT, padx=10)

        # Displaying
        self.image_canvas = tk.Canvas(self.root, width=1000, height=700)
        self.image_canvas.pack(pady=5)

    def on_result_type_change(self, event=None):
        result_type = self.result_type_var.get()
        if result_type == "Regular Results (Viewable only after training v8)":
            self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "runs", "detect"))
        elif result_type == "Obtained Results ( Ready to View- Custom Trained)":
            self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "obtained_runs", "detect"))
        elif result_type == "Enhanced Results (Ready to View - Custom Trained)":
            self.base_dir = os.path.normpath(os.path.join(os.getcwd(), "enhanced_runs", "detect"))
        else:
            messagebox.showerror("Error", "Invalid result type selected")

        self.current_image_index = 0
        self.load_images()
        self.show_image()

    def on_folder_change(self, event=None):
        print("Folder changed to:", self.folder_var.get())  # Debug statement-1
        self.current_image_index = 0
        self.load_images()
        self.show_image()

    def load_images(self):
        self.image_paths = []
        selected_folder = self.folder_var.get()
        folder_path = os.path.join(self.base_dir, selected_folder)
        print("Loading images from folder:", folder_path)  # Debug statement-2
        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.image_paths.append(os.path.join(folder_path, file_name))
        print("Found images:", self.image_paths)  # Debug statement-3

        # If no images found, display a message
        if not self.image_paths:
            self.image_canvas.delete("all")
            self.info_label.config(text="The YOLOv8 is not trained yet, please train it using (v8.py/enhanced_v8.py) to view the results, or use the Obtained/Enhanced (Ready to View Results) by selecting it from above Dropdown box.")
            return

    def show_image(self):
        if not self.image_paths:
            return

        file_path = self.image_paths[self.current_image_index]
        print("Displaying image:", file_path)  # Debug statement-4
        img = Image.open(file_path)
        img = img.resize((900, 700), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        self.image_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.image_canvas.image = img_tk

        folder_name = os.path.basename(os.path.dirname(file_path))
        file_name = os.path.basename(file_path)
        self.folder_name_label.config(text=f"Folder: {folder_name}")
        self.file_name_label.config(text=f"File: {file_name}")

    def show_prev_image(self):
        if self.image_paths:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
            self.show_image()

    def show_next_image(self):
        if self.image_paths:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = YOLOResultViewer(root)
    root.mainloop()
