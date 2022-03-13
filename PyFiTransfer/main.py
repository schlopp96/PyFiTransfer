#!/usr/bin/env python3
#< PyFiTransfer >#
#& Est. 1/15/22 $#

import logging
from os import PathLike, chdir
from os import scandir as lsContents
from os.path import dirname, exists as isDir
from os.path import basename as base
from shutil import move as copyfile
from typing import Any, NoReturn

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
    """Program entry point/wrapper.

    :return: Program starting method.
    :rtype: NoReturn | None
    """
    logger.debug('> Started PyFiTransfer... <\n')

    origin: str | PathLike = getOrigin()
    logger.info(f'Got origin directory:\n====> "{origin}"')

    destination: str | PathLike = getDestination()
    logger.info(f'Got file destination:\n====> "{destination}"')

    fileType: str = getFileType()
    logger.info(f'Got file-type to be transferred:\n====> ".{fileType}"')

    originClearance: bool = verify(origin)
    destinationClearance: bool = verify(destination)

    if originClearance and destinationClearance:
        logger.info('\n\t\t====> Transferring files now... <====')
        transfer(origin, destination, fileType)
        return Ex_0()
    return Ex_1(fileType)


def getOrigin() -> str | PathLike:
    """Prompt user for file-path of directory containing files to move.

    :return: directory path of files to move.
    :rtype: str | PathLike
    """
    return input(
        '\nPlease enter the file-path of the starting directory\'s location containing the files you wish to transfer:\n> '
    )


def getDestination() -> str | PathLike:
    """Prompt user for file-path of directory to move files to.

    :return: directory path of file destination.
    :rtype: str | PathLike
    """
    return input(
        '\nPlease enter the file-path of the directory intended to be the destination of transferred files:\n> '
    )


def getFileType() -> str:
    """Prompt user for type of file needing to be moved.

    :return: file-type/extension.
    :rtype: str
    """
    return input(
        '\nPlease enter the file-type/file-extension of the files intended to be tansferred between directory locations:\n> '
    )


def verify(directory: PathLike | str) -> bool:
    try:
        logger.info(
            f'Verifying directory of given file location:\n====> "{directory}"....'
        )
        if isDir(directory):
            load(
                f'\nVerifying destination for file location:\n====> "{directory}"',
                '\nDirectory verified successfully!', False)
            logger.info('Directory verified successfully.')
            return True
        else:
            logger.warning(
                f'- ERROR -\n> Directory: "{directory}"\n====> Unable to be found, thus could NOT be verified.'
            )
            load(
                f'\nVerifying destination for file location:\n====> "{directory}"',
                f'> ERROR\n> Directory: "{directory}"\n====> Unable to be found, thus could NOT be verified.',
                False)
            return False
    except (OSError, ValueError, TypeError, EOFError) as error:
        logger.exception(f'> ERROR!\n> {error}')
        print(f'> ERROR!\n> {error}')
        return False


def transfer(origin, destination, fileType) -> Any:
    files: list = []
    print('\n> Transferring files now...\n')
    with lsContents(origin) as dirFiles:
        for file in dirFiles:
            if not file.name.startswith('.') and file.name.endswith(
                    f'.{fileType}') == True and file.is_file():
                logger.info(f'====> Transferring file {file.name}...')
                files.append(file.name)
                copyfile(file, f'{destination}\{base(file)}')
        logger.info(
            f'{len(files)} files successfully copied to new location:\n{files}'
        )
        load(
            f'> Transferring all ".{fileType}" files to: "{destination}"',
            f'> {len(files)} files successfully copied to new location:\n{files}',
            time=len(files) if files else 5)


def Ex_0() -> NoReturn | None:
    """Exit program with success message.

    :return: Exits program.
    :rtype: NoReturn
    """
    logger.debug(
        f'\n====> Operation Successful! <====\n====>Exiting Program...{textborder}'
    )
    print('\n\nOperation Successfull!\n\nExiting Program...')
    return exit()


def Ex_1(fileType: str) -> NoReturn | None:
    """Exit program with error message.

    :param fileType: file-type of files not found
    :type fileType: str
    :return: Exits program.
    :rtype: NoReturn
    """
    logger.warning(
        f'\n====> Operation Failure! <====\n====> No Files were found with given extension: ".{fileType}".\n====>Exiting Program...{textborder}'
    )
    print(
        f'\n\n> Operation Failure!\n\n> No Files were found with given extension: ".{fileType}".\n\nExiting Program...'
    )
    return exit()


if __name__ == "__main__":
    main()
