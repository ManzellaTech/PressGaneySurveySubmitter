from argparse import ArgumentParser
from pathlib import Path
from typing import Sequence

from .transmit_report import get_transmit_option_from_cli_args
from .transmit_option import TransmitOption

def accept_arguments(sys_argv: Sequence[str]) -> tuple[Path,
                                                       Path | None,
                                                       TransmitOption]:
    """Parse options to the script."""  
    parser = ArgumentParser(description='Press Ganey Survey Submitter.  '
                            'Handle parsing of spreadsheet reports to a format '
                            'acceptable to Press Ganey then upload the spreadsheet '
                            'to Press Ganey to initiate patient survey distribution.')
    parser.add_argument('-c', '--config',
                        default='config.json',
                        dest='config_path',
                        help='Path to the config JSON file.')
    parser.add_argument('-f', '--file',
                        default=None,
                        dest='input_file',
                        help='Path to the input .xlsx spreadsheet.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--no-transmit',
                        action='store_true',
                        default=False,
                        dest='no_transmit',
                        help=('Do not transmit the output spreadsheet '
                              'to Press Ganey.'))
    group.add_argument('-s', '--sftp-transmit',
                        action='store_true',
                        default=None,
                        dest='sftp_transmit',
                        help=('Transmit the output spreadsheet to '
                              'Press Ganey via SFTP.'))
    args = parser.parse_args(sys_argv)
    if args.input_file is not None:
        input_file = Path(args.input_file)
    else:
        input_file = None
    transmit_option = get_transmit_option_from_cli_args(args.no_transmit,
                                                        args.sftp_transmit)
    return Path(args.config_path), input_file, transmit_option