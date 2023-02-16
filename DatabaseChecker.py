import sqlite3
from tkinter.messagebox import showinfo

try:
    my_connection = sqlite3.connect('palette.db')
    cursor = my_connection.cursor()
except sqlite3.Error as error:
    print("Error", error)


# Delete all records
def delete_color_records():
    cursor.execute("""DELETE FROM My_Palettes""")
    cursor.execute("""DELETE FROM Palette_Colors""")
    my_connection.commit()
    my_connection.close()
    showinfo(
        title="Competed",
        message='Palette Database has been erased'
    )


# Check new records
def check_color_records():
    cursor.execute("""SELECT * FROM My_Palettes""")
    for palette in cursor:
        print(palette)

    cursor.execute("""SELECT * FROM Palette_Colors""")
    for record in cursor:
        print(record)
