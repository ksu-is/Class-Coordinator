import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pdfplumber
import openai

open.ai_api_key= 'Placeholder'

def browse_file(entry_var):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        # Set the selected file path in the corresponding entry field
        entry_var.set(file_path)
#Read the text
def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        #read the text
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text()
        return text_content
#Read the pdf
def analyze_pdf(file_path):
    #read the pdf
    pdf_text=read_pdf(file_path)

window = tkinter.Tk()
window.title("Course Entry Form")

frame = tkinter.Frame(window)
frame.pack()

user_info_frame = tkinter.LabelFrame(frame, text="Course PDF")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

file_path_label=tkinter.Label(user_info_frame, text="File Path")
file_path_label.grid(row=0 , column=1)

label = tkinter.Label(user_info_frame, text="Course")
label.grid(row=1, column=0)

entry_var = tkinter.StringVar()
entry = tkinter.Entry(user_info_frame, textvariable=entry_var)
entry.grid(row=1, column=1)

browse_button = tkinter.Button(user_info_frame, text="Browse", command=lambda entry_var=entry_var: browse_file(entry_var))
browse_button.grid(row=1, column=2, pady=5)

courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)
#Get the file path
def import_files():
    #Get the file path
    file_path = entry_var.get()
    if file_path:
        analyze_pdf(file_path)
        
# Button
button = tkinter.Button(frame, text="Import Files", command=import_files)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
