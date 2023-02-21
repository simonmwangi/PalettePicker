import sqlite3
from tkinter.messagebox import showinfo

try:
    my_connection = sqlite3.connect('palette.db')
    cursor = my_connection.cursor()
except sqlite3.Error as error:
    print("Error", error)


# Read from the database and insert palette records to a dictionary
def read_color_records():
    palettes_view = "SELECT palette_name,created_date,no_of_colors," \
                    "Palette_Colors.color_id_1,Palette_Colors.color_id_2,Palette_Colors.color_id_3," \
                    "Palette_Colors.color_id_4,Palette_Colors.color_id_5,Palette_Colors.color_id_6," \
                    "Palette_Colors.color_id_7,Palette_Colors.color_id_8,Palette_Colors.color_id_9," \
                    "Palette_Colors.color_id_10 FROM My_Palettes JOIN Palette_Colors ON Palette_Colors.palette_id =" \
                    "My_Palettes.palette_id"
    cursor.execute(palettes_view)

    rows = cursor.fetchall()  # Fetch all rows from the JOIN query

    palette_dict = {}  # To hold the rows from the JOIN query with a unique key
    for i, row in enumerate(rows):
        palette_dict[i] = list(row)

    return palette_dict


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


def get_row_count():
    cursor.execute("SELECT COUNT(*) FROM My_Palettes")
    row_numbers = list(cursor)
    return row_numbers[0][0]


# Check new records
def check_color_records():
    cursor.execute("""SELECT * FROM My_Palettes""")
    for palette in cursor:
        print(palette)

    cursor.execute("""SELECT * FROM Palette_Colors""")
    for record in cursor:
        print(record)


# Update color and palette records
# For now it is only used for updating the palette name to the My_Palettes table
def update_records(record_no, changed_text, previous_text):
    cursor.execute(f"UPDATE My_Palettes SET palette_name = '{changed_text}' WHERE palette_no = {record_no}")
    my_connection.commit()
    showinfo(
        title="Competed",
        message='Palette Name has been changed'
    )

############# To Test the SQL Queries
# check_color_records()
# print(read_color_records())
# delete_color_records()
# get_row_count()
