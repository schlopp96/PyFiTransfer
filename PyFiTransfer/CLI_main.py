#!/usr/bin/env python3

import sys
from msvcrt import getch
from os import chdir
from os.path import dirname

sys.path.insert(0, dirname(
    dirname(__file__)))  # Ensure main module can be found by Python.

# > Set CWD:
chdir(dirname(__file__))

from PyFiTransfer.appevents.events import logger, CLI_loop


def main() -> None:
    """Initialize logging subsystem and start CLI program.

    ---

    :return: Program start
    :rtype: None
    """
    logger.info("PyFiTransfer-CLI Started...\n")
    return CLI_loop()


if __name__ == "__main__":
    main()
