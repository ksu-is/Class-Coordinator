# Project Roadmap
- [X] Create README.md
- [X] Review the following files
  - [X]   tkinter-data-entry
  - [X]   assignment_tracker
- [X] Test both files above
- [X] Use tkinter-data-entry as a base code
- [X] Code Updates: Wording Improvements
	- [X] Change “Enter Data” to “Import File”
 	- [X] Change “Data Entry Form” to “Course Entry Form”
 	- [X] Change “User Information” to “Course Entry”
 - [ ] Build Path:
 	- [X] Prompt user to enter PDF
 	- [X] Create OpenAI API Assistant
 		- [X] Enter PDF
   		- [X] Tell the Assistant "I need the list of all assignments and due dates"
     		- [ ] Organize Assistant response to fit the format "assignment name, YYYY-MM-DD"
       		- [X] Copy the output from the assistant and enter that manually as the data_string variable (only if the above task doesn't work)
	- [X] Create Google Calendar API to link to a new or existing Calendar (GCalendar.py)
 		- [X] Test with simple data and check if the calendar is linked by running GCalendar.py
		- [X] Call Google Calendar in the main.py code to enter information extracted by the Assistant
		- [X] Check Google Calendar for updated events
  	- [X] Create a Google Sheets API to create an info Sheet (Gsheets.py)
   		- [X] Test Gsheets.py with simple data, ensure that assignments and dates are listed and organized
		- [X] Call Gsheets.py in the main.py code to enter the information extracted by the Assistant
   		- [X] Check Google sheet for updated data
     	
  
