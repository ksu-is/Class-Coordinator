import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

def browse_file(entry_var):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        # Set the selected file path in the corresponding entry field
        entry_var.set(file_path)

window = tkinter.Tk()
window.title("Course Entry Form")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="Course Entry")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

file_path_label=tkinter.Label(user_info_frame, text="File Path")
file_path_label.grid(row=0 , column=1)

# Create entry fields and browse buttons up to 5
for i in range(1, 6):
    label = tkinter.Label(user_info_frame, text=str(i))
    label.grid(row=i, column=0)

    entry_var = tkinter.StringVar()
    entry = tkinter.Entry(user_info_frame, textvariable=entry_var)
    entry.grid(row=i, column=1)

    browse_button = tkinter.Button(user_info_frame, text="Browse", command=lambda entry_var=entry_var: browse_file(entry_var))
    browse_button.grid(row=i, column=2, pady=5)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button
button = tkinter.Button(frame, text="Import Files", command=lambda: None)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
