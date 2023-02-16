# image_viewer.py

import io
import os
import PySimpleGUI as sg
from PIL import Image
import pyautogui


file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

def main():
    global img
    layout = [
        [sg.Image(key="-IMAGE-")],
        [sg.Text("Image File")],
        [
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
            sg.Button("Get Colors"),
        ],
    ]

    window = sg.Window("Image Viewer", layout)

    while True:

        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                max_colors = 100000000
                #print(image.getcolors(image.size[0]*image.size[1]))
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

        if event == "Get Colors":
            currentMouseX, currentMouseY = pyautogui.position()
            print(f"The current locations is {currentMouseX}, {currentMouseY}")


    window.close()


if __name__ == "__main__":
    main()