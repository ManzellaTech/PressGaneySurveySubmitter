import subprocess
import os
import re
from .user_interaction import input_environment_variable
from .report import Column
from .validation_sanitization import get_validator_func_from_name
from .transmit_option import TransmitOption

class EnvVar:
    """Handle getting and setting environment variables."""

    def __init__(self, pretty_name: str) -> None:
        self.pretty_name = pretty_name
        self.name = self.sanitize_env_var(pretty_name)
        self._value: str | None = None

    def sanitize_env_var(self, pretty_name: str) -> str:
        """
        Take in a pretty string and generate a string that is appropriate to be
        used as an Environment Variable key.
        """
        name = pretty_name.strip().upper().replace(' ', '_')
        return re.sub(r'\W+', '', name)

    def set_env(self, value: str) -> None:
        """Set User Environment Variable using Powershell."""
        cmd = ('[Environment]::SetEnvironmentVariable('
              f'"{self.name}", "{value}", "User")') #pragma: no cover
        subprocess.run(["powershell", "-Command", cmd],
                       capture_output=True) #pragma: no cover

    @property
    def value(self) -> str | None:
        """
        Get Environment Variable.  Check object attribute first then User 
        Environment Variable.
        """
        if self._value is not None:
            return self._value
        else:
            self._value = os.getenv(self.name)
            return self._value

    @value.setter
    def value(self, value: str) -> None:
        """Set Environment Variable and update object attribute."""
        self.set_env(value)
        self._value = value

def get_connection_options(transmit_option: TransmitOption,
                           address_name: str = 'Press Ganey SFTP Address',
                           username_name: str = 'Press Ganey SFTP Username',
                           password_name: str = 'Press Ganey SFTP Password') -> dict[str, str]:
    """Return connnection details needed for a specific transmission method."""
    match transmit_option:
        case TransmitOption.SFTP:
            sftp_address = EnvVar(address_name)
            if sftp_address.value is None:
                sftp_address.value = input_environment_variable( # pragma: no cover
                                            sftp_address.pretty_name)
            sftp_username = EnvVar(username_name)
            if sftp_username.value is None:
                sftp_username.value = input_environment_variable( # pragma: no cover
                                            sftp_username.pretty_name)
            sftp_password = EnvVar(password_name)
            if sftp_password.value is None:
                sftp_password.value = input_environment_variable( # pragma: no cover
                                            sftp_password.pretty_name)
            return {
                'address': sftp_address.value,
                'username': sftp_username.value,
                'password': sftp_password.value
            }
        case _:
            raise ValueError

def read_config(config_serialized: dict) -> tuple[str, list[Column], list[str]]:
    client_id = config_serialized['client_id']
    actions = config_serialized['actions']
    columns = []
    for col in config_serialized['columns']:
        func_name = col.get('func')
        if func_name:
            col['func'] = get_validator_func_from_name(func_name)
        columns.append(Column(**col))
    return client_id, columns, actions

