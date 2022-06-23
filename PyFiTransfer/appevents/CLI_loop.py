from msvcrt import getch

from PyFiTransfer.appevents.events import Events, exprogram, logger


def CLI_loop() -> None:
    """CLI program event loop.

    :return: run CLI program.
    :rtype: None
    """
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
