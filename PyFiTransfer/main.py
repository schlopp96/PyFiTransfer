import sys
from os import chdir
from os.path import dirname

sys.path.insert(0, dirname(
    dirname(__file__)))  # Ensure main module can be found by Python.

# > Set CWD:
chdir(dirname(__file__))

from PyFiTransfer.appevents.events import logger, GUI_loop


def main():
    logger.info("Starting PyFiTransfer-GUI...\n")
    GUI_loop()


if __name__ == '__main__':
    main()