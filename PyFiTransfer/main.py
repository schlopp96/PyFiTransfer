#!/usr/bin/env python3

import logging
import os
from os import PathLike, chdir
from os import scandir as lsContents
import os
from os.path import basename as base
from os.path import dirname
from os.path import exists as isDir
from shutil import move as copyfile
from typing import NoReturn

from PyLoadBar import load

# > Set CWD:
chdir(dirname(__file__))


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s : %(levelname)s] - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S')

    logHandler = logging.FileHandler("./logs/log.log", "a")

    logHandler.setFormatter(formatter)

    logger.addHandler(logHandler)
    return logger


logger = init_logger()

BORDER: str = '='.ljust(50, '=')


def main() -> NoReturn | None:
    """Initialize logging subsystem and start program.

    ---

    :return: Program start
    :rtype: NoReturn | None
    """
    logger.info(" PyFiTransfer Started...\n")

    origin: str = getStartDir()
    logger.info(f'Got origin directory:\n>> "{origin}"')

    targetDir: str = getTargetDir()
    logger.info(f'Got file destination:\n>> "{targetDir}"')

    fileExt: str = getExt()
    logger.info(f'Got file-type to be transferred:\n>> ".{fileExt}"')

    if verifyPath(origin) and verifyPath(targetDir):
        logger.info("Starting file transfer...")
        transfer(origin, targetDir, fileExt)
        return Ex_0()
    return Ex_1(fileExt)


def getStartDir() -> str:
    """Prompt user for filepath of directory containing files to move.

    ---

    :return: filepath containing files to be transferred
    :rtype: str | PathLike
    """
    return input(
        "\nPlease enter the filepath of the starting directory's location containing the files you wish to transfer:\n> "
    )


def getTargetDir() -> str:
    """Prompt user for filepath of directory to move files to.

    ---

    :return: target destination of file transfer.
    :rtype: str | PathLike
    """
    return input(
        "\nPlease enter the destination filepath for transferred files:\n> ")


def getExt() -> str:
    """Prompt user for extension of files to be transferred.

    ---

    :return: file-type/extension of files to be transferred.
    :rtype: str
    """
    return input(
        '\nPlease enter the file-type/extension of the files intended to be tansferred between directory locations.\nOnly include letters of extension:\n>> Correct Ex (without quotes): "mp4"\n> '
    )


def verifyPath(filepath: PathLike | str) -> bool:
    """Verify existence of a given directory path.

    ---

    :param filepath: path to directory.
    :type filepath: PathLike | str
    :return: verification existence of given directory, or lack thereof.
    :rtype: bool
    """
    try:
        logger.info(
            f'Verifying directory of given file location:\n>> "{filepath}"...')
        if isDir(filepath):
            load(
                f'\nVerifying file transfer destination:\n>> "{filepath}"',
                "\nDirectory verified successfully!",
                enable_display=False,
            )
            logger.info(f"Filepath \"{filepath}\" verified successfully!")
            return True
        else:
            load(
                f'\nVerifying file transfer destination:\n>> "{filepath}"',
                f'>> ERROR:\n>> Directory: "{filepath}" could NOT be verified.',
                enable_display=False,
            )
            logger.warning(
                f'Directory: "{filepath}" could NOT be verified...s')
            return False
    except (OSError, ValueError, TypeError, EOFError) as error:
        logger.exception(
            f"Something went wrong during directory verification...\n>> {error}"
        )
        print(
            f">> ERROR:\nSomething went wrong during directory verification...\n>> {error.__traceback__}"
        )
        return False


def transfer(startingDir: str, finalDir: str, fileType: str) -> None:
    """Transfer files of certain extensions from original directory to given destination.

    ---

    :param startingDir: starting location of transfer
    :type startingDir: str
    :param finalDir: file transfer destination
    :type destination: str
    :param fileType: extension of files to be transferred
    :type fileType: str
    :return: Transfers files to new destination.
    :rtype: Any
    """
    files: list = []
    print("\n> Transferring files now...\n")
    with lsContents(startingDir) as dirFiles:
        for file in dirFiles:
            if (not file.name.startswith(".")
                    and file.name.endswith(f".{fileType}") == True
                    and file.is_file()):
                logger.info(f">> Transferring file: \"{file.name}\"...")
                files.append(file.name)
                copyfile(file, f"{finalDir}\{base(file)}")
        load(
            f'> Transferring all files with extension ".{fileType}" to:\n>> "{finalDir}"',
            f"> {len(files)} files successfully copied to new location:\n>> {files}",
            time=len(files) if files else 5,
        )
        logger.info(
            f"{len(files)} files successfully copied to new location:\n>> \"{finalDir}\""
        )


def Ex_0() -> NoReturn | None:
    """Exit program with success message.

    ---

    :return: Exits program.
    :rtype: NoReturn
    """
    logger.info(f"Operation Successful!\n\n>> Exiting Program...{BORDER}")
    print("\n\nOperation Successfull!\n\nExiting Program...")
    return exit()


def Ex_1(fileType: str) -> NoReturn | None:
    """Exit program with error message.

    ---

    :param fileType: extension of files not found
    :type fileType: str
    :return: Closes application
    :rtype: NoReturn | None
    """
    logger.warning(
        f'No Files were found with given extension: ".{fileType}".\n>> Exiting Program...{BORDER}'
    )
    print(
        f'\n\nOperation Failure!\n\n>> No Files were found with given extension: ".{fileType}".\n\n>> Exiting Program...'
    )
    return exit()


def change_ext(path, curext, newext):
    for filename in os.listdir(os.path.dirname(os.path.abspath(path))):
        base_file, ext = os.path.splitext(filename)
        if ext == curext:
            os.rename(filename, base_file + newext)


if __name__ == "__main__":
    main()
