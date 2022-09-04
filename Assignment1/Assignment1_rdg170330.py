import sys
import os
import re
import pickle
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords


class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("\nEmployee id: ", self.id)
        print("\t", self.first, self.mi, self.last)
        print("\t", self.phone)


def process_text(text_from_file):
    """
    Processes the text from the input file ("data.csv")
    :param text_from_file: The text from the input file ("data.csv")
    :return employee_dict: Returns a dictionary of employees (employees are created via the Person class)
    """
    # Remove the first line from the text because that's just the heading
    text_without_heading = text_from_file[45:]

    # Split on commas to get the different fields
    new_text = re.split(',|\n', text_without_heading)

    # Dictionary of employees
    employee_dict = {}

    # List for employee IDs
    employee_id_list = []

    for i in range(0, 25, 5):
        # Get the elements in the list that correspond to the way we initialize the Person class
        # (i.e., (last, first, mi, id, phone)
        new_text[i + 0] = new_text[i + 0].capitalize()  # Last name
        new_text[i + 1] = new_text[i + 1].capitalize()  # First name

        new_text[i + 2] = new_text[i + 2].upper()  # Middle name

        # If there is no middle name, then replace it with a capital 'X'
        if new_text[i + 2] == "":
            new_text[i + 2] = "X"

        id_of_employee = new_text[i + 3]  # Employee ID

        # Check to see if the ID is valid (i.e., it must be 2 letters followed by 4 digits).
        # If it's not valid, then prompt the user to enter a valid ID
        pattern_for_id = re.compile(r'[a-zA-Z][a-zA-Z]\d\d\d\d')
        new_id_of_employee = id_of_employee

        if not pattern_for_id.match(id_of_employee):
            while not pattern_for_id.match(new_id_of_employee):
                # Prompt user to input new ID
                print("ID invalid: ", new_id_of_employee)
                print("ID is two letters followed by 4 digits")
                new_id_of_employee = input("Please enter a valid id: ")

                # Check to see if the new ID they entered is a duplicate
                if new_id_of_employee not in employee_id_list:
                    employee_id_list.append(new_id_of_employee)
                elif new_id_of_employee in employee_id_list:
                    print("*** ERROR: Duplicate ID. The old employee's information associated with this ID will be"
                          " erased and populated by the new employee's information ***")

        # Make the ID in list the new ID (if it wasn't valid)
        new_text[i + 3] = new_id_of_employee

        phone_number = new_text[i + 4]  # Employee phone number

        # Check to see if the phone number is valid (i.e., it must be in the form '999-999-9999'.
        # If it's not valid, then prompt the user to enter a valid phone number
        pattern_for_phone = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
        new_phone_number = phone_number

        if not pattern_for_phone.match(phone_number):
            while not pattern_for_phone.match(new_phone_number):
                # Prompt user to enter new phone number
                print("Phone ", phone_number, " is invalid")
                print("Enter phone number in form 123-456-7890")
                new_phone_number = input("Enter phone number: ")

        # Make the phone number in list the new phone number (if it wasn't valid)
        new_text[i + 4] = new_phone_number

        # Create a Person object for the employee.
        # Person object is created passing in the parameters for: last name, first name, middle name, id, phone number
        employee = Person(new_text[i + 0], new_text[i + 1], new_text[i + 2], new_text[i + 3], new_text[i + 4])

        # Put employee in dictionary
        # (key, value) = (id, Person object)
        employee_dict[new_text[i + 3]] = employee

    # Return dictionary of employees
    return employee_dict


def get_file(input_filepath):
    """
    Returns the text from the input file (data.csv)
    :param input_filepath: path to the file we take as input as a parameter into the program
    :return read_text_in: the text from the input file
    """
    with open(os.path.join(os.getcwd(), input_filepath), 'r') as file:
        read_text_in = file.read()
    file.close()

    return read_text_in


def main(input_file):
    """
    Calls series of methods to process text from data.csv and puts that text into a dict.
    After that, save the dict as a pickle file, read the pickle file, then display the list of employees
    :param input_file:
    :return:
    """
    # If user doesn't specify a sysarg, print an error message and terminate the program
    if input_file == "":
        print("ERROR: No relative path for data.csv was specified. Terminating program...")
        exit()

    text_from_file = get_file(input_file)  # Get the text from input file
    employee_dict = process_text(text_from_file)  # Process text and get dict of employees
    pickle.dump(employee_dict, open('employee_dict.p', 'wb'))  # Save employee_dict as pickle file
    read_employee_dict = pickle.load(open('employee_dict.p', 'rb'))  # Read employee_dict pickle file

    # Print out list of employees
    print("\n\nEmployee List:")
    for key in read_employee_dict:
        read_employee_dict[key].display()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Let the user enter the path
        input_file = input("Please enter the relative path for the input file as a system arg ('data/data.csv'): ")
        main(input_file)
    else:
        # Get file path for input file
        input_file = sys.argv[1]
        main(input_file)
