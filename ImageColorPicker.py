###### author: Senua Blade
# import matplotlib
import base64
import io
import os.path
import sys

import matplotlib.colors
from tkinter import *
from customtkinter import *
import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
import swatch as swatch
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
import string
import random  # to generate a random identifier for a palette
from datetime import datetime as current_date
import json

import DatabaseChecker  # Handles some main functions for the palette.db database
import FrameList
import check_image

# Check if the database is available at the start
try:
    my_connection = sqlite3.connect('palette.db')
    cursor = my_connection.cursor()
except sqlite3.Error as error:
    print("Error", error)


class Palette:
    def __init__(self, container=None):
        # The main window to hold the palette canvas
        self.palette_id = None
        self.palette_name = None
        self.palette_date = None
        self.palette_dict = None
        self.palette_colors = None
        self.palette_canvas = None
        self.container = container

        self.palette_length = 0

    def generate_palette(self, colors, color_list=None):
        self.palette_colors = colors
        self.palette_length = len(colors)

        self.container.configure(width=self.palette_length * 50)

        self.palette_canvas = Canvas(master=self.container, height=100, width=self.palette_length * 50, bg='#fff')
        self.palette_canvas.pack(side=LEFT, expand=True, ipady=5, ipadx=5, pady=10)

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

        self.save_to_db()  # Call to save the palette to the database
        self.container.mainloop()

    def save_to_db(self):
        row_count = DatabaseChecker.get_row_count()
        self.palette_id = ''.join((random.choice(string.ascii_lowercase) for x in range(10)))
        self.palette_date = current_date.now().strftime('%Y-%m-%d %H:%M:%S')
        self.palette_name = 'palette_' + str(row_count + 1)

        save_palette_to_db = "INSERT INTO My_Palettes VALUES (?, ?, ?, ?, ?)"
        data = (self.palette_id, self.palette_name, self.palette_date, self.palette_length, (row_count + 1))

        save_color_to_db = "INSERT INTO Palette_Colors(palette_id) VALUES (?)"

        try:
            cursor.execute(save_palette_to_db, data)
            my_connection.commit()
            cursor.execute(save_color_to_db, [self.palette_id])
            my_connection.commit()
        except sqlite3.Error as error:
            # in the event of error
            my_connection.rollback()
            print("Error: ", error)

        try:
            for value in range(self.palette_length):
                print("Data {}".format(value))
                color_id = f"color_id_{value + 1}"
                save_color_to_db = f"UPDATE Palette_Colors SET {color_id} = '{self.palette_colors[value]}' WHERE palette_id = '{self.palette_id}'"
                print(save_color_to_db)
                data_2 = (self.palette_colors[value])
                print(data_2)

                cursor.execute(save_color_to_db)
                # cursor.execute(save_color_to_db, data_2)
                my_connection.commit()
            print("Data DONE 2")
        except sqlite3.Error as error:
            print("An Error has occurred: ", str(error))
            my_connection.rollback()
        my_connection.close()

    def save_palette(self, selection):
        def save_1():  # To save to a JSON file
            print("save_1 has been called")
            colors_dict = {}
            i = 0
            for color in self.palette_colors:
                i += 1
                color_name = f'color_{i}'
                colors_dict[color_name] = str(color)

            save_details = [{'program': 'palette-picker', 'version': '1.0.0'},
                            {'palette name': self.palette_name, 'palette id': self.palette_id,
                             'created date': self.palette_date, 'no of colors': self.palette_length},
                            {"colors": colors_dict}]

            filename = self.palette_name + '.json'
            is_file = os.path.isfile(filename)
            if not is_file:
                with open(filename, 'w') as fp:
                    json.dump(save_details, fp, indent=2)
                showinfo(title='Success',
                         message=f"Your palette has been successfully saved as {filename}.")
            else:
                print(f'An error occurred writing to {filename}.')

        def save_2():  # TO save colors to an ASE swatch file
            print("save_2 has been called")

            filename = self.palette_name + '.ase'
            # Open a new ASE file for writing

            showinfo(title='Success',
                     message=f"Your palette has been successfully saved as {filename}.")

        def save_3():  # Save as image file
            print("Save_3 has been called")
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
            save_img.save(f"{self.palette_name}.jpg")
            showinfo(
                title='Success',
                message=f'Picture saved to current directory as ./saves/{self.palette_name}.jpg'
            )

        def save_4():  # Save to text file
            print("Save_4 has been called")
            filename = fr'{self.palette_name}.txt'
            is_file = os.path.isfile(filename)

            # open both files
            with open('./saves/colors.txt', 'r') as first_file, open(is_file, 'a') as second_file:
                # read content from first file
                for line in first_file:
                    # append content to second file
                    second_file.write(line)
            showinfo(title='Success',
                     message=f'File has been saved as: {self.palette_name}.txt')

        default = 'save_3'
        # getattr(self.save_palette, f'save_{selection}', lambda: default)()
        if selection == 1:
            save_1()
        elif selection == 2:
            save_2()
        elif selection == 3:
            save_3()
        else:
            save_4()


def get_points(filename):
    showinfo(
        title='Information',
        message='Right Click Mouse to Cancel Getting Points \n'
                'Default Maximum Points is 10'
    )
    img = plt.imread(filename)
    points = plt.ginput(n=10, show_clicks=True, mouse_stop=3)

    # print(points)

    def show(event):
        check = save_as_combo.get()
        drop_list = {1: "JSON File", 2: "ASE (Swatch File)", 3: "Image File", 4: "Txt File"}

        selection = {i for i in drop_list if drop_list[i] == str(check)}
        showinfo(
            title='Information',
            message=f'You have selected: {selection}'
        )
        print(">>>", list(selection)[0])
        new_palette.save_palette(list(selection)[0])

    # drop = OptionMenu(frame, save_menu, "CSV", "ASE (Swatch File)", "Image", "Text File")
    # drop.pack(side=RIGHT, pady=10)
    ttk.Label(master=frame, text="Save palette below.").place(x=10, y=10)
    save_as_combo = ctk.CTkComboBox(master=frame,
                                    values=["JSON File", "ASE (Swatch File)", "Image File", "Txt File"],
                                    state="readonly")
    save_as_combo.set("Save Palette as:")
    save_as_combo.bind("<<ComboboxSelected>>", show)
    save_as_combo.place(x=10, y=20)

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
            list_1 = rgb_codes.tolist()  # convert the numpy array to a list

            if any(i > 1 for i in
                   list_1):  # using the any() function to check if any element in the list is greater than 1
                color_to_hex = "#{:02x}{:02x}{:02x}".format(list_1[0], list_1[1], list_1[2])
                colors.append(color_to_hex)
                print("For list_1", color_to_hex)
            else:
                color_to_hex = matplotlib.colors.to_hex(rgb_codes)
                colors.append(color_to_hex)
                print("For rgb_codes", color_to_hex)

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
        with open("saves/colors.txt", "w") as f:
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
    open_my_palettes_btn.pack_forget()
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
        toolbar = NavigationToolbar2Tk(canvas, welcome_window)
        toolbar.update()

        # clear graph
        def clear_graph():
            for widgets in frame.winfo_children():
                widgets.destroy()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        # delete_button = Button(master=welcome_window, command=clear_graph, height=2, width=10,
        #                       text="Delete Graph")
        delete_button = ctk.CTkButton(master=welcome_window, command=clear_graph, height=3, width=10,
                                      border_width=0, corner_radius=8,
                                      text="Delete Graph")
        delete_button.place(relx=0.5, rely=0.5, anchor=CENTER)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# The main tkinter window
welcome_window = ctk.CTk()
# window title
welcome_window.title("Palette~Hive v1.0.0")
# window dimensions
# window.geometry('width x height + x + y
# x is the window's horizontal position
# y is the window's vertical position
welcome_window.geometry("600x400")
welcome_window.resizable(False, False)
# Add a background image for the application welcome screen
welcome_bg = ImageTk.PhotoImage(Image.open("./assets/app_images/welcome-bg.jpg").resize((1000, 500)))
welcome_canvas = Canvas(welcome_window, width=600, height=400)

welcome_canvas.create_image(0, 0, image=welcome_bg, anchor="nw")
txt = welcome_canvas.create_text((590, 390), text="background: from vecteezy.com", fill='white', font='tkDefaultFont 6',
                                 anchor=SE)
# Logo for the Welcome Screen
logo = PhotoImage(file="assets/app_images/app-logo.png")
# NOTE: To display pictures with transparent backgrounds use the Canvas
welcome_canvas.create_image((300, 10), image=logo, anchor=N)

welcome_canvas.pack(fill="both", expand=True)

# Create a frame widget to group the color palette and the matplotlib figure
frame = Frame(master=welcome_window)
frame.configure(bg='white')
frame.pack()


def destroyer():  # terminates the program by destroying the main window and killing the process using the exit()
    welcome_window.quit()
    welcome_window.destroy()
    sys.exit()


welcome_window.protocol("WM_DELETE_WINDOW", destroyer)  # kill the app process thread


def delete_graph(filename):
    pass


def upload_file(file_data):
    for widgets in frame.winfo_children():
        widgets.destroy()

    plot(file_data)  # call the plot function with the obtained file
    welcome_canvas.pack_forget()
    welcome_window.state('zoomed')
    points_button = Button(master=frame, command=lambda: get_points(file_data), height=2, width=10, text="Get Points")
    points_button.pack(side=RIGHT, padx=10)


def open_new_project_window():
    new_window = ctk.CTk()
    new_window.title('New Project ~ Untitled-1')
    new_window.geometry('400x300')
    new_window.configure(background="white")
    new_window.attributes('-topmost', True)


    def open_prompts(check, prompt=None):
        new_window.attributes('-topmost', check)
        if prompt == 1:
            webbrowser.open('https://images.google.com/')
        elif prompt == 0:
            file_types = [('Compatible Files', '*.jpg, *.png')]
            filename = filedialog.askopenfilename(filetypes=file_types)
            upload_file(filename)
            welcome_canvas.destroy()
            new_window.destroy()

    def get_image_data(widget):
        image_url = widget.get(1.0, tk.END).strip()

        if len(image_url) != 0:
            if image_url[0] == 'd':
                data_img = fr"{image_url[image_url.find(r'/9'):]}"
                Image.open(io.BytesIO(base64.b64decode(data_img))).save('web-image.jpg')
                upload_file('web-image.jpg')
            else:
                get_image_name = check_image.get_image(url=fr"{image_url}")
                print(f'The image is {get_image_name}')

                upload_file(get_image_name)
            new_window.destroy()
        else:
            showinfo(title='Error',
                     message='Enter an image url first')

    def unlock(event):
        print('on')
        get_img_url.configure(state='normal')

    open_browser = ctk.CTkButton(master=new_window, text='Open Google Images',
                                 command=lambda check=False: open_prompts(check, 1))

    tk.Frame(new_window, height=2, bg="gray").pack(fill="x", padx=10, pady=10)
    tk.Label(new_window, text="Paste an image url address", foreground="black", background="white").place(anchor=NW)
    url_data = ctk.CTkTextbox(new_window, height=1, width=200, border_width=1, border_color='white')
    url_data.bind('<FocusIn>', unlock)
    url_data.pack()
    get_img_url = ctk.CTkButton(master=new_window, text="Enter", state='disabled',
                                command=lambda: get_image_data(url_data))
    get_img_url.pack(pady=10)
    open_file = ctk.CTkButton(master=new_window, text='Open Local Image File',
                              command=lambda check=False: open_prompts(check, 0))

    tk.Frame(new_window, height=2, bg="gray").pack(fill="x", padx=10, pady=10)
    open_browser.pack(side=TOP, pady=10)
    tk.Frame(new_window, height=2, bg="gray").pack(fill="x", padx=10, pady=10)
    open_file.pack(side=TOP, pady=30)

    # Open a website using pywebview package
    # webview.create_window('Google Images', 'https://google.com')
    # webview.start()

    new_window.mainloop()


# Create a menu bar for the main window containing links and adding functionality
menu_bar = Menu(master=welcome_window)
# setting tearoff=0 to avoid the menu from being torn off where the first position 0 in the list of choices
# is occupied by the tear-off element and the additional choices are added starting at position 1
file_menu = Menu(menu_bar, tearoff=0)
# add_command() -- adds a menu item to the menu
file_menu.add_command(label="New Project", command=open_new_project_window)
file_menu.add_command(label='Open Project')
file_menu.add_separator()
file_menu.add_command(label='Clear Saved Palettes', command=lambda: DatabaseChecker.delete_color_records())
file_menu.add_command(label='My Saved Palettes', command=lambda: open_my_palettes())
# ad_separator() -- adds a separator line to the menu
file_menu.add_separator()
file_menu.add_command(label='Close App', command=lambda: destroyer())

# add_cascade -- creates a new hierarchical menu by associating a given menu to a parent menu
menu_bar.add_cascade(label='File', menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo")
edit_menu.add_separator()
edit_menu.add_command(label='Cut')
edit_menu.add_command(label='Copy')
edit_menu.add_command(label='Delete Graph')

# Example of a menu inside another menu
# edit_menu.add_cascade(label='Edit', menu=file_menu)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
#
# Add the menu to the main window
welcome_window.config(menu=menu_bar)


def open_my_palettes():
    palette_win = Tk()
    palette_win.title('My Palettes')
    palette_win.geometry('500x400')
    palette_win.resizable(False, False)

    '''
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
    with open('saves/colors.txt') as file:
        for line in file:
            if line[0] == '#':
                print(line)
                colors.append(line[0:7])
    print(colors)
    previous_palette = Palette(palette_win)
    previous_palette.generate_palette(colors=colors)
    '''
    previous_palettes = DatabaseChecker.read_color_records()
    my_list = FrameList.FrameList(palette_win)
    print(previous_palettes)
    my_list.create_frames(previous_palettes)
    my_list.pack(fill="both", expand=True, padx=20, pady=20)

    palette_win.mainloop()


# Frame for button border
btn_border = tk.Frame(welcome_window, highlightbackground='black', highlightthickness=3, bd=0)


# button
def image(smp, url):
    test_img = tk.PhotoImage(file=url)
    test_img = test_img.subsample(smp, smp)
    return test_img


'''
but = ctk.CTkButton(
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
# new_icon = image(5, "./assets/create_new.png")
# create_icon = ImageTk.PhotoImage(resized_icon)
new_icon = ctk.CTkImage(light_image=Image.open("./assets/create_new.png"), size=(30, 30))
open_new_project_btn = ctk.CTkButton(master=welcome_canvas, width=30, height=10, image=new_icon, hover=True,
                                     text='Create New Project', bg_color='white', fg_color='black',
                                     font=('Arciform', 15), border_width=0, corner_radius=0,
                                     compound=tk.LEFT, anchor=CENTER,
                                     command=open_new_project_window)
# open_new_project_btn.configure(image=new_icon)
# open_file_icon = Image.open('./assets/open.png').resize((50, 50), resample=3)
# new_icon_1 = ImageTk.PhotoImage(open_file_icon)
# new_icon_1 = image(10, './assets/open.png')
my_image = ctk.CTkImage(dark_image=Image.open('./assets/open.png'), size=(30, 30))
open_my_palettes_btn = ctk.CTkButton(master=welcome_canvas, text='My Palettes', width=30, height=10,
                                     image=my_image, font=('Arciform', 15), border_width=0, corner_radius=0,
                                     hover=True, bg_color='white', fg_color='black',
                                     compound=tk.RIGHT,
                                     command=open_my_palettes)
open_new_project_btn.place(x=300, y=200, anchor=CENTER)
open_my_palettes_btn.place(x=300, y=270, anchor=CENTER)

# run the gui
welcome_window.mainloop()

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
