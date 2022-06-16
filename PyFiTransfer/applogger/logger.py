import logging


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
                 name: str = __name__,
                 filename: str = __name__,
                 logfmt: str = '[%(asctime)s - %(levelname)s] : %(message)s',
                 datefmt: str = "%Y-%m-%d %H:%M:%S",
                 level=DEBUG):
        """Initialize logger instance.

        - For the :int:`level` parameter, the level of logging can be any of the following:
            - CRITICAL = 50
            - FATAL = CRITICAL
            - ERROR = 40
            - WARNING = 30
            - WARN = WARNING
            - INFO = 20
            - DEBUG = 10
            - NOTSET = 0

        ---

        :param name: assign specific name to logger, defaults to `__name__`.
        :type name: :class:`str`, optional
        :param logfmt: Initialize the formatter either with the specified format string, or a default as described above, defaults to '[%(asctime)s - %(levelname)s] : %(message)s'
        :type logfmt: :class:`str`, optional
        :param datefmt: set date formatting, defaults to '%Y-%m-%d %H:%M:%S'
        :type datefmt: :class:`str`, optional
        :param level: Set the logging level of this logger. Level must be an int or a str, defaults to `DEBUG`.
        :type level: :class:`int`, optional
        """
        self.name = name
        self.filename = filename
        self.logger = logging.getLogger(self.name)
        log_file: str = f'./logs/{self.filename}.log'
        self.logfmt = logfmt
        self.datefmt = datefmt
        self.level = level
        self.formatter = logging.Formatter(logfmt, datefmt=datefmt)
        self.fhandler = logging.FileHandler(log_file)
        self.logger.addHandler(self.fhandler)
        self.fhandler.setFormatter(self.formatter)
        self.logger.setLevel(level)

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
        :param exc_info: include exception info, defaults to :bool:`True`
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