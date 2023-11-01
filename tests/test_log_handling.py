from pathlib import Path
import sys
import logging

from pgsurvey import (
    create_logger,
    create_logs_dir_if_not_exists,
    override_sys_excepthook_to_log_uncaught_exceptions
)

def test_create_logs_dir_if_not_exists():
    log_dir = Path('tests/temp_logs')
    assert create_logs_dir_if_not_exists(log_dir) is None
    log_dir.rmdir()

def test_logger_type_valid():
    log_dir = Path('tests/temp_logs')
    log_path = log_dir / Path('test.log')
    logger = create_logger(log_path=log_path)
    assert isinstance(logger, logging.Logger)
    log_text = 'Test Log'
    log_severity = 'INFO'
    # Generate a log message with same severity and text as below:
    # 2023-10-24 13:38:34,711 UTC|INFO|Test Log
    logger.info(log_text)
    _, logged_severity, logged_text = tuple(log_path.read_text().split('|'))
    assert log_severity == logged_severity
    assert log_text == logged_text.strip()
    logger.handlers.clear()
    log_path.unlink()
    log_dir.rmdir()

def test_override_sys_excepthook_and_set_logger_to_handle_uncaught_exceptions():
    log_dir = Path('tests/temp_logs')
    log_path = log_dir / Path('test.log')
    logger = create_logger(log_path=log_path)
    original_sys_excepthook = sys.excepthook
    assert override_sys_excepthook_to_log_uncaught_exceptions(logger) is None
    sys.excepthook = original_sys_excepthook
    logger.handlers.clear()
    log_path.unlink()
    log_dir.rmdir()