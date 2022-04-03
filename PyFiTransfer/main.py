#!/usr/bin/env python3
#< PyFiTransfer >#
#& Est. 1/15/22 $#

import logging
from os import PathLike, chdir
from os import scandir as lsContents
from os.path import basename as base
from os.path import dirname
from os.path import exists as isDir
from shutil import move as copyfile
from typing import NoReturn

from PyLoadBar import load

#> Set CWD:
chdir(dirname(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(asctime)s : %(levelname)s] - %(message)s')

logHandler = logging.FileHandler('./logs/log.log', 'a')

logHandler.setFormatter(formatter)

logger.addHandler(logHandler)

textborder: str = '\n========================\n'


def main() -> NoReturn | None:
    """Run `PyFiTransfer`.

    ---

    Parameters:
        :return: Program start
        :rtype: NoReturn | None
    """
    logger.debug('> Started PyFiTransfer... <\n')

    origin: str = getStartDir()
    logger.info(f'Got origin directory:\n==> "{origin}"')

    destination: str = getFinalDir()
    logger.info(f'Got file destination:\n==> "{destination}"')

    fileType: str = getFileType()
    logger.info(f'Got file-type to be transferred:\n==> ".{fileType}"')

    originClearance: bool = verify(origin)
    destinationClearance: bool = verify(destination)

    if originClearance and destinationClearance:
        logger.info('==> Transferring files now <==')
        transfer(origin, destination, fileType)
        return Ex_0()
    return Ex_1(fileType)


def getStartDir() -> str:
    """Prompt user for file-path of directory containing files to move.

    ---

    Parameters:
        :return: directory path of files to move
        :rtype: str | PathLike
    """
    return input(
        '\nPlease enter the file-path of the starting directory\'s location containing the files you wish to transfer:\n> '
    )


def getFinalDir() -> str:
    """Prompt user for file-path of directory to move files to.

    ---

    Parameters:
        :return: directory path of file destination.
        :rtype: str | PathLike
    """
    return input(
        '\nPlease enter the file-path of the directory intended to be the destination of transferred files:\n> '
    )


def getFileType() -> str:
    """Prompt user for type of file needing to be moved.

    ---

    Parameters:
        :return: file-type/extension.
        :rtype: str
    """
    return input(
        '\nPlease enter the file-type/file-extension of the files intended to be tansferred between directory locations.\nOnly include letters of extension.\n- INCORRECT Ex: ".mp4"\n- Correct Ex (without quotes): "mp4"\n> '
    )


def verify(filepath: PathLike | str) -> bool:
    """Verify existence of a given directory.

    ---

    Parameters:
        :param filepath: path to directory.
        :type filepath: PathLike | str
        :return: verification of existence of the given directory, or lack thereof.
        :rtype: bool
    """
    try:
        logger.info(
            f'Verifying directory of given file location:\n==> "{filepath}"...'
        )
        if isDir(filepath):
            load(
                f'\nVerifying destination for file location:\n==> "{filepath}"',
                '\nDirectory verified successfully!',
                enable_display=False)
            logger.info('Directory verified successfully.')
            return True
        else:
            logger.error(
                f'Directory: "{filepath}"\n==> Unable to be found, thus could NOT be verified.'
            )
            load(
                f'\nVerifying destination for file location:\n==> "{filepath}"',
                f'> ERROR\n> Directory: "{filepath}"\n==> Unable to be found, thus could NOT be verified.',
                enable_display=False)
            return False
    except (OSError, ValueError, TypeError, EOFError) as error:
        logger.exception(
            f'Something went wrong during directory verification...\n> {error}'
        )
        print(
            f'> ERROR!\nSomething went wrong during directory verification...\n> {error}'
        )
        return False


def transfer(startingDir: str, finalDir: str, fileType: str) -> None:
    """Transfer files of certain extensions from original directory to given destination.

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
    print('\n> Transferring files now...\n')
    with lsContents(startingDir) as dirFiles:
        for file in dirFiles:
            if not file.name.startswith('.') and file.name.endswith(
                    f'.{fileType}') == True and file.is_file():
                logger.info(f'==> Transferring file {file.name}...')
                files.append(file.name)
                copyfile(file, f'{finalDir}\{base(file)}')
        logger.info(
            f'{len(files)} files successfully copied to new location:\n==> {files}'
        )
        load(
            f'> Transferring all ".{fileType}" files to: "{finalDir}"',
            f'> {len(files)} files successfully copied to new location:\n{files}',
            time=len(files) if files else 5)


def Ex_0() -> NoReturn | None:
    """Exit program with success message.

    ---

    Parameters:
        :return: Exits program.
        :rtype: NoReturn
    """
    logger.debug(
        f'==> Operation Successful! <==\n==> Exiting Program...{textborder}')
    print('\n\nOperation Successfull!\n\nExiting Program...')
    return exit()


def Ex_1(fileType: str) -> NoReturn | None:
    """Exit program with error message.

    ---

    Parameters:
        :param fileType: extension of files not found
        :type fileType: str
        :return: Closes application
        :rtype: NoReturn | None
    """
    logger.warning(
        f'==> Operation Failure! <==\n==> No Files were found with given extension: ".{fileType}".\n==>Exiting Program...{textborder}'
    )
    print(
        f'\n\n> Operation Failure!\n\n> No Files were found with given extension: ".{fileType}".\n\nExiting Program...'
    )
    return exit()


if __name__ == "__main__":
    main()
