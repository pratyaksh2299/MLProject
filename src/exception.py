import sys  # Imports the sys module which allows access to system-specific parameters and functions, like exception info.

# This function helps generate a detailed error message with file name and line number
def error_msg_details(error, error_details: sys):
    _, _, exc_tb = error_details.exc_info()  # Extract traceback object from sys.exc_info(), used to get detailed exception info
    file_name = exc_tb.tb_frame.f_code.co_filename  # Get the name of the file where the exception occurred
    error_msg = "Error occurred in python Script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)  # Format the error message using file name, line number, and actual error text
    )
    return error_msg  # Return the full formatted error message string

# Creating a custom exception class named 'CustomException' 
class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):  # Constructor that takes the error message and sys module as arguments
        super().__init__(error_message)  # Call the base Exception class constructor with the original error message
        # Generate a detailed custom error message using the helper function and store in an instance variable
        self.error_message = error_msg_details(error_message, error_details=error_details)

    def __str__(self):  # This method returns the string representation when you print the exception object
        return self.error_message  # Return the detailed error message
