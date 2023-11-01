from unittest.mock import patch

import pytest

from pgsurvey import Transmission, TransmitOption, create_transmission_from_factory, get_transmit_option_from_cli_args


@patch('pgsurvey.transmit_report.get_connection_options', return_value={
    'address': 'sftp.example.com',
    'username': 'test',
    'password': 'test'
})
def test_transmission_factory_sftp_valid(mock_get_connection_options):
    transmit_option = TransmitOption.SFTP
    transmission = create_transmission_from_factory(transmit_option)
    assert isinstance(transmission, Transmission)

def test_transmission_factory_invalid_raises_value_error():
    with pytest.raises(ValueError):
        transmit_option = TransmitOption.NONE
        assert create_transmission_from_factory(transmit_option)

def test_get_transmit_option_from_cli_args_no_transmit():
    assert get_transmit_option_from_cli_args(no_transmit=True,
                                    sftp_transmit=False) == TransmitOption.NONE

def test_get_transmit_option_from_cli_args_sftp_transmit():
    assert get_transmit_option_from_cli_args(no_transmit=False,
                                    sftp_transmit=True) == TransmitOption.SFTP

def test_get_transmit_option_from_cli_args_user_input():
    assert get_transmit_option_from_cli_args(no_transmit=False,
                                    sftp_transmit=False) == TransmitOption.USER_INPUT