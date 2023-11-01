import pathlib
from pathlib import Path
from unittest.mock import patch
import datetime
import json

import pytest
import pandas as pd

from pgsurvey import (
    ReportPath,
    EnvVar,
    Report,
    get_dataframe,
    read_config,
)

def return_none(*args, **kwargs):
    return None

def return_true(*args, **kwargs):
    return True

@pytest.fixture
def project_directory():
    return Path(r'X:\does\not\exist')

@pytest.fixture
def report_path(project_directory):
    with patch.object(pathlib.Path, 'mkdir', return_none):
        return ReportPath(project_directory)


@pytest.fixture
def env_var():
    return EnvVar('Test Env Var')

@pytest.fixture
def mock_report_path():
    PROJECT_DIRECTORY = 'project'
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
def temp_dir():
    temp_dir_name = 'temp/'
    temp_dir = Path(temp_dir_name)
    temp_dir.mkdir(exist_ok=True)
    yield temp_dir
    temp_dir.rmdir()

@pytest.fixture
def df_instance():
    return pd.DataFrame()

@pytest.fixture
def input_xlsx_test():
    return Path('tests/EMR Report Example.xlsx')

@pytest.fixture
def config_test():
    return Path('tests/config.json')

@pytest.fixture
def report_instance(input_xlsx_test, config_test):
    df = get_dataframe(input_xlsx_test)
    config_serialized = json.loads(config_test.read_text())
    _, columns, actions = read_config(config_serialized)
    return Report(df, columns, actions)

@pytest.fixture
def csv_path(temp_dir):
    csv_path = temp_dir / Path('output.csv')
    yield csv_path
    csv_path.unlink()

@pytest.fixture
def xlsx_path(temp_dir):
    xlsx_path = temp_dir / Path('output.xlsx')
    yield xlsx_path
    xlsx_path.unlink()

def test_report_path_initialization_type_check(report_path):
    assert isinstance(report_path, ReportPath)

def test_report_path_project_directory(project_directory, report_path):
    assert report_path.project_directory == project_directory

def test_report_path_project_directory_input(project_directory, report_path):
    assert report_path.input_directory == project_directory / Path('input')

def test_report_path_project_directory_output(project_directory, report_path):
    assert report_path.output_directory == project_directory / Path('output')

def test_report_path_file_extension(report_path):
    assert report_path.INPUT_FILE_EXT == '.xlsx'

def test_report_path_output_path_valid(report_path, project_directory):
    today = datetime.date.today()
    client_id = '654321'
    suffix = '.xlsx'
    output_dir = project_directory / Path('output')
    output_path = output_dir / Path(f'{client_id}{today.strftime('%m%d%Y')}{suffix}')
    assert report_path.get_output_path(client_id, suffix) == output_path

def test_report_path_output_path_invalid_suffix(report_path):
    client_id = '654321'
    suffix = '.xls'
    with pytest.raises(ValueError):
        assert report_path.get_output_path(client_id, suffix)

def test_report_path_initialization_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        ReportPath(Path(r'X:\does\not\exist'))

def test_report_path_get_input_file_path_success1(project_directory,
                                                 report_path):
    stem = 'test'
    report_path = report_path
    test_path = project_directory / Path(f'input/{stem}.xlsx')
    with patch.object(pathlib.Path, 'exists', return_true):
        assert report_path.get_input_file_path(stem) == test_path

def test_report_path_get_input_file_path_success2(project_directory,
                                                 report_path):
    stem = 'test.xlsx'
    report_path = report_path
    test_path = project_directory / Path(f'input/{stem}')
    with patch.object(pathlib.Path, 'exists', return_true):
        assert report_path.get_input_file_path(stem) == test_path

def test_report_path_get_input_file_path_file_not_found(report_path):
    report_path = report_path
    with pytest.raises(FileNotFoundError):
        report_path.get_input_file_path('test')

def test_report_path_initilization(temp_dir):
    report_path = ReportPath(project_directory=temp_dir)
    assert isinstance(report_path, ReportPath)
    input_dir = temp_dir / Path('input')
    input_dir.rmdir()
    output_dir = temp_dir / Path('output')
    output_dir.rmdir()

def test_report_initialization(report_instance: Report):
    assert isinstance(report_instance, Report)

def test_report_save_output_csv(report_instance: Report, csv_path):
    assert report_instance.save_output_csv(csv_path) is None

def test_report_save_output_xlsx(report_instance: Report, xlsx_path):
    assert report_instance.save_output_xlsx(xlsx_path) is None

def test_coerce_all_columns_to_data_type_string(report_instance: Report):
    assert report_instance.coerce_all_columns_to_data_type_string() is None

def test_trim_whitespace_from_all_columns(report_instance: Report):
    assert report_instance.trim_whitespace_from_all_columns() is None

def test_create_new_columns_from_source_columns(report_instance: Report):
    report_instance.coerce_all_columns_to_data_type_string()
    report_instance.add_columns_with_default_values()
    assert report_instance.create_new_columns_from_source_columns() is None

def test_rename_column_headers(report_instance: Report):
    assert report_instance.rename_column_headers() is None

def test_run_functions_on_columns(report_instance: Report):
    report_instance.coerce_all_columns_to_data_type_string()
    report_instance.rename_column_headers()
    assert report_instance.run_functions_on_columns() is None

def test_add_columns_with_default_values(report_instance: Report):
    assert report_instance.add_columns_with_default_values() is None

def test_truncate_columns_longer_than_max_length(report_instance: Report):
    report_instance.coerce_all_columns_to_data_type_string()
    report_instance.add_columns_with_default_values()
    report_instance.rename_column_headers()
    assert report_instance.truncate_columns_longer_than_max_length() is None

def test_sort_column_order(report_instance: Report):
    assert report_instance.sort_column_order() is None

def test_remove_email_if_patient_did_not_opt_in(report_instance: Report):
    report_instance.rename_column_headers()
    assert report_instance.remove_email_if_patient_did_not_opt_in() is None

def test_drop_columns_that_are_not_needed(report_instance: Report):
    report_instance.coerce_all_columns_to_data_type_string()
    report_instance.add_columns_with_default_values()
    report_instance.rename_column_headers()
    assert report_instance.drop_columns_that_are_not_needed() is None

def test_report_run_actions(report_instance: Report):
    assert report_instance.run_actions() is None