from msvcrt import getch

from PyFiTransfer.appevents.events import events, exit_program, logger


def CLI_loop() -> None:
    """CLI program event loop.

    ---

    :return: run CLI program.
    :rtype: None
    """

    origin: str = events._get_src_dir()  # Get source directory
    logger.info(f'Got containing directory:\n>> "{origin}"\n')

    targetDir: str = events._get_dest_dir()  # Get target directory
    logger.info(f'Got target destination:\n>> "{targetDir}"\n')

    fileExt: str = events._get_ext()  # Get file extension
    logger.info(
        f'Got extension of files to be transferred:\n>> ".{fileExt}"\n')

    # Verify existence of directories
    if events._verify_dir(origin) and events._verify_dir(targetDir):
        logger.info("Starting file transfer...\n")

        # Transfer fail
        if not events.transfer(origin, targetDir, fileExt, gui=False):
            print('\nPress any key to exit...')
            getch()
            return exit_program.error("File transfer failed!")

        # Transfer success
        print('\nPress any key to exit...')
        getch()
        return exit_program.success()

    return exit_program.error(f'No files found with extension: "{fileExt}"')
