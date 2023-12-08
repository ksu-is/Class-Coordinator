from sys import thread_info
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pdfplumber
from openai import OpenAI
import os
import time
import gcalendar
import gsheets

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] ='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'
client= OpenAI()

def run_assistant(pdf_file):
 # Upload a file with an "assistants" purpose
    file = client.files.create(
    file=open(pdf_file, "rb"),
    purpose='assistants'
    )

    # Add the file to the assistant
    assistant = client.beta.assistants.create(
    instructions="You can read a course syllabus.",
    model="gpt-4-1106-preview",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id]
    )
    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": "First, I need the semester/year of this syllabus. Then, I need a list of all assignments and due dates from the syllabus. Date format needs to be YYYY-MM-DD, assuming all of the assignments are in the same year as the syllabus. Ex: 'Assignment name, YYYY-MM-DD'",
        "file_ids": [file.id]
        }
    ]
    )
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    )
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
    #time.sleep(60)
    #print(messages.data)
# Example usage
    gcalendar.add_calendar_event("P2M5","2023-12-10")
    gsheets.add_assignment("P2M5","2023-12-10")

def analyze_pdf(file_path):
    # Read the PDF
    #pdf_text = read_pdf(file_path)

    # Use OpenAI to extract information (replace 'your-model' with the appropriate model name)
    response = openai.completions.create(
        model="text-davinci-003",  # Choose the engine you want to use
        prompt="Here is the syllabus text: Schedule See the section titled Course Locations and Timing to know on which dates there are in-class sessions. All actual due dates are posted in D2L. Some items listed here are earlier and prompt you to get moving and are relative to when they are actually due in D2L, which might be a day or more later. ALL in-person session dates for the hybrid section are teal and bold. Aug 14: Get code and Use it: Application Development = Coding + Management, VideoQuiz1: Watch the intro video. - setup Python and Teams, Ex1. Turn in IDLE screenshot; Monday Aug 18: Get code and Use. \n\n Question: Show me the assignment names and the days they are due, formatted with Assignents and dates as two columns",

        #prompt= "What class is this?",
        max_tokens=1000  # Adjust as needed based on your text length
    )
    #response = openai.completions.create(
        #model="text-davinci-003",  # Choose the engine you want to use
        #prompt="Hello my name is zach and this is sample text. August 28th Test 4. IS 3020: Application Development",
        #prompt= "Show me the assignment names and the days they are due",
        #max_tokens=4000  # Adjust as needed based on your text length
    #)
    # Extract information from OpenAI response (modify as per your use case)
    #extracted_info = response['choices'][0]['text']

    # Display or process the extracted information
    print(response.choices[0].text.strip())

def browse_file(entry_var):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        # Set the selected file path in the corresponding entry field
        entry_var.set(file_path)

def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        #read the text
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text()
        
        return text_content
    
window = tkinter.Tk()
window.title("PDF Reader")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="Course PDF")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

file_path_label=tkinter.Label(user_info_frame, text="File Path")
file_path_label.grid(row=0 , column=1)

# Create entry fields and browse buttons up to 5

label = tkinter.Label(user_info_frame, text="Course")
label.grid(row=1, column=0)

entry_var = tkinter.StringVar()
entry = tkinter.Entry(user_info_frame, textvariable=entry_var)
entry.grid(row=1, column=1)

browse_button = tkinter.Button(user_info_frame, text="Browse", command=lambda entry_var=entry_var: browse_file(entry_var))
browse_button.grid(row=1, column=2, pady=5)

# Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

def import_files():
    #Get the file path
    file_path = entry_var.get()
    if file_path:
        run_assistant(file_path)
        

# Button
button = tkinter.Button(frame, text="Read PDF", command=import_files)
button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

window.mainloop()


