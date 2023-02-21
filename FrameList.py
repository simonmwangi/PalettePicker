import tkinter as tk

import DatabaseChecker


class FrameList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.palette_texts = []
        self.colors_dict = {}
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.frame_container = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame_container, anchor="nw")
        self.frame_container.bind("<Configure>", self._on_frame_container_configure)

    def create_frames(self, colors):
        root = self.frame_container
        self.colors_dict = colors

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
            tk.Frame(self.frame_container, height=1, bg="gray").pack(fill="x", padx=10, pady=10)

        for widget, text in self.palette_texts:
            print("The following: {text}")
            widget.bind("<Return>", self.on_text_changed)

    # Wait for user Return key input and updates the palette name with the new value and also in the database record
    def on_text_changed(self, event):
        i = 0   # Used in updating the records
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


test_obj = ('\n'
            'def main():\n'
            '    root = tk.Tk()\n'
            '    root.title("Frame List Example")\n'
            '    root.geometry("400x400")\n'
            '\n'
            '    # create the FrameList widget and pack it into the root window\n'
            '    frame_list = FrameList(root)\n'
            '    frame_list.create_frames()\n'
            '    frame_list.pack(fill="both", expand=True, padx=20, pady=20)\n'
            '\n'
            '    root.mainloop()\n'
            '\n'
            '\n'
            'if __name__ == \'__main__\':\n'
            '    main()\n')
