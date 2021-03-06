import os
from os.path import dirname
from os import PathLike, chdir
from os import scandir as lsContents
from os.path import basename as base
from shutil import move
from typing import NoReturn

from genericpath import isdir
from PyFiTransfer.applogger.logger import _LogGenerator
from PyLoadBar import PyLoadBar

chdir(dirname(dirname(__file__)))

txt_seq = PyLoadBar(bar_sequence=False)
bar_seq = PyLoadBar()

logger = _LogGenerator('transferlog', 'Program')

BORDER: str = '\n<='.ljust(50, '=') + '=>'


class FileTransfer:
    """Class containing various methods related to transferring files.

    - Contains the following class methods:

        - :func:`__get_src_dir(self) -> str`
            - Get starting location of files to be transferred.

        - :func:`__get_dest_dir(self) -> str`
            - Get target destination for file transfer.

        - :func:`__get_ext(self) -> str`
            - Get extension of files to transfer.

        - :func:`__verify_dir(self, filepath: PathLike | str) -> bool`
            - Verify if given filepath is a directory.

        - :func:`transfer(self, src_dir: str | PathLike, target_dir: str | PathLike, file_ext: str | PathLike) -> bool | int`
            - Transfer files from source directory to target directory.
    """

    def _get_src_dir(self) -> str:
        """Get starting location of files to be transferred.

        ---

        :return: directory of files to be transferred
        :rtype: :class:`str`
        """
        return input(
            "\nEnter filepath of the directory containing the files to be transferred:\n> "
        )

    def _get_dest_dir(self) -> str:
        """Get target destination for file transfer.

        ---

        :return: destination of file transfer.
        :rtype: :class:`str`
        """
        return input("\nEnter destination to transfer files:\n> ")

    def _get_ext(self) -> str:
        """Get extension of files to transfer.

        ---

        :return: file-type/extension of files to be transferred.
        :rtype: :class:`str`
        """
        return input(
            '\nEnter type/extension of the files to transfer.\n- Only include letters of extension.\n\t\t- Correct Example (without quotes): "mp4"\n>> '
        )

    def _verify_dir(self, filepath: PathLike | str) -> bool:
        """Verify if given filepath is a directory.

        ---

        :param filepath: path to directory.
        :type filepath: :class:`PathLike` | :class:`str`
        :return: `True` if directory exists, `False` if not.
        :rtype: :class:`bool`
        """
        try:
            logger.info(
                f'Verifying directory of given file location:\n>> "{filepath}"...'
            )
            if isdir(filepath):
                txt_seq.start(
                    f'Verifying file transfer destination: "{filepath}"',
                    "Directory verified successfully!",
                    iter_total=5,
                    txt_seq_speed=0.25)
                logger.info(
                    f"Filepath \"{filepath}\" verified successfully!\n")
                return True
            else:
                txt_seq.start(
                    f'Verifying file transfer destination: "{filepath}"',
                    f'>> ERROR:\n>> Directory: "{filepath}" could NOT be verified.',
                    iter_total=5,
                    txt_seq_speed=0.25)
                logger.warning(
                    f'Directory: "{filepath}" could NOT be verified...\n')
                return False
        except (OSError, ValueError, TypeError, EOFError) as error:
            logger.exception(
                f"Something went wrong during directory verification...\n>> {error}"
            )
            return False

    def transfer(self, src_dir: str | PathLike, target_dir: str | PathLike,
                 file_ext: str | PathLike, gui: bool) -> bool | int:
        """Transfer files of a given extension from source directory to target destination.

        ---

        :param src_dir: starting location of transfer
        :type src_dir: :class:`str` | :class:`PathLike`
        :param target_dir: file transfer destination
        :type target_dir: :class:`str` | :class:`PathLike`
        :param file_ext: extension of files to be transferred
        :type file_ext: :class:`str` | :class:`PathLike`
        :return: if :param:`gui` is `True`, return number of files transferred, else return `True` or `False` depending if transfer was successful or not.
        :rtype: :class:`bool` | :class:`int`
        """

        files: list = []

        logger.info("> Transferring files now...\n")

        with lsContents(str(src_dir)) as dirFiles:
            try:
                for file in dirFiles:
                    if file.is_file() and (not file.name.startswith(".") and
                                           file.name.endswith(f".{file_ext}")):
                        logger.info(
                            f">> Transferring file: \"{file.name}\"...")
                        files.append(file.name)
                        move(file, f"{target_dir}\{base(file)}")

                if not files:
                    logger.info(
                        f">> No files found with extension: \"{file_ext}\" in directory: \"{src_dir}\"\n"
                    )
                    print(
                        f"\n> No files found with extension: \"{file_ext}\" in directory: \"{src_dir}\""
                    )
                    return False

                if gui:
                    print(
                        f'> Transferring all files with extension ".{file_ext}" to:\n>> "{target_dir}"\n'
                    )
                    logger.info(
                        f'{len(files)} files successfully copied to new location:\n>> "{target_dir}"\n'
                    )
                    return len(files)

                bar_seq.start(
                    msg_loading=
                    f'> Transferring all files with extension ".{file_ext}" to:\n>> "{target_dir}"',
                    msg_complete=
                    f'> {len(files)} files successfully copied to new location:\n>> {files}',
                    min_iter=0.01,
                    max_iter=0.2,
                    iter_total=len(files))

                logger.info(
                    f'{len(files)} files successfully copied to new location:\n>> "{target_dir}"\n'
                )

                return True

            except (OSError, ValueError, TypeError, EOFError) as error:
                logger.exception(
                    f'Something went wrong during file transfer...\n>> {error}\n'
                )
                return False


def change_ext(path: str | PathLike, curext: str, newext: str) -> None:
    """Change extension of all files of a given type.

    :param path: path to containing directory of files to be changed
    :type path: :class:`str` | :class:`PathLike`
    :param curext: extension of files to be changed
    :type curext: :class:`str`
    :param newext: extension to change files to.
    :type newext: :class:`str`
    :return: change extension of all files of a certain type in directory.
    :rtype: None
    """
    for filename in os.listdir(os.path.dirname(os.path.abspath(path))):
        base_file, ext = os.path.splitext(filename)
        if ext == curext:
            return os.rename(filename, base_file + newext)


class Exit:
    """Exit program with success or error.

    - Uses built-in Python `sys` module.

    - Contains the following class methods:

        - :func:`success(self) -> None`
            - Exit program with success.

        - :func:`error(self) -> None`
            - Exit program with error.
    """

    def __init__(self) -> None:
        """Initialize exit instance.

        ---

        :return: :class:`Exit` class instance.
        :rtype: None
        """

        self.exit_code = 0

    def success(self) -> NoReturn | None:
        """Exit program with success.

        ---

        :return: exit program with success.
        :rtype: None
        """

        logger.info(f"Operation Successful!\n\n>> Exiting Program...{BORDER}")

        self.exit_code = 0
        return exit(self.exit_code)

    def error(self, msg: str) -> NoReturn | None:
        """Exit program with error.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: exit program with error.
        :rtype: None
        """

        self.exit_code = 1

        logger.error(f'{msg}\n>> Exiting Program...{BORDER}')
        return exit(self.exit_code)


events = FileTransfer()
exit_program = Exit()
