"""
Script to transform a report from an EMR to a .csv file that can be uploaded to 
PressGaney for survey distribution.
"""

import json
from pathlib import Path
import sys

from pgsurvey import (
    Report,
    ReportPath,
    create_transmission_from_factory,
    accept_arguments,
    create_logger,
    get_dataframe_from_user_input,
    get_dataframe,
    input_to_transmit_to_press_ganey,
    override_sys_excepthook_to_log_uncaught_exceptions,
    read_config,
    TransmitOption
)


def main():
    logger = create_logger()
    override_sys_excepthook_to_log_uncaught_exceptions(logger)
    logger.info('************************ START ************************')
    logger.info('Parse options passed')
    config_path, input_file, transmit_option = accept_arguments(sys.argv[1:])
    print('Press Ganey - Survey Submission')
    project_directory = Path().resolve()
    logger.info('Creating report path')
    report_path = ReportPath(project_directory)
    if input_file is not None:
        logger.info('Get dataframe from CLI "-f", "--file" input')
        df = get_dataframe(report_path.input_directory / Path(input_file))
    else:
        logger.info('User input to get input file path and dataframe')
        df = get_dataframe_from_user_input(report_path.input_directory)
    logger.info(f'Load config json from "{config_path.name}"')
    config_serialized = json.loads(config_path.read_text())
    logger.info(f'Read config file "{config_path.name}"')
    client_id, columns, actions = read_config(config_serialized)
    logger.info('Initialize Report object')
    report = Report(df, columns, actions)
    logger.info('Run actions on dataframe')
    report.run_actions()
    logger.info('Get output .csv file path')
    output_csv = report_path.get_output_path(client_id, '.csv')
    logger.info(f'Save output .csv file "{output_csv.absolute()}"')
    report.save_output_csv(output_csv)
    print('Output .csv file saved at the following location: '
          f'"{output_csv.absolute()}"')
    logger.info('Get output .xlsx file path')
    output_xlsx = report_path.get_output_path(client_id, '.xlsx')
    logger.info(f'Save output .xlsx file "{output_xlsx.absolute()}"')
    report.save_output_xlsx(output_xlsx)
    if transmit_option is TransmitOption.USER_INPUT:
        logger.info('Checking if transmitting file to Press Ganey')
        transmit_option = input_to_transmit_to_press_ganey()
    if transmit_option is TransmitOption.NONE:
        logger.info('Not transmitting to Press Ganey')
    else:
        logger.info('Transmitting file to Press Ganey via '
                    f'{transmit_option.value}')
        transmission = create_transmission_from_factory(transmit_option)
        transmission.send(output_csv)
    logger.info('************************ END ************************')

if __name__ == '__main__':
    main()