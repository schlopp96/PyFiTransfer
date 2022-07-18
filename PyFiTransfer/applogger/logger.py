import logging
from os import PathLike


class _LogGenerator():
    """Wrapper for application logging.

    - Uses built-in Python :module:`logging` module.
    """

    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self,
                 log_file: str | PathLike,
                 logger_name: str = __name__,
                 msgfmt: str = '[%(asctime)s - %(levelname)s] : %(message)s',
                 datefmt: str = "%Y-%m-%d %H:%M:%S",
                 level: int = DEBUG,
                 stream: bool = False) -> None:
        """Initialize logger instance.

        - For the :param:`level` parameter, the level of logging can be any of the following:
            - CRITICAL = 50
            - FATAL = CRITICAL
            - ERROR = 40
            - WARNING = 30
            - WARN = WARNING
            - INFO = 20
            - DEBUG = 10 (default)
            - NOTSET = 0

        - Example of a log entry with default parameters:

            >>> [2020-01-01 00:00:00 - DEBUG] : This is a debug message.

        ---

        :param log_file: File to which logger output is written
        :type log_file: :class:`str`
        :param logname: assign specific name to logger, defaults to `__name__`
        :type logname: :class:`str`, optional
        :param msgfmt: initialize log entry formatter either with a specified custom formatting, or the default formatting as described above, defaults to `'[%(asctime)s - %(levelname)s] : %(message)s'`
        :type msgfmt: :class:`str`, optional
        :param datefmt: set date formatting, defaults to `'%Y-%m-%d %H:%M:%S'`
        :type datefmt: :class:`str`, optional
        :param level: Set the logging level of this logger. Level must be an int or a str, defaults to `DEBUG` (10)
        :type level: :class:`int`, optional
        :param stream: If `True`, log to stdout, defaults to `False`
        :type stream: :class:`bool`, optional
        :return: program logging instance
        :rtype: None
        """

        self.logname: str = logger_name
        self.log_file: str | PathLike = log_file
        self.msgfmt: str = msgfmt
        self.datefmt: str = datefmt
        self.level: int = level
        self.logger: logging.Logger = logging.getLogger(self.logname)
        self.formatter: logging.Formatter = logging.Formatter(msgfmt, datefmt)
        self.fhandler: logging.FileHandler = logging.FileHandler(
            f'./logs/{log_file}.log')
        self.logger.addHandler(self.fhandler)
        self.fhandler.setFormatter(self.formatter)
        self.logger.setLevel(level)
        self.stream = stream

        if self.stream:  # If stream is True, log to stderr
            self.logger.addHandler(logging.StreamHandler())

    def debug(self, msg: str) -> None:
        """Log :param:`msg` with severity `DEBUG`.

        ---

        :param msg: message to log
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """

        return self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log :param:`msg` with severity `INFO`.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """

        return self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """Log :param:`msg` with severity `WARNING`.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """

        return self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """Log :param:`msg` with severity `ERROR`.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """

        return self.logger.error(msg)

    def exception(self, msg: str, exc_info=True) -> None:
        """Convenience method for logging an `ERROR` with exception information.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :param exc_info: include exception info, defaults to `True`
        :type exc_info: :class:`bool`, optional
        :return: create log entry with given context and include exception info.
        :rtype: None
        """

        return self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg: str) -> None:
        """Log :param:`msg` with severity 'CRITICAL'.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """

        return self.logger.critical(msg)
