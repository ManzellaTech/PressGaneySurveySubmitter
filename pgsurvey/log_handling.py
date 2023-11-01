from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import time
import sys

def create_logs_dir_if_not_exists(logs_directory: Path) -> None:
    """Create a logs directory."""
    logs_directory.mkdir(exist_ok=True)

def create_logger(name: str = 'Press Ganey Survey Submitter',
                  log_path: Path = Path('logs/press_ganey_survey.log')) -> logging.Logger:
    """Create a logger with rotating files."""
    TEN_MEBIBYTES = 10485760
    create_logs_dir_if_not_exists(logs_directory=log_path.parent)
    level = logging.INFO
    log_format = '%(asctime)s UTC|%(levelname)s|%(message)s'
    formatter = logging.Formatter(log_format)
    formatter.converter = time.gmtime # Set to UTC
    file_handler = RotatingFileHandler(filename=log_path,
                                       mode='a',
                                       maxBytes=TEN_MEBIBYTES,
                                       backupCount=100) 
    file_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    return logger

def override_sys_excepthook_to_log_uncaught_exceptions(
        logger: logging.Logger) -> None: # pragma: no cover
    """
    Have logger handle any uncaught exceptions.
    'sys.excepthook' will be overridden.
    Keyboard interrupts will not be logged.
    """
    def handle_uncaught_exceptions(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return None
        logger.critical("Uncaught exception", exc_info=(exc_type,
                                                        exc_value,
                                                        exc_traceback))
    sys.excepthook = handle_uncaught_exceptions