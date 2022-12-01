import os
import configparser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyperclip


def ask_attribute(ask_text, ask_type, default=None):
    while True:
        attribute = input(ask_text)

        if ask_type == bool:
            if attribute.lower() in ["y", "true", "yes", "ja"]:
                return True
            elif attribute.lower() in ["n", "false", "no", "nein"]:
                return False
            elif default is not None:
                return default
        if ask_type == int:
            try:
                attribute = int(attribute)
                return attribute
            except ValueError as e:
                if default is not None:
                    return default
                print(f"Please enter a valid {ask_type}.")
        elif ask_type == str:
            if attribute == "":
                if default is not None:
                    return default
                else:
                    print(f"Please enter a not empty {ask_type}.")
            else:
                return attribute
        elif type(attribute) == ask_type:
            return attribute
        elif default is not None:
            return default
        else:
            print(f"Please enter a valid {ask_type}.")


class Config:
    def __init__(self, filename="config.ini"):
        self.file = None
        self.filename = filename
        self.parser = configparser.ConfigParser()

    def open_file(self, mode):
        self.file = open(self.filename, mode)

    def close_file(self):
        self.file.close()

    def get_or_ask_attribute(self, section, attribute, ask_text, ask_type, ask_default=None):
        retrieve = self.get_attribute(section, attribute)

        if not retrieve:
            retrieve = ask_attribute(ask_text, ask_type, ask_default)

            if ask_attribute("Do you want to save this into the config to reuse in the future? [y/N] ", bool, False):
                self.set_attribute(section, attribute, retrieve)

        return retrieve

    def get_or_set_attribute(self, section, attribute, value):
        retrieve = self.get_attribute(section, attribute)

        if not retrieve:
            self.set_attribute(section, attribute, value)

    def get_attribute(self, section, attribute):
        self.parser.read(self.filename)

        try:
            value = self.parser.get(section, attribute)
        except configparser.NoSectionError as e:
            return
        except configparser.NoOptionError as e:
            return
        return value

    def set_attribute(self, section, attribute, value):
        self.open_file("w")

        if not self.parser.has_section(section):
            self.parser.add_section(section)

        self.parser.set(section, attribute, str(value))

        self.parser.write(self.file)
        self.close_file()


def strip(data):
    data_new = []
    for element in data:
        element = element.rstrip().lstrip()
        data_new.append(element)
    return data_new


def write_and_append(file, string, data):
    string += data
    file.write(data)

    return string


def write(file, data):
    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    output_string = ""

    for index, day in enumerate(data):
        if day != ["-"] and day != "" and day != "-":
            output_string = write_and_append(file, output_string, f"{days[index]}: \r\n")
            for activity in day:
                output_string = write_and_append(file, output_string, f"- {activity}\n")
            output_string = write_and_append(file, output_string, "\r\n")
        else:
            print(f"Warning: Day {days[index]} seems to be empty, skipping.")

    return output_string

# Parse the config
config_file_name = "config.ini"

config = Config()

secret_file_name = config.get_or_ask_attribute("config", "secret_file_name", "Please input your secret file name: [client_secret.json] ", str, "client_secret.json")
sheet_name = config.get_or_ask_attribute("config", "sheet_name", "Please input the sheetname: ", str)
user = config.get_or_ask_attribute("config", "user", "Please input the user: [1/2] ", int)
copy_to_clipboard = config.get_or_ask_attribute("config", "copy_to_clipboard", "Do you want to copy the text to clipboard? [y/N]", bool, False)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(secret_file_name, scope)
except FileNotFoundError as e:
    print(f"Secret file \"{secret_file_name}\" was not found, did you spell it right?")
    raise e

client = gspread.authorize(credentials)

sheet_number = ask_attribute("Sheetnumber: ", int)

try:
    sheet = client.open(sheet_name)
    worksheet = sheet.get_worksheet(sheet_number)

    rows = 2
    cols = 5
    week_array = []

    for i in range(0, rows):
        row_array = []

        for j in range(0, cols):
            current_row = i + 2
            current_col = j + 2

            current_data = worksheet.cell(row=current_row, col=current_col).value
            if current_data:
                current_data = strip(current_data.split('/'))
            else:
                current_data = ""

            row_array.append(current_data)

        week_array.append(row_array)
except gspread.exceptions.SpreadsheetNotFound as e:
    print(f"Sheet \"{sheet_name}\" was not found, did you spell it right?")
    raise e
except gspread.exceptions.WorksheetNotFound as e:
    print(f"Worksheet with the number \"{sheet_number}\" was not found, does that sheet exist?")
    raise e

output_file = open("output.txt", "w+")
output_data = write(output_file, week_array[int(user) - 1])
output_file.close()

print("File succesfully created (output.txt)")

if copy_to_clipboard:
    pyperclip.copy(output_data)

    print("The text was copied to your clipboard!")


