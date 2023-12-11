from sys import thread_info
import tkinter
from tkinter import filedialog
from openai import OpenAI
import os
import gcalendar
import gsheets
import json


# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] ='ENTER API KEY HERE'
client= OpenAI()

def run_assistant(pdf_file):
 # Upload a file that the assistant will read
    file = client.files.create(
    file=open(pdf_file, "rb"),
    purpose='assistants'
    )

    # Add the file to the assistant
    #Enter the GPT model and what the purpose of the asistant is
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
    #data_string = messages.model_dump_json()
    #^^^^^^ This is the code that I cannot get to work correctly. The output of this code is below as data_string (For the IS3020 Syllabus). There is an problem when I try to parse the data. 
    data_string = """
    {
    \"data\":[{\"id\":\"msg_rvcPR5GWSt7HptgVERh3YIA5\",\"assistant_id\":\"asst_grSrhz0V8afBAiWBFfoN8NlB\",\"content\":[{\"text\":{\"annotations\":[],\"value\":\"The semester and year of the syllabus are Fall 2023, as stated in the document title \\\"IS 3020 Syllabus Fa23 Sample\\\"\u301016\u2020source\u3011. The due dates and assignments listed in the syllabus are as follows:\\n\\n- **Assignment name: Ex1. Turn in IDLE screenshot**\\n  - Due date: 2023-08-14\\n- **Assignment name: Ex2. Intro in Teams; VideoQuiz2; VideoQuiz3**\\n  - Due date: 2023-08-18\\n- **Assignment name: Ex3. Hack GradeTracker.py; VideoQuiz4**\\n  - Due date: 2023-08-21\\n- **Assignment name: Ex4. TacoCopter**\\n  - Due date: 2023-08-25\\n- **Assignment name: Ex5. Conveyor Sushi; Modeling Quiz in D2L**\\n  - Due date: 2023-08-28\\n- **Assignment name: VideoQuiz5**\\n  - Due date: 2023-09-05\\n- **Assignment name: Complete P1M1 - post questions; Complete P1 Quiz 1**\\n  - Due date: 2023-09-11\\n- **Assignment name: Complete P1 Quiz 2**\\n  - Due date: 2023-09-18\\n- **Assignment name: Turn in Code Demo 1 CalcGUI**\\n  - Due date: 2023-09-22\\n- **Assignment name: Complete P1M3 - post questions; Complete P1 Quiz 3**\\n  - Due date: 2023-09-25\\n- **Assignment name: Complete P1M4 - post questions; Complete P1 Quiz 4**\\n  - Due date: 2023-09-29\\n- **Assignment name: Submit P1M5; Complete P2M1; Complete P2 Quiz 1**\\n  - Due date: 2023-10-02\\n- **Assignment name: Watch Project Demo: Flask Webpage Walkthrough**\\n  - Due date: 2023-10-09\\n- **Assignment name: Complete P2M2 - post questions; Complete P2 Quiz 2**\\n  - Due date: 2023-10-16\\n- **Assignment name: Turn in Code Demo 2 Webpage with Flask; Complete P2M3; Complete P2 Quiz 3**\\n  - Due date: 2023-10-23\\n- **Assignment name: Complete P2M4 - post questions; Complete P2 Quiz 4; Turn in Project Idea Ex6**\\n  - Due date: 2023-10-30\\n- **Assignment name: Do final coding evaluation; Submit P2M5; Prepare for projects**\\n  - Due date: 2023-10-31\\n- **Assignment name: Ensure everyone is started and has themselves setup**\\n  - Due date: 2023-11-06\\n- **Assignment name: Setup your Github repository; Update documents in Github**\\n  - Due date: 2023-11-12\\n- **Assignment name: Complete the Sprint 1 Review and Log in D2L**\\n  - Due date: 2023-11-13\\n- **Assignment name: Complete the Sprint 2 Review and Log in D2L**\\n  - Due date: 2023-11-21\\n- **Assignment name: Test and edit your code; Update the project roadmap**\\n  - Due date: 2023-11-27\\n- **Assignment name: Complete Sprint 3; Design and Turn in your PPT marketing slide**\\n  - Due date: 2023-12-04\\n- **Assignment name: Schedule your Presentation; Present and record it**\\n  - Due date: 2023-12-05\\n\\nPlease note that some assignments might have additional due dates associated with them, which can be adequately informed by reviewing the detailed syllabus document.\"},\"type\":\"text\"}],\"created_at\":1702158519,\"file_ids\":[],\"metadata\":{},\"object\":\"thread.message\",\"role\":\"assistant\",\"run_id\":\"run_argXbf1L13slCy0QqKXNQ313\",\"thread_id\":\"thread_X4jUL0fTKTevl4s2K4JuTTCz\"},{\"id\":\"msg_grGRNM2mxdhuJgx0PaQ5gf2o\",\"assistant_id\":null,\"content\":[{\"text\":{\"annotations\":[],\"value\":\"First, I need the semester/year of this syllabus. Then, I need a list of all assignments and due dates from the syllabus. Date format needs to be YYYY-MM-DD, assuming all of the assignments are in the same year as the syllabus. Ex: 'Assignment name, YYYY-MM-DD'\"},\"type\":\"text\"}],\"created_at\":1702158496,\"file_ids\":[\"file-BRG9sVDlqdUHWjnnwHFAyZUM\"],\"metadata\":{},\"object\":\"thread.message\",\"role\":\"user\",\"run_id\":null,\"thread_id\":\"thread_X4jUL0fTKTevl4s2K4JuTTCz\"}],\"object\":\"list\",\"first_id\":\"msg_rvcPR5GWSt7HptgVERh3YIA5\",\"last_id\":\"msg_grGRNM2mxdhuJgx0PaQ5gf2o\",\"has_more\":false
    }
    """

    response_dict = json.loads(data_string)
    # Extract the assistant's message, which presumably contains the assignments and due dates
    # The assistant's response seems to be the first item in the 'data' list
    assistant_message = response_dict["data"][0]["content"][0]["text"]["value"]

    # Replace unnecessary characters and split the string into lines for easier processing
    formatted_text = assistant_message.replace("\\n", "\n").replace("\\\"", "\"")
    lines = formatted_text.split('\n')

    # Initialize variables to hold semester/year and the list of assignments with due dates
    assignments = []

    # Extract the assignments from the formatted lines
    for line in lines:
        if "**Assignment name:" in line:
            assignment_info = line.split("**Assignment name: ")[1].rstrip("**")
            due_date_line = lines[lines.index(line) + 1]  # Due date is on the next line
            due_date = due_date_line.split(": ")[1]
            assignments.append((assignment_info, due_date))

    # Display extracted information
    #Call gcalendar.py and gsheets.py functions that enter the following into the right places
    #Prints the results to double check the info is correct
    for assignment, due_date in assignments:
        print(assignment,due_date)
        gcalendar.add_calendar_event(assignment,due_date)
        gsheets.add_assignment(assignment,due_date)

def browse_file(entry_var):
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    if file_path:
        # Set the selected file path in the corresponding entry field
        entry_var.set(file_path)

window = tkinter.Tk()
window.title("PDF Reader")

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

def import_files():
    #Get the file path
    file_path = entry_var.get()
    if file_path:
        run_assistant(file_path)
        
# Read PDF Button
button = tkinter.Button(frame, text="Read PDF", command=import_files)
button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
