import os
from typing import Callable
from unittest.mock import patch

import pytest

from pgsurvey import Column, EnvVar, TransmitOption, get_connection_options, read_config


def return_none(*args, **kwargs):
    return None

@pytest.mark.parametrize('test_input, expected', [
    ('Test Env Var', 'TEST_ENV_VAR'),
    ('My Env Var!', 'MY_ENV_VAR'),
])
def test_env_var_name_valid(test_input, expected):
    env_var = EnvVar(test_input)
    assert env_var.name == expected

@pytest.mark.parametrize('test_input, expected', [
    ('Test Env Var', 'Test Env Var'),
    ('My Env Var!', 'My Env Var!'),
])
def test_env_var_pretty_name_valid(test_input, expected):
    with patch.dict(os.environ, { 'Test Env Var': 'Test Env Var'}):
        env_var = EnvVar(test_input)
        assert env_var.pretty_name == expected

@pytest.fixture
def config():
    return {
        'client_id': '654321',
        'actions': [
            'coerce_all_columns_to_data_type_string',
            'trim_whitespace_from_all_columns',
            'create_new_columns_from_source_columns',
            'rename_column_headers',
            'run_functions_on_columns',
            'add_columns_with_default_values',
            'truncate_columns_longer_than_max_length',
            'sort_column_order',
            'drop_columns_that_are_not_needed'
        ],
        'columns': [
            {
                'name': 'Survey Designator',
                'max_length': 8,
                'col_index': 0,
                'default_value': 'MD4321'
            },
            {
                'name': 'Client ID',
                'max_length': 7,
                'col_index': 1,
                'default_value': '654321'
            },
            {
                'name': 'Last Name',
                'old_name': 'Patient Last Name',
                'max_length': 25,
                'col_index': 2,
                'func': 'has_characters',
            },
        ]
    }

def test_env_var_value_valid():
    with patch.object(EnvVar, 'set_env', return_none):
        value = 'a123'
        with patch.dict(os.environ, {'Test Env Var': value}):
            env_var = EnvVar('Test Env Var')
            env_var.value = value
            assert env_var.value == value

@patch('pgsurvey.user_interaction.input_environment_variable', return_value='foo')
def test_get_connection_options_returns_dict(mock_input_environment_variable):
    assert isinstance(get_connection_options(TransmitOption.SFTP), dict)

@patch('builtins.input', return_value='foo')
def test_get_connection_options_get_user_input(mock_input_environment_variable):
    mock_env_vars = {
        'PRESS_GANEY_SFTP_ADDRESS': 'foo',
        'PRESS_GANEY_SFTP_USERNAME': 'foo',
        'PRESS_GANEY_SFTP_PASSWORD': 'foo'
    }
    with patch.dict(os.environ, mock_env_vars):
        connection_options_foo = { 'address': 'foo', 'username': 'foo', 'password': 'foo' }
        assert get_connection_options(
            transmit_option=TransmitOption.SFTP) == connection_options_foo

@pytest.mark.parametrize('test_input', ['address', 'username', 'password'])
def test_get_connection_options_has_keys(test_input):
    connection_options = get_connection_options(TransmitOption.SFTP)
    assert test_input in connection_options.keys()

def test_get_connection_options_transmit_type_invalid():
    with pytest.raises(ValueError):
        assert get_connection_options(TransmitOption.NONE)

@patch('pgsurvey.user_settings.input_environment_variable', return_value='foo')
def test_get_connection_options_address_valid(mock_input_environment_variable):
    connection_options = get_connection_options(TransmitOption.SFTP,
                                                address_name='ENV_VAR_DOES_NOT_EXIST',
                                                username_name='ENV_VAR_DOES_NOT_EXIST',
                                                password_name='ENV_VAR_DOES_NOT_EXIST')
    assert connection_options['address'] == 'foo'
    assert connection_options['username'] == 'foo'
    assert connection_options['password'] == 'foo'

def test_import_json_config1(config):
    _, columns, _ = read_config(config)
    assert isinstance(columns, list)

def test_import_json_config2(config):
    _, columns, _ = read_config(config)
    assert isinstance(columns[0], Column)

def test_import_json_config3(config):
    _, columns, _ = read_config(config)
    assert isinstance(columns[2].func, Callable)