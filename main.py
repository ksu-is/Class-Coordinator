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
import json
import re

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] ='Enter API KEY HERE'
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
    #Check status of assistant run. Wait for status is complete
    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        if run.status == "completed" or run.status == "failed":
            break
        
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )      
    #extract_data(messages.model_dump_json())
    data_string = json.dumps(messages.model_dump_json())
    #extract_assignments_dates(data_string)
    #print(data_string)
#def extract_assignments_dates(json_data):
    response_dict = json.loads(data_string)
    # Extract the assistant's message, which presumably contains the assignments and due dates
    # The assistant's response seems to be the first item in the 'data' list
    assistant_message = response_dict["data"][0]["content"][0]["text"]["value"]

    # Replace unnecessary characters and split the string into lines for easier processing
    formatted_text = assistant_message.replace("\\n", "\n").replace("\\\"", "\"")
    lines = formatted_text.split('\n')

    # Initialize variables to hold semester/year and the list of assignments with due dates
    semester_year = "Unknown"  # placeholder in case the semester/year can't be determined
    assignments = []

    # Extract the semester/year and assignments from the formatted lines
    for line in lines:
        if "The semester and year of the syllabus are" in line:
            semester_year = line.split("are ")[1].rstrip(".")
        elif "**Assignment name:" in line:
            assignment_info = line.split("**Assignment name: ")[1].rstrip("**")
            due_date_line = lines[lines.index(line) + 1]  # Due date is on the next line
            due_date = due_date_line.split(": ")[1]
            assignments.append((assignment_info, due_date))

    # Display extracted information

    for assignment, due_date in assignments:
        print(assignment,due_date)





    #assignments = []
    #dates = []
    #for item in data_string['data']:
        #content = item.get('content', [{}])[0].get('text', {}).get('value', '')
        #matches = re.findall(r'- \*\*Assignment name: (.*?)\*\*\\n\s+- Due date: (\d{4}-\d{2}-\d{2})', content)
        #for match in matches:
            #assignments.append(match[0])
            #dates.append(match[1])
            #gcalendar.add_calendar_event(match[0],match[1])
            #gsheets.add_assignment(match[0],match[1])
        #return assignments, dates




# Example usage:
#your_json_data = "{\"data\":[{ ... (your JSON data here) ... }]}"
#extracted_assignments, extracted_dates = extract_assignments_dates(your_json_data)

#for assignment, date in zip(extracted_assignments, extracted_dates):
    #print(f"Assignment: {assignment.strip()}, Date: {date}")

    #print(messages.model_dump_json)
    # Extract the last message, which we'll assume contains our relevant data.
    #extraction_message = messages.data[-1].content
    #split into individual lines
    
    
    #assignments=[]
    #dates=[]

    #for line in extraction_message:
        #if line:  # Check if the line is not empty
        # Split each line into assignment and date, and strip whitespace
            #assignment, date = line.split(', ')
            #assignments.append(assignment.strip())
            #dates.append(date.strip())  
# Now, we parse the extracted message which contains the assignments and dates.
# This parsing would depend on the actual format of `extraction_message`. Assuming it's a string with lines like "Assignment name, YYYY-MM-DD".
# Loop through and add each assignment to the calendar and Google Sheets
    #for assignment, date in zip(assignments, dates):
        #gcalendar.add_calendar_event(assignment, date)
        #gsheets.add_assignment(assignment, date)
    #print(messages)
# Example usage
    #gcalendar.add_calendar_event("P2M5","2023-12-10")
    #gsheets.add_assignment("P2M5","2023-12-10")

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

