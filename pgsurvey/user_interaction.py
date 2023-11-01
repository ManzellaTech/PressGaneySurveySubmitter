import functools
from pathlib import Path
from typing import Any

import pandas as pd

from .transmit_option import TransmitOption

class UserInputException(Exception):
    def __init__(self, response):
        super().__init__(response)

def loop_user_input(func, loop_count: int = 10) -> Any:
    """Decorator to handle invalid user input."""
    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        for _ in range(loop_count):
            try:
                return func(*args, **kwargs)
            except UserInputException as e:
                print(e)
        raise ValueError(f'Invalid input received {loop_count} times.')
    return wrapped_func

def get_input_file(input_directory: Path) -> Path:
    """
    User input the file name of the input .xlsx spreadsheet.  
    Validate that the input file exists.
    """
    report_file_name = input('Please save the EMR report to the '
                             f'"{input_directory}" folder '
                             'then type the exact file name of the EMR report: ')
    input_file = input_directory / Path(report_file_name)
    if input_file.exists():
        return input_file
    raise UserInputException('Unable to locate the input file. Please try again.')

def get_dataframe(input_file: Path) -> pd.DataFrame:
    """Get a Pandas dataframe from an .xlsx file path."""
    try:
        return pd.read_excel(input_file)
    except (PermissionError, AssertionError):
        pass
    raise UserInputException('Unable to open the EMR report file.  '
                             'Ensure it is a valid .xlsx file.'
                             'If it is currently open in another program, '
                             'such as Excel, please close it.')

@loop_user_input
def get_dataframe_from_user_input(input_directory: Path) -> pd.DataFrame:
    """
    User input to provide the report file name then generate a Pandas dataframe.
    If the user input is invalid loop until it is valid or an exception is raised
    when the loop ends.
    """
    input_file = get_input_file(input_directory)
    return get_dataframe(input_file)

@loop_user_input
def input_to_transmit_to_press_ganey() -> TransmitOption:
    """
    User input to transmit the .csv file to Press Ganey or not.
    If the user input is invalid loop until it is valid or an exception is raised
    when the loop ends.
    """
    transmit_input = input('Transmit the created .csv file to Press Ganey? '
                            '[yes/no]: ')
    if transmit_input.lower() in ('yes', 'y'):
        return TransmitOption.SFTP
    elif transmit_input.lower() in ('no', 'n'):
        return TransmitOption.NONE
    else:
        raise UserInputException(f'Unrecognized input: "{transmit_input}". '
                                 'Please try again.')

@loop_user_input
def input_environment_variable(pretty_name: str) -> str:
    """
    User input to get a value for an environment variable.
    If the user input is invalid loop until it is valid or an exception is raised
    when the loop ends.
    """
    value = input(f'Type the value for the {pretty_name}: ')
    if len(value.strip()) >= 1:
        return value
    raise UserInputException('The environment variable value cannot be empty.  '
                             'Please try again.')