from abc import ABC, abstractmethod
import pysftp
from pathlib import Path
from .user_settings import get_connection_options
from .transmit_option import TransmitOption

def get_transmit_option_from_cli_args(no_transmit: bool,
                                      sftp_transmit: bool) -> TransmitOption:
    """Return the appropriate transmit option based off of CLI arguments."""
    if no_transmit is True:
        return TransmitOption.NONE
    if sftp_transmit is True:
        return TransmitOption.SFTP
    return TransmitOption.USER_INPUT

class Transmission(ABC):
    """Abstract base class to handle transmission of .csv files to Press Ganey."""
    @abstractmethod
    def __init__(self) -> None: # pragma: no cover
        pass

    @abstractmethod
    def send(self, file: Path) -> None: # pragma: no cover
        pass

class SftpTransmission(Transmission):
    """Concrete class to transmit .csv files to Press Ganey via SFTP."""
    def __init__(self, address: str, username: str, password: str) -> None:
        self.address = address
        self.username = username
        self.password = password

    def send(self, file: Path) -> None: # pragma: no cover
        """Upload the .csv file to Press Ganey."""
        cnopts = pysftp.CnOpts()
        self.pub_key = f'{self.address}.pub'
        if Path(self.pub_key).exists():
            cnopts.hostkeys.load(self.pub_key) # type: ignore
        with pysftp.Connection(self.address,
                            username=self.username,
                            password=self.password,
                            cnopts=cnopts) as sftp:
            sub_directory = '/Inbox'
            with sftp.cd(sub_directory):
                sftp.put(str(file))
                print(f'Uploaded "{str(file)}" to Press Ganey')

def create_transmission_from_factory(transmit_option: TransmitOption) -> Transmission:
    """Factory to create concrete transmission classes."""
    match transmit_option:
        case TransmitOption.SFTP:
            connection_options = get_connection_options(TransmitOption.SFTP)
            return SftpTransmission(**connection_options)
        case _:
            raise ValueError