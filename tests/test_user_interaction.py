import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd

from pgsurvey import (
    ReportPath,
    get_input_file,
    input_environment_variable,
    input_to_transmit_to_press_ganey,
    get_dataframe,
    UserInputException,
    TransmitOption,
    get_dataframe_from_user_input
)

@pytest.fixture
def temp_dir():
    temp_dir_name = 'temp'
    temp_dir = Path(temp_dir_name)
    temp_dir.mkdir(exist_ok=True)
    yield temp_dir
    temp_dir.rmdir()

@pytest.fixture
def mock_report_path():
    PROJECT_DIRECTORY = ''
    INPUT_DIRECTORY = 'input'
    report_path = ReportPath(Path(PROJECT_DIRECTORY),
                             create_input_directory=False,
                             create_output_directory=False)
    report_path.input_directory = Path(PROJECT_DIRECTORY)
    def mock_get_input_file_path(*args, **kwargs):
        return PROJECT_DIRECTORY / Path(INPUT_DIRECTORY)
    report_path.get_input_file_path = mock_get_input_file_path
    return report_path

@pytest.fixture
def temp_xlsx():
    temp_dir_name = 'temp'
    temp_dir = Path(temp_dir_name)
    temp_dir.mkdir(exist_ok=True)
    temp_xlsx_file_name = 'temp.xlsx'
    temp_xlsx = temp_dir / Path(temp_xlsx_file_name)
    df = pd.DataFrame([['a', 'b'], ['c', 'd']],
                   index=['row 1', 'row 2'],
                   columns=['col 1', 'col 2'])
    # writer = pd.ExcelWriter(temp_xlsx_file_name)
    df.to_excel(temp_xlsx, index=False)  
    # df.to_excel(writer, 'Sheet1', index=False)
    yield temp_xlsx
    temp_xlsx.unlink()
    temp_dir.rmdir()

@patch('builtins.input', return_value='temp.xlsx')
def test_get_input_file_valid(mock_input, temp_xlsx):
    assert get_input_file(Path('temp')) == temp_xlsx

@patch('builtins.input', return_value='foo')
def test_get_input_file_user_input_exception(_):
    with pytest.raises(UserInputException):
        temp_dir = 'dir_does_not_exist'
        report_path_temp = ReportPath(project_directory=Path(temp_dir),
                                      create_input_directory=False,
                                      create_output_directory=False)
        assert get_input_file(report_path_temp.input_directory)

@patch('builtins.input', return_value='y')
def test_input_to_transmit_to_press_ganey_y_valid(mock_input):
    assert input_to_transmit_to_press_ganey() is TransmitOption.SFTP

@patch('builtins.input', return_value='yes')
def test_input_to_transmit_to_press_ganey_yes_valid(mock_input):
    assert input_to_transmit_to_press_ganey() is TransmitOption.SFTP

@patch('builtins.input', return_value='n')
def test_input_to_transmit_to_press_ganey_n_valid(mock_input):
    assert input_to_transmit_to_press_ganey() is TransmitOption.NONE

@patch('builtins.input', return_value='no')
def test_input_to_transmit_to_press_ganey_no_valid(mock_input):
    assert input_to_transmit_to_press_ganey() is TransmitOption.NONE

@patch('builtins.input', return_value='???')
def test_input_to_transmit_to_press_ganey_value_error(mock_input):
    with pytest.raises(ValueError):
        assert input_to_transmit_to_press_ganey()

@patch('builtins.input', return_value='foo')
def test_input_environment_variable_valid(mock_input):
    assert input_environment_variable('foo') == 'foo'

@patch('builtins.input', return_value='')
def test_input_environment_variable_value_error(mock_input):
    with pytest.raises(ValueError):
        assert input_environment_variable('')

def test_get_dataframe_valid():
    df = get_dataframe(Path('tests/EMR Report Example.xlsx'))
    assert isinstance(df, pd.DataFrame)

def test_get_dataframe_user_input_exception():
    with patch.object(pd, 'read_excel', MagicMock(side_effect=PermissionError())):
        with pytest.raises(UserInputException):
            assert get_dataframe(Path('missing.xlsx'))

@patch.object(ReportPath,
              'get_input_file_path',
              return_value=Path('temp_project_dir/foo.txt'))
@patch('builtins.input', return_value='')
def test_get_dataframe_from_user_input_value_error(mock_input, mock_report_path):
    with pytest.raises(ValueError):
        assert get_dataframe_from_user_input(mock_report_path.input_directory)

@patch('builtins.input', return_value='temp.xlsx')
def test_get_dataframe_from_user_input_valid(mock_input, temp_xlsx):
    assert isinstance(get_dataframe_from_user_input(Path('temp')),
                          pd.DataFrame)
