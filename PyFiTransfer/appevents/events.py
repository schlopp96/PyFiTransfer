import os
from msvcrt import getch
from os import PathLike
from os import scandir as lsContents
from os.path import basename as base
from shutil import copyfile

from genericpath import isdir
import PySimpleGUI as sg
from PyFiTransfer.applogger.logger import _LogGenerator
from PyFiTransfer.appgui.gui import window
from PyLoadBar import PyLoadBar

logger = _LogGenerator(name='transferlog', filename='transferlog')

loader = PyLoadBar()

BORDER: str = '\n='.ljust(50, '=')


class FileTransfer:

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
        """Get destination of transferred files.

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
        :return: :bool:`True` if directory exists, :bool:`False` if not.
        :rtype: :class:`bool`
        """
        try:
            logger.info(
                f'Verifying directory of given file location:\n>> "{filepath}"...'
            )
            if isdir(filepath):
                loader.load(
                    f'\nVerifying file transfer destination:\n>> "{filepath}"',
                    "\nDirectory verified successfully!",
                    enable_display=False,
                )
                logger.info(
                    f"Filepath \"{filepath}\" verified successfully!\n")
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

    def transfer(self, src_dir: str | os.PathLike,
                 target_dir: str | os.PathLike,
                 file_ext: str | os.PathLike) -> bool:
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
        with lsContents(str(src_dir)) as dirFiles:
            try:
                for file in dirFiles:
                    if file.is_file() and (not file.name.startswith(".") and
                                           file.name.endswith(f".{file_ext}")):
                        logger.info(
                            f">> Transferring file: \"{file.name}\"...")
                        files.append(file.name)
                        copyfile(file, f"{target_dir}\{base(file)}")

                if not files:
                    logger.info(
                        f">> No files found with extension: \"{file_ext}\" in directory: \"{src_dir}\""
                    )
                    print(
                        f"\n> No files found with extension: \"{file_ext}\" in directory: \"{src_dir}\""
                    )
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
                    f'Something went wrong during file transfer...\n>> {error}\n'
                )
                return False


def change_ext(path, curext, newext):
    for filename in os.listdir(os.path.dirname(os.path.abspath(path))):
        base_file, ext = os.path.splitext(filename)
        if ext == curext:
            os.rename(filename, base_file + newext)


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


Events = FileTransfer()
exprogram = _Exit()


def CLI_loop() -> None:
    origin: str = Events._get_src_dir()
    logger.info(f'Got containing directory:\n>> "{origin}"\n')

    targetDir: str = Events._get_dest_dir()
    logger.info(f'Got target destination:\n>> "{targetDir}"\n')

    fileExt: str = Events._get_ext()
    logger.info(
        f'Got extension of files to be transferred:\n>> ".{fileExt}"\n')

    if Events._verify_dir(origin) and Events._verify_dir(targetDir):
        logger.info("Starting file transfer...\n")

        if not Events.transfer(origin, targetDir, fileExt):
            print('Press any key to exit...')
            getch()
            return exprogram.error("File transfer failed!")
        print('Press any key to exit...')
        getch()
        return exprogram.success()
    return exprogram.error(f'No files found with extension: "{fileExt}"')


def GUI_loop() -> None:
    while True:
        event, vals = window.read()

        logger.info(f'{event} : {vals}')

        if event in [sg.WIN_X_EVENT, sg.WIN_CLOSED, 'Exit']:
            break

        if event == '-Transfer-':
            if len(vals['-SourceFolderInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue
            if len(vals['-TargetFolderInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue
            if len(vals['-FileExtensionInput-']) < 1:
                sg.Popup('Make sure all fields are filled out!')
                continue
            Events.transfer(vals['-SourceFolderInput-'],
                            vals['-TargetFolderInput-'],
                            vals['-FileExtensionInput-'])

    window.close()

    return exprogram.success()
