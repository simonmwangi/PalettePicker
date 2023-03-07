###### author: Senua Blade
# import matplotlib
import base64
import io
import os.path
import re
import shutil

import matplotlib.colors
from tkinter import *
from tkinter.colorchooser import askcolor
from customtkinter import *
import customtkinter as ctk
# from tkinter import ttk ##  unused
import matplotlib.pyplot as plt
# import swatch as swatch ##  unused
from matplotlib import image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from PIL import ImageTk, Image, ImageDraw
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import showinfo, askyesno
import webbrowser
import sqlite3
import string
import random  # to generate a random identifier for a palette
from datetime import datetime as current_date
import json
import pyperclip  # to copy text to the clipboard

import database_checker  # Handles some main functions for the palette.db database
import palette_frames
import check_image

# Check if the database is available at the start
try:
    my_connection = sqlite3.connect('assets\palette.db')
    cursor = my_connection.cursor()
except sqlite3.Error as error:
    print("Error", error)

""""""""""""""""""""""""""
loaded_space = None  # Holds the current workspace object


# terminates the program by destroying the main window and killing the process using the exit()
def destroyer(self):
    answer = askyesno(title='Exit Program?',
                      message='Are you sure you want to exit the program?')

    if answer:
        global loaded_space
        loaded_space = None  # resets the loaded space var when the workspace is deleted

        my_connection.close()
        self.quit()
        self.destroy()
        sys.exit()


class Palette:
    palette_id = None
    palette_name = None
    palette_date = None
    palette_dict = None
    palette_colors = None
    palette_canvas = None

    palette_length = 5

    def __init__(self, container=None):
        # The main window to hold the palette canvas
        palette_id = None
        palette_name = None
        palette_date = None
        palette_dict = None
        palette_colors = None
        palette_canvas = None
        container = container

        palette_length = 5

    '''
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


        palette_canvas.create_rectangle(0, 0, 50, 50, fill=str(colors[0]))
        palette_canvas.create_rectangle(100, 0, 50, 50, fill=str(colors[1]))
        palette_canvas.create_rectangle(150, 0, 100, 50, fill=str(colors[2]))
        palette_canvas.create_rectangle(200, 0, 150, 50, fill=str(colors[3]))
        palette_canvas.create_text(25, 50, text=colors[0], fill='black', font='Helvetica 10')
        palette_canvas.create_text(75, 50, text=colors[0], fill='black', font='Helvetica 10')
        

        self.save_to_db()  # Call to save the palette to the database
        self.container.mainloop()
    '''

    @classmethod
    def save_to_db(cls, my_colors):
        cls.palette_colors = my_colors

        row_count = database_checker.get_row_count()
        cls.palette_id = ''.join((random.choice(string.ascii_lowercase) for x in range(10)))
        cls.palette_date = current_date.now().strftime('%Y-%m-%d %H:%M:%S')
        cls.palette_name = 'palette_' + str(row_count + 1)

        save_palette_to_db = "INSERT INTO My_Palettes VALUES (?, ?, ?, ?, ?)"
        data = (cls.palette_id, cls.palette_name, cls.palette_date, cls.palette_length, (row_count + 1))

        save_color_to_db = "INSERT INTO Palette_Colors(palette_id) VALUES (?)"

        try:
            cursor.execute(save_palette_to_db, data)
            my_connection.commit()
            cursor.execute(save_color_to_db, [cls.palette_id])
            my_connection.commit()
        except sqlite3.Error as error:
            # in the event of error
            my_connection.rollback()
            print("Error: ", error)

        try:
            for value in range(cls.palette_length):
                print("Data {}".format(value))
                color_id = f"color_id_{value + 1}"
                save_color_to_db = f"UPDATE Palette_Colors SET {color_id} = '{cls.palette_colors[value]}' WHERE palette_id = '{cls.palette_id}'"
                print(save_color_to_db)
                data_2 = (cls.palette_colors[value])
                print(data_2)

                cursor.execute(save_color_to_db)
                # cursor.execute(save_color_to_db, data_2)
                my_connection.commit()
            print("Data DONE 2")
        except sqlite3.Error as error:
            print("An Error has occurred: ", str(error))
            my_connection.rollback()
        # my_connection.close()

    @classmethod
    def save_palette(cls, selection):
        if cls.palette_colors is not None:
            def save_1():  # To save to a JSON file
                print("save_1 has been called")
                colors_dict = {}
                i = 0
                for color in cls.palette_colors:
                    i += 1
                    color_name = f'color_{i}'
                    colors_dict[color_name] = str(color)

                save_details = [{'program': 'palette-picker', 'version': '1.0.0'},
                                {'palette name': cls.palette_name, 'palette id': cls.palette_id,
                                 'created date': cls.palette_date, 'no of colors': cls.palette_length},
                                {"colors": colors_dict}]

                filename = cls.palette_name + '.json'
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

                showinfo(title='Information',
                         message=f"Under Development.\n Try Other Options.")

            def save_3():  # Save as image file
                print("Save_3 has been called")
                save_img = Image.new("RGB", (50 * cls.palette_length, 50), 'white')
                draw = ImageDraw.Draw(save_img)

                draw_colors = cls.palette_colors
                x = 0
                a, b, c, = 100, 0, 50
                if cls.palette_length == 1:
                    draw.rectangle((0, 0, 50, 50), fill=draw_colors[0], outline='white')
                else:
                    draw.rectangle((0, 0, 50, 50), fill=draw_colors[0], outline='white')
                    del draw_colors[0]

                    for color in draw_colors:
                        draw.rectangle((a, 0, c, 50), fill=color, outline='white')
                        a += 50
                        c += 50
                save_img.save(f"{cls.palette_name}.jpg")
                asksaveasfile(
                    initialfile=f"{cls.palette_name}.jpg",
                    defaultextension='.jpg', filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")]
                )

                showinfo(
                    title='Success',
                    message=f'Picture saved to current directory as ./saves/{cls.palette_name}.jpg'
                )

            def save_4():  # Save to text file
                print("Save_4 has been called")
                filename = fr'{cls.palette_name}.txt'
                is_file = os.path.isfile(filename)

                # open both files
                with open('./saves/colors.txt', 'r') as first_file, open(is_file, 'a') as second_file:
                    # read content from first file
                    for line in first_file:
                        # append content to second file
                        second_file.write(line)
                showinfo(title='Success',
                         message=f'File has been saved as: {cls.palette_name}.txt')

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
        else:
            showinfo(title='Warning',
                     message='Save the palette first')


# The Main Window onStartup()
class WelcomeWindow(tk.Tk):
    # welcome_canvas = None
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_workspace_window = None
        self.welcome_bg = None
        self.new_image_window = None

        self.title("Palette~Hive v1.0.0")  # window title
        # window.geometry('width x height + x + y x is the window's horizontal position y is the window's vertical
        # position
        self.geometry("600x400")
        self.resizable(False, False)

        # Add a background image for the application welcome screen
        welcome_bg = ImageTk.PhotoImage(Image.open(r"assets\app_images\welcome-bg.jpg").resize((1000, 500)))
        self.welcome_bg = welcome_bg
        # welcome_bg = ctk.CTkImage(dark_image=Image.open('./assets/app_images/welcome-bg.jpg'), size=(1000, 500))
        welcome_canvas = Canvas(self, width=600, height=400)

        welcome_canvas.pack(fill="both", expand=True)
        # self.configure(bg=welcome_bg)
        welcome_canvas.create_image(0, 0, image=welcome_bg, anchor="nw")
        welcome_canvas.create_text((590, 390), text="background: from vecteezy.com", fill='white',
                                   font='tkDefaultFont 6', anchor=SE)
        # Logo for the Welcome Screen
        logo = PhotoImage(file=r"assets/app_images/app-logo.png")
        self.logo = logo
        # NOTE: To display pictures with transparent backgrounds use the Canvas
        welcome_canvas.create_image((300, 10), image=logo, anchor=N)

        # Create a frame widget to group the color palette and the matplotlib figure
        self.frame = Frame(master=self, bg='white')
        self.frame.pack()

        open_icon = ctk.CTkImage(dark_image=Image.open('assets/app_images/open.png'), size=(30, 30))
        create_icon = ctk.CTkImage(light_image=Image.open("assets/app_images/create_new.png"), size=(30, 30))
        exit_icon = ctk.CTkImage(light_image=Image.open("assets/app_images/exit.png"), size=(30, 30))
        self.open_new_project_btn = ctk.CTkButton(master=welcome_canvas, width=30, height=10, image=create_icon,
                                                  hover=True,
                                                  text='Create New Project', bg_color='white', fg_color='black',
                                                  font=('Arciform', 15), border_width=0, corner_radius=0,
                                                  compound=tk.LEFT, anchor=CENTER,
                                                  command=self.open_new_workspace)
        self.open_my_palettes_btn = ctk.CTkButton(master=welcome_canvas, text='My Palettes', width=30, height=10,
                                                  image=open_icon, font=('Arciform', 15), border_width=0,
                                                  corner_radius=0,
                                                  hover=True, bg_color='white', fg_color='black',
                                                  compound=tk.RIGHT,
                                                  command=open_my_palettes)
        self.exit_btn = ctk.CTkButton(master=welcome_canvas, text='Exit Program', width=30, height=10,
                                      image=exit_icon, font=('Arciform', 15), border_width=0,
                                      corner_radius=0,
                                      hover=True, bg_color='white', fg_color='black',
                                      compound=tk.RIGHT,
                                      command=lambda: destroyer(self))
        self.exit_btn.place(x=300, y=310, anchor=CENTER)
        self.open_new_project_btn.place(x=300, y=200, anchor=CENTER)
        self.open_my_palettes_btn.place(x=300, y=270, anchor=CENTER)

        self.protocol("WM_DELETE_WINDOW", lambda: destroyer(self))  # kill the app process thread

    def delete_graph(self):
        pass

    def open_new_image_window(self):
        if self.new_image_window is None or not self.new_image_window.winfo_exists():
            self.new_image_window = NewImageWindow(self)  # create a new window
        else:
            self.new_image_window.focus()  # if the window exists

    def open_new_workspace(self):
        if self.new_workspace_window is None or not self.new_workspace_window.winfo_exists():
            self.new_workspace_window = NewWorkspace(self)  # create a new window

            self.wm_state('iconic')  # minimize the main window to the taskbar
            # self.forget(window=Wel)
        else:
            self.new_workspace_window.focus()  # if the window exists


# Frames for RGB toggles
class ColorSettingFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # self = ctk.CTkFrame(master=self, fg_color='red', width=200, height=200, corner_radius=0)
        # self.grid(row=0, padx=5, pady=5)
        self.slider_value = 0

        def only_numbers(char):
            return char.isdigit()

        def character_limit(entry_text):
            if len(entry_text.get()) > 0:
                entry_text.set(entry_text.get()[:3])

        def slider_event(value):
            self.slider_value = int(value)
            entry_text.set(str(int(value)))

        # self.frame_label = str(frame_label)
        # Frame Label
        self.label = ctk.CTkLabel(master=self, text_color='white', font=('Calibri', 15))
        self.label.grid(row=0, column=0, sticky='n')
        # Slider Toggle
        slider_var = tk.DoubleVar()
        self.slider = ctk.CTkSlider(master=self, from_=0, to=255, variable=slider_var, command=slider_event)
        self.slider.grid(row=1, column=0, pady=5)
        # Entry Widget
        validation = master.register(only_numbers)
        entry_text = StringVar()  # the text in  your entry
        entry_text.trace("w", lambda *args: character_limit(entry_text))
        entry_text.set('0')
        self.entry = ctk.CTkEntry(master=self, width=50, height=1, fg_color='#1b1c1c', border_color='black',
                                  border_width=1, text_color='white', validate="key",
                                  validatecommand=(validation, '%S'),
                                  textvariable=entry_text)
        self.entry.grid(row=1, column=1, padx=5, pady=5)


def get_images_count():
    dir_path = r'assets\my_images'  # the directory path
    count = 0

    for path in os.listdir(dir_path):  # iterate through the path
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    return count


# Creates an instance of a new window for obtaining an image
class NewImageWindow(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title('New Project ~ Untitled-1')
        self.geometry('400x300')
        self.configure(background="white")
        self.attributes('-topmost', True)
        self.iconbitmap('logo.ico')
        self.images_count = get_images_count()
        self.my_master = master
        open_browser = ctk.CTkButton(master=self, text='Open Google Images',
                                     command=lambda check=False: self.open_prompts(check, 1))

        tk.Frame(self, height=2, bg="gray").pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(self, text="Paste an image url address.  ", text_color='white').place(anchor=NW)
        url_data = ctk.CTkTextbox(self, height=1, width=200, border_width=1, border_color='white')
        # url_data.bind('<FocusIn>', self.unlock)
        url_data.pack()
        self.get_img_url = ctk.CTkButton(master=self, text="Enter", state='normal',
                                         command=lambda: self.get_image_data(url_data)).pack(pady=10)
        open_file = ctk.CTkButton(master=self, text='Open Local Image File',
                                  command=lambda check=False: self.open_prompts(check, 0))

        tk.Frame(self, height=2, bg="gray").pack(fill="x", padx=10, pady=10)
        open_browser.pack(side=TOP, pady=10)
        tk.Frame(self, height=2, bg="gray").pack(fill="x", padx=10, pady=10)
        open_file.pack(side=TOP, pady=30)

    def upload_file(self, master, file_data):
        NewWorkspace.plot(master, file_data)  # call the plot function with the obtained file

    def open_prompts(self, check, prompt=None):
        self.attributes('-topmost', check)
        if prompt == 1:
            webbrowser.open('https://images.google.com/')
        elif prompt == 0:
            file_types = [('Compatible Files', '*.jpg, *.png')]
            filename = filedialog.askopenfilename(filetypes=file_types)

            my_image = fr'assets\my_images\image_{self.images_count}.jpg'
            shutil.copyfile(filename, my_image)  # copies the file to the user's images folder

            # Creates a button on the images frame where the user can load an image to the matplotlib canvas
            image = ctk.CTkImage(light_image=Image.open(my_image),
                                 size=(100, 50))
            ctk.CTkButton(master=self.my_master.images_frame, height=60, width=100, text=f'Image: {self.images_count}',
                          image=image, anchor=N, command=lambda: self.my_master.plot(my_image)).pack(pady=10)
            self.destroy()  # closes the new_image_window dialog
            NewWorkspace.plot(self.my_master, filename)  # plot the new image

    def get_image_data(self, widget):
        image_url = widget.get(1.0, tk.END).strip()

        if len(image_url) != 0:
            if image_url[0] == 'd':
                data_img = fr"{image_url[image_url.find(r'/9'):]}"
                Image.open(io.BytesIO(base64.b64decode(data_img))).save('test_images/web-image.jpg')

                my_image = fr'assets\my_images\image_{self.images_count}.jpg'
                shutil.copyfile(r'test_images\web-image.jpg', my_image)

                image = ctk.CTkImage(light_image=Image.open(my_image),
                                     size=(100, 50))
                ctk.CTkButton(master=self.my_master.images_frame, height=60, width=100,
                              text=f'Image: {self.images_count}',
                              image=image, anchor=N, command=lambda: self.my_master.plot(my_image)).pack(pady=10)

                self.destroy()
                self.upload_file(self.my_master, r'test_images\web-image.jpg')
            else:
                get_image_name = check_image.get_image(url=fr"{image_url}")
                print(f'The image is {get_image_name}')

                my_image = fr'assets\my_images\image_{self.images_count}.jpg'
                shutil.copyfile(get_image_name, my_image)

                image = ctk.CTkImage(light_image=Image.open(my_image),
                                     size=(100, 50))
                ctk.CTkButton(master=self.my_master.images_frame, height=60, width=100,
                              text=f'Image: {self.images_count}',
                              image=image, anchor=N, command=lambda: self.my_master.plot(my_image)).pack(pady=10)

                self.destroy()
                self.upload_file(self.my_master, get_image_name)

        else:
            showinfo(title='Error',
                     message='Enter an image url first')

    def unlock(self, event):
        print('on')
        self.get_img_url.configure(state='normal')

    # Open a website using pywebview package
    # webview.create_window('Google Images', 'https://google.com')
    # webview.start()


# Creates a new workspace window
class NewWorkspace(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.windows_menu = None
        self.toggle_win_menu = None
        global loaded_space
        loaded_space = self

        """Class Variables"""
        self.img_toolbar = None
        self.attr_window = None
        self.image_filename = None
        self.canvas = None
        self.new_image_window = None
        self.palette_widget = None
        self.matplotlib_canvas = None
        self.fig = None
        """"""""""""""""""""""""""

        self.title('My Workspace')
        # self.geometry('400x300')
        # self.state('zoomed')
        self.minsize(self.winfo_screenwidth() / 2, self.winfo_screenheight() / 2)
        self.configure(background="white")
        self.attributes('-topmost', False)
        self.resizable(False, False)
        self.iconbitmap('logo.ico')
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(1, weight=1)

        self.create_window_menu()  # The window's top menu
        self.protocol("WM_DELETE_WINDOW", lambda: destroyer(self))

        self.tools_frame = ctk.CTkFrame(master=self, width=50, height=50, fg_color='grey')
        self.tools_frame.grid(row=0, column=0, padx=5, sticky='news', pady=10, ipadx=5)
        self.main_frame = ctk.CTkFrame(master=self, width=200, height=50, fg_color='#17191a')
        self.main_frame.grid(row=0, column=1, padx=5, sticky='nsew')

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(master=self.tools_frame, text='My Tools', anchor=CENTER, padx=20, width=20, pady=10,
                     fg_color='grey').pack()
        ctk.CTkButton(master=self.tools_frame, width=50, height=20, border_width=0, corner_radius=8,
                      text="Add Image", command=lambda: WelcomeWindow.open_new_image_window(self)).pack(pady=(10, 0))
        ctk.CTkButton(master=self.tools_frame, width=50, height=20, border_width=0, corner_radius=8,
                      text="Get Points", command=lambda: self.get_points(self.image_filename, self.fig)).pack(
            pady=(10, 0))
        ctk.CTkButton(master=self.tools_frame, width=50, height=50, border_width=0, corner_radius=8,
                      text="Generate Random\n Colors", command=self.random_palette).pack(pady=(10, 0))

        # Find a way to clear the image from the workspace
        # NOT URGENT!!!
        # ctk.CTkButton(master=self.tools_frame, width=50, height=30, border_width=0, corner_radius=8,
        #              text="Clear Image \n From Workspace").pack(pady=(10, 0))

        ctk.CTkButton(master=self.tools_frame, width=5, height=20, border_width=0, corner_radius=8, hover=True,
                      hover_color='red', text="Delete All Images", command=self.delete_images).pack(pady=(10, 0))

        # Displays all images loaded to the program, so they can be displayed in the graph
        self.images_frame = ctk.CTkScrollableFrame(master=self.main_frame, fg_color='white', border_width=0,
                                                   corner_radius=0, label_text='My Images', label_text_color='black',
                                                   label_fg_color='white',
                                                   height=200, label_anchor='n')
        self.images_frame.grid(row=0, column=0, sticky='n', padx=5, pady=5)

        self.palette_canvas = Canvas(master=self.main_frame, height=150, width=5 * 100 + 20,
                                     bg='#17191a')
        self.palette_canvas.grid(row=1, column=1, padx=10, pady=10, sticky='s')

        CTkButton(master=self.palette_canvas, text='Save To My Palettes', width=60, height=5,
                  command=self.save_palette).place(x=10, y=130, anchor=W)
        CTkButton(master=self.palette_canvas, text='Clear Current Palette', width=60, height=5, hover_color='red',
                  fg_color='grey', command=self.clear_palette).place(x=150, y=130, anchor=W)
        CTkButton(master=self.palette_canvas, text='Clear Current Palette', width=60, height=5, hover_color='red',
                  fg_color='grey', command=self.clear_palette).place(x=150, y=130, anchor=W)

        def show(event):
            check = save_as_combo.get()
            drop_list = {1: "JSON File", 2: "ASE (Swatch File)", 3: "Image File", 4: "Txt File"}

            selection = {i for i in drop_list if drop_list[i] == str(check)}
            showinfo(
                title='Information',
                message=f'You have selected: {selection}'
            )
            print(">>>", list(selection)[0])
            Palette.save_palette(list(selection)[0])

        save_as_combo = ctk.CTkComboBox(master=self.palette_canvas,
                                        values=["JSON File", "ASE (Swatch File)", "Image File", "Txt File"],
                                        state="readonly", command=show)
        save_as_combo.set("Export Palette as:")
        # save_as_combo.bind("<<ComboboxSelected>>", show)
        save_as_combo.place(x=300, y=130, anchor=W)

        canvas = tk.Canvas(self.palette_canvas, bg='#808080', height=100, width=100)
        canvas.place(x=0, y=0, anchor=NW)
        canvas.create_text(50, 50, text='#808080', fill='black', font='Helvetica 10')

        canvas2 = tk.Canvas(self.palette_canvas, bg='#808080', height=100, width=100)
        canvas2.place(x=105, y=0, anchor=NW)
        canvas2.create_text(50, 50, text='#808080', fill='black', font='Helvetica 10')

        canvas3 = tk.Canvas(self.palette_canvas, bg='#808080', height=100, width=100)
        canvas3.place(x=210, y=0, anchor=NW)
        canvas3.create_text(50, 50, text='#808080', fill='black', font='Helvetica 10')

        canvas4 = tk.Canvas(self.palette_canvas, bg='#808080', height=100, width=100)
        canvas4.place(x=315, y=0, anchor=NW)
        canvas4.create_text(50, 50, text='#808080', fill='black', font='Helvetica 10')

        canvas5 = tk.Canvas(self.palette_canvas, bg='#808080', height=100, width=100)
        canvas5.place(x=420, y=0, anchor=NW)
        canvas5.create_text(50, 50, text='#808080', fill='black', font='Helvetica 10')

        self.my_canvases = [canvas5, canvas4, canvas3, canvas2, canvas]

        for canvas in self.my_canvases:
            canvas.bind('<Button-1>', self.canvas_click_event)
            canvas.bind('<Button-3>', self.show_popup_menu)

        # Displays the current matplotlib graph containing the image
        self.image_graph = ctk.CTkFrame(master=self.main_frame, fg_color='#24292f', border_width=0, corner_radius=0)
        self.image_graph.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.image_graph_label = ctk.CTkLabel(master=self.image_graph, text_color='white',
                                              text='Add an image to the workspace by pressing \n the Add Image Button.',
                                              font=('Arciform', 20))
        self.image_graph_label.pack(pady=50, anchor=CENTER)

    @classmethod
    def load_palette(cls, workspace, colors):
        i = 0

        for canvas in workspace.my_canvases:
            canvas.configure(bg=f'{colors[i]}')
            canvas.itemconfigure(1, text=f'{colors[i]}')
            i += 1

    def random_palette(self):  # Generates random colors and adds them to the palette
        if self.my_canvases is not None:
            colors = []
            for j in range(5):
                rand_color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
                colors.append(rand_color)

            i = 0
            for canvas in self.my_canvases:
                canvas.configure(bg=f'{colors[i]}')
                canvas.itemconfigure(1, text=f'{colors[i]}')
                i += 1

    def show_popup_menu(self, event):

        def copy_hex():
            pyperclip.copy(event.widget.itemcget(1, 'text'))
            showinfo(title='Done!',
                     message='Color code copied to clipboard.')

        def reset_hex():
            event.widget.configure(bg='#808080')
            event.widget.itemconfigure(1, text='#808080')

        # create the popup menu
        popup_menu = tk.Menu(self, tearoff=0)
        popup_menu.add_command(label="Copy Hex Code", command=copy_hex)
        popup_menu.add_command(label="Reset Color", command=reset_hex)

        popup_menu.post(event.x_root, event.y_root)

    def canvas_click_event(self, event):

        if self.palette_widget is not None:
            self.palette_widget.configure(highlightbackground="black", highlightcolor="black")
            self.palette_widget = None
        else:
            self.palette_widget = event.widget

            if self.attr_window is None or not self.attr_window.winfo_exists():
                # open an attributes windows for the selected text
                event.widget.configure(highlightbackground="white", highlightcolor="white")
                print('Clicked canvas: ', event.x, event.y, event.widget)

                self.attr_window = CanvasAttributesWindow(self.palette_widget, self.fig, self.image_filename)
            else:
                self.attr_window.focus()  # if the window exists bring to top

    def create_window_menu(self):
        # Create a menu bar for the main window containing links and adding functionality
        self.menu_bar = Menu(master=self)
        # setting tearoff=0 to avoid the menu from being torn off where the first position 0 in the list of choices
        # is occupied by the tear-off element and the additional choices are added starting at position 1
        file_menu = Menu(self.menu_bar, tearoff=0)
        # add_command() -- adds a menu item to the menu
        file_menu.add_command(label="New Project", command=lambda: WelcomeWindow.open_new_image_window(self))
        file_menu.add_command(label='Open Project')
        file_menu.add_command(label='Close Project')
        file_menu.add_separator()
        file_menu.add_command(label='Clear Saved Palettes', command=lambda: database_checker.delete_color_records())
        file_menu.add_command(label='My Saved Palettes', command=lambda: open_my_palettes())
        # ad_separator() -- adds a separator line to the menu
        file_menu.add_separator()
        file_menu.add_command(label='Close App', command=lambda: destroyer(self))

        # add_cascade -- creates a new hierarchical menu by associating a given menu to a parent menu
        self.menu_bar.add_cascade(label='File', menu=file_menu)

        edit_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo")
        edit_menu.add_separator()
        edit_menu.add_command(label='Cut')
        edit_menu.add_command(label='Copy')
        edit_menu.add_command(label='Delete Graph')

        # Example of a menu inside another menu
        # edit_menu.add_cascade(label='Edit', menu=file_menu)
        self.menu_bar.add_cascade(label='Edit', menu=edit_menu)

        self.windows_menu = Menu(self.menu_bar, tearoff=0)
        self.windows_menu.add_command(label="Image Toolbar",
                                      command=lambda: self.open_image_toolbar(self.matplotlib_canvas))
        #self.windows_menu.entryconfig(1, state=DISABLED)
        self.windows_menu.add_separator()
        self.windows_menu.add_command(label='Current Palette')

        self.menu_bar.add_cascade(label='Windows', menu=self.windows_menu)
        #
        # Add the menu to the main window
        self.config(menu=self.menu_bar)

    def delete_callback(self, win):
        win.destroy()
        self.img_toolbar = None

    # Opens the matplotlib toolbar for the loaded image graph
    def open_image_toolbar(self, canvas):
        if canvas is not None:
            if self.img_toolbar is None or not self.img_toolbar.winfo_exists():
                # open an attributes windows for the selected text
                self.img_toolbar = ctk.CTk()
                self.img_toolbar.geometry("400x50")
                self.img_toolbar.resizable(False, False)
                self.img_toolbar.attributes('-topmost', True)
                self.img_toolbar.title('Image Toolbar')

                frame = ctk.CTkFrame(master=self.img_toolbar, width=200, height=200, )
                frame.pack()

                toolbar = NavigationToolbar2Tk(canvas, frame)
                toolbar.update()

                self.img_toolbar.protocol("WM_DELETE_WINDOW", lambda: self.delete_callback(self.img_toolbar))
                self.img_toolbar.mainloop()
            else:
                self.img_toolbar.focus()  # if the window exists bring to top
                for item in self.img_toolbar.winfo_children():
                    item.destroy()
                frame = ctk.CTkFrame(master=self.img_toolbar, width=200, height=200, )
                frame.pack()

                toolbar = NavigationToolbar2Tk(self.matplotlib_canvas, frame)
                toolbar.update()
                # self.open_image_toolbar(canvas)
        else:
            tk.messagebox.showerror(title='No Image',message='Please add an image first')

    # plot function for plotting the graph in the tkinter window
    def plot(self, uploaded_img):
        self.state('zoomed')  # maximise the workspace window so as to interact well with the image
        self.image_filename = uploaded_img

        self.image_graph_label.pack_forget()

        plt.clf()  # clears the current image graph
        if uploaded_img is not None:
            # create Matplotlib figure
            fig = Figure(figsize=(7, 7), dpi=100)
            self.fig = fig
            # load image and plot it
            img = mpimg.imread(uploaded_img)
            ax = fig.add_subplot(111)
            ax.axis('off')
            ax.imshow(img)

            # create Matplotlib canvas
            canvas = FigureCanvasTkAgg(fig, master=self.image_graph)
            self.matplotlib_canvas = canvas
            canvas.draw()

            # pack canvas into Tkinter window to fill whole window
            canvas.get_tk_widget().grid(row=0, column=0, columnspan=1, sticky='nsew')
            self.open_image_toolbar(canvas)

            points = fig.ginput(n=5, show_clicks=True, mouse_stop=3)
            for point in points:
                print(f'Point:{point}')

            # clear graph
            def clear_graph():
                for widgets in self.frame.winfo_children():
                    widgets.destroy()

            #self.windows_menu.entryconfig(1, state='normal')  # enable the image toolbar toggle menu

    def get_points(self, filename, fig, selected_canvas=None):

        points = 0
        img = mpimg.imread(filename)
        change_canvas = False
        if str(self) == '.!newworkspace':

            if fig is not None:
                showinfo(
                    title='Information',
                    message='Capture five points from the Image'
                )
                points = fig.ginput(n=5, show_clicks=True, mouse_stop=3)
        else:
            change_canvas = True
            showinfo(
                title='Information',
                message='Pick a point'
            )
            points = fig.ginput(n=1, show_clicks=True, mouse_stop=3)

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

                # using the any() function to check if any element in the list is greater than 1
                if any(i > 1 for i in list_1):
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
            i = 0
            #
            #
            if change_canvas:
                selected_canvas.configure(bg=colors[0])
                selected_canvas.itemconfigure(1, text=f'{colors[0]}')
            else:
                for canvas in self.my_canvases:
                    canvas.configure(bg=colors[i])
                    canvas.itemconfigure(1, text=f'{colors[i]}')
                    i += 1
                i = 0

                showinfo(
                    title='Information',
                    message='Color Palette Generated.'
                )
            '''
            for widgets in frame.winfo_children():
                widgets.destroy()
            '''
            # new_palette = Palette(self.frame)
            # new_palette.generate_palette(colors=colors)
        else:
            showinfo(
                title='Warning',
                message='You did not select any points in the picture. \n'
                        'Select points from the picture again')

    def save_palette(self):
        colors = []
        for canvas in self.my_canvases:
            colors.append(canvas['bg'])
        print(colors)

        my_palette = Palette
        my_palette.save_to_db(colors)

        showinfo(title='Information',
                 message='The Palette has been saved.')

    def clear_palette(self):
        for canvas in self.my_canvases:
            canvas.configure(bg='#808080')
            canvas.itemconfigure(1, text='#808080')

    def delete_images(self):
        path = r'.\assets\my_images\\'
        answer = askyesno(title='Delete Images?',
                          message='Do you really want to delete all images')

        if answer:
            for image_name in os.listdir(path):
                file = path + image_name  # the full path to the file
                if os.path.isfile(file):
                    print('Deleting file: ', file)
                    os.remove(file)
            for widget in self.images_frame.winfo_children():
                widget.destroy()

            showinfo(title='Done!',
                     message=f'Deleted all images from {path}')


# RED # GREEN # BLUE
# Frame containing color setting widgets for RGB Values and HEX
class CanvasAttributesWindow(ctk.CTkToplevel):
    def __init__(self, selected_canvas, fig=None, current_img=None, *args, **kwargs):
        super().__init__(*args, selected_canvas, **kwargs)

        self.canvas = selected_canvas
        self.current_img = current_img
        self.fig = fig
        self.title('Color Attributes')
        self.geometry('300x400')
        self.configure(background="white")
        self.attributes('-topmost', True)
        self.resizable(False, False)

        self.main_frame = ctk.CTkFrame(master=self, fg_color='white', width=250, height=self.winfo_screenheight(),
                                       corner_radius=0)
        self.main_frame.pack()  # holds the various color settings for a canvas

        # RGB Frame
        self.red_frame = ColorSettingFrame(master=self.main_frame)
        self.red_frame.label.configure(text='Red')
        self.red_frame.configure(border_width=0, corner_radius=0)
        self.red_frame.grid(row=0, pady=10, padx=5)
        self.green_frame = ColorSettingFrame(master=self.main_frame)
        self.green_frame.label.configure(text='Green')
        self.green_frame.configure(border_width=0, corner_radius=0)
        self.green_frame.grid(row=1, pady=10, padx=5)
        self.blue_frame = ColorSettingFrame(master=self.main_frame)
        self.blue_frame.label.configure(text='Blue')
        self.blue_frame.configure(border_width=0, corner_radius=0)
        self.blue_frame.grid(row=2, pady=10, padx=5)

        # HEx Frame
        self.hex_frame = CTkFrame(master=self.main_frame, corner_radius=0, border_width=0)
        self.hex_frame.grid(row=3, pady=10, padx=5, ipady=10)
        CTkLabel(master=self.hex_frame, text='HEX', text_color='#fff').grid(row=0, column=0, sticky='e', padx=10)
        self.hex_code = CTkTextbox(master=self.hex_frame, width=100, height=1)
        self.hex_code.grid(row=0, column=1, sticky='w')

        # Opens the askColor() dialog
        def pick_color():
            colors = askcolor(title='Color Chooser', parent=self)
            # self.pick_color_btn.configure(state='disabled')

            r = colors[0][0]
            g = colors[0][1]
            b = colors[0][2]
            print(colors)
            print(r)
            print(g)
            print(b)
            hex_value = colors[1]
            self.red_frame.slider.set(r)
            self.red_frame.entry.insert('0', str(r))
            self.green_frame.slider.set(g)
            self.green_frame.entry.insert('0', str(g))
            self.blue_frame.slider.set(b)
            self.blue_frame.entry.insert('0', str(b))
            self.canvas.configure(bg=f'{hex_value}')
            self.canvas.itemconfigure(1, text=f'{hex_value}')

        self.pick_color_btn = ctk.CTkButton(master=self.main_frame, width=50, height=20, border_width=0,
                                            corner_radius=8,
                                            text="Pick a Color", command=pick_color, state='normal').grid(row=4, pady=5)

        if self.fig is not None:
            ctk.CTkButton(master=self.main_frame, width=100, height=20, border_width=0, corner_radius=8,
                          text="Pick Point from Image", fg_color='grey',
                          command=lambda: NewWorkspace.get_points(self, self.current_img, self.fig, self.canvas)) \
                .grid(row=5, pady=5)

        ctk.CTkButton(master=self.main_frame, width=50, height=20, border_width=0, corner_radius=8,
                      text="OK", command=self.get_color).grid(row=6, pady=10)

    def get_color(self):  # get the color values on button command
        hex_code = self.hex_code.get('0.0', 'end').strip()

        if len(hex_code) != 0:
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_code)

            if match:
                print('Hex is valid', hex_code)
                self.canvas.configure(bg=f'{hex_code}')
                self.canvas.itemconfigure(1, text=f'{hex_code}')
                self.hex_code.delete('0.0', END)
            else:
                showinfo(title='Warning',
                         message='Input valid hex value')
        else:
            r = self.red_frame.slider_value
            g = self.green_frame.slider_value
            b = self.blue_frame.slider_value

            hex_value = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            print(hex_value)
            self.canvas.configure(bg=f'{hex_value}')
            self.canvas.itemconfigure(1, text=f'{hex_value}')


# Opens the Palette Window
def open_my_palettes():
    palette_win = CTk()
    palette_win.title('My Palettes')
    palette_win.geometry('500x400')
    palette_win.resizable(False, False)
    palette_win.iconbitmap('logo.ico')
    palette_win.grid_rowconfigure(0, weight=1)
    palette_win.grid_columnconfigure(0, weight=1)

    palette_frame = ctk.CTkScrollableFrame(master=palette_win, fg_color='transparent', corner_radius=0)
    palette_frame.grid(row=0, column=0, stick='nsew')

    previous_palettes = database_checker.read_color_records()
    for i in range(len(previous_palettes)):
        frame = palette_frames.CreateFrame(master=palette_frame)
        frame.loaded_space = loaded_space
        frame.create_frame(previous_palettes[i])
        frame.pack()

    palette_win.mainloop()


# """MIGHT BE IMPORTANT LATER"""
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
