import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("/home/swaraj/Documents/Python Stuff/Habit Tracker/client_secret.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Habit Tracker").sheet1

def find_next_empty_row():
    str_list = list(filter(None, sheet.col_values(1)))  # Get all values in column A
    return len(str_list) + 1

#insert the values passed in as parameter to the google spreadsheet:
def update_sheet(values):
    sheet.insert_row(values, find_next_empty_row())

#just trying out different ways to access data in the google spreadsheet:

#retrieving data:
#print(sheet.get_all_records())
#print(sheet.row_values(1)) #seems like the first index of the sheet is 1, not 0 like normal
#print(sheet.cell(2, 1).value)

#inserting data:
#sheet.insert_row(["2/2/2020", "This is my SECOND GOAL", "I did this much work on my second day", "2 hours", "No", "These are my future improvements for my second day", "These were the distractions on the second day"], 3)

#deleting data
#sheet.delete_rows(3)

#updating data
#sheet.update_cell(2, 2, "This is my first goal, UPDATED!")

#finding value:
# cell = sheet.find("This is my first goal, UPDATED!")
# print(cell.value)
# print(cell.row)
# print(cell.col)


