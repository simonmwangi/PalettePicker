import tkinter as tk
import customtkinter as ctk

import database_checker
import app_windows

'''
class FrameList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.palette_texts = []
        self.colors_dict = {}
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.frame_container = tk.Frame(self.canvas)
        self.load_workspace = None
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame_container, anchor="nw")
        self.frame_container.bind("<Configure>", self._on_frame_container_configure)

    def create_frames(self, colors):
        root = self.frame_container
        self.colors_dict = colors
        print(self.colors_dict)
        self.palette_num = 0
        for record in self.colors_dict:

            records = self.colors_dict[record]
            palette_name = records[0]
            palette_created_date = records[1]
            palette_saved_colors = records[3:10]

            # Frame container to hold the palette details including the colors in the palette
            frame = tk.Canvas(root, bg="white", width=400, height=100)
            palette_name_text = tk.Text(master=self.frame_container, height=2, state=tk.NORMAL,
                                        font=("Helvetica", 12, "bold"))
            # palette_name_text.insert(tk.END, palette_name)
            palette_name_text.insert('1.0', palette_name)
            palette_name_text.pack()

            self.palette_texts.append([palette_name_text, palette_name])

            tk.Label(master=self.frame_container, text="Created date: {}".format(palette_created_date),
                     font=("Helvetica", 12, "bold")).pack()

            for i, rectangle in enumerate(palette_saved_colors):
                print(i)
                if rectangle != 'None':
                    frame.create_rectangle(30 + (i * 50), 10, 80 + (i * 50), 80, fill=rectangle)
                    frame.create_text(50 + (i * 50), 90, text=rectangle, fill='black', font='Helvetica 8')
                else:
                    break
            frame.pack(fill="both", expand=True)

            def load_palette(btn):
                num = btn.cget('textvariable')
                print('The palette num is: ', num)
                colors_dict = self.colors_dict[num - 1]
                colors_to_load = colors_dict[3:10]

                print(colors_to_load)
                self.parent.destroy()  # Destroys the palette window before loading the selected palette
                if self.load_workspace is None:
                    self.load_workspace = app_windows.NewWorkspace()
                    app_windows.NewWorkspace.load_palette(self.load_workspace, colors_to_load)
                else:
                    app_windows.NewWorkspace.load_palette(self.load_workspace, palette_saved_colors)

            ctk.CTkButton(master=self.frame_container, width=25, height=1, text=f'Load Palette_{self.palette_num} to Workspace',
                                 textvariable={self.palette_num}, command=lambda: load_palette()).pack(pady=10)

            tk.Frame(self.frame_container, height=1, bg="gray").pack(fill="x", padx=10, pady=10)

            self.palette_num += 1
            print('Check', self.palette_num)

        for widget, text in self.palette_texts:
            print("The following: {text}")
            widget.bind("<Return>", self.on_text_changed)

    # Wait for user Return key input and updates the palette name with the new value and also in the database record
    def on_text_changed(self, event):
        i = 0  # Used in updating the records
        # WIll be changed later on with more security
        for widget, previous_text in self.palette_texts:
            i += 1
            if event.widget == widget:
                new_text = widget.get(1.0, tk.END).strip()
                print(f"The extracted text is: {new_text}")
                DatabaseChecker.update_records(i, new_text, previous_text)
                break

    def _on_frame_container_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
'''


class CreateFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.loaded_space = None
        self.count_id = None
        self.palettes = None
        self.palette_saved_colors = None

    def create_frame(self, palette=None):
        self.palettes = palette

        print('********')
        palette_name = self.palettes[0]
        print(palette_name)
        palette_created_date = self.palettes[1]
        print(palette_created_date)
        self.palette_saved_colors = self.palettes[3:10]
        print(self.palette_saved_colors)
        print('********')

        # Frame container to hold the palette details including the colors in the palette
        frame = tk.Canvas(self, bg="white", width=400, height=100)
        palette_name_text = tk.Text(master=self, height=2, state=tk.NORMAL,
                                    font=("Helvetica", 12, "bold"))
        # palette_name_text.insert(tk.END, palette_name)
        palette_name_text.insert('1.0', palette_name)
        palette_name_text.pack()

        # self.palette_texts.append([palette_name_text, palette_name])

        tk.Label(master=self, text="Created date: {}".format(palette_created_date),
                 font=("Helvetica", 12, "bold")).pack(pady=10)

        for i, rectangle in enumerate(self.palette_saved_colors):
            print(i)
            if rectangle != 'None':
                frame.create_rectangle(30 + (i * 50), 10, 80 + (i * 50), 80, fill=rectangle)
                frame.create_text(50 + (i * 50), 90, text=rectangle, fill='black', font='Helvetica 8')
            else:
                break
            frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkButton(self, text='Load Palette to Workspace', width=100, height=10, command=self.print_palette).pack(
            pady=10)
        tk.Frame(self, height=1, bg="gray").pack(fill="x", padx=10, pady=10)

    def print_palette(self):
        print(self.palette_saved_colors)
        # TODO Find a way to load a workspace

        # space = loaded_space
        if self.loaded_space is None:
            self.loaded_space = app_windows.NewWorkspace()
            app_windows.NewWorkspace.load_palette(self.loaded_space, self.palette_saved_colors)
        else:
            self.loaded_space.focus()
            app_windows.NewWorkspace.load_palette(self.loaded_space, self.palette_saved_colors)
