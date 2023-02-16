# import matplotlib
import matplotlib.colors
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from PIL import ImageTk, Image, ImageDraw
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter.messagebox import showinfo
import webbrowser
import sqlite3

'''
my_connection = sqlite3.connect('palette_db')
print('Connected to db successfully')
cursor = my_connection.cursor()

create_users_sql = "CREATE TABLE Users (first_name TEXT, second_name TEXT)"
#cursor.execute(create_users_sql)

try:
    my_data = ('Senua', 'Blade')
    my_query = "INSERT INTO Users VALUES(?,?)"
    cursor.execute(my_query, my_data)
    my_connection.commit()
    my_connection.close()
    print("Success")
except sqlite3.Error as my_error:
    print(f"An error has occured {my_error}")
'''


class Palette:
    def __init__(self, container=None):
        # The main window to hold the palette canvas
        self.palette_colors = None
        self.palette_canvas = None
        self.container = container

        self.palette_length = 0

    def generate_palette(self, colors, color_list=None):
        self.palette_colors = colors
        self.palette_length = len(colors)
        self.container.configure(width=self.palette_length * 50)

        self.palette_canvas = Canvas(master=self.container, height=100, width=self.palette_length * 50, bg='#fff')
        self.palette_canvas.pack(side=LEFT, expand=True)

        bottom_frame = Frame(self.container)
        bottom_frame.pack(side=BOTTOM)
        # create rectangle syntax x1,y1,x2,y2
        x1, x2, x3, x4 = 0, 0, 50, 50
        self.palette_canvas.create_rectangle(0, 0, 50, 50, fill=str(colors[0]))
        self.palette_canvas.create_rectangle(100, 0, 50, 50, fill=str(colors[1]))
        for color in colors:
            self.palette_canvas.create_rectangle(x1, x2, x3, x4, fill=str(color))
            x1 += 50
            x3 += 50

        x = 25
        for color_codes in colors:
            self.palette_canvas.create_text(x, 75, text=color_codes, fill='black', font='Helvetica 8')
            x += 50

            '''
        palette_canvas.create_rectangle(0, 0, 50, 50, fill=str(colors[0]))
        palette_canvas.create_rectangle(100, 0, 50, 50, fill=str(colors[1]))
        palette_canvas.create_rectangle(150, 0, 100, 50, fill=str(colors[2]))
        palette_canvas.create_rectangle(200, 0, 150, 50, fill=str(colors[3]))
        palette_canvas.create_text(25, 50, text=colors[0], fill='black', font='Helvetica 10')
        palette_canvas.create_text(75, 50, text=colors[0], fill='black', font='Helvetica 10')
            '''

        self.container.mainloop()

    def save_palette(self):
        save_img = Image.new("RGB", (50 * self.palette_length, 50), 'white')

        draw = ImageDraw.Draw(save_img)

        draw_colors = self.palette_colors
        x = 0
        a, b, c, = 100, 0, 50
        if self.palette_length == 1:
            draw.rectangle((0, 0, 50, 50), fill=draw_colors[0], outline='white')
        else:
            draw.rectangle((0, 0, 50, 50), fill=draw_colors[0], outline='white')
            del draw_colors[0]

            for color in draw_colors:
                draw.rectangle((a, 0, c, 50), fill=color, outline='white')
                a += 50
                c += 50
        save_img.save("palette.jpg")
        showinfo(
            title='Information',
            message='Picture saved to current directory as ./palette.jpg'
        )


def get_points(filename):
    showinfo(
        title='Information',
        message='Right Click Mouse to Cancel Getting Points \n'
                'Default Maximum Points is 10'
    )
    img = plt.imread(filename)
    points = plt.ginput(n=10, show_clicks=True, mouse_stop=3)
    # print(points)
    save_palette_btn = Button(master=frame, command=lambda: new_palette.save_palette(), height=2, width=20,
                              text="Save Palette as Image")
    save_palette_btn.pack(side=RIGHT, pady=10)
    # check if any points were captured
    if len(points) > 0:
        # Store the selected points in a list
        selected_points = []
        for point in points:
            x, y = point
            selected_points.append((x, y))

        # Extract the color codes for the selected points
        colors = []
        for point in selected_points:
            x, y = point
            rgb_codes = img[int(y)][int(x)]
            color_to_hex = matplotlib.colors.to_hex(rgb_codes)
            colors.append(color_to_hex)

        # get the rgb codes from the hex values in the color array
        new_rgb = []
        for hex_code in colors:
            rgb = []
            new_hex_code = hex_code.replace("#", "")
            for i in (0, 2, 4):
                decimal = int(new_hex_code[i:i + 2], 16)
                rgb.append(decimal)
            new_rgb.append(tuple(rgb))

        # Store the color codes in a separate file
        with open("colors.txt", "w") as f:
            f.write("HEX Codes" + "\n")
            for color in colors:
                f.write(str(color) + "\n")
            f.write("RGB Codes" + "\n")
            for color in new_rgb:
                f.write(str(color) + "\n")

        f.close()
        showinfo(
            title='Information',
            message='Colors extracted from the points. Saved to ./color.txt \n'
                    'Color Palette Generated'
        )
        '''
        for widgets in frame.winfo_children():
            widgets.destroy()
        '''

        new_palette = Palette(frame)
        new_palette.generate_palette(colors=colors)

    else:
        showinfo(
            title='Warning',
            message='You did not select any points in the picture. \n'
                    'Select points from the picture again'
        )

        get_points(filename)


# plot function for plotting the graph in the tkinter window
def plot(uploaded_img):
    open_color_file_btn.pack_forget()
    open_new_project_btn.pack_forget()

    plt.clf()
    if uploaded_img is not None:
        # figure that will contain the plot
        fig = Figure(figsize=(5, 5), dpi=100)
        # list of squares
        y = [i ** 2 for i in range(101)]

        # adding the subplot
        image = Image.open(uploaded_img)
        # img = plt.imread(image)
        fig, ax = plt.subplots()
        ax.axis('off')
        plt.imshow(image)  # to add extent use extent=[0, 300, 0, 300]

        # creating the Tkinter canvas containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=frame)

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        delete_button = Button(master=window, command=lambda: plt.figure().close(), height=2, width=10,
                               text="Delete Graph")
        delete_button.pack(side=TOP, pady=10)


# The main tkinter window
window = Tk()
# window title
window.title("X Color Palette Picker")
# window dimensions
# window.geometry('width x height + x + y
# x is the window's horizontal position
# y is the window's vertical position
window.geometry("600x400+50+50")
# Create a frame widget to group the color palette and the matplotlib figure

frame = Frame(master=window)
frame.configure(bg='white')
frame.pack()

# Create a menu bar for the main window containing links and adding functionality
menu_bar = Menu(master=window)
# setting tearoff=0 to avoid the menu from being torn off where the first position 0 in the list of choices
# is occupied by the tear-off element and the additional choices are added starting at position 1
file_menu = Menu(menu_bar, tearoff=0)
# add_command() -- adds a menu item to the menu
file_menu.add_command(label="New")
file_menu.add_command(label='Open')
# ad_separator() -- adds a separator line to the menu
file_menu.add_separator()
file_menu.add_command(label='Close App', command=lambda: window.quit())

# add_cascade -- creates a new hierarchical menu by associating a given menu to a parent menu
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo")
edit_menu.add_separator()
edit_menu.add_command(label='Cut')
edit_menu.add_command(label='Copy')

# Example of a menu inside another menu
# edit_menu.add_cascade(label='Edit', menu=file_menu)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
#
# Add the menu to the main window
window.config(menu=menu_bar)


def delete_graph(filename):
    pass


def upload_file():
    global img
    file_types = [('Compatible Files', '*.jpg, *.png')]
    filename = filedialog.askopenfilename(filetypes=file_types)
    img = ImageTk.PhotoImage(file=filename)

    for widgets in frame.winfo_children():
        widgets.destroy()

    plot(filename)  # call the plot function with the obtained file
    window.state('zoomed')
    points_button = Button(master=frame, command=lambda: get_points(filename), height=2, width=10, text="Get Points")
    points_button.pack(side=RIGHT, padx=10)


def open_new_project_window():
    new_window = Tk()
    new_window.title('NEw WinDOw')
    new_window.geometry('800x600')
    new_window.attributes('-topmost', True)

    def open_prompts(check, prompt=None):
        new_window.attributes('-topmost', check)
        if prompt == 1:
            webbrowser.open('https://images.google.com/')
        elif prompt == 2:
            upload_file()
            new_window.destroy()

    new_frame = Frame(master=new_window)
    new_frame.configure(bg='white')
    new_frame.pack(pady=50, ipady=10, ipadx=10)
    open_browser = tk.Button(master=new_frame, text='Copy Image Url From Web',
                             command=lambda check=False: open_prompts(check, 1))
    open_file = tk.Button(master=new_frame, text='Open Local File', command=lambda check=False: open_prompts(check, 2))

    open_browser.pack(side=TOP, pady=10)
    open_file.pack(side=TOP, pady=20)

    # Open a website using pywebview package
    # webview.create_window('Google Images', 'https://google.com')
    # webview.start()

    new_window.mainloop()


def open_color_file():
    palette_win = Tk()
    palette_win.title('My Palettes')
    palette_win.geometry('250x100')
    palette_win.resizable(False, False)

    # A listbox to attach to the root window containing all color palettes
    listbox = Listbox(master=palette_win)
    listbox.pack(side=LEFT, fill=BOTH)

    scrollbar = Scrollbar(master=palette_win)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    for values in range(100):
        listbox.insert(END, values)

    # Attaching the listbox to the scrollbar
    listbox.config(yscrollcommand=scrollbar.set)  # to get the vertical scrollbar
    # setting the listbox.yview method since we require the vertical view
    scrollbar.config(command=listbox.yview)
    # palette_win.mainloop()
    colors = []
    with open('./colors.txt') as file:
        for line in file:
            if line[0] == '#':
                print(line)
                colors.append(line[0:7])
    print(colors)

    previous_palette = Palette(palette_win)
    previous_palette.generate_palette(colors=colors)


# Frame for button border
btn_border = tk.Frame(window, highlightbackground='black', highlightthickness=3, bd=0)


# button
def image(smp, url):
    test_img = tk.PhotoImage(file=url)
    test_img = test_img.subsample(smp, smp)
    return test_img


'''
but = tk.Button(
    master=window,
    bd=0,
    relief="groove",
    compound=tk.CENTER,
    bg="blue",
    fg="yellow",
    activeforeground="pink",
    activebackground="blue",
    font="arial 30",
    text="Click me",
    pady=10,
    # width=300
)

img = image(2, "./assets/button_images/red.png")  # 1=normal, 2=small, 3=smallest
but.config(image=img)
but.pack()
'''

# create_icon = Image.open('./assets/create_new.png').resize((50, 50), resample=3)
# new_icon = ImageTk.PhotoImage(create_icon)
new_icon = image(5, "./assets/create_new.png")
# create_icon = ImageTk.PhotoImage(resized_icon)
open_new_project_btn = tk.Button(master=window,
                                 text='Create New Project', bg='white', fg='black',
                                 font=('Arciform', 15),
                                 compound=tk.LEFT,
                                 command=open_new_project_window)
open_new_project_btn.configure(image=new_icon, activebackground='white', activeforeground='black')
# open_file_icon = Image.open('./assets/open.png').resize((50, 50), resample=3)
# new_icon_1 = ImageTk.PhotoImage(open_file_icon)
new_icon_1 = image(5, './assets/open.png')
open_color_file_btn = tk.Button(master=window, text='Open Previous Color File',
                                image=new_icon_1, font=('Arciform', 13),
                                compound=tk.LEFT,
                                command=open_color_file)
open_new_project_btn.pack(side=TOP, pady=10, ipadx=2, ipady=2, expand=True)
open_color_file_btn.pack(side=TOP, pady=10, ipadx=2, ipady=2, expand=True)
# open_window = tk.Button(master=window, command=open_new_project_window, text='Import')
# place the button in the window
# open_window.pack(side=BOTTOM)

# btn_border.pack()
# run the gui


window.configure(bg='blue')
window.mainloop()

'''
# Load the image
img = plt.imread("./flag.png")

# Plot the image
plt.imshow(img)
plt.axis('off')

# Call the ginput function to select specific points
points = plt.ginput(n=4, show_clicks=True)

# Store the selected points in a list
selected_points = []
for point in points:
    x, y = point
    selected_points.append((x, y))

# Extract the color codes for the selected points
colors = []
for point in selected_points:
    x, y = point
    rgb_codes = img[int(y)][int(x)]
    color_to_hex = matplotlib.colors.to_hex(rgb_codes)
    colors.append(color_to_hex)

# get the rgb codes from the hex values in the color array
new_rgb = []
for hex_code in colors:
    rgb = []
    new_hex_code = hex_code.replace("#", "")
    for i in (0, 2, 4):
        decimal = int(new_hex_code[i:i + 2], 16)
        rgb.append(decimal)
    new_rgb.append(tuple(rgb))

# Store the color codes in a separate file
with open("colors.txt", "w") as f:
    f.write("HEX Codes" + "\n")
    for color in colors:
        f.write(str(color) + "\n")
    f.write("RGB Codes" + "\n")
    for color in new_rgb:
        f.write(str(color) + "\n")
'''
'''
# create background color
fig, ax = plt.subplots(figsize=(192, 108), dpi=10)
fig.set_facecolor('white')
plt.savefig('bg.png')
plt.close(fig)

# create color palette
bg = plt.imread('bg.png')
fig = plt.figure(figsize=(90, 90), dpi=10)
ax = fig.add_subplot(1, 1, 1)

x_posi, y_posi, y_posi2 = 320, 25, 25
for c in colors:
    if colors.index(c) <= 5:
        y_posi += 125
        rect = patches.Rectangle((x_posi, y_posi), 290, 115, facecolor=c)
        ax.add_patch(rect)
        ax.text(x=x_posi + 360, y=y_posi + 80, s=c, fontdict={'fontsize': 150})
    else:
        y_posi2 += 125
        rect = patches.Rectangle((x_posi + 800, y_posi2), 290, 115, facecolor=c)
        ax.add_artist(rect)
        ax.text(x=x_posi + 1160, y=y_posi2 + 80, s=c, fontdict={'fontsize': 150})

ax.axis('off')

plt.imshow(bg)
plt.show() '''
