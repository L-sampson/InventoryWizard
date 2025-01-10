from tkinter import *
import tkinter.font as tkFont

root = Tk()
root.title("Inventory File Wizard")
root.config(bg="skyblue")
root.geometry("500x500")

main_frame = Frame(root, bg="skyblue")
main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)

tool_bar = Frame(main_frame, bg="#f9f9f9")
tool_bar.pack(expand=True, fill=BOTH, padx=1, pady=1)
font_style = tkFont.Font(family="Helvetica", size=16, weight="bold")
Label(tool_bar, text="Select Inventory File(s) to Convert", font=font_style, bg="#f9f9f9").pack(pady=5)

drop_zone = Frame(tool_bar, width=250, height=250, bg="purple", borderwidth=2, relief="groove")
drop_zone.pack(padx=5, pady=5)


file_entry_frame = Frame(tool_bar, bg="white")
file_entry_frame.pack(pady=5)
file_entry_label = Label(tool_bar,text="File:", font=('calibre', 10, 'bold'))
file_entry = Entry(tool_bar, font=('calibre', 10, 'normal'), width=40)
import_file_btn = Button(tool_bar, text="Import File", width=10, height=1)

file_entry_label.pack(side=LEFT, padx=5, pady=10)
file_entry.pack(side=LEFT, padx=5, pady=10)
import_file_btn.pack(side=RIGHT, padx=5, pady=5)

root.mainloop()
