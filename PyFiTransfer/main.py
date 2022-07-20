#!/usr/bin/env python3

import sys
from os import chdir
from os.path import dirname

sys.path.insert(0, dirname(
    dirname(__file__)))  # Ensure main module can be found by Python.

chdir(dirname(__file__))  # Set cwd to main module directory.

from PyFiTransfer.appevents.events import logger
from PyFiTransfer.appevents.GUI_loop import GUI_loop


def main() -> None:
    """GUI entry point.

    ---

    :return: start GUI program.
    :rtype: None
    """

    logger.info("Starting PyFiTransfer-GUI...\n")
    return GUI_loop()


if __name__ == '__main__':
    main()
