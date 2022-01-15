#!/usr/bin/env python3
#< PyFiTransfer >#
#& Est. 1/15/22 $#

from os import PathLike
from os import scandir as lsContents
from os.path import basename as base
from os.path import exists as isDir
from shutil import move as copyfile
from typing import Any

from loadSequence import load


def main():
    origin: str | PathLike = getOrigin()
    destination: str | PathLike = getDestination()
    fileType: str | PathLike = getFileType()
    originClearance: bool = verify(origin)
    destinationClearance: bool = verify(destination)

    if originClearance and destinationClearance:
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
        if isDir(directory):
            load(
                f'\nVerifying destination for file location:\n> "{directory}"',
                'Directory verified successfully!', False)
            return True
        else:
            load(
                f'\nVerifying destination for file location:\n> "{directory}"',
                f'> ERROR\n> Directory: "{directory}"\n> Unable to be found, thus could NOT be verified.',
                False)
            return False
    except (OSError, ValueError, TypeError) as error:
        print(f'> ERROR!\n> {error}')
        return False


def transfer(origin, destination, fileType) -> Any:
    files: list = []
    print('\n> Transferring files now...')
    with lsContents(origin) as dirFiles:
        for file in dirFiles:
            if not file.name.startswith('.') and file.name.endswith(
                    f'.{fileType}') == True and file.is_file():
                files.append(file.name)

                copyfile(file, (destination + "\\" + base(file)))
        load(
            '> Copying correct files',
            f'> {len(files)} files successfully copied to new location:\n{files}'
        )


def Ex_0():
    """Exit program with success message.

    :return: Exits program.
    :rtype: NoReturn
    """
    print('\n\nOperation Successfull!')
    return exit()


def Ex_1(fileType: str):
    """Exit program with error message.

    :param fileType: file-type of files not found
    :type fileType: str
    :return: Exits program.
    :rtype: NoReturn
    """
    print(
        f'\n\n> Operation Failure!\n\n> No Files were found with given extension: ".{fileType}".\n'
    )
    return exit()


if __name__ == "__main__":
    main()
