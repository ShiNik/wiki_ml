# user define imports
import src.util as util
from src.singleton import Singleton

# python imports
import logging


@Singleton
class LogManager():
    def __init__(self):
        self.Logging_Levels = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0}
        self.initialized = False
        self.logger = self.init()
        self.debug_level = logging.WARNING
        self.set_color_enabled = False
        return

    def init(self):
        if self.initialized:
            return

        self.initialized = True
        logger = logging.getLogger('root')
        logger.setLevel(logging.DEBUG)
        # Create handlers
        c_handler = logging.StreamHandler()
        file_name = "log.log"
        full_path = util.get_full_log_path(file_name)

        f_handler = logging.FileHandler(full_path)
        c_handler.setLevel(logging.WARNING)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        c_format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] - %(levelname)s - %(message)s"
        c_format = logging.Formatter(c_format)

        f_format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] - %(asctime)s - %(levelname)s - %(message)s"
        f_format = logging.Formatter(f_format)

        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        return logger

    def get_logger(self):
        return self.logger

    def get_log_level(self):
        return util.convert_to_const(self.logger.level)

    def debug_enabled(self, ):
        log_level = self.get_log_level()
        if log_level == self.debug_level:
            return True

        return False

    def update_set_color_enabled(self, value):
        self.set_color_enabled = value

    def get_set_color_enabled(self):
        return util.convert_to_const(self.set_color_enabled)

    def set_color(self, org_string):
        color_levels = {
            10: "\033[36m{}\033[0m",  # DEBUG
            20: "\033[32m{}\033[0m",  # INFO
            30: "\033[33m{}\033[0m",  # WARNING
            40: "\033[31m{}\033[0m",  # ERROR
            50: "\033[7;31;31m{}\033[0m"  # FATAL/CRITICAL/EXCEPTION
        }

        level = self.get_log_level()
        if level is None:
            return color_levels[20].format(org_string)
        else:
            return color_levels[int(level)].format(org_string)

    def get_log_function(self, log_function_type):
        switcher = {
            # "CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0
            self.Logging_Levels["CRITICAL"]: self.logger.critical,
            self.Logging_Levels["ERROR"]: self.logger.error,
            self.Logging_Levels["WARNING"]: self.logger.warn,
            self.Logging_Levels["INFO"]: self.logger.info,
            self.Logging_Levels["DEBUG"]: self.logger.debug,
        }

        logger_function = None
        logger_function = switcher.get(log_function_type, None)
        if logger_function is None:
            logger_function = self.logger.debug
        return logger_function

    def log(self, message, log_function_type="DEBUG"):
        color_enabled = self.get_set_color_enabled()
        colored_message = self.set_color(message) if color_enabled else message
        self.get_log_function(log_function_type)(colored_message)
