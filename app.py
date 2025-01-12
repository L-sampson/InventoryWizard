from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import os
import re
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
from typing import List
from inventory_converter import InventoryConverter

# Root Window of Application
root = TkinterDnD.Tk()
root.title("Inventory File Wizard")
root.iconbitmap("assets/inspired-logo.ico")
root.config(bg="#0077C8")
root.geometry("500x500")
root.resizable(False, False)

def drop_files(event):
    print(f"Original event data: {event.data}")
    allowed_extensions = {'.xlsx', '.xlsm', '.xls', '.csv'}

    # Extract all paths using a regex
    # TODO: Review regex patterns
    file_paths = re.findall(r'{[^}]+}|[^\s]+', event.data)
    print(f"File paths after regex findall: {file_paths}")
    file_paths = [path.strip('{}') for path in file_paths]  # Remove curly braces if present
    print(f"File paths after stripping curly braces: {file_paths}")

    invalid_files = []
    for file_path in file_paths:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension in allowed_extensions:
            file_listbox.insert(END, file_path)
        else:
            invalid_files.append(file_path)

    # Show an error message if there are invalid files
    if invalid_files:
        invalid_files_str = '\n'.join(invalid_files)
        msg.showerror(
            "Invalid File Type",
            f"The following files are not accepted types:\n{invalid_files_str}"
        )

# Import files dialog
def select_files() -> int:
    filetypes = (
        ('Excel Files', '*.xlsx;*xlsm;*.xls'),
        ('CSV Files', '*.csv')
    )
    files = fd.askopenfilenames(title='Open files',
                            initialdir='/Downloads',
                            filetypes=filetypes)
    
    file_listbox.delete(0, END)

    for file in files:
        file_listbox.insert(END, file)
    file_count = file_listbox.size()
    msg.showinfo("Number of Files", f"You selected {file_count} file(s).")
    return file_count

def save_files(files: List[str]):
    save_directory = fd.askdirectory(title='Select Directory to Save Files')
    if save_directory:
        converter = InventoryConverter(files)
        converter.convert_files(save_directory)
        msg.showinfo("Conversion Complete", f"Files have been saved to {save_directory}")
    else:
        msg.showerror("No Directory Selected", "Please select a directory to save the files.")

def remove_files():
    file_count = file_listbox.size()
    if file_count > 0:
        confirm = msg.askyesno("Remove files", f"Would you like to remove {file_count} files from conversion?")
        if confirm:
            msg.showinfo("Removed Files", f"Removed {file_count} file!")
            file_listbox.delete(0, END)
    else:
        msg.showerror("Empty Files List", "No files are pending conversion")    
    
def convert_files():
    file_count = file_listbox.size()
    
    if file_count == 0:
        msg.showerror("No Files","No files to convert. Please select files first")
    else:
        confirm = msg.askokcancel("Convert Files", f"Do you want to convert {file_count} file(s)?")
        if confirm:
            msg.showinfo("Proceeding", "Proceeding to convert the files...")
            files = list(file_listbox.get(0, END))
            save_files(files)
            
header = Frame(root, bg="#0077C8", height=100)
header.pack(fill=X)
image = Image.open("assets/inspiredu_logo.png")
resized_logo = image.resize((25, 25))
photo = ImageTk.PhotoImage(resized_logo)

title_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
title_label = Label(header, image=photo, text="Inventory File Wizard", font=title_font, bg="#0077C8", fg="white", compound=LEFT)
title_label.pack(pady=10)

main_frame = Frame(root, bg="skyblue")
main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)


tool_bar = Frame(main_frame, bg="white")
tool_bar.pack(expand=True, fill=BOTH, padx=1, pady=1)
font_style = tkFont.Font(family="Helvetica", size=16, weight="bold")

drop_image = Image.open("assets/file-upload.png")
resized = drop_image.resize((50, 50))
upload_logo = ImageTk.PhotoImage(resized)

drop_zone = Frame(tool_bar, bg="white", highlightbackground="#0077C8", highlightthickness=2, height=200, width=400)
drop_zone.pack(pady=20)
drop_zone.drop_target_register(DND_FILES)
drop_zone.dnd_bind('<<Drop>>', drop_files)

drop_logo = Label(drop_zone, image=upload_logo, bg="white")
drop_logo.pack(pady=10)

drop_text = Label(drop_zone, text="Drop files here\n\nSupported file types:\n'.xlsx', '.xlsm', '.xls', '.csv'", font=('Helvetica', 12, 'bold'), bg="white")
drop_text.pack()


file_entry_frame = Frame(tool_bar, bg="white")
file_entry_frame.pack(fill=X, padx=20, pady=10)

file_entry_label = Label(file_entry_frame,text="Select Files to be Converted: ", font=('Arial', 12, 'bold'), bg="white")
file_entry_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
import_file_btn = Button(file_entry_frame, text="Import File(s)", width=15, height=1, command=select_files, bg="#0077C8", fg="white", font=button_font)
import_file_btn.grid(row=0, column=1, padx=5, pady=5, sticky=W)
file_listbox = Listbox(file_entry_frame, width=60, height=5, font=("Arial", 10, "italic"), bd=2, relief="groove")

# Button Section
button_frame = Frame(tool_bar, bg="white")
button_frame.pack(pady=1)

button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
remove_btn = Button(button_frame, text="Remove Files(s)", width=15, height=1, bg="#FE0944", font=button_font, fg="white", command=remove_files)
remove_btn.grid(row=0, column=0, padx=10)

convert_file_btn = Button(button_frame, text="Convert File(s)", width=15, height=1, command=convert_files, bg="#00B28F", fg="white", font=button_font)
convert_file_btn.grid(row=0, column=1, padx=10)

file_entry_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
file_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=W+E)

root.mainloop()