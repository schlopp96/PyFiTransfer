#!/usr/bin/env python3

import logging
import os
from msvcrt import getch
from os import PathLike, chdir
from os import scandir as lsContents
from os.path import basename as base
from os.path import dirname
from os.path import exists as isDir
from shutil import move as copyfile

from PyLoadBar import PyLoadBar

loader = PyLoadBar()

# > Set CWD:
chdir(dirname(__file__))

BORDER: str = '\n='.ljust(50, '=')


class _LogGenerator():
    """Wrapper for application logging.

    - Uses built-in Python `logging` module.
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
                 logfmt: str = '[%(asctime)s - %(levelname)s] : %(message)s',
                 datefmt: str = "%Y-%m-%d %H:%M:%S",
                 log_lvl=DEBUG):
        """Initialize logger instance.

        - For the `log_lvl` parameter, the level of logging can be any of the following:
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
        :param log_lvl: Set the logging level of this logger. Level must be an int or a str, defaults to `DEBUG`.
        :type log_lvl: :class:`int`, optional
        """
        self.name = name
        log_file: str = f'./logs/{self.name}.log'
        self.logger = logging.getLogger(self.name)
        self.logfmt = logfmt
        self.datefmt = datefmt
        self.log_lvl = log_lvl
        self.formatter = logging.Formatter(logfmt, datefmt=datefmt)
        self.fhandler = logging.FileHandler(log_file)
        self.logger.addHandler(self.fhandler)
        self.fhandler.setFormatter(self.formatter)
        self.logger.setLevel(log_lvl)

    def debug(self, msg: str) -> None:
        """Log 'msg' with severity 'DEBUG'.

        ---

        :param msg: message to log
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """
        return self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log 'msg' with severity 'INFO'.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """
        return self.logger.info(msg)

    def warning(self, msg) -> None:
        """Log 'msg' with severity 'WARNING'.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """
        return self.logger.warning(msg)

    def error(self, msg) -> None:
        """Log 'msg' with severity 'ERROR'.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """
        return self.logger.error(msg)

    def exception(self, msg, exc_info=True) -> None:
        """Convenience method for logging an ERROR with exception information.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :param exc_info: include exception info, defaults to True
        :type exc_info: :class:`bool`, optional
        :return: create log entry with given context and include exception info.
        :rtype: None
        """
        return self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg) -> None:
        """Log 'msg' with severity 'CRITICAL'.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: create log entry with given context.
        :rtype: None
        """
        return self.logger.critical(msg)


class _Exit:
    """Exit program with success or error.

    - Uses built-in Python `sys` module.

    - Contains the following class methods:

        - :func:`success(self) -> None`
            - Exit program with success.

        - :func:`error(self) -> None`
            - Exit program with error.

    """

    def __init__(self):
        """Initialize exit instance."""
        self.exit_code = 0

    def success(self) -> None:
        """Exit program with success.

        ---

        :return: exit program with success.
        :rtype: None
        """
        logger.info(f"Operation Successful!\n\n>> Exiting Program...{BORDER}")
        self.exit_code = 0
        exit(self.exit_code)

    def error(self, msg: str) -> None:
        """Exit program with error.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: exit program with error.
        :rtype: None
        """
        self.exit_code = 1
        logger.error(f'{msg}\n>> Exiting Program...{BORDER}')
        exit(self.exit_code)


logger = _LogGenerator(name='transferlog')
exit_program = _Exit()


def main() -> None:
    """Initialize logging subsystem and start program.

    ---

    :return: Program start
    :rtype: None
    """
    logger.info("PyFiTransfer Started...\n")

    origin: str = _get_src_dir()
    logger.info(f'Got containing directory:\n>> "{origin}"\n')

    targetDir: str = _get_dest_dir()
    logger.info(f'Got target destination:\n>> "{targetDir}"\n')

    fileExt: str = _get_ext()
    logger.info(
        f'Got extension of files to be transferred:\n>> ".{fileExt}"\n')

    if _verify_dir(origin) and _verify_dir(targetDir):
        logger.info("Starting file transfer...\n")

        if not transfer(origin, targetDir, fileExt):
            print('Press any key to exit...')
            getch()
            return exit_program.error("File transfer failed!")
        print('Press any key to exit...')
        getch()
        return exit_program.success()
    return exit_program.error(f'No files found with extension: "{fileExt}"')


def _get_src_dir() -> str:
    """Get starting location of files to be transferred.

    ---

    :return: directory of files to be transferred
    :rtype: :class:`str`
    """
    return input(
        "\nEnter filepath of the directory containing the files to be transferred:\n> "
    )


def _get_dest_dir() -> str:
    """Get destination of transferred files.

    ---

    :return: destination of file transfer.
    :rtype: :class:`str`
    """
    return input("\nEnter destination to transfer files:\n> ")


def _get_ext() -> str:
    """Get extension of files to transfer.

    ---

    :return: file-type/extension of files to be transferred.
    :rtype: :class:`str`
    """
    return input(
        '\nEnter type/extension of the files to transfer.\n- Only include letters of extension.\n\t\t- Correct Example (without quotes): "mp4"\n>> '
    )


def _verify_dir(filepath: PathLike | str) -> bool:
    """Verify if given filepath is a directory.

    ---

    :param filepath: path to directory.
    :type filepath: :class:`PathLike` | :class:`str`
    :return: :bool:`True` if directory exists, :bool:`False` if not.
    :rtype: :class:`bool`
    """
    try:
        logger.info(
            f'Verifying directory of given file location:\n>> "{filepath}"...')
        if isDir(filepath):
            loader.load(
                f'\nVerifying file transfer destination:\n>> "{filepath}"',
                "\nDirectory verified successfully!",
                enable_display=False,
            )
            logger.info(f"Filepath \"{filepath}\" verified successfully!\n")
            return True
        else:
            loader.load(
                f'\nVerifying file transfer destination:\n>> "{filepath}"',
                f'>> ERROR:\n>> Directory: "{filepath}" could NOT be verified.',
                enable_display=False,
            )
            logger.warning(
                f'Directory: "{filepath}" could NOT be verified...\n')
            return False
    except (OSError, ValueError, TypeError, EOFError) as error:
        logger.exception(
            f"Something went wrong during directory verification...\n>> {error}"
        )
        logger.info(
            f">> ERROR:\nSomething went wrong during directory verification...\n>> {error.__traceback__}"
        )
        return False


def transfer(src_dir: str, target_dir: str, file_ext: str) -> bool:
    """Transfer files of a given extension from `src_dir` to `target_dir`.

    ---

    :param src_dir: starting location of transfer
    :type src_dir: :class:`str`
    :param target_dir: file transfer destination
    :type target_dir: :class:`str`
    :param file_ext: extension of files to be transferred
    :type file_ext: :class:`str`
    :return: Transfers files to new destination.
    :rtype: :class:`Any`
    """
    files: list = []
    logger.info("\n> Transferring files now...\n")
    with lsContents(src_dir) as dirFiles:
        try:
            for file in dirFiles:
                if file.is_file() and (not file.name.startswith(".")
                                       and file.name.endswith(f".{file_ext}")):
                    logger.info(f">> Transferring file: \"{file.name}\"...")
                    files.append(file.name)
                    copyfile(file, f"{target_dir}\{base(file)}")

            if not files:
                logger.info(
                    f">> No files found with extension: \"{file_ext}\" in directory: \"{src_dir}\""
                )
                print(f"\n> No files found with extension: \"{file_ext}\" in directory: \"{src_dir}\"")
                return False

            loader.load(
                msg_loading=
                f'> Transferring all files with extension ".{file_ext}" to:\n>> "{target_dir}"',
                msg_complete=
                f'> {len(files)} files successfully copied to new location:\n>> {files}',
                time=len(files) // 2)

            logger.info(
                f'{len(files)} files successfully copied to new location:\n>> "{target_dir}"\n'
            )
            return True
        except (OSError, ValueError, TypeError, EOFError) as error:
            logger.exception(
                f'Something went wrong during file transfer...\n>> {error}\n')
            return False


def change_ext(path, curext, newext):
    for filename in os.listdir(os.path.dirname(os.path.abspath(path))):
        base_file, ext = os.path.splitext(filename)
        if ext == curext:
            os.rename(filename, base_file + newext)


if __name__ == "__main__":
    main()
