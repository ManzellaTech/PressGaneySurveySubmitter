from pgsurvey import accept_arguments, TransmitOption
from pathlib import Path

def test_accept_arguments_config_path():
    config = 'example_config.json'
    config_path, _, _ = accept_arguments(['-c', config])
    assert config_path == Path(config)

def test_accept_arguments_no_transmit():
    _, _, transmit_option = accept_arguments(['-n'])
    assert transmit_option is TransmitOption.NONE

def test_accept_arguments_input_file():
    _, input_file, _ = accept_arguments(['-f', 'test.xlsx'])
    assert isinstance(input_file, Path)

def test_accept_arguments_empty():
    config_path, input_file, transmit_option = accept_arguments([])
    assert config_path == Path('config.json')
    assert input_file is None
    assert transmit_option == TransmitOption.USER_INPUT