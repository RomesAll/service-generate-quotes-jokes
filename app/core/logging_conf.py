import logging
import logging as _logging

class LoggingSetup:

    def __init__(self, level=_logging.DEBUG, logger_name='logger-generate-quotes-jokes'):
        self.logger = _logging.getLogger(logger_name)
        self.logger.setLevel(level)

    @staticmethod
    def create_formatter(formatter: str):
        return _logging.Formatter(formatter)

    def get_logger(self):
        return self.logger

    def create_handler_console(self, level = _logging.DEBUG, formatter: str = '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=level)
        console_handler.setFormatter(self.create_formatter(formatter))
        self.logger.addHandler(console_handler)

    def create_handler_file(self, filename: str, filemode: str, level = _logging.DEBUG, formatter: str = '%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s'):
        file_handler = logging.FileHandler(filename=filename, mode=filemode)
        file_handler.setLevel(level=level)
        file_handler.setFormatter(self.create_formatter(formatter))
        self.logger.addHandler(file_handler)

logger_setup = LoggingSetup(level=_logging.DEBUG, logger_name=f'logger-app')
logger_setup.create_handler_console(level=_logging.DEBUG)
logger_setup.create_handler_file(filename='info.log', filemode='a', level=_logging.INFO)
logger_setup.create_handler_file(filename='warning.log', filemode='a', level=_logging.WARNING)
logger_setup.create_handler_file(filename='error.log', filemode='a', level=_logging.ERROR)