from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Import Pillow
import os  # Import os for file handling

root = Tk()
root.title("Art - Mmmabia")
root.geometry("1050x570+150+50")
root.configure(bg="#f2f3f5")
root.resizable(True, True)

# Variables
current_x = 0
current_y = 0
color = 'black'
ink_width = 2

# Color palette options
color_options = ['black', 'grey', 'brown4', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'aqua', 'pink']

# Functions
def locate_xy(work):
    global current_x, current_y
    current_x = work.x
    current_y = work.y

def AddLine(work):
    global current_x, current_y
    canvas.create_line((current_x, current_y, work.x, work.y), width=ink_width, fill=color)
    current_x, current_y = work.x, work.y

def show_color(new_color):
    global color
    color = new_color

def new_canvas():
    canvas.delete('all')
    display_pallete()

def clear_canvas():
    canvas.delete('all')

def load_image(path, size=None):
    img = Image.open(path)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

def save_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file=file_path + ".eps")
        img = Image.open(file_path + ".eps")
        img.save(file_path, "png")
        os.remove(file_path + ".eps")
        messagebox.showinfo("Save", "Canvas saved successfully!")

def about():
    messagebox.showinfo("About", 
        "This is a simple art and paint program with some cool features like:\n"
        "- Drawing with different colors\n"
        "- Adjustable ink width\n"
        "- Clear and new canvas options\n"
        "- Light and dark themes\n"
        "Created by a young and junior developer named Mmabiaa.\n"
        "Reach me through: email: isbbydior@gmail.com")

def toggle_theme():
    global is_dark_theme
    is_dark_theme = not is_dark_theme
    if is_dark_theme:
        root.configure(bg="#333333")
        status_bar.configure(bg="#555555", fg="white")
        menubar.configure(bg="#444444", fg="white")
        canvas.configure(bg="#ffffff")  # Keep the canvas white
        ink_width_slider.configure(bg="#444444", fg="white", activebackground="#555555", highlightbackground="#444444")
    else:
        root.configure(bg="#f2f3f5")
        status_bar.configure(bg="#f2f3f5", fg="black")
        menubar.configure(bg="#f2f3f5", fg="black")
        canvas.configure(bg="#ffffff")  # Keep the canvas white
        ink_width_slider.configure(bg="#f2f3f5", fg="black", activebackground="#d9d9d9", highlightbackground="#f2f3f5")

# Load the icon
image_icon = load_image("C:/Users/dell/OneDrive/Documents/Apps/PYTHON/Art/icon.png")
root.iconphoto(False, image_icon)

# Load and resize the eraser image
eraser_size = (30, 30)
eraser = load_image("C:/Users/dell/OneDrive/Documents/Apps/PYTHON/Art/eraser.png", eraser_size)

# Create a menu bar
menubar = Menu(root)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=new_canvas)
file_menu.add_command(label="Save As", command=save_canvas)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

theme_menu = Menu(menubar, tearoff=0)
theme_menu.add_command(label="Toggle Theme", command=toggle_theme)
menubar.add_cascade(label="Theme", menu=theme_menu)

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

# Create a button that clears the canvas when clicked
eraser_button = Button(root, image=eraser, bg="#f2f3f5", command=clear_canvas)
eraser_button.place(x=30, y=400)

colors = Canvas(root, bg="#ffffff", width=37, height=300, bd=0)
colors.place(x=30, y=60)

def display_pallete():
    for i, col in enumerate(color_options):
        id = colors.create_rectangle((10, 10 + i * 30, 30, 30 + i * 30), fill=col, outline="")
        colors.tag_bind(id, '<Button-1>', lambda x, col=col: show_color(col))

display_pallete()

canvas = Canvas(root, width=930, height=500, background="white", cursor="hand2")
canvas.place(x=100, y=10)

canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', AddLine)

# Ink Width Slider
ink_width_slider = Scale(root, from_=1, to=10, orient=VERTICAL, label="Ink Width", command=lambda val: update_ink_width(val),
                          bg="#444444", fg="white", activebackground="#555555", highlightbackground="#444444")
ink_width_slider.set(ink_width)  # Set default value
ink_width_slider.place(x=1030, y=60)

def update_ink_width(val):
    global ink_width
    ink_width = int(val)

# Status Bar
status_bar = Label(root, text="Welcome to Art - Mmmabia!", bd=1, relief=SUNKEN, anchor=W)
status_bar.place(x=0, y=550, relwidth=1, height=20)

is_dark_theme = False  # Initialize theme variable
root.mainloop()
