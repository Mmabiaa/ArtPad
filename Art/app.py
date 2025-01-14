from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import tempfile
import win32api
import win32print
from math import cos, sin, radians, sqrt

root = Tk()
root.title("Art - Mmabiaa")
root.geometry("1200x600+150+50")
root.configure(bg="#f2f3f5")
root.resizable(False, False)

# Variables
current_x = 0
current_y = 0
color = 'black'
fill_color = 'white'
ink_width = 2
canvas_image = None
current_tool = "brush"
rect_start_x = None
rect_start_y = None
polygon_points = []

# Color palette options
color_options = ['black', 'grey', 'brown4', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'aqua', 'pink']

# Functions
def locate_xy(work):
    global current_x, current_y
    current_x = work.x
    current_y = work.y

def AddLine(work):
    global current_x, current_y, rect_start_x, rect_start_y, polygon_points
    if current_tool == "brush":
        canvas.create_line((current_x, current_y, work.x, work.y), width=ink_width, fill=color)
    elif current_tool == "rectangle":
        if rect_start_x is None or rect_start_y is None:
            rect_start_x, rect_start_y = current_x, current_y
        canvas.delete("temp_rectangle")
        canvas.create_rectangle(rect_start_x, rect_start_y, work.x, work.y, outline=color, width=ink_width, tags="temp_rectangle")
    elif current_tool == "oval":
        if rect_start_x is None or rect_start_y is None:
            rect_start_x, rect_start_y = current_x, current_y
        canvas.delete("temp_oval")
        canvas.create_oval(rect_start_x, rect_start_y, work.x, work.y, outline=color, width=ink_width, tags="temp_oval")
    elif current_tool == "polygon":
        polygon_points.append((work.x, work.y))
        canvas.delete("temp_polygon")
        if len(polygon_points) > 1:
            canvas.create_line(polygon_points, fill=color, width=ink_width, tags="temp_polygon")
    elif current_tool == "freeform":
        canvas.create_line((current_x, current_y, work.x, work.y), width=ink_width, fill=color)
    elif current_tool in ["star", "kite", "question"]:
        draw_shape(current_tool, current_x, current_y, work.x, work.y)
    
    current_x, current_y = work.x, work.y

def draw_shape(tool, x1, y1, x2, y2):
    size = int(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))  # Calculate size based on distance
    if tool == "star":
        draw_star(x1, y1, size)
    elif tool == "kite":
        draw_kite(x1, y1, size)
    elif tool == "question":
        draw_question(x1, y1, size)

def draw_star(x, y, size):
    points = []
    for i in range(5):
        angle = i * (144)  # 144 degrees between points
        x_point = x + size * (1.5 if i % 2 == 0 else 0.5) * cos(radians(angle))
        y_point = y + size * (1.5 if i % 2 == 0 else 0.5) * sin(radians(angle))
        points.append((x_point, y_point))
    canvas.create_polygon(points, fill=fill_color, outline=color, width=ink_width)

def draw_kite(x, y, size):
    points = [
        (x, y - size),  # Top
        (x + size, y),  # Right
        (x, y + size),  # Bottom
        (x - size, y),  # Left
    ]
    canvas.create_polygon(points, fill=fill_color, outline=color, width=ink_width)

def draw_question(x, y, size):
    canvas.create_text(x, y, text="?", font=("Arial", size), fill=color)

def release_shape():
    global rect_start_x, rect_start_y, polygon_points
    rect_start_x = None
    rect_start_y = None
    if current_tool == "rectangle" or current_tool == "oval":
        polygon_points = []

def show_color(new_color):
    global color
    color = new_color

def show_fill_color(new_color):
    global fill_color
    fill_color = new_color

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

def open_canvas():
    global canvas_image
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas.delete('all')
        img = Image.open(file_path)
        canvas_image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=NW, image=canvas_image)

def insert_image():
    global canvas_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")])
    if file_path:
        img = Image.open(file_path)
        canvas_image = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=NW, image=canvas_image)

def print_canvas():
    temp_file = tempfile.mktemp(suffix=".eps")
    canvas.postscript(file=temp_file)
    img = Image.open(temp_file)
    img.save(temp_file.replace(".eps", ".png"), "png")
    win32api.ShellExecute(0, "print", temp_file.replace(".eps", ".png"), None, ".", 0)
    os.remove(temp_file)

def share_canvas():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        save_canvas()
        messagebox.showinfo("Share", "Canvas saved for sharing!\nYou can now attach it to your email.")

def about():
    messagebox.showinfo("About", 
        "This is a simple art and paint program with some cool features like:\n"
        "- Drawing various shapes (including stars, kites, questions, polygons)\n"
        "- Freeform drawing\n"
        "- Text placement\n"
        "- Adjustable ink width and colors\n"
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
        canvas.configure(bg="#ffffff")
        ink_width_slider.configure(bg="#444444", fg="white", activebackground="#555555", highlightbackground="#444444")
    else:
        root.configure(bg="#f2f3f5")
        status_bar.configure(bg="#f2f3f5", fg="black")
        menubar.configure(bg="#f2f3f5", fg="black")
        canvas.configure(bg="#ffffff")
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
file_menu.add_command(label="Open", command=open_canvas)
file_menu.add_command(label="Insert", command=insert_image)
file_menu.add_command(label="Save", command=save_canvas)
file_menu.add_command(label="Save As", command=save_canvas)
file_menu.add_command(label="Print", command=print_canvas)
file_menu.add_command(label="Share", command=share_canvas)
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

# Create Formatting Toolbar
toolbar_frame = Frame(root, bg="#f2f3f5")
toolbar_frame.place(x=0, y=0, width=1200, height=40)

# Tools
brush_button = Button(toolbar_frame, text="Brush", command=lambda: set_tool("brush"), bg="#f2f3f5")
brush_button.pack(side=LEFT, padx=5, pady=5)

rectangle_button = Button(toolbar_frame, text="Rectangle", command=lambda: set_tool("rectangle"), bg="#f2f3f5")
rectangle_button.pack(side=LEFT, padx=5, pady=5)

oval_button = Button(toolbar_frame, text="Oval", command=lambda: set_tool("oval"), bg="#f2f3f5")
oval_button.pack(side=LEFT, padx=5, pady=5)

polygon_button = Button(toolbar_frame, text="Polygon", command=lambda: set_tool("polygon"), bg="#f2f3f5")
polygon_button.pack(side=LEFT, padx=5, pady=5)

star_button = Button(toolbar_frame, text="Star", command=lambda: set_tool("star"), bg="#f2f3f5")
star_button.pack(side=LEFT, padx=5, pady=5)

kite_button = Button(toolbar_frame, text="Kite", command=lambda: set_tool("kite"), bg="#f2f3f5")
kite_button.pack(side=LEFT, padx=5, pady=5)

question_button = Button(toolbar_frame, text="Question", command=lambda: set_tool("question"), bg="#f2f3f5")
question_button.pack(side=LEFT, padx=5, pady=5)

eraser_button = Button(toolbar_frame, image=eraser, bg="#f2f3f5", command=clear_canvas)
eraser_button.pack(side=LEFT, padx=5, pady=5)

colors = Canvas(root, bg="#ffffff", width=37, height=300, bd=0)
colors.place(x=30, y=60)

def display_pallete():
    for i, col in enumerate(color_options):
        id = colors.create_rectangle((10, 10 + i * 30, 30, 30 + i * 30), fill=col, outline="")
        colors.tag_bind(id, '<Button-1>', lambda x, col=col: show_color(col))

display_pallete()

canvas = Canvas(root, width=930, height=500, background="white", cursor="hand2")
canvas.place(x=100, y=50)

canvas.bind('<Button-1>', locate_xy)
canvas.bind('<B1-Motion>', AddLine)
canvas.bind('<ButtonRelease-1>', release_shape)

# Ink Width Slider
ink_width_slider = Scale(root, from_=1, to=10, orient=VERTICAL, label="Ink Width", command=lambda val: update_ink_width(val),
                          bg="#444444", fg="white", activebackground="#555555", highlightbackground="#444444", length=500)
ink_width_slider.set(ink_width)
ink_width_slider.place(x=1030, y=60)

def update_ink_width(val):
    global ink_width
    ink_width = int(val)

def set_tool(tool):
    global current_tool, rect_start_x, rect_start_y, polygon_points
    current_tool = tool
    rect_start_x = None
    rect_start_y = None
    polygon_points = []

# Status Bar
status_bar = Label(root, text="Welcome to Art - Mmmabia!", bd=1, relief=SUNKEN, anchor=W)
status_bar.place(x=0, y=550, relwidth=1, height=20)

is_dark_theme = False
root.mainloop()
